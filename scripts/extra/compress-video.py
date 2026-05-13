from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


VIDEO_EXTENSIONS = {
	".mp4",
	".mov",
	".avi",
	".mkv",
	".webm",
	".m4v",
}


@dataclass(frozen=True)
class Preset:
	name: str
	target_size_mb: float
	max_width: int
	fps: int
	audio_bitrate_kbps: int
	min_video_bitrate_kbps: int


PRESETS = {
	"small": Preset(
		name="small",
		target_size_mb=8,
		max_width=720,
		fps=24,
		audio_bitrate_kbps=40,
		min_video_bitrate_kbps=120,
	),
	"whatsapp": Preset(
		name="whatsapp",
		target_size_mb=16,
		max_width=854,
		fps=30,
		audio_bitrate_kbps=48,
		min_video_bitrate_kbps=180,
	),
	"medium": Preset(
		name="medium",
		target_size_mb=32,
		max_width=1280,
		fps=30,
		audio_bitrate_kbps=64,
		min_video_bitrate_kbps=250,
	),
}


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description=(
			"Compress HD videos to MP4 sizes that are easier to send in messaging apps. "
			"Requires ffmpeg and ffprobe, either in PATH or via --ffmpeg-bin-dir."
		)
	)
	parser.add_argument(
		"input",
		nargs="+",
		help="One or more video files or directories.",
	)
	parser.add_argument(
		"-o",
		"--output-dir",
		type=Path,
		help="Directory for compressed files. Defaults to the source file folder.",
	)
	parser.add_argument(
		"--preset",
		choices=sorted(PRESETS),
		default="whatsapp",
		help="Compression preset. Default: whatsapp.",
	)
	parser.add_argument(
		"--target-size-mb",
		type=float,
		help="Override the preset target size in MB.",
	)
	parser.add_argument(
		"--max-width",
		type=int,
		help="Override the preset maximum width in pixels.",
	)
	parser.add_argument(
		"--fps",
		type=int,
		help="Override the preset output FPS.",
	)
	parser.add_argument(
		"--audio-bitrate",
		type=int,
		help="Override audio bitrate in kbps.",
	)
	parser.add_argument(
		"--ffmpeg-bin-dir",
		type=Path,
		help="Directory containing ffmpeg.exe and ffprobe.exe. Use this if ffmpeg is not on PATH.",
	)
	parser.add_argument(
		"--recursive",
		action="store_true",
		help="Recursively collect videos from input directories.",
	)
	parser.add_argument(
		"--suffix",
		default="_wa",
		help="Suffix added to the compressed file name. Default: _wa.",
	)
	parser.add_argument(
		"--overwrite",
		action="store_true",
		help="Overwrite output files if they already exist.",
	)
	parser.add_argument(
		"--keep-audio",
		action="store_true",
		help="Copy the original audio stream instead of re-encoding it. Useful for short clips.",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Show what would be done without running ffmpeg.",
	)
	return parser


def require_tool(name: str, bin_dir: Path | None = None) -> str:
	if bin_dir:
		candidate = bin_dir / f"{name}.exe"
		if candidate.exists():
			return str(candidate)
		candidate = bin_dir / name
		if candidate.exists():
			return str(candidate)

	executable = shutil.which(name)
	if not executable:
		raise SystemExit(
			f"{name} was not found. Install ffmpeg or pass --ffmpeg-bin-dir with the folder containing it."
		)
	return executable


def collect_video_files(paths: list[str], recursive: bool) -> list[Path]:
	files: list[Path] = []
	for raw_path in paths:
		path = Path(raw_path).expanduser()
		if not path.exists():
			print(f"Skipping missing path: {path}", file=sys.stderr)
			continue

		if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
			files.append(path)
			continue

		if path.is_dir():
			iterator = path.rglob("*") if recursive else path.glob("*")
			for candidate in iterator:
				if candidate.is_file() and candidate.suffix.lower() in VIDEO_EXTENSIONS:
					files.append(candidate)
			continue

		print(f"Skipping unsupported input: {path}", file=sys.stderr)

	unique_files = sorted({file.resolve() for file in files})
	return unique_files


def probe_duration_seconds(ffprobe: str, input_file: Path) -> float:
	command = [
		ffprobe,
		"-v",
		"error",
		"-show_entries",
		"format=duration",
		"-of",
		"json",
		str(input_file),
	]
	result = subprocess.run(command, capture_output=True, text=True, check=True)
	payload = json.loads(result.stdout)
	duration = float(payload["format"]["duration"])
	if duration <= 0:
		raise ValueError(f"Invalid duration for {input_file}")
	return duration


def build_scale_filter(max_width: int, fps: int) -> str:
	return (
		f"scale='if(gt(iw,{max_width}),{max_width},iw)':-2:force_original_aspect_ratio=decrease:force_divisible_by=2,"
		f"fps={fps}"
	)


def calculate_video_bitrate_kbps(
	duration_seconds: float,
	target_size_mb: float,
	audio_bitrate_kbps: int,
	min_video_bitrate_kbps: int,
) -> tuple[int, bool]:
	target_bits = target_size_mb * 1024 * 1024 * 8 * 0.96
	total_bitrate_kbps = int(target_bits / duration_seconds / 1000)
	video_bitrate_kbps = total_bitrate_kbps - audio_bitrate_kbps
	clamped = video_bitrate_kbps < min_video_bitrate_kbps
	if clamped:
		video_bitrate_kbps = min_video_bitrate_kbps
	return video_bitrate_kbps, clamped


def format_size_mb(size_bytes: int) -> str:
	return f"{size_bytes / (1024 * 1024):.2f} MB"


def get_output_path(input_file: Path, output_dir: Path | None, suffix: str) -> Path:
	directory = output_dir if output_dir else input_file.parent
	return directory / f"{input_file.stem}{suffix}.mp4"


def run_ffmpeg_pass(command: list[str]) -> None:
	subprocess.run(command, check=True)


def compress_video(
	ffmpeg: str,
	ffprobe: str,
	input_file: Path,
	output_file: Path,
	preset: Preset,
	overwrite: bool,
	keep_audio: bool,
	dry_run: bool,
) -> None:
	duration_seconds = probe_duration_seconds(ffprobe, input_file)
	audio_bitrate_kbps = 0 if keep_audio else preset.audio_bitrate_kbps
	video_bitrate_kbps, clamped = calculate_video_bitrate_kbps(
		duration_seconds=duration_seconds,
		target_size_mb=preset.target_size_mb,
		audio_bitrate_kbps=audio_bitrate_kbps,
		min_video_bitrate_kbps=preset.min_video_bitrate_kbps,
	)

	scale_filter = build_scale_filter(preset.max_width, preset.fps)
	overwrite_flag = "-y" if overwrite else "-n"
	null_output = "NUL" if sys.platform.startswith("win") else "/dev/null"

	print(f"Input   : {input_file}")
	print(f"Output  : {output_file}")
	print(f"Duration: {duration_seconds:.1f} s")
	print(f"Preset  : {preset.name} ({preset.target_size_mb:.0f} MB target)")
	print(f"Video   : {video_bitrate_kbps} kbps")
	if keep_audio:
		print("Audio   : copy")
	else:
		print(f"Audio   : {preset.audio_bitrate_kbps} kbps AAC")
	if clamped:
		print(
			"Warning : Target size is very aggressive for this duration. "
			"The script clamped video bitrate to keep compatibility.",
			file=sys.stderr,
		)

	output_file.parent.mkdir(parents=True, exist_ok=True)
	passlog_dir = Path(tempfile.mkdtemp(prefix="compress-video-"))
	passlog_base = passlog_dir / input_file.stem

	first_pass = [
		ffmpeg,
		overwrite_flag,
		"-i",
		str(input_file),
		"-vf",
		scale_filter,
		"-c:v",
		"libx264",
		"-preset",
		"medium",
		"-profile:v",
		"high",
		"-pix_fmt",
		"yuv420p",
		"-b:v",
		f"{video_bitrate_kbps}k",
		"-maxrate",
		f"{video_bitrate_kbps}k",
		"-bufsize",
		f"{video_bitrate_kbps * 2}k",
		"-pass",
		"1",
		"-passlogfile",
		str(passlog_base),
		"-an",
		"-f",
		"mp4",
		null_output,
	]

	second_pass = [
		ffmpeg,
		overwrite_flag,
		"-i",
		str(input_file),
		"-vf",
		scale_filter,
		"-c:v",
		"libx264",
		"-preset",
		"medium",
		"-profile:v",
		"high",
		"-pix_fmt",
		"yuv420p",
		"-movflags",
		"+faststart",
		"-b:v",
		f"{video_bitrate_kbps}k",
		"-maxrate",
		f"{video_bitrate_kbps}k",
		"-bufsize",
		f"{video_bitrate_kbps * 2}k",
		"-pass",
		"2",
		"-passlogfile",
		str(passlog_base),
	]

	if keep_audio:
		second_pass.extend(["-c:a", "copy"])
	else:
		second_pass.extend(["-c:a", "aac", "-b:a", f"{preset.audio_bitrate_kbps}k"])

	second_pass.append(str(output_file))

	if dry_run:
		print("Dry run : ffmpeg commands were not executed")
		return

	try:
		run_ffmpeg_pass(first_pass)
		run_ffmpeg_pass(second_pass)
	finally:
		for artifact in passlog_dir.glob(f"{input_file.stem}*"):
			artifact.unlink(missing_ok=True)
		passlog_dir.rmdir()

	if output_file.exists():
		print(f"Created : {output_file} ({format_size_mb(output_file.stat().st_size)})")
	print()


def resolve_preset(args: argparse.Namespace) -> Preset:
	base = PRESETS[args.preset]
	return Preset(
		name=base.name,
		target_size_mb=args.target_size_mb or base.target_size_mb,
		max_width=args.max_width or base.max_width,
		fps=args.fps or base.fps,
		audio_bitrate_kbps=args.audio_bitrate or base.audio_bitrate_kbps,
		min_video_bitrate_kbps=base.min_video_bitrate_kbps,
	)


def main() -> int:
	parser = build_parser()
	args = parser.parse_args()

	ffmpeg = require_tool("ffmpeg", args.ffmpeg_bin_dir)
	ffprobe = require_tool("ffprobe", args.ffmpeg_bin_dir)
	preset = resolve_preset(args)
	input_files = collect_video_files(args.input, recursive=args.recursive)

	if not input_files:
		parser.error("No supported video files were found.")

	failures = 0
	for input_file in input_files:
		output_file = get_output_path(input_file, args.output_dir, args.suffix)
		if output_file.exists() and not args.overwrite:
			print(
				f"Skipping existing output: {output_file} "
				"(use --overwrite to replace it)",
				file=sys.stderr,
			)
			continue
		try:
			compress_video(
				ffmpeg=ffmpeg,
				ffprobe=ffprobe,
				input_file=input_file,
				output_file=output_file,
				preset=preset,
				overwrite=args.overwrite,
				keep_audio=args.keep_audio,
				dry_run=args.dry_run,
			)
		except subprocess.CalledProcessError as error:
			failures += 1
			print(f"ffmpeg failed for {input_file}: {error}", file=sys.stderr)
		except Exception as error:
			failures += 1
			print(f"Failed to compress {input_file}: {error}", file=sys.stderr)

	return 1 if failures else 0


if __name__ == "__main__":
	raise SystemExit(main())

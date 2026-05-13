from manim import *
import numpy as np
import warnings

warnings.filterwarnings(
    "ignore", category=UserWarning, message="pkg_resources is deprecated"
)

config.media_width = "75%"
config.verbosity = "WARNING"

# ── Palette ───────────────────────────────────────────────────────────────────
BG = BLACK
FG = WHITE
C_E = "#e74c3c"        # red – Electric field
C_E_BRIGHT = "#ff6b6b"  # bright red for glow effects
C_H = "#3498db"         # blue – Magnetic field
C_H_CYAN = "#00d4ff"    # cyan accent
C_S = "#f1c40f"         # yellow/gold – Poynting vector
C_S_GOLD = "#d4a017"    # darker gold
C_PANEL = "#1a1a1a"     # dark panel fill
C_GRID = "#333333"      # grid lines
C_CONDUCTOR = "#7f8c8d" # gray for conductor
C_HEAT = "#e67e22"      # orange – Joule heating

INVIS = np.array([0.001, 0, 0])  # fallback for zero-length vectors

# Rainbow spectrum colors for Cena 3
SPECTRUM_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]


# ═════════════════════════════════════════════════════════════════════════════
class EmagWaveOpus(ThreeDScene):
    """Dinâmica e Energia da Onda Eletromagnética – 5 cenas."""

    # ── Setup ─────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        MathTex.set_default(color=FG)
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        self.cena_1_anatomia_energia()
        self.clean_up()

        self.cena_2_poynting()
        self.clean_up()

        self.cena_3_espectro()
        self.clean_up()

        self.cena_4_polarizacao()
        self.clean_up()

        self.cena_5_atenuacao()
        self.wait(1)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def clean_up(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.wait(0.25)

    def scene_header(self, text, font_size=36):
        title = Text(text, font_size=font_size, color=FG, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        sep = Line(LEFT * 5.8, RIGHT * 5.8, color=FG, stroke_width=1.2)
        sep.next_to(title, DOWN, buff=0.14)
        return title, sep

    def boxed(self, mob, color=C_S, buff=0.18):
        box = SurroundingRectangle(
            mob, color=color, buff=buff,
            stroke_width=2.8, corner_radius=0.12,
        )
        box.set_fill(color, opacity=0.08)
        return box

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 1: A Anatomia da Energia (Densidades W_e e W_h)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_1_anatomia_energia(self):
        title, sep = self.scene_header("Densidades de Energia na Onda EM")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # ── 1.1  Split screen: E wave top, H wave bottom ────────────────────
        ax_e = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.3, 1.3, 1],
            x_length=5.5, y_length=1.6,
            axis_config={"color": GREY_D, "stroke_width": 1.2},
            tips=False,
        )
        ax_e.next_to(sep, DOWN, buff=0.35).shift(LEFT * 1.8)

        ax_h = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.3, 1.3, 1],
            x_length=5.5, y_length=1.6,
            axis_config={"color": GREY_D, "stroke_width": 1.2},
            tips=False,
        )
        ax_h.next_to(ax_e, DOWN, buff=0.55)

        lbl_e_axis = MathTex(r"\vec{e}(t)", font_size=20, color=C_E)
        lbl_e_axis.next_to(ax_e, LEFT, buff=0.15)
        lbl_h_axis = MathTex(r"\vec{h}(t)", font_size=20, color=C_H)
        lbl_h_axis.next_to(ax_h, LEFT, buff=0.15)

        t_track = ValueTracker(0)

        def e_curve():
            return ax_e.plot(
                lambda x: np.sin(x - t_track.get_value()),
                x_range=[0, 4 * PI, 0.05],
                color=C_E, stroke_width=2.5,
            )

        def h_curve():
            return ax_h.plot(
                lambda x: np.sin(x - t_track.get_value()),
                x_range=[0, 4 * PI, 0.05],
                color=C_H, stroke_width=2.5,
            )

        e_wave = always_redraw(e_curve)
        h_wave = always_redraw(h_curve)

        self.play(
            Create(ax_e), Create(ax_h),
            FadeIn(lbl_e_axis), FadeIn(lbl_h_axis),
            run_time=0.8,
        )
        self.play(Create(e_wave), Create(h_wave), run_time=1.5)

        # Let them oscillate briefly
        self.play(t_track.animate.set_value(PI), run_time=1.5, rate_func=linear)

        # ── 1.2  Fill area under curves (energy density) ─────────────────────
        def e_fill():
            return ax_e.get_area(
                ax_e.plot(
                    lambda x: np.sin(x - t_track.get_value()),
                    x_range=[0, 4 * PI, 0.05],
                    stroke_width=0,
                ),
                x_range=[0, 4 * PI],
                color=C_E, opacity=0.25,
            )

        def h_fill():
            return ax_h.get_area(
                ax_h.plot(
                    lambda x: np.sin(x - t_track.get_value()),
                    x_range=[0, 4 * PI, 0.05],
                    stroke_width=0,
                ),
                x_range=[0, 4 * PI],
                color=C_H, opacity=0.25,
            )

        e_area = always_redraw(e_fill)
        h_area = always_redraw(h_fill)

        self.play(FadeIn(e_area), FadeIn(h_area), run_time=0.8)
        self.play(t_track.animate.set_value(2 * PI), run_time=1.5, rate_func=linear)

        # ── 1.3  Energy density equations ────────────────────────────────────
        eq_we = MathTex(
            r"W_e = \frac{1}{2}\epsilon|\vec{e}|^2",
            font_size=30, color=C_E,
        )
        eq_we.next_to(ax_e, RIGHT, buff=0.35)

        eq_wh = MathTex(
            r"W_h = \frac{1}{2}\mu|\vec{h}|^2",
            font_size=30, color=C_H,
        )
        eq_wh.next_to(ax_h, RIGHT, buff=0.35)

        self.play(Write(eq_we), run_time=0.9)
        self.play(Write(eq_wh), run_time=0.9)
        self.wait(1.0)

        # Oscillate a bit more
        self.play(t_track.animate.set_value(3 * PI), run_time=1.5, rate_func=linear)

        # ── 1.4  Merge: equality in vacuum ───────────────────────────────────
        # FadeOut the split view, merge to center
        self.play(
            FadeOut(ax_e), FadeOut(ax_h),
            FadeOut(e_wave), FadeOut(h_wave),
            FadeOut(e_area), FadeOut(h_area),
            FadeOut(lbl_e_axis), FadeOut(lbl_h_axis),
            FadeOut(eq_we), FadeOut(eq_wh),
            run_time=0.7,
        )

        # Single merged axis
        ax_merged = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.3, 1.3, 1],
            x_length=7, y_length=2.5,
            axis_config={"color": GREY_D, "stroke_width": 1.2},
            tips=False,
        )
        ax_merged.next_to(sep, DOWN, buff=0.5)

        e_merged = ax_merged.plot(
            lambda x: np.sin(x), x_range=[0, 4 * PI, 0.05],
            color=C_E, stroke_width=2.5,
        )
        h_merged = ax_merged.plot(
            lambda x: np.sin(x), x_range=[0, 4 * PI, 0.05],
            color=C_H, stroke_width=2.5, stroke_opacity=0.6,
        )
        e_fill_m = ax_merged.get_area(
            e_merged, x_range=[0, 4 * PI],
            color=PURPLE, opacity=0.2,
        )

        self.play(
            Create(ax_merged),
            Create(e_merged), Create(h_merged),
            FadeIn(e_fill_m),
            run_time=1.2,
        )

        lbl_overlap = Text(
            "No vácuo, a energia se divide igualmente",
            font_size=20, color=GREY_B,
        )
        lbl_overlap.next_to(ax_merged, DOWN, buff=0.3)

        eq_equal = MathTex(
            r"W_{e_{AV}} = W_{h_{AV}}",
            font_size=40, color=C_S,
        )
        eq_equal.next_to(lbl_overlap, DOWN, buff=0.3)
        box_eq = self.boxed(eq_equal, color=C_S)

        self.play(FadeIn(lbl_overlap), run_time=0.6)
        self.play(Write(eq_equal), run_time=1.0)
        self.play(Create(box_eq), run_time=0.5)
        self.wait(2.5)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 2: O Teorema de Poynting (O Fluxo de Energia)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_2_poynting(self):
        # ── 2.1  Transition to 3D with propagating wave ──────────────────────
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, run_time=1.5)

        axes = ThreeDAxes(
            x_range=[-0.5, 8, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=8, y_length=3.5, z_length=3.5,
            axis_config={"color": FG, "stroke_width": 1.5, "stroke_opacity": 0.35},
        )

        t_val = ValueTracker(0)

        def e_wave_3d():
            t = t_val.get_value()
            return ParametricFunction(
                lambda s: axes.c2p(s, np.sin(2 * s - t), 0),
                t_range=[0, 7.5, 0.05],
                color=C_E, stroke_width=3,
            )

        def h_wave_3d():
            t = t_val.get_value()
            return ParametricFunction(
                lambda s: axes.c2p(s, 0, np.sin(2 * s - t)),
                t_range=[0, 7.5, 0.05],
                color=C_H, stroke_width=3,
            )

        e_wave = always_redraw(e_wave_3d)
        h_wave = always_redraw(h_wave_3d)

        # Axis labels – placed as fixed-in-frame legend to avoid sitting on top of axes
        legend = VGroup(
            MathTex(r"\vec{E}", font_size=24, color=C_E),
            MathTex(r"\vec{H}", font_size=24, color=C_H),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.to_corner(DR, buff=0.5)

        z_lbl = MathTex(r"z", font_size=22, color=FG)
        z_lbl.to_corner(DR, buff=1.5).shift(UP * 0.5)

        self.play(Create(axes), run_time=0.8)
        self.add_fixed_in_frame_mobjects(legend, z_lbl)
        self.play(FadeIn(legend), FadeIn(z_lbl))
        self.play(Create(e_wave), Create(h_wave), run_time=1.5)

        # Propagate briefly
        self.play(t_val.animate.set_value(PI), run_time=1.5, rate_func=linear)

        # ── 2.2  E, H vectors at origin + Poynting vector ───────────────────
        phase = ValueTracker(0)

        def e_vec_up():
            val = np.sin(phase.get_value())
            start = axes.c2p(0, 0, 0)
            end = axes.c2p(0, val * 1.5, 0)
            if np.linalg.norm(end - start) < 0.01:
                end = start + INVIS
            return Arrow3D(start, end, color=C_E, thickness=0.03)

        def h_vec_up():
            val = np.sin(phase.get_value())
            start = axes.c2p(0, 0, 0)
            end = axes.c2p(0, 0, val * 1.5)
            if np.linalg.norm(end - start) < 0.01:
                end = start + np.array([0, 0, 0.001])
            return Arrow3D(start, end, color=C_H, thickness=0.03)

        def s_vec_up():
            val = np.sin(phase.get_value()) ** 2
            start = axes.c2p(0, 0, 0)
            end = axes.c2p(val * 2.0, 0, 0)
            if np.linalg.norm(end - start) < 0.01:
                end = start + INVIS
            return Arrow3D(start, end, color=C_S, thickness=0.04)

        e_arr = always_redraw(e_vec_up)
        h_arr = always_redraw(h_vec_up)
        s_arr = always_redraw(s_vec_up)

        self.play(FadeIn(e_arr), FadeIn(h_arr), run_time=0.8)
        self.add(e_arr, h_arr)

        self.play(
            phase.animate.set_value(PI),
            t_val.animate.set_value(2 * PI),
            run_time=2.0, rate_func=linear,
        )

        # Poynting vector appears
        self.play(FadeIn(s_arr), run_time=0.6)
        self.add(s_arr)

        # ── 2.3  Equation: S = E × H ────────────────────────────────────────
        eq_poynting = MathTex(
            r"\vec{S}", r"=", r"\vec{E}", r"\times", r"\vec{H}",
            font_size=34,
        )
        eq_poynting[0].set_color(C_S)
        eq_poynting[2].set_color(C_E)
        eq_poynting[4].set_color(C_H)
        eq_poynting.to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(eq_poynting)
        self.play(Write(eq_poynting), run_time=1.0)

        box_poynting = self.boxed(eq_poynting, color=C_S)
        self.add_fixed_in_frame_mobjects(box_poynting)
        self.play(Create(box_poynting), run_time=0.5)

        self.play(
            phase.animate.set_value(3 * PI),
            t_val.animate.set_value(4 * PI),
            run_time=3.0, rate_func=linear,
        )

        # ── 2.4  Transform to average (phasor) form ──────────────────────────
        eq_avg = MathTex(
            r"S_{AV}", r"=", r"\frac{1}{2}",
            r"\text{Re}\{", r"\vec{E}", r"\times", r"\vec{H}^*", r"\}",
            font_size=32,
        )
        eq_avg[0].set_color(C_S)
        eq_avg[4].set_color(C_E)
        eq_avg[6].set_color(C_H)
        eq_avg.to_corner(UL, buff=0.4)

        box_avg = self.boxed(eq_avg, color=C_S)

        self.add_fixed_in_frame_mobjects(eq_avg, box_avg)
        self.play(
            FadeOut(box_poynting),
            TransformMatchingTex(eq_poynting, eq_avg),
            run_time=1.5,
        )
        self.play(Create(box_avg), run_time=0.5)
        self.wait(1.5)

        # ── 2.5  V_e = S_AV / W_AV ──────────────────────────────────────────
        eq_ve = MathTex(
            r"V_e = \frac{S_{AV}}{W_{AV}}",
            font_size=32, color=C_S,
        )
        eq_ve.next_to(eq_avg, DOWN, buff=0.6)
        self.add_fixed_in_frame_mobjects(eq_ve)
        self.play(Write(eq_ve), run_time=1.0)
        self.wait(0.5)

        box_ve = self.boxed(eq_ve, color=C_S_GOLD)
        self.add_fixed_in_frame_mobjects(box_ve)
        self.play(Create(box_ve), run_time=0.5)

        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(
            phase.animate.set_value(5 * PI),
            t_val.animate.set_value(6 * PI),
            run_time=3.0, rate_func=linear,
        )
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 3: O Espectro Eletromagnético (A Grande Escala)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_3_espectro(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        title, sep = self.scene_header("Espectro Eletromagnético")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # ── 3.1  Logarithmic ruler ───────────────────────────────────────────
        # Frequency range: 10^3 to 10^20  → 17 decades
        ruler_y = -2.8
        ruler_width = 12.0
        decades = list(range(3, 21))  # 10^3 to 10^20
        n_dec = len(decades)
        x_left = -ruler_width / 2
        step = ruler_width / (n_dec - 1)

        ruler_line = Line(
            LEFT * ruler_width / 2 + UP * ruler_y,
            RIGHT * ruler_width / 2 + UP * ruler_y,
            color=GREY_B, stroke_width=2,
        )

        freq_ticks = VGroup()
        freq_labels = VGroup()
        for i, d in enumerate(decades):
            x = x_left + i * step
            tick = Line(
                np.array([x, ruler_y - 0.08, 0]),
                np.array([x, ruler_y + 0.08, 0]),
                color=GREY_B, stroke_width=1.5,
            )
            freq_ticks.add(tick)
            if d % 3 == 0:  # label every 3 decades
                lbl = MathTex(
                    f"10^{{{d}}}", font_size=16, color=GREY_B,
                )
                lbl.next_to(tick, DOWN, buff=0.10)
                freq_labels.add(lbl)

        hz_unit = Text("Hz", font_size=16, color=GREY_B)
        hz_unit.next_to(ruler_line, RIGHT, buff=0.2).shift(DOWN * 0.05)

        self.play(
            Create(ruler_line), FadeIn(freq_ticks),
            FadeIn(freq_labels), FadeIn(hz_unit),
            run_time=1.2,
        )

        # ── 3.2  Wave above the ruler (controlled by camera pan) ─────────────
        # We'll draw several waves at different positions along the ruler
        # representing different frequencies, then pan camera left→right

        wave_y = -0.6  # vertical center for the wave
        wave_height = 1.5

        # Segment definitions: (name, color, exponent_center, freq_per_unit)
        segments = [
            ("Ondas de Rádio", GREY_B, 6, 0.3),
            ("Micro-ondas", GREY_B, 9, 1.0),
            ("Infravermelho", GREY_B, 12, 3.0),
            # visible light handled specially
            ("Ultravioleta", PURPLE_A, 16, 15.0),
            ("Raios X", BLUE_A, 18, 25.0),
            ("Raios γ", WHITE, 19.5, 40.0),
        ]

        # Helper: exponent → x position on ruler
        def exp_to_x(exp):
            return x_left + (exp - decades[0]) * step

        # Draw a static wave for each segment
        segment_groups = VGroup()
        for name, color, exp_c, freq_scale in segments:
            xc = exp_to_x(exp_c)
            w = step * 2.5
            wave_seg = FunctionGraph(
                lambda x, fs=freq_scale, xc_=xc: np.sin(fs * (x - xc_)) * wave_height / 2,
                x_range=[xc - w / 2, xc + w / 2, 0.02],
                color=color, stroke_width=2,
            ).shift(UP * wave_y)
            lbl = Text(name, font_size=16, color=color)
            lbl.next_to(wave_seg, UP, buff=0.12)
            grp = VGroup(wave_seg, lbl)
            segment_groups.add(grp)

        # ── Visible light rainbow segment ────────────────────────────────────
        vis_exp = 14.5
        vis_xc = exp_to_x(vis_exp)
        vis_w = step * 2.0
        n_rainbow = len(SPECTRUM_COLORS)
        rainbow_waves = VGroup()
        for j, sc in enumerate(SPECTRUM_COLORS):
            frac = j / (n_rainbow - 1)
            x_start = vis_xc - vis_w / 2 + frac * vis_w * 0.7
            x_end = x_start + vis_w * 0.3
            rw = FunctionGraph(
                lambda x, f=(6 + j * 2): np.sin(f * x) * wave_height / 2.5,
                x_range=[x_start, x_end, 0.01],
                color=sc, stroke_width=2.5,
            ).shift(UP * wave_y)
            rainbow_waves.add(rw)

        vis_label = Text("Luz Visível", font_size=16, color=YELLOW)
        vis_label.move_to(np.array([vis_xc, wave_y + wave_height / 2 + 0.3, 0]))
        vis_group = VGroup(rainbow_waves, vis_label)

        # Animate appearance left to right
        all_segs = VGroup()
        for i, seg in enumerate(segment_groups):
            all_segs.add(seg)
            if i == 2:  # after infrared, insert visible
                all_segs.add(vis_group)

        for seg in all_segs:
            self.play(FadeIn(seg, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        # ── 3.3  Red light callout ───────────────────────────────────────────
        red_note = VGroup(
            Text("Luz Vermelha:", font_size=20, color=C_E_BRIGHT, weight=BOLD),
            MathTex(
                r"473\text{ THz}\;\;|\;\;\lambda = 633\text{ nm}",
                font_size=24, color=C_E_BRIGHT,
            ),
        ).arrange(RIGHT, buff=0.2)
        red_note.next_to(sep, DOWN, buff=0.25)

        self.play(FadeIn(red_note, shift=DOWN * 0.2), run_time=0.8)
        self.wait(1.5)

        # ── 3.4  Fundamental equation ────────────────────────────────────────
        eq_clf = MathTex(
            r"c = \lambda \cdot f",
            font_size=44, color=C_S,
        )
        eq_clf.move_to(np.array([0, wave_y + wave_height / 2 + 0.95, 0]))

        box_clf = self.boxed(eq_clf, color=C_S)

        self.play(FadeOut(red_note), run_time=0.4)
        self.play(Write(eq_clf), run_time=1.0)
        self.play(Create(box_clf), run_time=0.5)
        self.wait(2.5)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 4: A Geometria da Onda (Polarização Complexa)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_4_polarizacao(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        title, sep = self.scene_header("Polarização da Onda EM")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # ── 4.1  Front view grid ─────────────────────────────────────────────
        grid = NumberPlane(
            x_range=[-2.2, 2.2, 0.5],
            y_range=[-2.2, 2.2, 0.5],
            x_length=5, y_length=5,
            background_line_style={
                "stroke_color": C_GRID, "stroke_width": 0.8, "stroke_opacity": 0.4,
            },
            axis_config={"stroke_color": GREY_D, "stroke_width": 1.2},
        )
        grid.shift(DOWN * 0.3)

        x_ax = MathTex(r"E_x", font_size=22, color=C_E).next_to(grid, RIGHT, buff=0.15)
        y_ax = MathTex(r"E_y", font_size=22, color=C_E).next_to(grid, UP, buff=0.15)

        self.play(FadeIn(grid), run_time=0.6)
        self.play(FadeIn(x_ax), FadeIn(y_ax), run_time=0.4)

        # ── 4.2  General equation ────────────────────────────────────────────
        eq_general = MathTex(
            r"\vec{E} = (E_x\,\hat{x} + E_y\,\hat{y}\,",
            r"e^{i\phi}", r")\,e^{-\gamma z}",
            font_size=28,
        )
        eq_general[1].set_color(C_S)
        eq_general.next_to(sep, DOWN, buff=0.18).shift(RIGHT * 2.5)

        self.play(Write(eq_general), run_time=1.0)
        self.wait(0.8)

        # ── 4.3  Linear Polarization (φ = 0) ─────────────────────────────────
        phase_lin = ValueTracker(0)

        # Diagonal linear: Ex = Ey, φ = 0 → resultant at 45°
        lin_vec = always_redraw(
            lambda: Arrow(
                grid.c2p(0, 0),
                grid.c2p(
                    np.sin(phase_lin.get_value()) * 1.2,
                    np.sin(phase_lin.get_value()) * 1.2,
                ),
                color=C_E, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            ) if abs(np.sin(phase_lin.get_value())) > 0.01 else Arrow(
                grid.c2p(0, 0), grid.c2p(0.001, 0.001),
                color=C_E, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            )
        )

        lin_trace = TracedPath(
            lambda: grid.c2p(
                np.sin(phase_lin.get_value()) * 1.2,
                np.sin(phase_lin.get_value()) * 1.2,
            ),
            stroke_color=C_E_BRIGHT, stroke_width=2, stroke_opacity=0.6,
            dissipating_time=2.0,
        )

        phi_indicator = MathTex(r"\phi = 0°", font_size=26, color=C_S)
        phi_indicator.to_corner(DL, buff=0.5)

        lbl_lin = Text("Polarização Linear", font_size=24, color=C_E)
        lbl_lin.to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(lin_vec), FadeIn(phi_indicator), FadeIn(lbl_lin),
            run_time=0.6,
        )
        self.add(lin_trace)

        self.play(
            phase_lin.animate.set_value(4 * PI),
            run_time=4.0, rate_func=linear,
        )
        self.wait(0.3)

        self.play(
            FadeOut(lin_vec), FadeOut(lin_trace), FadeOut(lbl_lin),
            run_time=0.5,
        )

        # ── 4.4  Circular Polarization (φ = 90°) ────────────────────────────
        phase_c = ValueTracker(0)

        # Morph phi indicator
        phi_circ = MathTex(r"\phi = 90°", font_size=26, color=C_S)
        phi_circ.to_corner(DL, buff=0.5)

        self.play(TransformMatchingTex(phi_indicator, phi_circ), run_time=0.8)

        circ_vec = always_redraw(
            lambda: Arrow(
                grid.c2p(0, 0),
                grid.c2p(
                    np.cos(phase_c.get_value()) * 1.4,
                    np.sin(phase_c.get_value()) * 1.4,
                ),
                color=C_E, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            ) if (abs(np.cos(phase_c.get_value())) > 0.01 or abs(np.sin(phase_c.get_value())) > 0.01) else Arrow(
                grid.c2p(0, 0), grid.c2p(0.001, 0),
                color=C_E, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            )
        )

        circ_trace = TracedPath(
            lambda: grid.c2p(
                np.cos(phase_c.get_value()) * 1.4,
                np.sin(phase_c.get_value()) * 1.4,
            ),
            stroke_color=C_S, stroke_width=2.5, stroke_opacity=0.8,
            dissipating_time=3.5,
        )

        lbl_circ = Text("Polarização Circular", font_size=24, color=C_S)
        lbl_circ.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(circ_vec), FadeIn(lbl_circ), run_time=0.6)
        self.add(circ_trace)

        self.play(
            phase_c.animate.set_value(4 * PI),
            run_time=5.0, rate_func=linear,
        )
        self.wait(0.3)

        # ── 4.5  Elliptical Polarization (E_x ≠ E_y) ────────────────────────
        self.remove(circ_trace)
        amp_x = ValueTracker(1.4)
        phase_e = ValueTracker(0)

        ellip_vec = always_redraw(
            lambda: Arrow(
                grid.c2p(0, 0),
                grid.c2p(
                    np.cos(phase_e.get_value()) * amp_x.get_value(),
                    np.sin(phase_e.get_value()) * 1.4,
                ),
                color=C_E, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            ) if (abs(np.cos(phase_e.get_value()) * amp_x.get_value()) > 0.01 or abs(np.sin(phase_e.get_value())) > 0.01) else Arrow(
                grid.c2p(0, 0), grid.c2p(0.001, 0),
                color=C_E, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.2,
            )
        )

        ellip_trace = TracedPath(
            lambda: grid.c2p(
                np.cos(phase_e.get_value()) * amp_x.get_value(),
                np.sin(phase_e.get_value()) * 1.4,
            ),
            stroke_color=C_E_BRIGHT, stroke_width=2.5, stroke_opacity=0.8,
            dissipating_time=4.0,
        )

        lbl_ellip = Text("Polarização Elíptica", font_size=24, color=C_E_BRIGHT)
        lbl_ellip.to_edge(DOWN, buff=0.35)

        note_neq = MathTex(r"E_x \neq E_y", font_size=26, color=C_E_BRIGHT)
        note_neq.to_corner(DL, buff=0.5)

        self.play(
            FadeOut(circ_vec), FadeOut(lbl_circ),
            TransformMatchingTex(phi_circ, note_neq),
            run_time=0.6,
        )

        self.play(FadeIn(ellip_vec), FadeIn(lbl_ellip), run_time=0.5)
        self.add(ellip_trace)

        # Shrink amplitude to form ellipse
        self.play(
            amp_x.animate.set_value(0.6),
            phase_e.animate.set_value(2 * PI),
            run_time=3.0, rate_func=linear,
        )

        self.play(
            phase_e.animate.set_value(6 * PI),
            run_time=4.0, rate_func=linear,
        )
        self.wait(1.0)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 5: Atenuação e Dissipação Térmica
    # ═════════════════════════════════════════════════════════════════════════
    def cena_5_atenuacao(self):
        # ── 5.1  3D isometric view ───────────────────────────────────────────
        self.set_camera_orientation(phi=60 * DEGREES, theta=-55 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-0.5, 14, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=12, y_length=3.5, z_length=3.5,
            axis_config={"color": FG, "stroke_width": 1.2, "stroke_opacity": 0.3},
        )

        self.play(Create(axes), run_time=0.8)

        # Conductor wall at z = 7
        wall_z = 7.0
        wall = Prism(
            dimensions=[0.4, 4.0, 4.0],
            fill_color=C_CONDUCTOR, fill_opacity=0.35,
            stroke_color=C_CONDUCTOR, stroke_width=1,
        )
        wall.move_to(axes.c2p(wall_z, 0, 0))

        # Label – placed as fixed-in-frame to avoid overlap with 3D axes
        wall_label = Text("Condutor", font_size=22, color=C_CONDUCTOR, weight=BOLD)
        wall_label.to_corner(UR, buff=0.4)
        self.add_fixed_in_frame_mobjects(wall_label)

        self.play(FadeIn(wall, shift=LEFT * 0.3), FadeIn(wall_label), run_time=0.8)
        self.wait(0.3)

        # ── 5.2  Propagating wave with attenuation ───────────────────────────
        t_val = ValueTracker(0)
        alpha = 1.5  # attenuation constant

        def e_wave_atten():
            t = t_val.get_value()
            def param(s):
                if s < wall_z:
                    return axes.c2p(s, np.sin(2 * s - t), 0)
                else:
                    decay = np.exp(-alpha * (s - wall_z))
                    return axes.c2p(s, np.sin(2 * s - t) * decay, 0)
            return ParametricFunction(
                param, t_range=[0, 13, 0.05],
                color=C_E, stroke_width=3,
            )

        def h_wave_atten():
            t = t_val.get_value()
            def param(s):
                if s < wall_z:
                    return axes.c2p(s, 0, np.sin(2 * s - t))
                else:
                    decay = np.exp(-alpha * (s - wall_z))
                    return axes.c2p(s, 0, np.sin(2 * s - t) * decay)
            return ParametricFunction(
                param, t_range=[0, 13, 0.05],
                color=C_H, stroke_width=3,
            )

        e_wave = always_redraw(e_wave_atten)
        h_wave = always_redraw(h_wave_atten)

        # Legend in corner, not on axes
        legend = VGroup(
            MathTex(r"\vec{E}", font_size=24, color=C_E),
            MathTex(r"\vec{H}", font_size=24, color=C_H),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(legend)
        self.play(FadeIn(legend))

        self.play(Create(e_wave), Create(h_wave), run_time=1.5)
        self.add(e_wave, h_wave)

        # Propagate
        self.play(
            t_val.animate.set_value(3 * PI),
            run_time=3.5, rate_func=linear,
        )
        self.wait(0.3)

        # ── 5.3  Exponential envelope (dashed) ───────────────────────────────
        envelope_upper = ParametricFunction(
            lambda s: axes.c2p(s, np.exp(-alpha * (s - wall_z)), 0),
            t_range=[wall_z, 13, 0.05],
            color=C_S, stroke_width=2, stroke_opacity=0.7,
        )
        envelope_lower = ParametricFunction(
            lambda s: axes.c2p(s, -np.exp(-alpha * (s - wall_z)), 0),
            t_range=[wall_z, 13, 0.05],
            color=C_S, stroke_width=2, stroke_opacity=0.7,
        )
        envelope_upper_d = DashedVMobject(envelope_upper, num_dashes=20)
        envelope_lower_d = DashedVMobject(envelope_lower, num_dashes=20)

        self.play(Create(envelope_upper_d), Create(envelope_lower_d), run_time=1.0)

        # ── 5.4  Decay equation: e^{-αz} ────────────────────────────────────
        eq_decay = MathTex(r"e^{-\alpha z}", font_size=40, color=C_S)
        eq_decay.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(eq_decay)
        self.play(Write(eq_decay), run_time=0.8)
        self.wait(0.5)

        # ── 5.5  Skin depth δ ────────────────────────────────────────────────
        delta_z = wall_z + 1.0 / alpha  # 1/α

        delta_line = DashedLine(
            axes.c2p(delta_z, -1.8, 0),
            axes.c2p(delta_z, 1.8, 0),
            color=C_S, stroke_width=2, dash_length=0.15,
        )
        self.play(Create(delta_line), run_time=0.6)

        brace_mid = (np.array(axes.c2p(wall_z, -1.5, 0)) +
                     np.array(axes.c2p(delta_z, -1.5, 0))) / 2

        delta_label = MathTex(r"\delta", font_size=32, color=C_S)
        delta_label.move_to(brace_mid + DOWN * 0.4)
        self.add_fixed_orientation_mobjects(delta_label)

        pct_label = MathTex(r"37\%\;(e^{-1})", font_size=22, color=C_S)
        pct_label.move_to(brace_mid + DOWN * 0.9)
        self.add_fixed_orientation_mobjects(pct_label)

        self.play(FadeIn(delta_label), FadeIn(pct_label), run_time=0.8)

        depth_text = Text(
            "Profundidade de Penetração (δ)",
            font_size=26, color=C_S, weight=BOLD,
        )
        depth_text.next_to(eq_decay, DOWN, buff=0.3)
        depth_text.to_edge(LEFT, buff=0.3)
        self.add_fixed_in_frame_mobjects(depth_text)
        self.play(FadeIn(depth_text, shift=DOWN * 0.2), run_time=0.8)

        # Continue wave
        self.play(
            t_val.animate.set_value(5 * PI),
            run_time=2.5, rate_func=linear,
        )

        # ── 5.6  Dissipation integral equation ──────────────────────────────
        eq_dissip = MathTex(
            r"\int_V \sigma\,\vec{e}\cdot\vec{e}\;dV",
            font_size=32, color=C_HEAT,
        )
        eq_dissip.next_to(depth_text, DOWN, buff=0.3)
        eq_dissip.to_edge(LEFT, buff=0.3)
        self.add_fixed_in_frame_mobjects(eq_dissip)
        self.play(Write(eq_dissip), run_time=1.0)
        self.wait(0.5)

        # ── 5.7  Joule heating glow inside conductor ────────────────────────
        # Create glowing rectangles inside the conductor to simulate heat
        np.random.seed(42)
        heat_dots = VGroup()
        for _ in range(35):
            d = Dot3D(
                point=axes.c2p(
                    np.random.uniform(wall_z + 0.05, wall_z + 1.2),
                    np.random.uniform(-0.9, 0.9),
                    np.random.uniform(-0.9, 0.9),
                ),
                radius=np.random.uniform(0.04, 0.08),
                color=interpolate_color(ManimColor(C_HEAT), ManimColor(RED), np.random.uniform(0, 0.5)),
            )
            d.set_opacity(0.0)
            heat_dots.add(d)

        self.add(heat_dots)

        # Animate glow appearing (energy being dissipated as heat)
        self.play(
            *[d.animate.set_opacity(np.random.uniform(0.4, 0.9)) for d in heat_dots],
            t_val.animate.set_value(6 * PI),
            run_time=2.0,
        )

        heat_label = Text(
            "Efeito Joule – Dissipação Térmica",
            font_size=20, color=C_HEAT,
        )
        heat_label.to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(heat_label)
        self.play(FadeIn(heat_label), run_time=0.6)

        # Pulsing glow
        for _ in range(2):
            self.play(
                *[d.animate.set_opacity(
                    np.clip(d.get_fill_opacity() + np.random.uniform(-0.3, 0.3), 0.2, 1.0)
                ) for d in heat_dots],
                t_val.animate.set_value(t_val.get_value() + PI),
                run_time=1.5, rate_func=there_and_back,
            )

        self.wait(0.5)

        # ── 5.8  Fade to black ───────────────────────────────────────────────
        self.play(
            *[mob.animate.set_opacity(0) for mob in self.mobjects],
            run_time=2.5, rate_func=smooth,
        )
        self.wait(1.0)

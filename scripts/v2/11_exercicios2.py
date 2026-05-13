from manim import *
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#ece6e2"
FG      = "#5c5c5c"
C_GOLD  = "#d4a017"
C_ALPHA = "#27ae60"   # green  – attenuation α
C_BETA  = "#2471a3"   # blue   – phase constant β
C_GAMMA = "#a93226"   # red    – propagation γ
C_ETA   = "#8e44ad"   # purple – impedance η
C_VP    = "#e67e22"   # orange – phase velocity
C_VG    = "#16a085"   # teal   – group velocity
C_EPS   = "#2980b9"   # blue   – permittivity
C_SIGMA = "#c0392b"   # red    – conductivity
C_OMEGA = "#d9a441"   # amber  – angular frequency
C_PANEL = "#f7f2ee"
C_RED   = "#a93226"

EPS0 = 8.854e-12
MU0  = 4 * np.pi * 1e-7


# ═════════════════════════════════════════════════════════════════════════════
class Exercicios2Scene(Scene):
    """Resolução da Lista 2 – Atenuação, Velocidades e Fasores."""

    # ── Setup ─────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        MathTex.set_default(color=FG)

        self.cena_1_alpha_beta()
        self.clean_up()

        self.cena_2_amplitude_metade()
        self.clean_up()

        self.cena_3_impedancia_velocidades()
        self.clean_up()

        self.cena_3b_exercicio5()
        self.clean_up()

        self.cena_4_fasor_magnetico()
        self.clean_up()

        self.cena_5_dominio_tempo()
        self.wait(1)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def clean_up(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.wait(0.25)

    def scene_header(self, text, font_size=34):
        title = Text(text, font_size=font_size, color=FG, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        sep = Line(LEFT * 6.2, RIGHT * 6.2, color=FG, stroke_width=1.2)
        sep.next_to(title, DOWN, buff=0.14)
        return title, sep

    def boxed(self, mob, color=C_GOLD, buff=0.18):
        box = SurroundingRectangle(mob, color=color, buff=buff,
                                   stroke_width=2.8, corner_radius=0.12)
        box.set_fill(color, opacity=0.06)
        return box

    def data_card(self, lines, width=5.8, color=C_GOLD):
        """Build a rounded-rect panel showing given list of (tex_str, color) tuples."""
        rect = RoundedRectangle(
            corner_radius=0.14, width=width,
            height=max(1.8, 0.6 * len(lines) + 0.6),
            color=color, stroke_width=2.5,
        )
        rect.set_fill(C_PANEL, opacity=0.92)
        mobs = []
        for tex, col in lines:
            m = MathTex(tex, font_size=28, color=col)
            mobs.append(m)
        content = VGroup(*mobs).arrange(DOWN, buff=0.22)
        max_w = width - 0.5
        if content.get_width() > max_w:
            content.scale_to_fit_width(max_w)
        content.move_to(rect.get_center())
        return VGroup(rect, content)

    def caption_bottom(self, text, color=C_GOLD, font_size=22):
        mob = Text(text, font_size=font_size, color=color)
        mob.to_edge(DOWN, buff=0.30)
        return mob

    # helpers shared by scene methods
    def _cp(self, group, ctop):
        """Center a VGroup in the available area below ctop, clamping above footer."""
        group.move_to([0, ctop - group.get_height() / 2, 0])
        if group.get_bottom()[1] < -3.2:
            group.shift(UP * (-3.2 - group.get_bottom()[1]))
        return group

    def _show_phase(self, group, ctop, wait=0.8):
        """Position, animate Write/FadeIn, wait, then FadeOut."""
        self._cp(group, ctop)
        for m in group:
            if isinstance(m, (Text,)):
                self.play(FadeIn(m), run_time=0.5)
            else:
                self.play(Write(m), run_time=0.9)
        self.wait(wait)
        self.play(FadeOut(group))
        self.wait(0.2)

    def _show_panel(self, lines, ctop, width=5.0):
        panel = self.data_card(lines, width=width)
        self._cp(panel, ctop)
        panel.shift(RIGHT * 8)
        self.play(panel.animate.shift(LEFT * 8), run_time=0.9)
        self.wait(1.2)
        self.play(FadeOut(panel), run_time=0.5)
        self.wait(0.2)

    # ─────────────────────────────────────────────────────────────────────────
    # Cena 1 – Exercício 1: Encontrando α e β
    # ─────────────────────────────────────────────────────────────────────────
    def cena_1_alpha_beta(self):
        title, sep = self.scene_header("Exercício 1: Encontrando os Fatores de Propagação")
        # Shift title and separator slightly up to gain space
        title.shift(UP * 0.25)
        sep.shift(UP * 0.25)
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # Increase margin below separator from 0.55 to 0.75
        ctop = sep.get_bottom()[1] - 0.75

        # ── Painel de dados ───────────────────────────────────────────────────
        self._show_panel([
            (r"f = 12\,\text{MHz}", C_OMEGA),
            (r"\sigma = 2{,}0\times10^{-3}\,\text{S/m}", C_SIGMA),
            (r"\varepsilon = 3\varepsilon_0", C_EPS),
            (r"\mu = \mu_0", FG),
        ], ctop)

        # ── Passo 1: ω ────────────────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 1 – Calcular ω:", font_size=26),
            MathTex(r"\omega = 2\pi f = 2\pi\times12\times10^6",
                    font_size=30, color=C_OMEGA),
            MathTex(r"\omega \approx 7{,}540\times10^7\,\text{rad/s}",
                    font_size=32, color=C_OMEGA),
        ).arrange(DOWN, buff=0.30), ctop)

        # ── Passo 2: ωε e razão σ/ωε ─────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 2 – Calcular ωε e testar o meio:", font_size=26),
            MathTex(r"\omega\varepsilon = 7{,}540\times10^7\times3\times8{,}854\times10^{-12}",
                    font_size=26, color=C_EPS),
            MathTex(r"\omega\varepsilon \approx 2{,}003\times10^{-3}\,\text{S/m}",
                    font_size=28, color=C_EPS),
            MathTex(
                r"\frac{\sigma}{\omega\varepsilon} = \frac{2{,}0\times10^{-3}}"
                r"{2{,}003\times10^{-3}} \approx 0{,}999"
                r"\;\Rightarrow\;\text{meio geral}",
                font_size=26, color=C_GOLD),
        ).arrange(DOWN, buff=0.30), ctop)

        # ── Passo 3: argumento interno √(1+ratio²) e με ───────────────────────
        self._show_phase(VGroup(
            Text("Passo 3 – Termos intermediários:", font_size=26),
            MathTex(r"\sqrt{1+0{,}999^2} = \sqrt{1{,}998} \approx 1{,}414",
                    font_size=30, color=FG),
            MathTex(r"\mu\varepsilon = \mu_0\times3\varepsilon_0"
                    r"\approx 3{,}339\times10^{-17}\,\text{s}^2\!/\text{m}^2",
                    font_size=28, color=FG),
        ).arrange(DOWN, buff=0.34), ctop)

        # ── Passo 4: α ────────────────────────────────────────────────────────
        lbl_a  = Text("Passo 4 – Calculando α:", font_size=26)
        fa     = MathTex(
            r"\alpha = \omega\sqrt{\frac{\mu\varepsilon}{2}\!\left["
            r"\sqrt{1+(\sigma/\omega\varepsilon)^2}-1\right]}",
            font_size=28, color=C_ALPHA)
        sub_a  = MathTex(
            r"= 7{,}540\times10^7\times\sqrt{\frac{3{,}339\times10^{-17}}{2}\,(1{,}414-1)}",
            font_size=26, color=C_ALPHA)
        res_a  = MathTex(r"\alpha \approx 0{,}198\,\text{Np/m}",
                         font_size=36, color=C_ALPHA)
        ga = VGroup(lbl_a, fa, sub_a, res_a).arrange(DOWN, buff=0.30)
        self._cp(ga, ctop)
        self.play(FadeIn(lbl_a))
        self.play(Write(fa), run_time=1.0)
        self.play(Write(sub_a), run_time=1.0)
        self.play(Write(res_a), run_time=0.8)
        ba = self.boxed(res_a, color=C_ALPHA)
        self.play(Create(ba))
        self.wait(1.0)
        self.play(FadeOut(VGroup(ga, ba)))
        self.wait(0.2)

        # ── Passo 5: β ────────────────────────────────────────────────────────
        lbl_b  = Text("Passo 5 – Calculando β:", font_size=26)
        fb     = MathTex(
            r"\beta = \omega\sqrt{\frac{\mu\varepsilon}{2}\!\left["
            r"\sqrt{1+(\sigma/\omega\varepsilon)^2}+1\right]}",
            font_size=28, color=C_BETA)
        sub_b  = MathTex(
            r"= 7{,}540\times10^7\times\sqrt{\frac{3{,}339\times10^{-17}}{2}\,(1{,}414+1)}",
            font_size=26, color=C_BETA)
        res_b  = MathTex(r"\beta \approx 0{,}479\,\text{rad/m}",
                         font_size=36, color=C_BETA)
        gb = VGroup(lbl_b, fb, sub_b, res_b).arrange(DOWN, buff=0.30)
        self._cp(gb, ctop)
        self.play(FadeIn(lbl_b))
        self.play(Write(fb), run_time=1.0)
        self.play(Write(sub_b), run_time=1.0)
        self.play(Write(res_b), run_time=0.8)
        bb = self.boxed(res_b, color=C_BETA)
        self.play(Create(bb))
        self.wait(0.5)

        footer = self.caption_bottom(
            "α e β completamente calculados para o Exercício 1!", color=FG)
        self.play(FadeIn(footer))
        self.wait(2.5)

    # ─────────────────────────────────────────────────────────────────────────
    # Cena 2 – Exercício 2: A queda da amplitude pela metade
    # ─────────────────────────────────────────────────────────────────────────
    def cena_2_amplitude_metade(self):
        title, sep = self.scene_header("Exercício 2: Onde a onda perde metade de sua força?")
        # Move up to gain space
        title.shift(UP * 0.25)
        sep.shift(UP * 0.25)
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        ctop = sep.get_bottom()[1] - 0.75

        # ── Painel de dados ───────────────────────────────────────────────────
        self._show_panel([
            (r"f = 5\,\text{MHz}", C_OMEGA),
            (r"\sigma = 2{,}0\times10^{-3}\,\text{S/m}", C_SIGMA),
            (r"\varepsilon = 2\varepsilon_0", C_EPS),
            (r"E_0 = 200\,\text{mV/m}", C_ALPHA),
        ], ctop)

        # ── Passo 1: ω ────────────────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 1 – Calcular ω:", font_size=26),
            MathTex(r"\omega = 2\pi\times5\times10^6 \approx 3{,}142\times10^7\,\text{rad/s}",
                    font_size=30, color=C_OMEGA),
        ).arrange(DOWN, buff=0.30), ctop)

        # ── Passo 2: ωε e razão ───────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 2 – Calcular ωε e a razão σ/ωε:", font_size=26),
            MathTex(r"\omega\varepsilon = 3{,}142\times10^7\times2\times8{,}854\times10^{-12}",
                    font_size=26, color=C_EPS),
            MathTex(r"\omega\varepsilon \approx 5{,}563\times10^{-4}\,\text{S/m}",
                    font_size=28, color=C_EPS),
            MathTex(
                r"\frac{\sigma}{\omega\varepsilon}=\frac{2{,}0\times10^{-3}}"
                r"{5{,}563\times10^{-4}}\approx3{,}595\;\Rightarrow\;\text{meio geral}",
                font_size=26, color=C_GOLD),
        ).arrange(DOWN, buff=0.28), ctop)

        # ── Passo 3: termos intermediários ────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 3 – Termos intermediários:", font_size=26),
            MathTex(r"\sqrt{1+3{,}595^2}=\sqrt{13{,}924}\approx3{,}731",
                    font_size=30, color=FG),
            MathTex(r"\mu\varepsilon = \mu_0\times2\varepsilon_0"
                    r"\approx2{,}225\times10^{-17}\,\text{s}^2\!/\text{m}^2",
                    font_size=28, color=FG),
        ).arrange(DOWN, buff=0.34), ctop)

        # ── Passo 4: α ────────────────────────────────────────────────────────
        lbl_a = Text("Passo 4 – Calculando α:", font_size=26)
        fa    = MathTex(
            r"\alpha = \omega\sqrt{\frac{\mu\varepsilon}{2}(\sqrt{1+ratio^2}-1)}",
            font_size=28, color=C_ALPHA)
        sa    = MathTex(
            r"= 3{,}142\times10^7\times\sqrt{\frac{2{,}225\times10^{-17}}{2}\,(3{,}731-1)}",
            font_size=26, color=C_ALPHA)
        ra    = MathTex(r"\alpha \approx 0{,}173\,\text{Np/m}",
                        font_size=36, color=C_ALPHA)
        ga = VGroup(lbl_a, fa, sa, ra).arrange(DOWN, buff=0.30)
        self._cp(ga, ctop)
        self.play(FadeIn(lbl_a))
        self.play(Write(fa), run_time=1.0)
        self.play(Write(sa), run_time=1.0)
        self.play(Write(ra), run_time=0.8)
        bxa = self.boxed(ra, color=C_ALPHA)
        self.play(Create(bxa))
        self.wait(1.0)
        self.play(FadeOut(VGroup(ga, bxa)))
        self.wait(0.2)

        # ── Passo 5: β (mostrado rapidamente antes do cálculo de z) ──────────
        lbl_b = Text("Passo 5 – Calculando β:", font_size=26)
        sb    = MathTex(
            r"= 3{,}142\times10^7\times\sqrt{\frac{2{,}225\times10^{-17}}{2}\,(3{,}731+1)}",
            font_size=26, color=C_BETA)
        rb    = MathTex(r"\beta \approx 0{,}228\,\text{rad/m}",
                        font_size=36, color=C_BETA)
        gb = VGroup(lbl_b, sb, rb).arrange(DOWN, buff=0.30)
        self._cp(gb, ctop)
        self.play(FadeIn(lbl_b))
        self.play(Write(sb), run_time=1.0)
        self.play(Write(rb), run_time=0.8)
        bxb = self.boxed(rb, color=C_BETA)
        self.play(Create(bxb))
        self.wait(0.8)
        self.play(FadeOut(VGroup(gb, bxb)))
        self.wait(0.2)

        # ── Passo 6: Campo instantâneo ────────────────────────────────────────
        lbl_build = Text("Montando o campo instantâneo:", font_size=26, color=FG)
        field_eq  = MathTex(
            r"\vec{e} = E_0\,e^{-\alpha z}\cos(\omega t-\beta z)\,\hat{x}",
            font_size=32)
        field_sub = MathTex(
            r"\vec{e} = 200\,e^{-0{,}173\,z}"
            r"\cos(3{,}14\times10^7\,t-0{,}228\,z)\,\hat{x}\;[\text{mV/m}]",
            font_size=26, color=C_ALPHA)
        gf = VGroup(lbl_build, field_eq, field_sub).arrange(DOWN, buff=0.35)
        self._cp(gf, ctop)
        self.play(FadeIn(lbl_build))
        self.play(Write(field_eq), run_time=1.0)
        self.play(Write(field_sub), run_time=1.0)

        amp_box = SurroundingRectangle(
            field_sub, color=C_GOLD, buff=0.12, stroke_width=3)
        amp_lbl = Text("Amplitude: 200 e^(-0,173z)", font_size=20, color=C_GOLD)
        amp_lbl.next_to(amp_box, DOWN, buff=0.14)
        self.play(Create(amp_box), FadeIn(amp_lbl))
        self.wait(0.8)
        self.play(FadeOut(VGroup(gf, amp_box, amp_lbl)))
        self.wait(0.2)

        # ── Passo 7: Algebrizar para encontrar z ──────────────────────────────
        lbl_q  = Text("Passo 7 – Onde a amplitude cai à metade?",
                      font_size=26, color=C_GOLD, weight=BOLD)
        eq_half = MathTex(r"200\,e^{-0{,}173\,z} = 100", font_size=40)
        gq = VGroup(lbl_q, eq_half).arrange(DOWN, buff=0.35)
        # Shift slightly more down to avoid confusion with previous transient steps
        self._cp(gq, ctop)
        gq.shift(DOWN * 0.4)
        self.play(FadeIn(lbl_q))
        self.play(Write(eq_half))
        self.wait(0.5)

        alg_y = eq_half.get_center()[1]
        step1 = MathTex(r"e^{-0{,}173\,z} = 0{,}5",
                        font_size=42).move_to([0, alg_y, 0])
        step2 = MathTex(r"-0{,}173\,z = \ln(0{,}5) = -0{,}693",
                        font_size=38).move_to([0, alg_y, 0])
        step3 = MathTex(r"z = \frac{0{,}693}{0{,}173} \approx 4{,}01\,\text{m}",
                        font_size=42, color=C_GOLD).move_to([0, alg_y, 0])

        self.play(TransformMatchingTex(eq_half, step1), run_time=1.0)
        self.wait(0.6)
        self.play(TransformMatchingTex(step1, step2), run_time=1.1)
        self.wait(0.6)

        # Shift step3 slightly down to avoid overlapping the bounding box with step2's position
        step3.shift(DOWN * 0.4)
        self.play(TransformMatchingTex(step2, step3), run_time=1.1)
        br = self.boxed(step3)
        self.play(Create(br))
        self.wait(0.4)
        self.play(FadeOut(lbl_q))

        footer = self.caption_bottom(
            "Isolamos a amplitude para encontrar a distância z!", color=FG)
        self.play(FadeIn(footer))
        self.wait(2.5)

    # ─────────────────────────────────────────────────────────────────────────
    # Cena 3 – Exercício 3: Resolução completa (γ, η, Vp, Vg)
    # ─────────────────────────────────────────────────────────────────────────
    def cena_3_impedancia_velocidades(self):
        title, sep = self.scene_header("Exercício 3: Fator de Propagação, η e Velocidades")
        # Global vertical shift to avoid overlap
        title.shift(UP * 0.25)
        sep.shift(UP * 0.25)
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        ctop = sep.get_bottom()[1] - 0.75

        # ── Painel de dados ───────────────────────────────────────────────────
        self._show_panel([
            (r"\omega = 5\times10^7\,\text{rad/s}", C_OMEGA),
            (r"\mu = \mu_0,\quad\varepsilon = 20\varepsilon_0", C_EPS),
            (r"\sigma = 12\,\text{mS/m}", C_SIGMA),
        ], ctop, width=5.8)

        # ── Passo 1: ωε e razão ───────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 1 – Calcular ωε e testar o meio:", font_size=26),
            MathTex(r"\omega\varepsilon = 5\times10^7\times20\times8{,}854\times10^{-12}",
                    font_size=26, color=C_EPS),
            MathTex(r"\omega\varepsilon \approx 8{,}854\times10^{-3}\,\text{S/m}",
                    font_size=28, color=C_EPS),
            MathTex(
                r"\frac{\sigma}{\omega\varepsilon}=\frac{0{,}012}{8{,}854\times10^{-3}}"
                r"\approx1{,}355\;\Rightarrow\;\text{meio geral}",
                font_size=26, color=C_GOLD),
        ).arrange(DOWN, buff=0.28), ctop)

        # ── Passo 2: termos intermediários ────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 2 – Termos intermediários:", font_size=26),
            MathTex(r"\sqrt{1+1{,}355^2}=\sqrt{2{,}836}\approx1{,}684",
                    font_size=30, color=FG),
            MathTex(r"\mu\varepsilon=\mu_0\times20\varepsilon_0"
                    r"\approx2{,}226\times10^{-16}\,\text{s}^2\!/\text{m}^2",
                    font_size=28, color=FG),
        ).arrange(DOWN, buff=0.34), ctop)

        # ── Passo 3: α ────────────────────────────────────────────────────────
        lbl_a = Text("Passo 3 – Calculando α:", font_size=26)
        sa    = MathTex(
            r"\alpha = 5\times10^7\times\sqrt{\frac{2{,}226\times10^{-16}}{2}\,(1{,}684-1)}",
            font_size=26, color=C_ALPHA)
        ra    = MathTex(r"\alpha \approx 0{,}436\,\text{Np/m}",
                        font_size=36, color=C_ALPHA)
        ga = VGroup(lbl_a, sa, ra).arrange(DOWN, buff=0.32)
        self._cp(ga, ctop)
        self.play(FadeIn(lbl_a)); self.play(Write(sa), run_time=1.0)
        self.play(Write(ra), run_time=0.8)
        ba = self.boxed(ra, color=C_ALPHA); self.play(Create(ba))
        self.wait(0.9); self.play(FadeOut(VGroup(ga, ba))); self.wait(0.2)

        # ── Passo 4: β ────────────────────────────────────────────────────────
        lbl_b = Text("Passo 4 – Calculando β:", font_size=26)
        sb    = MathTex(
            r"\beta = 5\times10^7\times\sqrt{\frac{2{,}226\times10^{-16}}{2}\,(1{,}684+1)}",
            font_size=26, color=C_BETA)
        rb    = MathTex(r"\beta \approx 0{,}864\,\text{rad/m}",
                        font_size=36, color=C_BETA)
        gb = VGroup(lbl_b, sb, rb).arrange(DOWN, buff=0.32)
        self._cp(gb, ctop)
        self.play(FadeIn(lbl_b)); self.play(Write(sb), run_time=1.0)
        self.play(Write(rb), run_time=0.8)
        bb = self.boxed(rb, color=C_BETA); self.play(Create(bb))
        self.wait(0.9); self.play(FadeOut(VGroup(gb, bb))); self.wait(0.2)

        # ── Passo 5: η ────────────────────────────────────────────────────────
        lbl_e = Text("Passo 5 – Impedância intrínseca η:", font_size=26)
        fe    = MathTex(r"\eta = \frac{j\omega\mu}{\gamma}",
                        font_size=34, color=C_ETA)
        ne1   = MathTex(
            r"j\omega\mu = j\times5\times10^7\times4\pi\times10^{-7} = j\,62{,}83\,\Omega/\text{m}",
            font_size=26, color=C_ETA)
        ne2   = MathTex(
            r"\gamma = 0{,}436 + j\,0{,}864 \;\Rightarrow\; |\gamma|=\sqrt{0{,}436^2+0{,}864^2}\approx0{,}968",
            font_size=24, color=C_GAMMA)
        ne3   = MathTex(
            r"|\eta| = \frac{|j\omega\mu|}{|\gamma|} = \frac{62{,}83}{0{,}968} \approx 64{,}9\,\Omega",
            font_size=28, color=C_ETA)
        ne4   = MathTex(
            r"\angle\eta = 90^\circ - \arctan\!\left(\frac{0{,}864}{0{,}436}\right)"
            r"= 90^\circ - 63{,}2^\circ \approx 26{,}8^\circ",
            font_size=26, color=C_ETA)
        re    = MathTex(r"\eta \approx 64{,}9\,\angle\,26{,}8^\circ\,\Omega",
                        font_size=34, color=C_ETA)
        ge = VGroup(lbl_e, fe, ne1, ne2, ne3, ne4, re).arrange(DOWN, buff=0.25)
        self._cp(ge, ctop)
        self.play(FadeIn(lbl_e)); self.play(Write(fe), run_time=0.8)
        self.play(Write(ne1), run_time=0.9)
        self.play(Write(ne2), run_time=0.9)
        self.play(Write(ne3), run_time=0.9)
        self.play(Write(ne4), run_time=0.9)
        self.play(Write(re), run_time=0.8)
        be = self.boxed(re, color=C_ETA); self.play(Create(be))
        self.wait(1.0); self.play(FadeOut(VGroup(ge, be))); self.wait(0.2)

        # ── Passo 6: Vp ───────────────────────────────────────────────────────
        lbl_vp = Text("Passo 6 – Velocidade de fase Vp:", font_size=26, color=C_VP)
        fvp    = MathTex(r"V_p = \frac{\omega}{\beta}", font_size=34, color=C_VP)
        svp    = MathTex(r"= \frac{5\times10^7}{0{,}864}", font_size=30, color=C_VP)
        rvp    = MathTex(r"V_p \approx 5{,}79\times10^7\,\text{m/s}",
                         font_size=34, color=C_VP)
        gvp = VGroup(lbl_vp, fvp, svp, rvp).arrange(DOWN, buff=0.30)
        self._cp(gvp, ctop)
        self.play(FadeIn(lbl_vp)); self.play(Write(fvp), run_time=0.8)
        self.play(Write(svp), run_time=0.7); self.play(Write(rvp), run_time=0.8)
        bvp = self.boxed(rvp, color=C_VP); self.play(Create(bvp))
        self.wait(0.9); self.play(FadeOut(VGroup(gvp, bvp))); self.wait(0.2)

        # ── Passo 7: Vg ───────────────────────────────────────────────────────
        lbl_vg = Text("Passo 7 – Velocidade de grupo Vg:", font_size=26, color=C_VG)
        fvg    = MathTex(
            r"V_g = \left\{ \text{Im} \left[ \frac{-2\omega\mu\varepsilon + j\mu\sigma}{2\gamma} \right] \right\}^{-1}",
            font_size=32, color=C_VG)
        nvg    = MathTex(
            r"\text{Im}\left[\frac{N}{D}\right] \approx 1{,}377\times10^{-8}\,\text{s/m}",
            font_size=26, color=C_VG)
        rvg    = MathTex(r"V_g = (1{,}377\times10^{-8})^{-1} \approx 7{,}26\times10^7\,\text{m/s}",
                         font_size=32, color=C_VG)
        cmp    = MathTex(r"V_g > V_p \;\Rightarrow\;\text{dispersão normal}",
                         font_size=26, color=FG)
        gvg = VGroup(lbl_vg, fvg, nvg, rvg, cmp).arrange(DOWN, buff=0.28)
        self._cp(gvg, ctop)
        self.play(FadeIn(lbl_vg)); self.play(Write(fvg), run_time=0.8)
        self.play(Write(nvg), run_time=1.0); self.play(Write(rvg), run_time=0.8)
        bvg = self.boxed(rvg, color=C_VG); self.play(Create(bvg))
        self.play(FadeIn(cmp))
        self.wait(0.8)

        footer = self.caption_bottom(
            "Exercício 3 completo: γ, η, Vp e Vg calculados!", color=FG)
        self.play(FadeIn(footer))
        self.wait(2.0)

    # ─────────────────────────────────────────────────────────────────────────
    # Cena 3b – Exercício 5: Velocidades de fase e grupo
    # ─────────────────────────────────────────────────────────────────────────
    def cena_3b_exercicio5(self):
        title, sep = self.scene_header("Exercício 5: Velocidades de Fase e de Grupo")
        # Shift up to gain space below
        title.shift(UP * 0.25)
        sep.shift(UP * 0.25)
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        ctop = sep.get_bottom()[1] - 0.75

        # ── Painel de dados ───────────────────────────────────────────────────
        self._show_panel([
            (r"f = 18\,\text{MHz}", C_OMEGA),
            (r"\varepsilon = 4\varepsilon_0,\quad\mu = \mu_0", C_EPS),
            (r"\sigma = 4\times10^{-3}\,\text{S/m}", C_SIGMA),
        ], ctop, width=5.4)

        # ── Passo 1: ω ────────────────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 1 – Calcular ω:", font_size=26),
            MathTex(r"\omega = 2\pi\times18\times10^6"
                    r"\approx1{,}131\times10^8\,\text{rad/s}",
                    font_size=30, color=C_OMEGA),
        ).arrange(DOWN, buff=0.30), ctop)

        # ── Passo 2: ωε e razão ───────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 2 – Calcular ωε e testar o meio:", font_size=26),
            MathTex(r"\omega\varepsilon=1{,}131\times10^8\times4\times8{,}854\times10^{-12}",
                    font_size=26, color=C_EPS),
            MathTex(r"\omega\varepsilon\approx4{,}006\times10^{-3}\,\text{S/m}",
                    font_size=28, color=C_EPS),
            MathTex(
                r"\frac{\sigma}{\omega\varepsilon}=\frac{4\times10^{-3}}"
                r"{4{,}006\times10^{-3}}\approx0{,}998\;\Rightarrow\;\text{meio geral}",
                font_size=26, color=C_GOLD),
        ).arrange(DOWN, buff=0.28), ctop)

        # ── Passo 3: termos intermediários ────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 3 – Termos intermediários:", font_size=26),
            MathTex(r"\sqrt{1+0{,}998^2}=\sqrt{1{,}996}\approx1{,}413",
                    font_size=30, color=FG),
            MathTex(r"\mu\varepsilon=\mu_0\times4\varepsilon_0"
                    r"\approx4{,}452\times10^{-17}\,\text{s}^2\!/\text{m}^2",
                    font_size=28, color=FG),
        ).arrange(DOWN, buff=0.34), ctop)

        # ── Passo 4: α ────────────────────────────────────────────────────────
        lbl_a = Text("Passo 4 – Calculando α:", font_size=26)
        sa    = MathTex(
            r"\alpha = 1{,}131\times10^8\times"
            r"\sqrt{\frac{4{,}452\times10^{-17}}{2}\,(1{,}413-1)}",
            font_size=26, color=C_ALPHA)
        ra    = MathTex(r"\alpha \approx 0{,}343\,\text{Np/m}",
                        font_size=36, color=C_ALPHA)
        ga = VGroup(lbl_a, sa, ra).arrange(DOWN, buff=0.32)
        self._cp(ga, ctop)
        self.play(FadeIn(lbl_a)); self.play(Write(sa), run_time=1.0)
        self.play(Write(ra), run_time=0.8)
        ba = self.boxed(ra, color=C_ALPHA); self.play(Create(ba))
        self.wait(0.9); self.play(FadeOut(VGroup(ga, ba))); self.wait(0.2)

        # ── Passo 5: β ────────────────────────────────────────────────────────
        lbl_b = Text("Passo 5 – Calculando β:", font_size=26)
        sb    = MathTex(
            r"\beta = 1{,}131\times10^8\times"
            r"\sqrt{\frac{4{,}452\times10^{-17}}{2}\,(1{,}413+1)}",
            font_size=26, color=C_BETA)
        rb    = MathTex(r"\beta \approx 0{,}829\,\text{rad/m}",
                        font_size=36, color=C_BETA)
        gb = VGroup(lbl_b, sb, rb).arrange(DOWN, buff=0.32)
        self._cp(gb, ctop)
        self.play(FadeIn(lbl_b)); self.play(Write(sb), run_time=1.0)
        self.play(Write(rb), run_time=0.8)
        bb = self.boxed(rb, color=C_BETA); self.play(Create(bb))
        self.wait(0.9); self.play(FadeOut(VGroup(gb, bb))); self.wait(0.2)

        # ── Passo 6: Vp ───────────────────────────────────────────────────────
        lbl_vp = Text("Passo 6 – Velocidade de fase Vp:", font_size=26, color=C_VP)
        fvp    = MathTex(r"V_p = \frac{\omega}{\beta}", font_size=34, color=C_VP)
        svp    = MathTex(r"= \frac{1{,}131\times10^8}{0{,}829}",
                         font_size=30, color=C_VP)
        rvp    = MathTex(r"V_p \approx 1{,}365\times10^8\,\text{m/s}",
                         font_size=34, color=C_VP)
        gvp = VGroup(lbl_vp, fvp, svp, rvp).arrange(DOWN, buff=0.30)
        self._cp(gvp, ctop)
        self.play(FadeIn(lbl_vp)); self.play(Write(fvp), run_time=0.8)
        self.play(Write(svp), run_time=0.7); self.play(Write(rvp), run_time=0.8)
        bvp = self.boxed(rvp, color=C_VP); self.play(Create(bvp))
        self.wait(0.9); self.play(FadeOut(VGroup(gvp, bvp))); self.wait(0.2)

        # ── Passo 7: Vg ───────────────────────────────────────────────────────
        lbl_vg = Text("Passo 7 – Velocidade de grupo Vg:", font_size=26, color=C_VG)
        fvg    = MathTex(
            r"V_g = \left\{ \text{Im} \left[ \frac{-2\omega\mu\varepsilon + j\mu\sigma}{2\gamma} \right] \right\}^{-1}",
            font_size=32, color=C_VG)
        nvg    = MathTex(
            r"\text{Im}\left[\frac{N}{D}\right] \approx 6{,}258\times10^{-9}\,\text{s/m}",
            font_size=26, color=C_VG)
        rvg    = MathTex(r"V_g = (6{,}258\times10^{-9})^{-1} \approx 1{,}598\times10^8\,\text{m/s}",
                         font_size=32, color=C_VG)
        cmp    = MathTex(r"V_g > V_p \;\Rightarrow\;\text{dispersão normal}",
                         font_size=26, color=FG)
        gvg = VGroup(lbl_vg, fvg, nvg, rvg, cmp).arrange(DOWN, buff=0.28)
        self._cp(gvg, ctop)
        self.play(FadeIn(lbl_vg)); self.play(Write(fvg), run_time=0.8)
        self.play(Write(nvg), run_time=1.0); self.play(Write(rvg), run_time=0.8)
        bvg = self.boxed(rvg, color=C_VG); self.play(Create(bvg))
        self.play(FadeIn(cmp))
        self.wait(0.8)

        footer = self.caption_bottom(
            "Calculando a rapidez da crista (Vp) e do pacote (Vg).", color=FG)
        self.play(FadeIn(footer))
        self.wait(2.5)

    # ─────────────────────────────────────────────────────────────────────────
    # Cena 4 – Exercício 4 (Parte 1): O Fasor Magnético
    # ─────────────────────────────────────────────────────────────────────────
    def cena_4_fasor_magnetico(self):
        title, sep = self.scene_header("Exercício 4: O Caminho Completo da Onda")
        # Global vertical shift
        title.shift(UP * 0.25)
        sep.shift(UP * 0.25)
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        ctop = sep.get_bottom()[1] - 0.75

        # ── Painel de dados + fasor de entrada ────────────────────────────────
        self._show_panel([
            (r"\omega = 10^8\,\text{rad/s}", C_OMEGA),
            (r"\varepsilon = 3\varepsilon_0,\quad\mu=\mu_0", C_EPS),
            (r"\sigma = 2\times10^{-3}\,\text{S/m}", C_SIGMA),
        ], ctop, width=5.4)

        lbl_E0 = Text("Fasor elétrico de entrada:", font_size=26)
        phasor_E = MathTex(
            r"\vec{E} = (10\,\hat{x} + j20\,\hat{y})\,e^{-\gamma z}",
            font_size=36, color=C_GAMMA)
        gE0 = VGroup(lbl_E0, phasor_E).arrange(DOWN, buff=0.30)
        self._cp(gE0, ctop)
        self.play(FadeIn(lbl_E0)); self.play(Write(phasor_E), run_time=1.0)
        box_E0 = self.boxed(phasor_E, color=C_GAMMA); self.play(Create(box_E0))
        self.wait(1.0); self.play(FadeOut(VGroup(gE0, box_E0))); self.wait(0.2)

        # ── Passo 1: ωε e razão ───────────────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 1 – Calcular ωε:", font_size=26),
            MathTex(r"\omega\varepsilon=10^8\times3\times8{,}854\times10^{-12}"
                    r"\approx2{,}656\times10^{-3}\,\text{S/m}",
                    font_size=27, color=C_EPS),
            MathTex(
                r"\frac{\sigma}{\omega\varepsilon}=\frac{2\times10^{-3}}"
                r"{2{,}656\times10^{-3}}\approx0{,}753\;\Rightarrow\;\text{meio geral}",
                font_size=26, color=C_GOLD),
        ).arrange(DOWN, buff=0.30), ctop)

        # ── Passo 2: termos intermediários ────────────────────────────────────
        self._show_phase(VGroup(
            Text("Passo 2 – Termos intermediários:", font_size=26),
            MathTex(r"\sqrt{1+0{,}753^2}=\sqrt{1{,}567}\approx1{,}252",
                    font_size=30, color=FG),
            MathTex(r"\mu\varepsilon=\mu_0\times3\varepsilon_0"
                    r"\approx3{,}339\times10^{-17}\,\text{s}^2\!/\text{m}^2",
                    font_size=28, color=FG),
        ).arrange(DOWN, buff=0.34), ctop)

        # ── Passo 3: α ────────────────────────────────────────────────────────
        lbl_a = Text("Passo 3 – Calculando α:", font_size=26)
        sa    = MathTex(
            r"\alpha=10^8\times\sqrt{\frac{3{,}339\times10^{-17}}{2}\,(1{,}252-1)}",
            font_size=26, color=C_ALPHA)
        ra    = MathTex(r"\alpha \approx 0{,}205\,\text{Np/m}",
                        font_size=36, color=C_ALPHA)
        ga = VGroup(lbl_a, sa, ra).arrange(DOWN, buff=0.32)
        self._cp(ga, ctop)
        self.play(FadeIn(lbl_a)); self.play(Write(sa), run_time=1.0)
        self.play(Write(ra), run_time=0.8)
        ba = self.boxed(ra, color=C_ALPHA); self.play(Create(ba))
        self.wait(0.9); self.play(FadeOut(VGroup(ga, ba))); self.wait(0.2)

        # ── Passo 4: β ────────────────────────────────────────────────────────
        lbl_b = Text("Passo 4 – Calculando β:", font_size=26)
        sb    = MathTex(
            r"\beta=10^8\times\sqrt{\frac{3{,}339\times10^{-17}}{2}\,(1{,}252+1)}",
            font_size=26, color=C_BETA)
        rb    = MathTex(r"\beta \approx 0{,}613\,\text{rad/m}",
                        font_size=36, color=C_BETA)
        gb = VGroup(lbl_b, sb, rb).arrange(DOWN, buff=0.32)
        self._cp(gb, ctop)
        self.play(FadeIn(lbl_b)); self.play(Write(sb), run_time=1.0)
        self.play(Write(rb), run_time=0.8)
        bb = self.boxed(rb, color=C_BETA); self.play(Create(bb))
        self.wait(0.9); self.play(FadeOut(VGroup(gb, bb))); self.wait(0.2)

        # ── Passo 5: η ────────────────────────────────────────────────────────
        lbl_e = Text("Passo 5 – Impedância intrínseca η:", font_size=26)
        fe    = MathTex(r"\eta = \frac{j\omega\mu}{\gamma}",
                        font_size=34, color=C_ETA)
        ne1   = MathTex(
            r"j\omega\mu=j\times10^8\times4\pi\times10^{-7}=j\,125{,}7\,\Omega/\text{m}",
            font_size=26, color=C_ETA)
        ne2   = MathTex(
            r"|\gamma|=\sqrt{0{,}205^2+0{,}613^2}\approx0{,}647",
            font_size=26, color=C_GAMMA)
        ne3   = MathTex(
            r"|\eta|=\frac{125{,}7}{0{,}647}\approx194{,}4\,\Omega",
            font_size=28, color=C_ETA)
        ne4   = MathTex(
            r"\angle\eta=90^\circ-\arctan\!\left(\frac{0{,}613}{0{,}205}\right)"
            r"=90^\circ-71{,}5^\circ\approx18{,}5^\circ",
            font_size=26, color=C_ETA)
        re    = MathTex(r"\eta\approx194{,}4\,\angle\,18{,}5^\circ\,\Omega",
                        font_size=34, color=C_ETA)
        ge = VGroup(lbl_e, fe, ne1, ne2, ne3, ne4, re).arrange(DOWN, buff=0.24)
        self._cp(ge, ctop)
        self.play(FadeIn(lbl_e)); self.play(Write(fe), run_time=0.7)
        for m in [ne1, ne2, ne3, ne4, re]:
            self.play(Write(m), run_time=0.8)
        be = self.boxed(re, color=C_ETA); self.play(Create(be))
        self.wait(1.0); self.play(FadeOut(VGroup(ge, be))); self.wait(0.2)

        # ── Passo 6: Regra H = (γ̂ × E)/η ────────────────────────────────────
        lbl_H = Text("Passo 6 – Calcular o fasor H:", font_size=26)
        rule_eq = MathTex(
            r"\vec{H} = \frac{\hat{\gamma}\times\vec{E}}{\eta}"
            r"\quad\text{com}\quad\hat{\gamma}=\hat{z}",
            font_size=30, color=C_ETA)
        dir_n = MathTex(
            r"\hat{z}\times(10\hat{x}+j20\hat{y})"
            r"= 10\underbrace{(\hat{z}\times\hat{x})}_{=\hat{y}}"
            r"+j20\underbrace{(\hat{z}\times\hat{y})}_{=-\hat{x}}",
            font_size=26, color=FG)
        H_res = MathTex(
            r"\vec{H}=\frac{-j20\,\hat{x}+10\,\hat{y}}{\eta}\,e^{-\gamma z}",
            font_size=32, color=C_ETA)
        gH = VGroup(lbl_H, rule_eq, dir_n, H_res).arrange(DOWN, buff=0.32)
        self._cp(gH, ctop)
        self.play(FadeIn(lbl_H)); self.play(Write(rule_eq), run_time=1.0)
        self.play(Write(dir_n), run_time=1.2)
        self.play(Write(H_res), run_time=1.0)
        bH = self.boxed(H_res, color=C_ETA); self.play(Create(bH))

        footer = self.caption_bottom("O Produto Vetorial define a direção de H!", color=FG)
        self.play(FadeIn(footer))
        self.wait(2.5)

    # ─────────────────────────────────────────────────────────────────────────
    # Cena 5 – Exercício 4 (Parte 2): Retorno ao Domínio do Tempo
    # ─────────────────────────────────────────────────────────────────────────
    def cena_5_dominio_tempo(self):
        title, sep = self.scene_header("Transformando Fasores em Campos Reais")
        # Global vertical shift
        title.shift(UP * 0.25)
        sep.shift(UP * 0.25)
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        ctop = sep.get_bottom()[1] - 1.10

        # ── Show E and H phasors side by side ─────────────────────────────────
        phasor_y = ctop - 0.40
        lbl_E = Text("Fasor E:", font_size=22, color=C_GAMMA)
        lbl_E.move_to([-4.5, phasor_y, 0])
        lbl_H = Text("Fasor H:", font_size=22, color=C_ETA)
        lbl_H.move_to([1.6, phasor_y, 0])

        eq_E_ph = MathTex(
            r"\vec{E} = (10\,\hat{x} + i20\,\hat{y})e^{-\gamma z}",
            font_size=28, color=C_GAMMA,
        ).next_to(lbl_E, DOWN, buff=0.18)

        eq_H_ph = MathTex(
            r"\vec{H} = \frac{-i20\,\hat{x} + 10\,\hat{y}}{\eta}\,e^{-\gamma z}",
            font_size=28, color=C_ETA,
        ).next_to(lbl_H, DOWN, buff=0.18)

        self.play(FadeIn(lbl_E), Write(eq_E_ph), run_time=0.9)
        self.play(FadeIn(lbl_H), Write(eq_H_ph), run_time=0.9)
        self.wait(0.6)

        # ── Highlight imaginary parts ─────────────────────────────────────────
        imag_note = Text(
            "Os coeficientes i e a fase de η introduzem defasagem entre E e H.",
            font_size=20, color=FG,
        ).next_to(eq_E_ph, DOWN, buff=0.88).to_edge(LEFT, buff=0.45)
        box_i_E = SurroundingRectangle(eq_E_ph, color=C_GOLD, buff=0.10, stroke_width=2)
        box_i_H = SurroundingRectangle(eq_H_ph, color=C_GOLD, buff=0.10, stroke_width=2)
        self.play(Create(box_i_E), Create(box_i_H))
        self.play(FadeIn(imag_note))
        self.wait(0.8)
        self.play(FadeOut(box_i_E), FadeOut(box_i_H), FadeOut(imag_note))

        # ── The magic step: multiply by e^{iωt} ───────────────────────────────
        lbl_magic = Text(
            "Multiplicar por e^(iwt), isolar e^(-az) e aplicar Euler!",
            font_size=22, color=C_GOLD,
        ).next_to(eq_E_ph, DOWN, buff=0.88).to_edge(LEFT, buff=0.45)
        self.play(FadeIn(lbl_magic))
        self.wait(0.5)

        expand_eq = MathTex(
            r"e^{-\gamma z} = e^{-(\alpha+i\beta)z} = e^{-\alpha z}\cdot e^{-i\beta z}",
            font_size=30, color=FG,
        ).next_to(lbl_magic, DOWN, buff=0.30)
        self.play(Write(expand_eq), run_time=1.0)
        self.wait(0.6)

        euler_note = MathTex(
            r"e^{i\omega t}\cdot e^{-i\beta z} = e^{i(\omega t-\beta z)}"
            r"= \cos(\omega t-\beta z) + i\sin(\omega t-\beta z)",
            font_size=24, color=FG,
        ).next_to(expand_eq, DOWN, buff=0.28)
        self.play(Write(euler_note), run_time=1.1)
        self.wait(0.6)

        # ── "Magic eraser": keep only real part ───────────────────────────────
        erase_note = Text("Selecionando apenas a parte Real…", font_size=22, color=C_RED)\
            .next_to(euler_note, DOWN, buff=0.30)
        self.play(FadeIn(erase_note, shift=UP * 0.1))
        self.wait(0.4)

        self.play(
            FadeOut(lbl_magic), FadeOut(expand_eq),
            FadeOut(euler_note), FadeOut(erase_note),
        )

        # ── Final instantaneous fields ─────────────────────────────────────────
        # Numerical values: |η|≈62.8, ∠η≈4.6° → phase_eta=0.080 rad
        # Ex phasor: 10x̂ + 20∠90° ŷ → 10∠0° x̂ + 20∠90° ŷ
        # At z=0, t-domain: e_x=10e^{-αz}cos(ωt-βz), e_y=20e^{-αz}cos(ωt-βz-90°)=-20e^{-αz}sin(ωt-βz)
        # H: (-i20x̂+10ŷ)/η = (-20∠90° x̂ + 10∠0° ŷ)/62.8∠4.6°
        #   h_x = -20/(62.8) cos(ωt-βz+90°-4.6°) = -0.318 cos(ωt-βz+85.4°)
        #   h_y = 10/(62.8) cos(ωt-βz-4.6°) = 0.159 cos(ωt-βz-4.6°)

        final_e = MathTex(
            r"\vec{e}(z,t) = e^{-\alpha z}\left["
            r"10\cos(\omega t - \beta z)\,\hat{x}"
            r"- 20\sin(\omega t - \beta z)\,\hat{y}\right]",
            font_size=28, color=C_GAMMA,
        ).next_to(sep, DOWN, buff=1.2)

        final_h = MathTex(
            r"\vec{h}(z,t) = \frac{e^{-\alpha z}}{|\eta|}\left["
            r"-20\cos(\omega t - \beta z + \varphi_\eta + 90^\circ)\,\hat{x}"
            r"+10\cos(\omega t - \beta z - \varphi_\eta)\,\hat{y}\right]",
            font_size=24, color=C_ETA,
        ).next_to(final_e, DOWN, buff=0.45)

        self.play(FadeOut(lbl_E), FadeOut(lbl_H), FadeOut(eq_E_ph), FadeOut(eq_H_ph))

        self.play(Write(final_e), run_time=1.4)
        box_e = self.boxed(final_e, color=C_GAMMA)
        self.play(Create(box_e))
        self.wait(0.5)

        self.play(Write(final_h), run_time=1.4)
        box_h = self.boxed(final_h, color=C_ETA)
        self.play(Create(box_h))
        self.wait(0.6)

        # pulse both boxes
        self.play(
            Indicate(final_e, color=C_GAMMA, scale_factor=1.04),
            Indicate(final_h, color=C_ETA,   scale_factor=1.04),
            run_time=1.0,
        )
        self.wait(0.3)
        self.play(
            Indicate(final_e, color=C_GAMMA, scale_factor=1.04),
            Indicate(final_h, color=C_ETA,   scale_factor=1.04),
            run_time=1.0,
        )

        footer = self.caption_bottom(
            "Selecionando apenas a parte Real… Temos nossa resposta final!", color=FG
        )
        self.play(FadeIn(footer))
        self.wait(3.0)

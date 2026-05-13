from manim import *
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = "#ece6e2"
FG      = "#5c5c5c"
C_GOLD  = "#d4a017"
C_ALPHA = "#27ae60"   # green – attenuation constant α
C_BETA  = "#2471a3"   # blue  – phase constant β
C_GAMMA = "#a93226"   # red   – propagation factor γ
C_PANEL = "#f7f2ee"


# ═════════════════════════════════════════════════════════════════════════════
class EqOndaScene(ThreeDScene):
    """All six scenes for the Wave Equation / Propagation Factor video."""

    # ── Setup ─────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        MathTex.set_default(color=FG)
        # Start in standard 2-D orientation
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        self.cena_1_genesis()
        self.clean_up()

        self.cena_2_dominio_frequencia()
        self.clean_up()

        self.cena_3_anatomia_gamma()
        self.clean_up()

        self.cena_4_casos_particulares()
        self.clean_up()

        self.cena_5_onda_tem()
        self.clean_up()

        self.cena_6_frentes_de_onda()
        self.wait(1)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def clean_up(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.wait(0.25)

    def scene_header(self, text, font_size=36):
        """Returns (title_mob, separator_line) already positioned."""
        title = Text(text, font_size=font_size, color=FG, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        sep = Line(LEFT * 5.8, RIGHT * 5.8, color=FG, stroke_width=1.2)
        sep.next_to(title, DOWN, buff=0.14)
        return title, sep

    def boxed(self, mob, color=C_GOLD, buff=0.18):
        """Surrounds mob with a soft rounded rectangle."""
        box = SurroundingRectangle(mob, color=color, buff=buff,
                                   stroke_width=2.8, corner_radius=0.12)
        box.set_fill(color, opacity=0.05)
        return box

    # ── Scene 1 ───────────────────────────────────────────────────────────────
    def cena_1_genesis(self):
        title, sep = self.scene_header("Derivando a Equação de Onda")
        self.play(Write(title), Create(sep))

        # Context: charge-free region
        region = MathTex(r"\nabla\cdot\vec{d}=0\;\;(\rho=0)",
                         font_size=28, color=C_GOLD)
        region.next_to(sep, DOWN, buff=0.32)
        self.play(FadeIn(region))
        self.wait(0.4)

        # ── Phase A: Faraday's law → apply curl ──────────────────────────────
        lbl_f = Text("Lei de Faraday:", font_size=24, color=FG)
        lbl_f.next_to(region, DOWN, buff=0.42)
        faraday = MathTex(
            r"\nabla\times\vec{e} = -\mu\frac{\partial\vec{h}}{\partial t}",
            font_size=34
        ).next_to(lbl_f, DOWN, buff=0.20)
        self.play(FadeIn(lbl_f), Write(faraday), run_time=1.2)
        self.wait(0.6)

        lbl_curl = Text("Aplicando ∇× em ambos os lados:", font_size=24, color=FG)
        lbl_curl.next_to(faraday, DOWN, buff=0.38)
        curl_eq = MathTex(
            r"\nabla\times(\nabla\times\vec{e}) ="
            r"-\mu\frac{\partial}{\partial t}(\nabla\times\vec{h})",
            font_size=30
        ).next_to(lbl_curl, DOWN, buff=0.20)
        self.play(FadeIn(lbl_curl), Write(curl_eq), run_time=1.3)
        self.wait(0.8)

        # Compact: keep only curl_eq, move it up
        self.play(
            FadeOut(lbl_f), FadeOut(faraday), FadeOut(lbl_curl),
            curl_eq.animate.next_to(region, DOWN, buff=0.38),
        )
        self.wait(0.3)

        # ── Phase B: vector identity → ∇·e = 0 vanishes ─────────────────────
        lbl_id = Text("Identidade vetorial:", font_size=24, color=FG)
        lbl_id.next_to(curl_eq, DOWN, buff=0.40)
        identity = MathTex(
            r"\nabla(\nabla\cdot\vec{e}) - \nabla^2\vec{e}"
            r"= -\mu\frac{\partial}{\partial t}(\nabla\times\vec{h})",
            font_size=28
        ).next_to(lbl_id, DOWN, buff=0.20)
        self.play(FadeIn(lbl_id), Write(identity), run_time=1.3)
        self.wait(0.7)

        # ∇·e = 0 indicator fades in, then term disappears
        zero_note = MathTex(r"\nabla\cdot\vec{e}=0", font_size=26, color=C_GAMMA)
        zero_note.next_to(identity, DOWN, buff=0.30)
        self.play(FadeIn(zero_note))
        self.wait(0.5)

        simplified = MathTex(
            r"-\nabla^2\vec{e}"
            r"= -\mu\frac{\partial}{\partial t}(\nabla\times\vec{h})",
            font_size=30
        ).move_to(identity)
        self.play(
            ReplacementTransform(identity, simplified),
            FadeOut(zero_note),
        )
        self.wait(0.5)

        # Keep simplified, compact upward
        self.play(
            FadeOut(lbl_id), FadeOut(curl_eq),
            simplified.animate.next_to(region, DOWN, buff=0.38),
        )
        self.wait(0.3)

        # ── Phase C: substitute Ampère → Helmholtz in time domain ────────────
        lbl_amp = Text("Substituindo ∇×h pela Lei de Ampère:", font_size=24, color=FG)
        lbl_amp.next_to(simplified, DOWN, buff=0.42)
        self.play(FadeIn(lbl_amp))

        helmholtz = MathTex(
            r"\nabla^2\vec{e}"
            r"-\mu\epsilon\frac{\partial^2\vec{e}}{\partial t^2}"
            r"-\mu\sigma\frac{\partial\vec{e}}{\partial t}=0",
            font_size=34
        ).next_to(lbl_amp, DOWN, buff=0.26)
        self.play(Write(helmholtz), run_time=1.5)
        self.wait(0.6)

        box_h = self.boxed(helmholtz, color=C_GOLD)
        helm_cap = Text("Equação de Helmholtz – domínio do tempo",
                        font_size=22, color=C_GOLD)
        helm_cap.next_to(helmholtz, DOWN, buff=0.36)
        self.play(Create(box_h), FadeIn(helm_cap))
        self.wait(2.5)

    # ── Scene 2 ───────────────────────────────────────────────────────────────
    def cena_2_dominio_frequencia(self):
        title, sep = self.scene_header("Domínio da Frequência (Fasores)")
        self.play(Write(title), Create(sep))

        # Substitution banner
        sub = MathTex(
            r"\frac{\partial}{\partial t}\;\longrightarrow\;i\omega",
            font_size=40, color=C_GOLD
        ).next_to(sep, DOWN, buff=0.40)
        self.play(Write(sub), run_time=1.0)
        self.wait(0.7)

        # Time-domain Helmholtz (reminder)
        helm_t = MathTex(
            r"\nabla^2\vec{e}"
            r"-\mu\epsilon\frac{\partial^2\vec{e}}{\partial t^2}"
            r"-\mu\sigma\frac{\partial\vec{e}}{\partial t}=0",
            font_size=28
        ).next_to(sub, DOWN, buff=0.40)
        self.play(Write(helm_t), run_time=1.2)
        self.wait(0.5)

        arrow_down = Arrow(DOWN * 0.05, DOWN * 0.55, color=C_GOLD, buff=0,
                           max_tip_length_to_length_ratio=0.35, stroke_width=2.5)
        arrow_down.next_to(helm_t, DOWN, buff=0.08)

        helm_f = MathTex(
            r"\nabla^2\vec{E} - i\omega\mu(\sigma+i\omega\epsilon)\vec{E}=0",
            font_size=32
        ).next_to(arrow_down, DOWN, buff=0.12)
        self.play(Create(arrow_down), Write(helm_f), run_time=1.3)
        self.wait(0.7)

        # Fade substitution + time eq; keep helm_f, promote it
        self.play(
            FadeOut(sub), FadeOut(helm_t), FadeOut(arrow_down),
            helm_f.animate.next_to(sep, DOWN, buff=0.42),
        )
        self.wait(0.4)

        # Define γ²
        lbl_def = Text("Identificando o Fator de Propagação:", font_size=24, color=FG)
        lbl_def.next_to(helm_f, DOWN, buff=0.44)
        gamma2 = MathTex(
            r"\gamma^2 = i\omega\mu(\sigma+i\omega\epsilon)",
            font_size=36, color=C_GAMMA
        ).next_to(lbl_def, DOWN, buff=0.22)
        self.play(FadeIn(lbl_def), Write(gamma2), run_time=1.2)
        self.wait(0.5)

        # Simplified wave equation
        wave_eq = MathTex(
            r"\nabla^2\vec{E} - \gamma^2\vec{E} = 0",
            font_size=38
        ).next_to(gamma2, DOWN, buff=0.42)
        self.play(Write(wave_eq), run_time=1.0)
        self.wait(0.5)

        # γ definition – boxed highlight
        gamma_def = MathTex(
            r"\gamma = \sqrt{i\omega\mu(\sigma+i\omega\epsilon)}",
            font_size=36, color=C_GAMMA
        ).next_to(wave_eq, DOWN, buff=0.40)
        self.play(Write(gamma_def), run_time=1.2)
        box_g = self.boxed(gamma_def, color=C_GAMMA)
        self.play(Create(box_g))
        self.wait(2.2)

    # ── Scene 3 ───────────────────────────────────────────────────────────────
    def cena_3_anatomia_gamma(self):
        title, sep = self.scene_header("A Anatomia de γ")
        self.play(Write(title), Create(sep))

        # γ = α + iβ (colour-coded)
        gamma_row = MathTex(
            r"\gamma\;=\;", r"\alpha", r"\;+\;i\,", r"\beta",
            font_size=52
        )
        gamma_row[1].set_color(C_ALPHA)
        gamma_row[3].set_color(C_BETA)
        gamma_row.next_to(sep, DOWN, buff=0.42)
        self.play(Write(gamma_row), run_time=1.0)
        self.wait(0.6)

        # Side-by-side cards for α and β
        alpha_card = self._gamma_card(
            sym=r"\alpha",
            formula=(r"\omega\sqrt{\dfrac{\mu\varepsilon}{2}}"
                     r"\!\left[\sqrt{1+\!\left(\dfrac{\sigma}{\omega\varepsilon}\right)^{\!2}}"
                     r"-1\right]^{\!1/2}"),
            unit=r"\mathrm{Np/m}",
            label="Fator de Atenuação",
            color=C_ALPHA,
        )
        beta_card = self._gamma_card(
            sym=r"\beta",
            formula=(r"\omega\sqrt{\dfrac{\mu\varepsilon}{2}}"
                     r"\!\left[\sqrt{1+\!\left(\dfrac{\sigma}{\omega\varepsilon}\right)^{\!2}}"
                     r"+1\right]^{\!1/2}"),
            unit=r"\mathrm{rad/m}",
            label="Fator de Fase",
            color=C_BETA,
        )

        cards = VGroup(alpha_card, beta_card).arrange(RIGHT, buff=0.5)
        cards.next_to(gamma_row, DOWN, buff=0.50)
        # Fit safely within frame width
        if cards.get_width() > 13.0:
            cards.scale_to_fit_width(13.0)

        self.play(FadeIn(alpha_card, shift=UP * 0.12), run_time=0.9)
        self.wait(0.3)
        self.play(FadeIn(beta_card, shift=UP * 0.12), run_time=0.9)
        self.wait(2.2)

    def _gamma_card(self, sym, formula, unit, label, color, width=6.0, height=3.4):
        rect = RoundedRectangle(corner_radius=0.14, width=width, height=height,
                                color=color, stroke_width=3)
        rect.set_fill(C_PANEL, opacity=0.96)

        sym_mob = MathTex(sym, font_size=40, color=color)
        sym_mob.move_to(rect.get_top() + DOWN * 0.44)

        div = Line(rect.get_left() + RIGHT * 0.18, rect.get_right() + LEFT * 0.18,
                   color=color, stroke_width=1.2)
        div.next_to(sym_mob, DOWN, buff=0.16)

        eq_mob  = MathTex(r"=\;" + formula, font_size=24, color=color)
        unit_mob = MathTex(r"\left[" + unit + r"\right]", font_size=24, color=color)
        lbl_mob  = Text(label, font_size=22, color=color)

        content = VGroup(eq_mob, unit_mob, lbl_mob).arrange(DOWN, buff=0.22)
        content.next_to(div, DOWN, buff=0.22)

        # Prevent content from overflowing card
        max_w = width - 0.36
        if content.get_width() > max_w:
            content.scale_to_fit_width(max_w)
        content.next_to(div, DOWN, buff=0.22)

        return VGroup(rect, sym_mob, div, content)

    # ── Scene 4 ───────────────────────────────────────────────────────────────
    def cena_4_casos_particulares(self):
        title, sep = self.scene_header("Como o Meio Afeta a Onda?")
        self.play(Write(title), Create(sep))
        self.wait(0.35)

        panels = self._case_panels()
        panels.next_to(sep, DOWN, buff=0.38)

        # Scale to fit without overflowing
        if panels.get_width() > 13.4:
            panels.scale_to_fit_width(13.4)
        if panels.get_height() > 5.6:
            panels.scale_to_fit_height(5.6)

        for p in panels:
            self.play(FadeIn(p, shift=UP * 0.12), run_time=0.85)
        self.wait(0.5)

        note = Text("Em meios sem perdas (σ = 0), não há atenuação (α = 0).",
                    font_size=24, color=C_ALPHA)
        note.to_edge(DOWN, buff=0.40)
        self.play(FadeIn(note, shift=UP * 0.15))
        self.wait(2.5)

    def _case_panels(self):
        def panel(title_text, color, lines, w=4.1, h=4.5):
            rect = RoundedRectangle(corner_radius=0.14, width=w, height=h,
                                    color=color, stroke_width=3)
            rect.set_fill(C_PANEL, opacity=0.96)

            ttl = Text(title_text, font_size=24, color=color, weight=BOLD)
            ttl.move_to(rect.get_top() + DOWN * 0.42)

            div = Line(rect.get_left() + RIGHT * 0.16, rect.get_right() + LEFT * 0.16,
                       color=color, stroke_width=1.2)
            div.next_to(ttl, DOWN, buff=0.14)

            mobs = []
            for src, is_math, c in lines:
                m = MathTex(src, font_size=27, color=c) if is_math \
                    else Text(src, font_size=21, color=c)
                mobs.append(m)

            content = VGroup(*mobs).arrange(DOWN, buff=0.30)
            max_w = w - 0.34
            if content.get_width() > max_w:
                content.scale_to_fit_width(max_w)
            content.next_to(div, DOWN, buff=0.28)

            return VGroup(rect, ttl, div, content)

        p1 = panel("Dielétrico Perfeito", C_ALPHA, [
            (r"\sigma = 0",                        True,  FG),
            (r"\alpha = 0",                        True,  C_ALPHA),
            (r"\beta = \omega\sqrt{\mu\varepsilon}", True, C_BETA),
            ("Sem atenuação",                      False, FG),
        ])
        p2 = panel("Dielétrico Real", C_GOLD, [
            (r"\sigma \ll \omega\varepsilon",                         True,  FG),
            (r"\alpha \cong \dfrac{\sigma}{2}\sqrt{\dfrac{\mu}{\varepsilon}}",
                                                                      True,  C_ALPHA),
            (r"\beta \cong \omega\sqrt{\mu\varepsilon}",              True,  C_BETA),
            ("Baixa atenuação",                                       False, FG),
        ])
        p3 = panel("Condutor Real", C_GAMMA, [
            (r"\sigma \gg \omega\varepsilon",                         True,  FG),
            (r"\alpha = \beta = \sqrt{\dfrac{\omega\mu\sigma}{2}}",   True,  C_GAMMA),
            ("Alta atenuação",                                        False, FG),
            ("Perdas dominam",                                        False, FG),
        ])
        return VGroup(p1, p2, p3).arrange(RIGHT, buff=0.30)

    # ── Scene 5 ───────────────────────────────────────────────────────────────
    def cena_5_onda_tem(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-0.5, 7.0, 1], y_range=[-2.4, 2.4, 1], z_range=[-2.4, 2.4, 1],
            x_length=6.8, y_length=4.6, z_length=4.6,
            axis_config={"color": FG, "stroke_width": 2},
        )
        x_lbl = axes.get_x_axis_label(
            MathTex(r"z\;(\vec{\gamma})", font_size=24, color=FG), direction=RIGHT)
        y_lbl = axes.get_y_axis_label(
            MathTex(r"\vec{E}", font_size=24, color=C_ALPHA), direction=UP)
        z_lbl = axes.get_z_axis_label(
            MathTex(r"\vec{H}", font_size=24, color=C_BETA), direction=OUT)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(z_lbl),
                  run_time=1.5)
        self.wait(0.4)

        # E wave oscillates along y-axis of ThreeDAxes (mapped from our x)
        e_wave = ParametricFunction(
            lambda t: axes.c2p(t, np.exp(-0.15 * t) * np.cos(2.3 * t), 0),
            t_range=[0, 6.8], color=C_ALPHA, stroke_width=3,
        )
        # H wave oscillates along z-axis of ThreeDAxes
        h_wave = ParametricFunction(
            lambda t: axes.c2p(t, 0, np.exp(-0.15 * t) * np.cos(2.3 * t)),
            t_range=[0, 6.8], color=C_BETA, stroke_width=3,
        )
        self.play(Create(e_wave), Create(h_wave), run_time=2.2)
        self.wait(0.5)

        # Propagation direction arrow
        prop_arr = Arrow3D(
            axes.c2p(0, 0, 0), axes.c2p(7.0, 0, 0),
            color=C_GOLD, thickness=0.028,
        )
        self.play(Create(prop_arr))
        self.wait(0.4)

        # Fixed-in-frame overlays
        title_3d = Text("Onda Eletromagnética Transversal (TEM)",
                        font_size=28, color=FG, weight=BOLD)
        title_3d.to_corner(UL, buff=0.38)

        ortho = MathTex(r"\vec{E}\;\perp\;\vec{H}\;\perp\;\vec{\gamma}",
                        font_size=32, color=FG)
        ortho.to_corner(UR, buff=0.50)

        legend = VGroup(
            MathTex(r"\vec{E}", font_size=26, color=C_ALPHA),
            MathTex(r"\vec{H}", font_size=26, color=C_BETA),
            MathTex(r"\vec{\gamma}", font_size=26, color=C_GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        legend.to_corner(DR, buff=0.50)

        self.add_fixed_in_frame_mobjects(title_3d, ortho, legend)
        self.play(FadeIn(title_3d), FadeIn(ortho), FadeIn(legend))

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)

        # Return to 2-D orientation before transition
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.2)
        self.wait(0.3)

    # ── Scene 6 ───────────────────────────────────────────────────────────────
    def cena_6_frentes_de_onda(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        title, sep = self.scene_header("Frentes de Onda e Propagação")
        self.play(Write(title), Create(sep))
        self.wait(0.35)

        origin = LEFT * 3.8 + DOWN * 0.2

        # Point source
        src_dot = Dot(origin, color=C_GOLD, radius=0.10)
        src_lbl = Text("Fonte\nPontual", font_size=20, color=C_GOLD)
        src_lbl.next_to(src_dot, DOWN, buff=0.14)
        self.play(FadeIn(src_dot), FadeIn(src_lbl))

        # Expanding spherical (circular) wave fronts
        wave_circles = VGroup(*[
            Circle(radius=r, color=C_BETA, stroke_width=2.0).move_to(origin)
            for r in [0.55, 1.05, 1.55, 2.05, 2.55]
        ])
        normal_arrows_radial = VGroup(*[
            Arrow(origin, origin + UP * r * 0.88,
                  color=C_GOLD, buff=0, stroke_width=1.8,
                  max_tip_length_to_length_ratio=0.18)
            for r in [0.55, 1.05, 1.55]
        ])
        self.play(
            LaggedStart(*[Create(c) for c in wave_circles], lag_ratio=0.25),
            run_time=2.0,
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in normal_arrows_radial],
                              lag_ratio=0.25), run_time=1.0)
        self.wait(0.5)

        # Far-field region label
        far_lbl = Text("Campo distante → Onda Plana",
                       font_size=22, color=C_GOLD)
        far_lbl.move_to(UP * 2.75 + RIGHT * 1.8)
        self.play(FadeIn(far_lbl))

        # Plane wave fronts (vertical lines on the right)
        front_xs = [0.8, 1.5, 2.2, 2.9, 3.6]
        plane_fronts = VGroup(*[
            Line(UP * 2.1 + RIGHT * x + DOWN * 0.2,
                 DOWN * 2.1 + RIGHT * x + DOWN * 0.2,
                 color=C_BETA, stroke_width=2.5)
            for x in front_xs
        ])
        self.play(
            LaggedStart(*[Create(l) for l in plane_fronts], lag_ratio=0.22),
            run_time=1.4,
        )
        self.wait(0.3)

        # Propagation arrows between plane fronts (normal to fronts)
        prop_arrows = VGroup(*[
            Arrow(RIGHT * 0.6 + UP * y + DOWN * 0.2,
                  RIGHT * 3.8 + UP * y + DOWN * 0.2,
                  color=C_GOLD, buff=0, stroke_width=2.2,
                  max_tip_length_to_length_ratio=0.10)
            for y in [-1.0, 0.0, 1.0]
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in prop_arrows],
                              lag_ratio=0.2), run_time=1.0)
        self.wait(0.5)

        # Final formula
        beta_eq = MathTex(r"\vec{\beta} = -\nabla\phi", font_size=36, color=FG)
        beta_eq.to_edge(DOWN, buff=0.60)
        normal_note = Text("A propagação é sempre normal à frente de onda.",
                           font_size=23, color=FG)
        normal_note.next_to(beta_eq, UP, buff=0.30)

        self.play(Write(beta_eq), run_time=0.9)
        box_b = self.boxed(beta_eq, color=C_GOLD)
        self.play(Create(box_b), FadeIn(normal_note))
        self.wait(2.8)

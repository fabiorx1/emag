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
C_ETA   = "#8e44ad"   # purple  – impedance η
C_VP    = "#e67e22"   # orange  – phase velocity Vp
C_VG    = "#16a085"   # teal    – group velocity Vg
C_ALPHA = "#27ae60"   # green   – used for E vectors / non-dispersive
C_BETA  = "#2471a3"   # blue    – used for H vectors / normal dispersion
C_GAMMA = "#a93226"   # red     – conductor / anomalous dispersion
C_PANEL = "#f7f2ee"


# ═════════════════════════════════════════════════════════════════════════════
class ImpedVelOndaScene(ThreeDScene):
    """Impedance and wave velocities – 5 scenes."""

    # ── Setup ─────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        MathTex.set_default(color=FG)
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        self.cena_1_impedancia()
        self.clean_up()

        self.cena_2_casos_criticos()
        self.clean_up()

        self.cena_2b_eta_campos()
        self.clean_up()

        self.cena_3_velocidade_fase()
        self.clean_up()

        self.cena_4_velocidade_grupo()
        self.clean_up()

        self.cena_5_dispersao()
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

    def boxed(self, mob, color=C_GOLD, buff=0.18):
        box = SurroundingRectangle(mob, color=color, buff=buff,
                                   stroke_width=2.8, corner_radius=0.12)
        box.set_fill(color, opacity=0.05)
        return box

    # ── Scene 1: η definition ─────────────────────────────────────────────────
    def cena_1_impedancia(self):
        title, sep = self.scene_header("Impedância de Onda (η)")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # ── Step 1: starting fasor relation ──────────────────────────────────
        lbl1 = Text("Relação fasorial dos campos:", font_size=24)
        lbl1.next_to(sep, DOWN, buff=0.38)

        eq1 = MathTex(
            r"\vec{\gamma}\times\vec{E} = i\omega\mu\,\vec{H}",
            font_size=38,
        ).next_to(lbl1, DOWN, buff=0.22)

        self.play(FadeIn(lbl1), Write(eq1), run_time=1.2)
        self.wait(0.8)

        # ── Step 2: isolate H ────────────────────────────────────────────────
        lbl2 = Text("Isolando H:", font_size=24)
        lbl2.next_to(eq1, DOWN, buff=0.38)

        eq2 = MathTex(
            r"\vec{H} = \frac{\vec{\gamma}\times\vec{E}}{i\omega\mu}",
            font_size=38,
        ).next_to(lbl2, DOWN, buff=0.22)

        self.play(FadeIn(lbl2), Write(eq2), run_time=1.1)
        self.wait(0.7)

        # Compact: keep eq2 near top, remove lbl1+eq1+lbl2
        self.play(
            FadeOut(lbl1), FadeOut(eq1), FadeOut(lbl2),
            eq2.animate.next_to(sep, DOWN, buff=0.38),
        )
        self.wait(0.2)

        # ── Step 3: define η = iωμ/γ ─────────────────────────────────────────
        lbl3 = Text("Definindo η (impedância de onda):", font_size=24)
        lbl3.next_to(eq2, DOWN, buff=0.40)

        eq3 = MathTex(
            r"\eta = \frac{i\omega\mu}{\gamma}",
            font_size=44, color=C_ETA,
        ).next_to(lbl3, DOWN, buff=0.22)

        self.play(FadeIn(lbl3), Write(eq3), run_time=1.0)
        self.wait(0.6)

        self.play(
            FadeOut(eq2), FadeOut(lbl3),
            eq3.animate.next_to(sep, DOWN, buff=0.38),
        )
        self.wait(0.2)

        # ── Step 4: intrinsic form ────────────────────────────────────────────
        lbl4 = Text("Substituindo γ:", font_size=24)
        lbl4.next_to(eq3, DOWN, buff=0.40)

        eq4 = MathTex(
            r"\eta = \sqrt{\frac{i\omega\mu}{\sigma + i\omega\varepsilon}}",
            font_size=44, color=C_ETA,
        ).next_to(lbl4, DOWN, buff=0.22)

        self.play(FadeIn(lbl4), Write(eq4), run_time=1.2)
        self.wait(0.7)

        # Keep eq4 at top, remove eq3 + lbl4
        self.play(
            FadeOut(eq3), FadeOut(lbl4),
            eq4.animate.next_to(sep, DOWN, buff=0.38),
        )
        self.wait(0.2)

        # ── Step 5: component form ────────────────────────────────────────────
        lbl5 = Text("Relação entre componentes:", font_size=24)
        lbl5.next_to(eq4, DOWN, buff=0.40)

        eq5 = MathTex(
            r"\eta = \frac{E_x}{H_y}",
            font_size=40,
        ).next_to(lbl5, DOWN, buff=0.22)

        self.play(FadeIn(lbl5), Write(eq5))
        self.wait(0.5)

        unit_row = VGroup(
            Text("Razão entre os campos Elétrico e Magnético",
                 font_size=22),
            MathTex(r"[\,\Omega\,]", font_size=28, color=C_ETA),
        ).arrange(RIGHT, buff=0.28)
        unit_row.next_to(eq5, DOWN, buff=0.36)

        self.play(FadeIn(unit_row))

        box_eta = self.boxed(eq4, color=C_ETA)
        self.play(Create(box_eta))
        self.wait(2.5)

    # ── Scene 2: critical cases ────────────────────────────────────────────────
    def cena_2_casos_criticos(self):
        title, sep = self.scene_header("Casos Críticos de η")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        vac_card = self._eta_card(
            titulo="Vácuo  (σ = 0)",
            color=C_GOLD,
            rows=[
                (r"\eta_0 = \sqrt{\dfrac{\mu_0}{\varepsilon_0}}", 30),
                (r"= \sqrt{\dfrac{4\pi\times10^{-7}}{10^{-9}/36\pi}}", 26),
                (r"= 120\pi \approx 377\,\Omega", 34),
            ],
            note="Impedância do espaço livre",
        )

        cond_card = self._eta_card(
            titulo="Condutor Real  (σ ≫ ωε)",
            color=C_GAMMA,
            rows=[
                (r"\eta \approx \sqrt{\dfrac{\omega\mu}{\sigma}}\cdot\sqrt{i}", 28),
                (r"\sqrt{i} = \dfrac{1+i}{\sqrt{2}}", 30),
                (r"\angle\,45°\text{ entre }\vec{E}\text{ e }\vec{H}", 28),
            ],
            note="E  adiantado 45° em relação a H",
        )

        cards = VGroup(vac_card, cond_card).arrange(RIGHT, buff=0.55)
        cards.next_to(sep, DOWN, buff=0.40)
        if cards.get_width() > 13.2:
            cards.scale_to_fit_width(13.2)
        if cards.get_height() > 6.0:
            cards.scale_to_fit_height(6.0)

        self.play(FadeIn(vac_card, shift=UP * 0.12), run_time=0.9)
        self.wait(0.3)
        self.play(FadeIn(cond_card, shift=UP * 0.12), run_time=0.9)
        self.wait(2.5)

    def _eta_card(self, titulo, color, rows, note, width=5.8, height=4.4):
        rect = RoundedRectangle(corner_radius=0.14, width=width, height=height,
                                color=color, stroke_width=3)
        rect.set_fill(C_PANEL, opacity=0.96)

        ttl = Text(titulo, font_size=22, color=color, weight=BOLD)
        ttl.move_to(rect.get_top() + DOWN * 0.44)

        div = Line(rect.get_left() + RIGHT * 0.18, rect.get_right() + LEFT * 0.18,
                   color=color, stroke_width=1.2)
        div.next_to(ttl, DOWN, buff=0.14)

        mobs = [MathTex(s, font_size=fs, color=color) for s, fs in rows]
        mobs.append(Text(note, font_size=19, color=FG))
        content = VGroup(*mobs).arrange(DOWN, buff=0.26)

        max_w = width - 0.36
        if content.get_width() > max_w:
            content.scale_to_fit_width(max_w)
        content.next_to(div, DOWN, buff=0.26)

        # Clip content if it overflows the card vertically
        max_bottom = rect.get_bottom()[1] + 0.12
        if content.get_bottom()[1] < max_bottom:
            shift_up = max_bottom - content.get_bottom()[1]
            content.shift(UP * shift_up)

        return VGroup(rect, ttl, div, content)

    # ── Scene 2b: η field visualisation ────────────────────────────────────────
    def cena_2b_eta_campos(self):
        # ── Case A: Vacuum (σ = 0) – E and H in phase ────────────────────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        axes_v = ThreeDAxes(
            x_range=[-0.5, 7.0, 1], y_range=[-1.5, 1.5, 1], z_range=[-1.5, 1.5, 1],
            x_length=6.8, y_length=3.8, z_length=3.8,
            axis_config={"color": FG, "stroke_width": 2},
        )
        x_lbl_v = axes_v.get_x_axis_label(
            MathTex(r"z", font_size=22, color=FG), direction=RIGHT)
        y_lbl_v = axes_v.get_y_axis_label(
            MathTex(r"\vec{E}", font_size=22, color=C_ALPHA), direction=UP)
        z_lbl_v = axes_v.get_z_axis_label(
            MathTex(r"\vec{H}", font_size=22, color=C_BETA), direction=OUT)

        e_wave_v = ParametricFunction(
            lambda t: axes_v.c2p(t, np.cos(2.0 * t), 0),
            t_range=[0, 6.8], color=C_ALPHA, stroke_width=3,
        )
        h_wave_v = ParametricFunction(
            lambda t: axes_v.c2p(t, 0, np.cos(2.0 * t)),
            t_range=[0, 6.8], color=C_BETA, stroke_width=3,
        )
        prop_v = Arrow3D(
            axes_v.c2p(0, 0, 0), axes_v.c2p(7.0, 0, 0),
            color=C_GOLD, thickness=0.025,
        )

        title_v = Text(
            "Vácuo  (σ = 0)", font_size=28, color=C_GOLD, weight=BOLD,
        )
        title_v.to_corner(UL, buff=0.38)
        eq_v = MathTex(
            r"\eta_0 = 377\,\Omega"
            r"\quad\Rightarrow\quad"
            r"\vec{E}\text{ e }\vec{H}\text{ em fase}",
            font_size=26, color=FG,
        )
        eq_v.to_corner(UR, buff=0.44)
        legend_v = VGroup(
            MathTex(r"\vec{E}", font_size=26, color=C_ALPHA),
            MathTex(r"\vec{H}", font_size=26, color=C_BETA),
            MathTex(r"\vec{\gamma}", font_size=26, color=C_GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        legend_v.to_corner(DR, buff=0.50)

        self.play(
            Create(axes_v), FadeIn(x_lbl_v), FadeIn(y_lbl_v), FadeIn(z_lbl_v),
            run_time=1.2,
        )
        self.add_fixed_in_frame_mobjects(title_v, eq_v, legend_v)
        self.play(FadeIn(title_v), FadeIn(eq_v), FadeIn(legend_v))
        self.play(Create(e_wave_v), Create(h_wave_v), run_time=2.0)
        self.play(Create(prop_v))
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(4.0)
        self.stop_ambient_camera_rotation()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.2)

        # ── Case B: Real conductor (σ ≫ ωε) – decay + 45° phase shift ────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        axes_c = ThreeDAxes(
            x_range=[-0.5, 7.0, 1], y_range=[-1.5, 1.5, 1], z_range=[-1.5, 1.5, 1],
            x_length=6.8, y_length=3.8, z_length=3.8,
            axis_config={"color": FG, "stroke_width": 2},
        )
        x_lbl_c = axes_c.get_x_axis_label(
            MathTex(r"z", font_size=22, color=FG), direction=RIGHT)
        y_lbl_c = axes_c.get_y_axis_label(
            MathTex(r"\vec{E}", font_size=22, color=C_ALPHA), direction=UP)
        z_lbl_c = axes_c.get_z_axis_label(
            MathTex(r"\vec{H}", font_size=22, color=C_BETA), direction=OUT)

        e_wave_c = ParametricFunction(
            lambda t: axes_c.c2p(t, np.exp(-0.45 * t) * np.cos(2.0 * t), 0),
            t_range=[0, 6.8], color=C_ALPHA, stroke_width=3,
        )
        h_wave_c = ParametricFunction(
            lambda t: axes_c.c2p(
                t, 0, np.exp(-0.45 * t) * np.cos(2.0 * t - PI / 4)
            ),
            t_range=[0, 6.8], color=C_BETA, stroke_width=3,
        )
        prop_c = Arrow3D(
            axes_c.c2p(0, 0, 0), axes_c.c2p(7.0, 0, 0),
            color=C_GOLD, thickness=0.025,
        )

        title_c = Text(
            "Condutor Real  (σ ≫ ωε)", font_size=28, color=C_GAMMA, weight=BOLD,
        )
        title_c.to_corner(UL, buff=0.38)
        eq_c = MathTex(
            r"\angle\,\eta = 45^\circ"
            r"\quad\Rightarrow\quad"
            r"\vec{E}\text{ adianta }\vec{H}\text{ em }45^\circ",
            font_size=26, color=FG,
        )
        eq_c.to_corner(UR, buff=0.44)
        decay_note = MathTex(
            r"e^{-\alpha z}:\text{ atenuação exponencial}",
            font_size=24, color=C_GAMMA,
        )
        decay_note.to_edge(DOWN, buff=0.42)
        legend_c = VGroup(
            MathTex(r"\vec{E}", font_size=26, color=C_ALPHA),
            MathTex(r"\vec{H}", font_size=26, color=C_BETA),
            MathTex(r"\vec{\gamma}", font_size=26, color=C_GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        legend_c.to_corner(DR, buff=0.50)

        self.play(
            Create(axes_c), FadeIn(x_lbl_c), FadeIn(y_lbl_c), FadeIn(z_lbl_c),
            run_time=1.2,
        )
        self.add_fixed_in_frame_mobjects(title_c, eq_c, decay_note, legend_c)
        self.play(FadeIn(title_c), FadeIn(eq_c), FadeIn(legend_c))
        self.play(Create(e_wave_c), Create(h_wave_c), run_time=2.0)
        self.play(Create(prop_c))
        self.play(FadeIn(decay_note))
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=0, theta=-PI / 2, run_time=1.2)
        self.wait(0.2)

    # ── Scene 3: phase velocity ────────────────────────────────────────────────
    def cena_3_velocidade_fase(self):
        title, sep = self.scene_header("Velocidade de Fase (Vp)")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        desc = Text("Rapidez de deslocamento da frente de onda",
                    font_size=24)
        desc.next_to(sep, DOWN, buff=0.36)
        self.play(FadeIn(desc))
        self.wait(0.5)

        # Phase constant condition
        lbl1 = Text("Fase constante ao longo da frente de onda:", font_size=23)
        lbl1.next_to(desc, DOWN, buff=0.36)
        eq1 = MathTex(
            r"\omega t - \beta\, r_p = \mathrm{cte}",
            font_size=38,
        ).next_to(lbl1, DOWN, buff=0.22)
        self.play(FadeIn(lbl1), Write(eq1))
        self.wait(0.7)

        # Differentiate wrt t
        lbl2 = Text("Derivando em relação ao tempo:", font_size=23)
        lbl2.next_to(eq1, DOWN, buff=0.36)
        eq2 = MathTex(
            r"\omega - \beta\,\frac{dr_p}{dt} = 0",
            font_size=38,
        ).next_to(lbl2, DOWN, buff=0.22)
        self.play(FadeIn(lbl2), Write(eq2))
        self.wait(0.7)

        # Remove first steps, bring eq2 to top
        self.play(
            FadeOut(desc), FadeOut(lbl1), FadeOut(eq1), FadeOut(lbl2),
            eq2.animate.next_to(sep, DOWN, buff=0.38),
        )
        self.wait(0.25)

        # Isolate Vp
        lbl3 = Text("Isolando a velocidade de fase:", font_size=23)
        lbl3.next_to(eq2, DOWN, buff=0.40)
        vp_eq = MathTex(
            r"V_p = \frac{\omega}{\beta}",
            font_size=52, color=C_VP,
        ).next_to(lbl3, DOWN, buff=0.22)
        self.play(FadeIn(lbl3), Write(vp_eq))
        self.wait(0.5)

        # Promote Vp, box it
        self.play(
            FadeOut(eq2), FadeOut(lbl3),
            vp_eq.animate.next_to(sep, DOWN, buff=0.44),
        )
        box_vp = self.boxed(vp_eq, color=C_VP)
        self.play(Create(box_vp))
        self.wait(0.3)

        # Vacuum special case
        lbl_vac = Text("No Vácuo  (σ = 0  →  β = ω√μ₀ε₀):", font_size=23)
        lbl_vac.next_to(vp_eq, DOWN, buff=0.52)
        eq_vac = MathTex(
            r"V_p = \frac{1}{\sqrt{\mu_0\varepsilon_0}}"
            r"= 3\times10^8\,\mathrm{m/s} = c",
            font_size=34, color=C_VP,
        ).next_to(lbl_vac, DOWN, buff=0.22)
        self.play(FadeIn(lbl_vac), Write(eq_vac))
        self.wait(0.4)
        box_c = self.boxed(eq_vac, color=C_GOLD)
        self.play(Create(box_c))
        self.wait(2.5)

    # ── Scene 4: group velocity ────────────────────────────────────────────────
    def cena_4_velocidade_grupo(self):
        title, sep = self.scene_header("Velocidade de Grupo (Vg)")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        desc = Text("Velocidade do envelope — transporte de informação / energia",
                    font_size=23)
        desc.next_to(sep, DOWN, buff=0.34)
        self.play(FadeIn(desc))
        self.wait(0.5)

        # Beat formula
        lbl_b = Text("Soma de duas ondas de frequências próximas:", font_size=22)
        lbl_b.next_to(desc, DOWN, buff=0.34)
        eq_beat = MathTex(
            r"\cos p + \cos q"
            r"= 2\cos\!\!\left(\frac{p+q}{2}\right)\!\cos\!\!\left(\frac{p-q}{2}\right)",
            font_size=28,
        ).next_to(lbl_b, DOWN, buff=0.18)
        self.play(FadeIn(lbl_b), Write(eq_beat), run_time=1.3)
        self.wait(0.7)

        # Move beat above and compact
        self.play(
            FadeOut(desc), FadeOut(lbl_b),
            eq_beat.animate.next_to(sep, DOWN, buff=0.32).scale(0.88),
        )
        self.wait(0.2)

        # Build wave plot
        ax = Axes(
            x_range=[0, 13, 2],
            y_range=[-2.3, 2.3, 1],
            x_length=9.0,
            y_length=3.0,
            axis_config={
                "color": FG, "stroke_width": 1.5, "include_tip": False,
                "include_numbers": False,
            },
        ).next_to(eq_beat, DOWN, buff=0.30)

        # β₁=5, β₂=7 → carrier mean β=6, Δβ=2
        # combined = 2·cos(6x)·cos(x)  →  envelope period = π ≈ 3.14
        # ≈ 4 full humps in x=[0,13], making modulation clearly visible
        combined = ax.plot(
            lambda x: np.cos(5.0 * x) + np.cos(7.0 * x),
            color=C_BETA, stroke_width=2.2,
        )
        env_top = ax.plot(
            lambda x: 2.0 * np.abs(np.cos(1.0 * x)),
            color=C_VG, stroke_width=2.8,
        )
        env_bot = ax.plot(
            lambda x: -2.0 * np.abs(np.cos(1.0 * x)),
            color=C_VG, stroke_width=2.8,
        )

        self.play(Create(ax), run_time=0.7)
        self.play(Create(combined), run_time=1.5)
        self.play(Create(env_top), Create(env_bot), run_time=1.0)
        self.wait(0.4)

        # Labels to the right of the axes
        carrier_lbl = Text("Portadora", font_size=21, color=C_BETA)
        carrier_lbl.next_to(ax, RIGHT, buff=0.22).shift(DOWN * 0.3)
        env_lbl = Text("Envelope\n(Grupo)", font_size=21, color=C_VG)
        env_lbl.next_to(carrier_lbl, DOWN, buff=0.22)
        self.play(FadeIn(carrier_lbl), FadeIn(env_lbl))

        # Vg definition – bottom of screen
        vg_eq = MathTex(
            r"V_g = \frac{d\omega}{d\beta}",
            font_size=46, color=C_VG,
        )
        vg_eq.to_edge(DOWN, buff=0.42)
        box_vg = self.boxed(vg_eq, color=C_VG)
        self.play(Write(vg_eq))
        self.play(Create(box_vg))
        self.wait(2.5)

    # ── Scene 5: dispersion relation ───────────────────────────────────────────
    def cena_5_dispersao(self):
        title, sep = self.scene_header("Relação de Dispersão")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # Master formula
        lbl_m = Text("Fórmula mestre:", font_size=24)
        lbl_m.next_to(sep, DOWN, buff=0.36)
        master = MathTex(
            r"V_g = \frac{V_p}{1 - \dfrac{\omega}{V_p}\dfrac{dV_p}{d\omega}}",
            font_size=38,
        ).next_to(lbl_m, DOWN, buff=0.24)
        self.play(FadeIn(lbl_m), Write(master), run_time=1.2)
        self.wait(0.6)
        box_m = self.boxed(master, color=FG)
        self.play(Create(box_m))
        self.wait(0.5)

        # Compact master upwards
        self.play(
            FadeOut(lbl_m), FadeOut(box_m),
            master.animate.next_to(sep, DOWN, buff=0.30).scale(0.84),
        )
        box_m2 = self.boxed(master, color=FG)
        self.play(Create(box_m2))
        self.wait(0.3)

        # Three comparative panels
        panels = self._dispersion_panels()
        panels.next_to(master, DOWN, buff=0.36)
        if panels.get_width() > 13.4:
            panels.scale_to_fit_width(13.4)
        if panels.get_bottom()[1] < -3.5:
            panels.scale_to_fit_height(
                panels.get_height() + panels.get_bottom()[1] + 3.5
            )

        for p in panels:
            self.play(FadeIn(p, shift=UP * 0.10), run_time=0.75)
        self.wait(0.4)

        foot = Text(
            "Se Vp depende da frequência, o meio é Dispersivo.",
            font_size=22, color=C_GOLD,
        )
        foot.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(foot))
        self.wait(2.5)

    def _dispersion_panels(self):
        def panel(title_text, cond_tex, result_tex, result_color, note, color,
                  w=4.0, h=3.2):
            rect = RoundedRectangle(corner_radius=0.14, width=w, height=h,
                                    color=color, stroke_width=2.8)
            rect.set_fill(C_PANEL, opacity=0.96)

            ttl = Text(title_text, font_size=21, color=color, weight=BOLD)
            ttl.move_to(rect.get_top() + DOWN * 0.40)

            div = Line(
                rect.get_left() + RIGHT * 0.16,
                rect.get_right() + LEFT * 0.16,
                color=color, stroke_width=1.2,
            )
            div.next_to(ttl, DOWN, buff=0.12)

            cond  = MathTex(cond_tex,  font_size=24, color=FG)
            res   = MathTex(result_tex, font_size=28, color=result_color)
            note_ = Text(note, font_size=18, color=FG)
            content = VGroup(cond, res, note_).arrange(DOWN, buff=0.24)

            max_w = w - 0.34
            if content.get_width() > max_w:
                content.scale_to_fit_width(max_w)
            content.next_to(div, DOWN, buff=0.22)

            # Guard against vertical overflow
            max_bottom = rect.get_bottom()[1] + 0.10
            if content.get_bottom()[1] < max_bottom:
                content.shift(UP * (max_bottom - content.get_bottom()[1]))

            return VGroup(rect, ttl, div, content)

        p1 = panel(
            "Não-Dispersivo",
            r"\dfrac{dV_p}{d\omega} = 0",
            r"V_g = V_p",
            C_ALPHA,
            "Ex.: dielétrico perfeito",
            C_ALPHA,
        )
        p2 = panel(
            "Dispersão Normal",
            r"\dfrac{dV_p}{d\omega} < 0",
            r"V_g < V_p",
            C_BETA,
            "Maioria dos meios reais",
            C_BETA,
        )
        p3 = panel(
            "Dispersão Anômala",
            r"\dfrac{dV_p}{d\omega} > 0",
            r"V_g > V_p",
            C_GAMMA,
            "Frequências de ressonância",
            C_GAMMA,
        )
        return VGroup(p1, p2, p3).arrange(RIGHT, buff=0.30)

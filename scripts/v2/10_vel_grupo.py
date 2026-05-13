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
C_VP    = "#e74c3c"   # red   – phase velocity / wave 1
C_VG    = "#e67e22"   # orange – group velocity / envelope marker
C_W2    = "#2471a3"   # blue  – wave 2
C_SUM   = "#5c5c5c"   # dark  – sum wave
C_ENV   = "#d4a017"   # gold  – envelope outline
C_CREST = "#00d4d4"   # cyan  – tracked crest
C_PANEL = "#f7f2ee"


# ═════════════════════════════════════════════════════════════════════════════
class VelGrupoScene(Scene):
    """The Group-Velocity Paradox – 4 scenes."""

    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        MathTex.set_default(color=FG)

        self.cena_1_cenario()
        self.clean_up()

        self.cena_2_batimento()
        self.clean_up()

        self.cena_3_corrida()
        self.clean_up()

        self.cena_4_tesoura()
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

    # ── Scene 1 ───────────────────────────────────────────────────────────────
    def cena_1_cenario(self):
        title, sep = self.scene_header("O Paradoxo do Pacote Rápido")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # Medium label
        medium = MathTex(r"\sigma \gg \omega\varepsilon",
                         font_size=36, color=C_GOLD)
        medium_lbl = Text("Condutores Reais em baixas frequências:",
                          font_size=24)
        medium_row = VGroup(medium_lbl, medium).arrange(RIGHT, buff=0.26)
        medium_row.next_to(sep, DOWN, buff=0.42)
        self.play(FadeIn(medium_row))
        self.wait(0.5)

        # Side-by-side formulas
        vp_eq = MathTex(
            r"V_p = \sqrt{\frac{2\omega}{\mu\sigma}}",
            font_size=42, color=C_VP,
        )
        vg_eq = MathTex(
            r"V_g = 2\sqrt{\frac{2\omega}{\mu\sigma}}",
            font_size=42, color=C_VG,
        )
        formulas = VGroup(vp_eq, vg_eq).arrange(RIGHT, buff=1.2)
        formulas.next_to(medium_row, DOWN, buff=0.52)
        self.play(Write(vp_eq), run_time=1.0)
        self.wait(0.3)
        self.play(Write(vg_eq), run_time=1.0)
        self.wait(0.6)

        # Highlight the conclusion
        conclusion = MathTex(r"V_g = 2\,V_p", font_size=68, color=FG)
        conclusion.next_to(formulas, DOWN, buff=0.56)
        self.play(
            FadeOut(medium_row),
            formulas.animate.scale(0.60).next_to(sep, DOWN, buff=0.30).to_edge(LEFT, buff=0.55),
            run_time=0.8,
        )
        self.play(Write(conclusion), run_time=1.0)
        box_c = self.boxed(conclusion, color=C_GOLD)
        self.play(Create(box_c))
        self.wait(0.5)

        # Explanatory texts
        lbl_bot = Text(
            "A velocidade do pacote (Vg) é o dobro da velocidade da onda (Vp)!",
            font_size=24, color=C_VG,
        )
        lbl_bot.next_to(conclusion, DOWN, buff=0.46)
        question = Text("Como isso é possível visualmente?", font_size=24,
                        color=FG)
        question.next_to(lbl_bot, DOWN, buff=0.28)
        self.play(FadeIn(lbl_bot, shift=UP * 0.1))
        self.wait(0.4)
        self.play(FadeIn(question, shift=UP * 0.1))
        self.wait(2.5)

    # ── Scene 2 ───────────────────────────────────────────────────────────────
    def cena_2_batimento(self):
        title, sep = self.scene_header("Construindo a Ilusão (O Batimento)")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        intro = Text("Somando duas ondas com frequências bem próximas...",
                     font_size=22)
        intro.next_to(sep, DOWN, buff=0.28)
        self.play(FadeIn(intro))
        self.wait(0.5)

        # ω₁=5, ω₂=7  →  carrier mean=6, Δω=2
        # envelope period = 4π/Δω = 2π ≈ 6.28  →  ~2 humps in x=[0,13]
        omega1, omega2 = 5.0, 7.0
        x_min, x_max = 0.0, 13.0

        def make_ax(y_len=1.2, y_range=1.3):
            return Axes(
                x_range=[x_min, x_max, PI],
                y_range=[-y_range, y_range, 1],
                x_length=9.5,
                y_length=y_len,
                axis_config={
                    "color": FG, "stroke_width": 1.4,
                    "include_tip": False, "include_numbers": False,
                },
            )

        ax1    = make_ax()
        ax2    = make_ax()
        ax_sum = make_ax(y_len=1.45, y_range=2.3)

        # ── 1. Position axes FIRST, then plot curves ──────────────────────────
        group = VGroup(ax1, ax2, ax_sum).arrange(DOWN, buff=0.50)
        group.next_to(intro, DOWN, buff=0.25)

        # Labels — positioned after axes are in their final spots
        lbl1  = MathTex(r"\omega_1", font_size=26, color=C_VP)
        lbl2  = MathTex(r"\omega_2", font_size=26, color=C_W2)
        lbl_s = Text("Soma", font_size=22, color=C_SUM)
        lbl1.next_to(ax1,    LEFT, buff=0.20)
        lbl2.next_to(ax2,    LEFT, buff=0.20)
        lbl_s.next_to(ax_sum, LEFT, buff=0.20)

        # ── 2. Thin dividers (correct midpoint Y) ─────────────────────────────
        mid_y1 = (ax1.get_bottom()[1] + ax2.get_top()[1]) / 2
        mid_y2 = (ax2.get_bottom()[1] + ax_sum.get_top()[1]) / 2
        x_left  = group.get_left()[0]
        x_right = group.get_right()[0]
        div1 = DashedLine(
            np.array([x_left,  mid_y1, 0]),
            np.array([x_right, mid_y1, 0]),
            color=FG, stroke_width=0.8, stroke_opacity=0.4, dash_length=0.12,
        )
        div2 = DashedLine(
            np.array([x_left,  mid_y2, 0]),
            np.array([x_right, mid_y2, 0]),
            color=FG, stroke_width=0.8, stroke_opacity=0.4, dash_length=0.12,
        )

        self.play(
            Create(ax1), Create(ax2), Create(ax_sum),
            FadeIn(lbl1), FadeIn(lbl2), FadeIn(lbl_s),
            Create(div1), Create(div2),
            run_time=0.8,
        )

        # ── 3. Curves plotted AFTER axes are in final position ─────────────────
        w1_curve = ax1.plot(
            lambda x: np.cos(omega1 * x),
            color=C_VP, stroke_width=2.2,
        )
        w2_curve = ax2.plot(
            lambda x: np.cos(omega2 * x),
            color=C_W2, stroke_width=2.2,
        )
        sum_curve = ax_sum.plot(
            lambda x: np.cos(omega1 * x) + np.cos(omega2 * x),
            color=C_SUM, stroke_width=2.2,
        )

        self.play(Create(w1_curve), Create(w2_curve), run_time=1.2)
        self.play(Create(sum_curve), run_time=1.0)
        self.wait(0.4)

        # Envelope outline — period = 2π (clearly ~2 humps in x=[0,13])
        env_top_curve = ax_sum.plot(
            lambda x: 2.0 * np.abs(np.cos((omega2 - omega1) / 2 * x)),
            color=C_ENV, stroke_width=2.8,
        )
        env_bot_curve = ax_sum.plot(
            lambda x: -2.0 * np.abs(np.cos((omega2 - omega1) / 2 * x)),
            color=C_ENV, stroke_width=2.8,
        )
        env_lbl = Text("Envelope", font_size=19, color=C_ENV)
        env_lbl.next_to(ax_sum, DOWN, buff=0.18)

        self.play(
            Create(env_top_curve), Create(env_bot_curve),
            FadeIn(env_lbl),
            run_time=1.0,
        )

        result_note = Text(
            "...criamos regiões de interferência construtiva — O Pacote!",
            font_size=21, color=C_VG,
        )
        result_note.next_to(env_lbl, DOWN, buff=0.22)
        self.play(FadeIn(result_note, shift=UP * 0.1))
        self.wait(2.8)

    # ── Scene 3 ───────────────────────────────────────────────────────────────
    def cena_3_corrida(self):
        title, sep = self.scene_header("A Corrida: Vg ultrapassando Vp")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        # Instruction + inline colour legend in one row (avoids DR-corner overlap)
        inst1 = VGroup(
            Text("Acompanhe: ", font_size=20, color=FG),
            VGroup(
                Dot(color=C_CREST, radius=0.09),
                Text("Crista/Fase (Vp)", font_size=20, color=C_CREST),
            ).arrange(RIGHT, buff=0.10),
            Text("  e  ", font_size=20, color=FG),
            VGroup(
                Dot(color=C_VG, radius=0.10),
                Text("Envelope/Grupo (Vg)", font_size=20, color=C_VG),
            ).arrange(RIGHT, buff=0.10),
        ).arrange(RIGHT, buff=0.14)
        inst1.next_to(sep, DOWN, buff=0.40)
        if inst1.width > 12.0:
            inst1.scale_to_fit_width(12.0)
        self.play(FadeIn(inst1))
        self.wait(0.5)

        # Relação de dispersão para condutor com perdas (σ≫ωε): ω = β²
        # β₁=2.0 → ω₁=4.0,  Vp₁=2.0
        # β₂=2.2 → ω₂=4.84, Vp₂=2.2  (dispersivo!)
        # Vg = Δω/Δβ = 0.84/0.2 = 4.2 ≈ 2×Vp_médio (2.1)  ✓
        omega1, k1 = 4.0,  2.0   # vp₁ = 2.0
        omega2, k2 = 4.84, 2.2   # vp₂ = 2.2
        # Vg = (4.84−4.0)/(2.2−2.0) = 4.2  ≈  2 × 2.1 = 2·Vp  ✓

        x_min, x_max = -PI, 3 * PI
        ax = Axes(
            x_range=[x_min, x_max, PI],
            y_range=[-2.5, 2.5, 1],
            x_length=11.0,
            y_length=3.2,
            axis_config={
                "color": FG, "stroke_width": 1.3,
                "include_tip": False, "include_numbers": False,
            },
        )
        ax.next_to(inst1, DOWN, buff=0.26)

        # ValueTracker for time
        t_tracker = ValueTracker(0.0)

        def combined(x, t):
            return (np.cos(k1 * x - omega1 * t)
                    + np.cos(k2 * x - omega2 * t))

        def envelope_top(x, t):
            # |2·cos(Δk/2·x - Δω/2·t)|  — coeficientes distintos (dispersivo!)
            return 2.0 * np.abs(
                np.cos((k2 - k1) / 2 * x - (omega2 - omega1) / 2 * t)
            )

        # Sum wave (updated via always_redraw)
        sum_wave = always_redraw(lambda: ax.plot(
            lambda x: combined(x, t_tracker.get_value()),
            color=C_SUM, stroke_width=2.0,
            x_range=[x_min, x_max],
        ))

        env_t = always_redraw(lambda: ax.plot(
            lambda x: envelope_top(x, t_tracker.get_value()),
            color=C_ENV, stroke_width=2.8,
            x_range=[x_min, x_max],
        ))
        env_b = always_redraw(lambda: ax.plot(
            lambda x: -envelope_top(x, t_tracker.get_value()),
            color=C_ENV, stroke_width=2.8,
            x_range=[x_min, x_max],
        ))

        # Tracked crest: the crest nearest x=0 at t=0 is at x=0 for combined
        # Phase velocity = omega1/k1 = 2; so crest position = vp·t
        crest_dot = always_redraw(lambda: Dot(
            ax.c2p(
                (omega1 / k1) * t_tracker.get_value() % (x_max - x_min) + x_min,
                combined(
                    (omega1 / k1) * t_tracker.get_value() % (x_max - x_min) + x_min,
                    t_tracker.get_value(),
                ),
            ),
            color=C_CREST, radius=0.12,
        ))

        # Envelope peak: group velocity = (omega2-omega1)/(k2-k1) = 2*vp
        # Nearest envelope peak at t=0: x=0
        env_peak_dot = always_redraw(lambda: Dot(
            ax.c2p(
                ((omega2 - omega1) / (k2 - k1)) * t_tracker.get_value()
                % (x_max - x_min) + x_min,
                envelope_top(
                    ((omega2 - omega1) / (k2 - k1)) * t_tracker.get_value()
                    % (x_max - x_min) + x_min,
                    t_tracker.get_value(),
                ),
            ),
            color=C_VG, radius=0.14,
        ))

        self.play(Create(ax), run_time=0.6)
        self.add(sum_wave, env_t, env_b, crest_dot, env_peak_dot)
        self.wait(0.5)

        # ── Slow-motion race ──────────────────────────────────────────────────
        note2 = Text(
            "O envelope viaja tão rápido que 'atropela' suas próprias ondas!",
            font_size=21, color=C_VG,
        )
        note2.next_to(ax, DOWN, buff=0.28)
        if note2.width > 12.0:
            note2.scale_to_fit_width(12.0)
        self.play(FadeIn(note2))

        self.play(
            t_tracker.animate.set_value(4.0),
            run_time=8.0,
            rate_func=linear,
        )
        self.wait(0.5)

        note3 = Text(
            "As cristas nascem na frente, escorregam para trás e desaparecem.",
            font_size=21, color=C_CREST,
        )
        note3.move_to(note2.get_center())
        if note3.width > 12.0:
            note3.scale_to_fit_width(12.0)
        self.play(FadeOut(note2, run_time=0.3), FadeIn(note3, run_time=0.6))

        self.play(
            t_tracker.animate.set_value(8.0),
            run_time=8.0,
            rate_func=linear,
        )
        self.wait(1.5)

    # ── Scene 4 ───────────────────────────────────────────────────────────────
    def cena_4_tesoura(self):
        title, sep = self.scene_header("A Analogia da Tesoura")
        self.play(Write(title), Create(sep))
        self.wait(0.3)

        desc = Text(
            "O Envelope não é um objeto sólido que 'carrega' as ondas...",
            font_size=24,
        )
        desc.next_to(sep, DOWN, buff=0.36)
        self.play(FadeIn(desc))
        self.wait(0.6)

        desc2 = Text(
            "Ele é apenas um ponto geométrico perfeito de encontro.",
            font_size=24,
        )
        desc2.next_to(desc, DOWN, buff=0.24)
        self.play(FadeIn(desc2))
        self.wait(0.5)

        # ── Build the scissor diagram ─────────────────────────────────────────
        # Two nearly-parallel lines crossing at a very acute angle
        # Line 1 (ω₁): y = m1·x + b1   Line 2 (ω₂): y = m2·x + b2
        # Use slopes that cross at a visible point inside the frame
        # m1 = 0.12,  m2 = -0.12  → crossing always at x=0 when b1=b2
        # We'll offset b2 slightly so they cross inside in x-range

        scissors_center = DOWN * 0.6

        t_var = ValueTracker(0.0)   # vertical shift applied to both lines

        def make_line(slope, intercept, color):
            return always_redraw(lambda: Line(
                scissors_center + LEFT * 5.5
                + UP * (slope * (-5.5) + intercept + t_var.get_value()),
                scissors_center + RIGHT * 5.5
                + UP * (slope * 5.5 + intercept + t_var.get_value()),
                color=color, stroke_width=3,
            ))

        slope1, slope2 = 0.09, -0.09
        intercept1, intercept2 = 0.0, 0.0   # both pass through scissors_center at x=0

        line1 = make_line(slope1, intercept1, C_VP)
        line2 = make_line(slope2, intercept2, C_W2)

        # Intersection: slope1·x + b1 + shift = slope2·x + b2 + shift  →  always x=0
        # As we shift, the intersection y changes but x stays at 0. Not dramatic.
        # Better: give them a small relative vertical drift so the crossing slides sideways.
        # line2 will drift DOWN by 0 → intercept unchanged; but we offset by extra:
        # Use line1 slanting slightly, line2 constant slope, intercept2 changing with t
        # Intersection x  = (b2 - b1) / (slope1 - slope2) = drift / (slope1-slope2)
        # drift = t_var → x_int = t_var / (2*slope1)  → x moves right as t increases ✓

        # Rebuild with better parameterisation
        self.remove(line1, line2)

        def make_line2(slope, get_intercept, color):
            return always_redraw(lambda: Line(
                scissors_center + LEFT * 5.8
                + UP * (slope * (-5.8) + get_intercept()),
                scissors_center + RIGHT * 5.8
                + UP * (slope * 5.8 + get_intercept()),
                color=color, stroke_width=3,
            ))

        # Line1: fixed intercept=0
        # Line2: intercept decreases (drifts down) as t_var increases
        # → x_int = (0 - t_var) / (slope1 - slope2) = t_var / (2·slope2) → moves RIGHT ✓
        sl = 0.11
        line1b = make_line2(sl,  lambda:  0.0,                  C_VP)
        line2b = make_line2(-sl, lambda: -t_var.get_value(),     C_W2)

        lbl_l1 = MathTex(r"\omega_1", font_size=24, color=C_VP)
        lbl_l2 = MathTex(r"\omega_2", font_size=24, color=C_W2)
        lbl_l1.to_corner(DL, buff=0.5)
        lbl_l2.next_to(lbl_l1, UP, buff=0.24)

        # Intersection dot (always redraw)
        def x_int():
            return t_var.get_value() / (2 * sl)

        def y_int():
            return sl * x_int() + 0.0   # from line1

        int_dot = always_redraw(lambda: Dot(
            scissors_center + RIGHT * x_int() + UP * y_int(),
            color=C_VP, radius=0.14,
        ).set_color(C_VP).set_glow_factor(2.0)
        if hasattr(Dot, "set_glow_factor") else
        Dot(
            scissors_center + RIGHT * x_int() + UP * y_int(),
            color=C_VP, radius=0.14,
        ))

        self.play(
            FadeOut(desc), FadeOut(desc2),
            Create(line1b), Create(line2b),
            FadeIn(lbl_l1), FadeIn(lbl_l2),
            run_time=1.0,
        )
        self.add(int_dot)
        self.wait(0.5)

        note_geo = Text(
            "Pequenos movimentos das ondas geram saltos gigantescos no ponto de interferência!",
            font_size=21, color=C_VG,
        )
        note_geo.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(note_geo))
        self.wait(0.5)

        # Slow upward drift → dot races right
        self.play(
            t_var.animate.set_value(0.9),
            run_time=6.0,
            rate_func=linear,
        )
        self.wait(0.5)

        # Final caption
        final = Text(
            "Vg é a velocidade de uma intersecção geométrica,\nnão de matéria se movendo!",
            font_size=26, color=FG, weight=BOLD,
        )
        final.next_to(note_geo, UP, buff=0.38)
        self.play(FadeIn(final, shift=UP * 0.12))
        self.wait(3.0)

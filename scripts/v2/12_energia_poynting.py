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
C_H = "#3498db"        # blue – Magnetic field
C_NABLA = "#2ecc71"    # green – Nabla operator
C_S = "#f1c40f"        # yellow/gold – Poynting vector
C_S_GOLD = "#d4a017"   # darker gold
C_PANEL = "#1a1a2e"    # dark panel fill
C_CONDUCTOR = "#7f8c8d"  # gray for conductor
C_HEAT = "#e67e22"     # orange – Joule heating
C_SPARK = "#ff6b35"    # orange sparks

INVIS = np.array([0.001, 0, 0])


# ═════════════════════════════════════════════════════════════════════════════
class PoyntingTheorem(ThreeDScene):
    """O Teorema de Poynting – Álgebra & Física – 5 cenas."""

    # ── Setup ─────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        MathTex.set_default(color=FG)
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        self.cena_1_faisca_inicial()
        self.clean_up()

        self.cena_2_truque_algebrico()
        self.clean_up()

        self.cena_3_nascimento_energia()
        self.clean_up()

        self.cena_4_pedagio_materia()
        self.clean_up()

        self.cena_5_teorema_integral()
        self.wait(1)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def clean_up(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.wait(0.25)

    def scene_header(self, text, font_size=34):
        title = Text(text, font_size=font_size, color=FG, weight=BOLD)
        title.to_edge(UP, buff=0.25)
        sep = Line(LEFT * 6.2, RIGHT * 6.2, color=FG, stroke_width=1.2)
        sep.next_to(title, DOWN, buff=0.12)
        return title, sep

    def boxed(self, mob, color=C_S, buff=0.15):
        box = SurroundingRectangle(
            mob, color=color, buff=buff,
            stroke_width=2.5, corner_radius=0.1,
        )
        box.set_fill(color, opacity=0.07)
        return box

    def label_arrow(self, mob, text, direction=DOWN, color=GREY_B, font_size=18):
        lbl = Text(text, font_size=font_size, color=color)
        lbl.next_to(mob, direction, buff=0.15)
        return lbl

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 1: A Faísca Inicial (Física → Matemática)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_1_faisca_inicial(self):
        # ── 1.1 Visão 3D: Volume de controle com onda EM ────────────────────
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, run_time=0.01)

        axes = ThreeDAxes(
            x_range=[-1, 8, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
            x_length=8, y_length=3.5, z_length=3.5,
            axis_config={"color": FG, "stroke_width": 1, "stroke_opacity": 0.25},
        )

        # Semitransparent cube (volume V)
        cube = Cube(side_length=2.8, fill_color=BLUE_E, fill_opacity=0.08,
                     stroke_color=BLUE_C, stroke_width=1.5, stroke_opacity=0.5)
        cube.move_to(axes.c2p(3.5, 0, 0))

        lbl_V = MathTex(r"V", font_size=28, color=BLUE_C)
        lbl_V.move_to(cube.get_corner(UR) + np.array([0.3, 0.3, 0]))

        t_val = ValueTracker(0)

        def e_wave():
            t = t_val.get_value()
            return ParametricFunction(
                lambda s: axes.c2p(s, np.sin(1.8 * s - t), 0),
                t_range=[0, 7, 0.05], color=C_E, stroke_width=2.8,
            )

        def h_wave():
            t = t_val.get_value()
            return ParametricFunction(
                lambda s: axes.c2p(s, 0, np.sin(1.8 * s - t)),
                t_range=[0, 7, 0.05], color=C_H, stroke_width=2.8,
            )

        e_w = always_redraw(e_wave)
        h_w = always_redraw(h_wave)

        legend_3d = VGroup(
            MathTex(r"\vec{e}", font_size=22, color=C_E),
            MathTex(r"\vec{h}", font_size=22, color=C_H),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend_3d.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(legend_3d)

        self.play(Create(axes), FadeIn(cube), FadeIn(lbl_V), run_time=1.2)
        self.play(Create(e_w), Create(h_w), FadeIn(legend_3d), run_time=1.5)
        self.play(t_val.animate.set_value(2 * PI), run_time=2.5, rate_func=linear)

        # ── 1.2 Congelar onda, destacar vetores E e H em um ponto ───────────
        # Freeze at a peak point
        freeze_x = 3.5
        freeze_val = np.sin(1.8 * freeze_x - 2 * PI)

        e_vec = Arrow3D(
            axes.c2p(freeze_x, 0, 0),
            axes.c2p(freeze_x, freeze_val * 1.5, 0),
            color=C_E, thickness=0.035,
        )
        h_vec = Arrow3D(
            axes.c2p(freeze_x, 0, 0),
            axes.c2p(freeze_x, 0, freeze_val * 1.5),
            color=C_H, thickness=0.035,
        )

        lbl_e3d = MathTex(r"\vec{e}", font_size=26, color=C_E)
        lbl_e3d.next_to(e_vec, UP, buff=0.1)
        lbl_h3d = MathTex(r"\vec{h}", font_size=26, color=C_H)
        lbl_h3d.next_to(h_vec, OUT, buff=0.1)

        self.play(Create(e_vec), Create(h_vec), run_time=1.0)
        self.wait(1.0)

        # ── 1.3 Transição para 2D: Equações de Maxwell ──────────────────────
        self.play(
            FadeOut(axes), FadeOut(cube), FadeOut(lbl_V),
            FadeOut(e_w), FadeOut(h_w),
            FadeOut(e_vec), FadeOut(h_vec),
            FadeOut(lbl_e3d), FadeOut(lbl_h3d),
            FadeOut(legend_3d),
            run_time=0.8,
        )
        self.move_camera(phi=0, theta=-PI / 2, run_time=0.8)

        title, sep = self.scene_header("As Equações de Maxwell (Rotacional)")
        self.add_fixed_in_frame_mobjects(title, sep)
        self.play(Write(title), Create(sep), run_time=0.8)

        # Equation (1): ∇ × e = -∂b/∂t
        eq1_lbl = MathTex(r"(1)", font_size=26, color=GREY_B)
        eq1 = MathTex(
            r"\nabla", r"\times", r"\vec{e}",
            r"=", r"-", r"\frac{\partial\vec{b}}{\partial t}",
            font_size=34,
        )
        eq1[0].set_color(C_NABLA)
        eq1[2].set_color(C_E)

        # Equation (2): ∇ × h = σe + ∂d/∂t
        eq2_lbl = MathTex(r"(2)", font_size=26, color=GREY_B)
        eq2 = MathTex(
            r"\nabla", r"\times", r"\vec{h}",
            r"=", r"\sigma\vec{e}", r"+",
            r"\frac{\partial\vec{d}}{\partial t}",
            font_size=34,
        )
        eq2[0].set_color(C_NABLA)
        eq2[2].set_color(C_H)
        eq2[4].set_color(C_E)

        eq1_group = VGroup(eq1_lbl, eq1).arrange(RIGHT, buff=0.3)
        eq2_group = VGroup(eq2_lbl, eq2).arrange(RIGHT, buff=0.3)
        maxwell_group = VGroup(eq1_group, eq2_group).arrange(DOWN, buff=0.5)
        maxwell_group.next_to(sep, DOWN, buff=0.5)

        self.add_fixed_in_frame_mobjects(maxwell_group)
        self.play(Write(eq1_group), run_time=1.2)
        self.play(Write(eq2_group), run_time=1.2)
        self.wait(0.5)

        # ── 1.4 Destaque dos termos físicos ──────────────────────────────────
        # Highlight ∂b/∂t
        brace_db = Brace(eq1[5], DOWN, buff=0.08, color=C_H)
        lbl_db = Text("Variação Magnética", font_size=14, color=C_H)
        lbl_db.next_to(brace_db, DOWN, buff=0.08)

        # Highlight σe
        brace_sigma = Brace(eq2[4], DOWN, buff=0.08, color=C_HEAT)
        lbl_sigma = Text("Corrente de Condução", font_size=14, color=C_HEAT)
        lbl_sigma.next_to(brace_sigma, DOWN, buff=0.08)

        # Highlight ∂d/∂t
        brace_dd = Brace(eq2[6], DOWN, buff=0.08, color=C_E)
        lbl_dd = Text("Variação Elétrica", font_size=14, color=C_E)
        lbl_dd.next_to(brace_dd, DOWN, buff=0.08)

        highlights = VGroup(brace_db, lbl_db, brace_sigma, lbl_sigma, brace_dd, lbl_dd)
        self.add_fixed_in_frame_mobjects(highlights)

        self.play(
            GrowFromCenter(brace_db), FadeIn(lbl_db),
            run_time=0.7,
        )
        self.play(
            GrowFromCenter(brace_sigma), FadeIn(lbl_sigma),
            GrowFromCenter(brace_dd), FadeIn(lbl_dd),
            run_time=0.7,
        )
        self.wait(2.5)

        # Store Maxwell equations for use in next scene
        self.maxwell_eq1 = eq1.copy()
        self.maxwell_eq2 = eq2.copy()

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 2: O Truque Algébrico (Matemática Pura)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_2_truque_algebrico(self):
        title, sep = self.scene_header("O Truque Algébrico")
        self.add_fixed_in_frame_mobjects(title, sep)
        self.play(Write(title), Create(sep), run_time=0.8)

        # ── 2.1 A Identidade Vetorial ────────────────────────────────────────
        identity = MathTex(
            r"\nabla", r"\cdot", r"(", r"\vec{A}", r"\times", r"\vec{B}", r")",
            r"=",
            r"(", r"\nabla", r"\times", r"\vec{A}", r")",
            r"\cdot", r"\vec{B}",
            r"-",
            r"(", r"\nabla", r"\times", r"\vec{B}", r")",
            r"\cdot", r"\vec{A}",
            font_size=30,
        )
        # Color nablas green
        for i in [0, 9, 17]:
            identity[i].set_color(C_NABLA)

        identity.next_to(sep, DOWN, buff=0.45)

        id_label = Text("Identidade do Divergente do Produto Vetorial",
                        font_size=16, color=GREY_B)
        id_label.next_to(identity, UP, buff=0.15)

        id_box = self.boxed(identity, color=C_NABLA)

        self.add_fixed_in_frame_mobjects(id_label, identity, id_box)
        self.play(FadeIn(id_label), Write(identity), run_time=1.5)
        self.play(Create(id_box), run_time=0.5)
        self.wait(1.0)

        # ── 2.2 Substituição: A → e, B → h ──────────────────────────────────
        identity_sub = MathTex(
            r"\nabla", r"\cdot", r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"(", r"\nabla", r"\times", r"\vec{e}", r")",
            r"\cdot", r"\vec{h}",
            r"-",
            r"(", r"\nabla", r"\times", r"\vec{h}", r")",
            r"\cdot", r"\vec{e}",
            font_size=30,
        )
        for i in [0, 9, 17]:
            identity_sub[i].set_color(C_NABLA)
        for i in [3, 11, 22]:
            identity_sub[i].set_color(C_E)
        for i in [5, 14, 19]:
            identity_sub[i].set_color(C_H)

        identity_sub.move_to(identity)

        id_box_sub = self.boxed(identity_sub, color=C_NABLA)

        self.add_fixed_in_frame_mobjects(identity_sub, id_box_sub)
        self.play(
            FadeOut(id_box),
            TransformMatchingTex(identity, identity_sub),
            run_time=1.5,
        )
        self.play(Create(id_box_sub), run_time=0.4)
        self.wait(1.0)

        # ── 2.3 Trazer as equações de Maxwell ────────────────────────────────
        eq1_recall = MathTex(
            r"(1)\;",
            r"\nabla", r"\times", r"\vec{e}",
            r"=", r"-\frac{\partial\vec{b}}{\partial t}",
            font_size=26,
        )
        eq1_recall[1].set_color(C_NABLA)
        eq1_recall[3].set_color(C_E)

        eq2_recall = MathTex(
            r"(2)\;",
            r"\nabla", r"\times", r"\vec{h}",
            r"=", r"\sigma\vec{e}", r"+",
            r"\frac{\partial\vec{d}}{\partial t}",
            font_size=26,
        )
        eq2_recall[1].set_color(C_NABLA)
        eq2_recall[3].set_color(C_H)

        maxwell_recall = VGroup(eq1_recall, eq2_recall).arrange(DOWN, buff=0.3)
        maxwell_recall.next_to(identity_sub, DOWN, buff=0.55)

        self.add_fixed_in_frame_mobjects(maxwell_recall)
        self.play(FadeIn(maxwell_recall, shift=DOWN * 0.3), run_time=0.8)
        self.wait(0.8)

        # ── 2.4 Substituir os rotacionais ────────────────────────────────────
        # Highlight the curl terms to be replaced
        hl_curl_e = SurroundingRectangle(
            identity_sub[8:13], color=C_E, buff=0.06, stroke_width=1.5,
        )
        hl_curl_h = SurroundingRectangle(
            identity_sub[16:21], color=C_H, buff=0.06, stroke_width=1.5,
        )
        self.add_fixed_in_frame_mobjects(hl_curl_e, hl_curl_h)
        self.play(Create(hl_curl_e), Create(hl_curl_h), run_time=0.6)
        self.wait(0.5)

        # The substituted equation
        eq_substituted = MathTex(
            r"\nabla", r"\cdot", r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"\left(", r"-\frac{\partial\vec{b}}{\partial t}", r"\right)",
            r"\cdot", r"\vec{h}",
            r"-",
            r"\left(", r"\sigma\vec{e}", r"+",
            r"\frac{\partial\vec{d}}{\partial t}", r"\right)",
            r"\cdot", r"\vec{e}",
            font_size=28,
        )
        eq_substituted[0].set_color(C_NABLA)
        eq_substituted[3].set_color(C_E)
        eq_substituted[5].set_color(C_H)
        eq_substituted[12].set_color(C_H)
        eq_substituted[20].set_color(C_E)

        eq_substituted.next_to(sep, DOWN, buff=0.45)

        self.add_fixed_in_frame_mobjects(eq_substituted)
        self.play(
            FadeOut(id_label), FadeOut(id_box_sub),
            FadeOut(hl_curl_e), FadeOut(hl_curl_h),
            FadeOut(maxwell_recall),
            TransformMatchingTex(identity_sub, eq_substituted),
            run_time=1.8,
        )
        self.wait(1.0)

        # ── 2.5 Expandir e reorganizar ───────────────────────────────────────
        eq_expanded = MathTex(
            r"\nabla", r"\cdot", r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"-", r"\vec{h}", r"\cdot",
            r"\frac{\partial\vec{b}}{\partial t}",
            r"-", r"\vec{e}", r"\cdot",
            r"\frac{\partial\vec{d}}{\partial t}",
            r"-", r"\sigma\vec{e}", r"\cdot", r"\vec{e}",
            font_size=28,
        )
        eq_expanded[0].set_color(C_NABLA)
        eq_expanded[3].set_color(C_E)
        eq_expanded[5].set_color(C_H)
        eq_expanded[9].set_color(C_H)
        eq_expanded[13].set_color(C_E)
        eq_expanded[17].set_color(C_E)
        eq_expanded[19].set_color(C_E)

        eq_expanded.move_to(eq_substituted)

        self.add_fixed_in_frame_mobjects(eq_expanded)
        self.play(
            TransformMatchingTex(eq_substituted, eq_expanded),
            run_time=1.5,
        )
        self.wait(0.8)

        # ── 2.6 Multiplicar por (-1) ─────────────────────────────────────────
        mult_label = MathTex(r"\times\;(-1)", font_size=24, color=C_S)
        mult_label.next_to(eq_expanded, RIGHT, buff=0.3)
        self.add_fixed_in_frame_mobjects(mult_label)
        self.play(FadeIn(mult_label), run_time=0.5)
        self.wait(0.5)

        eq_final = MathTex(
            r"-", r"\nabla", r"\cdot",
            r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"\vec{h}", r"\cdot",
            r"\frac{\partial\vec{b}}{\partial t}",
            r"+", r"\vec{e}", r"\cdot",
            r"\frac{\partial\vec{d}}{\partial t}",
            r"+", r"\sigma\vec{e}", r"\cdot", r"\vec{e}",
            font_size=28,
        )
        eq_final[1].set_color(C_NABLA)
        eq_final[4].set_color(C_E)
        eq_final[6].set_color(C_H)
        eq_final[9].set_color(C_H)
        eq_final[13].set_color(C_E)
        eq_final[17].set_color(C_E)
        eq_final[19].set_color(C_E)
        eq_final.move_to(eq_expanded)

        final_box = self.boxed(eq_final, color=C_S)

        lbl_result = Text("Equação Diferencial de Balanço de Energia",
                          font_size=16, color=C_S)
        lbl_result.next_to(eq_final, DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(eq_final, final_box, lbl_result)
        self.play(
            FadeOut(mult_label),
            TransformMatchingTex(eq_expanded, eq_final),
            run_time=1.5,
        )
        self.play(Create(final_box), FadeIn(lbl_result), run_time=0.6)
        self.wait(2.5)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 3: O Nascimento da Energia (Matemática → Física)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_3_nascimento_energia(self):
        title, sep = self.scene_header("O Nascimento da Energia")
        self.add_fixed_in_frame_mobjects(title, sep)
        self.play(Write(title), Create(sep), run_time=0.8)

        # ── 3.1 Equação do balanço (da Cena 2) no topo ──────────────────────
        eq_balance = MathTex(
            r"-", r"\nabla", r"\cdot",
            r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"\vec{h}", r"\cdot",
            r"\frac{\partial\vec{b}}{\partial t}",
            r"+", r"\vec{e}", r"\cdot",
            r"\frac{\partial\vec{d}}{\partial t}",
            r"+", r"\sigma\vec{e}", r"\cdot", r"\vec{e}",
            font_size=26,
        )
        eq_balance[1].set_color(C_NABLA)
        eq_balance[4].set_color(C_E)
        eq_balance[6].set_color(C_H)
        eq_balance[9].set_color(C_H)
        eq_balance[13].set_color(C_E)
        eq_balance[17].set_color(C_E)
        eq_balance[19].set_color(C_E)
        eq_balance.next_to(sep, DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(eq_balance)
        self.play(Write(eq_balance), run_time=1.0)
        self.wait(0.5)

        # ── 3.2 Destacar os termos temporais ─────────────────────────────────
        hl_mag = SurroundingRectangle(
            eq_balance[9:12], color=C_H, buff=0.06, stroke_width=2,
        )
        hl_elec = SurroundingRectangle(
            eq_balance[13:16], color=C_E, buff=0.06, stroke_width=2,
        )
        self.add_fixed_in_frame_mobjects(hl_mag, hl_elec)
        self.play(Create(hl_mag), Create(hl_elec), run_time=0.6)
        self.wait(0.8)

        # ── 3.3 Regra da Cadeia (caixa lateral) ─────────────────────────────
        chain_title = Text("Regra da Cadeia:", font_size=16, color=C_S, weight=BOLD)

        chain_eq1 = MathTex(
            r"\frac{\partial}{\partial t}",
            r"(\vec{h} \cdot \vec{b})",
            r"= 2\vec{h} \cdot \frac{\partial\vec{b}}{\partial t}",
            font_size=22,
        )
        chain_eq1[1].set_color(C_H)

        chain_arrow = MathTex(r"\Rightarrow", font_size=22, color=C_S)

        chain_eq2 = MathTex(
            r"\vec{h} \cdot \frac{\partial\vec{b}}{\partial t}",
            r"=",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{h} \cdot \vec{b}}{2}\right)",
            font_size=22,
        )
        chain_eq2[0].set_color(C_H)
        chain_eq2[3].set_color(C_H)

        chain_box_content = VGroup(
            chain_title, chain_eq1, chain_arrow, chain_eq2
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        chain_box_content.scale(0.9)

        chain_panel = SurroundingRectangle(
            chain_box_content, color=GREY_C, buff=0.2,
            stroke_width=1.5, corner_radius=0.1,
        )
        chain_panel.set_fill(C_PANEL, opacity=0.85)

        chain_group = VGroup(chain_panel, chain_box_content)
        chain_group.next_to(eq_balance, DOWN, buff=0.5)
        chain_group.shift(LEFT * 1.8)

        self.add_fixed_in_frame_mobjects(chain_group)
        self.play(FadeIn(chain_group, shift=LEFT * 0.3), run_time=1.0)
        self.wait(1.5)

        # Similarly for E·∂d/∂t
        chain2_eq = MathTex(
            r"\vec{e} \cdot \frac{\partial\vec{d}}{\partial t}",
            r"=",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{e} \cdot \vec{d}}{2}\right)",
            font_size=22,
        )
        chain2_eq[0].set_color(C_E)
        chain2_eq[3].set_color(C_E)

        chain2_lbl = Text("Analogamente:", font_size=16, color=C_S, weight=BOLD)
        chain2_content = VGroup(chain2_lbl, chain2_eq).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        chain2_content.scale(0.9)

        chain2_panel = SurroundingRectangle(
            chain2_content, color=GREY_C, buff=0.2,
            stroke_width=1.5, corner_radius=0.1,
        )
        chain2_panel.set_fill(C_PANEL, opacity=0.85)

        chain2_group = VGroup(chain2_panel, chain2_content)
        chain2_group.next_to(eq_balance, DOWN, buff=0.5)
        chain2_group.shift(RIGHT * 2.2)

        self.add_fixed_in_frame_mobjects(chain2_group)
        self.play(FadeIn(chain2_group, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(1.2)

        # ── 3.4 Transformar a equação principal ──────────────────────────────
        self.play(FadeOut(hl_mag), FadeOut(hl_elec), run_time=0.3)

        eq_energy = MathTex(
            r"-", r"\nabla", r"\cdot",
            r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{h}\cdot\vec{b}}{2}\right)",
            r"+",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{e}\cdot\vec{d}}{2}\right)",
            r"+", r"\sigma|\vec{e}|^2",
            font_size=26,
        )
        eq_energy[1].set_color(C_NABLA)
        eq_energy[4].set_color(C_E)
        eq_energy[6].set_color(C_H)
        eq_energy[10].set_color(C_H)
        eq_energy[13].set_color(C_E)
        eq_energy[15].set_color(C_HEAT)
        eq_energy.move_to(eq_balance)

        self.add_fixed_in_frame_mobjects(eq_energy)
        self.play(
            FadeOut(chain_group), FadeOut(chain2_group),
            TransformMatchingTex(eq_balance, eq_energy),
            run_time=1.8,
        )
        self.wait(0.8)

        # ── 3.5 Labels de densidade de energia ──────────────────────────────
        brace_wh = Brace(eq_energy[9:11], DOWN, buff=0.08, color=C_H)
        lbl_wh = MathTex(r"W_h", font_size=20, color=C_H)
        lbl_wh.next_to(brace_wh, DOWN, buff=0.06)

        brace_we = Brace(eq_energy[12:14], DOWN, buff=0.08, color=C_E)
        lbl_we = MathTex(r"W_e", font_size=20, color=C_E)
        lbl_we.next_to(brace_we, DOWN, buff=0.06)

        brace_pd = Brace(eq_energy[15], DOWN, buff=0.08, color=C_HEAT)
        lbl_pd = Text("Perdas", font_size=14, color=C_HEAT)
        lbl_pd.next_to(brace_pd, DOWN, buff=0.06)

        energy_labels = VGroup(brace_wh, lbl_wh, brace_we, lbl_we, brace_pd, lbl_pd)
        self.add_fixed_in_frame_mobjects(energy_labels)
        self.play(
            GrowFromCenter(brace_wh), FadeIn(lbl_wh),
            GrowFromCenter(brace_we), FadeIn(lbl_we),
            GrowFromCenter(brace_pd), FadeIn(lbl_pd),
            run_time=0.8,
        )
        self.wait(1.0)

        # ── 3.6 Visualização 3D do cubo com pulsos de energia ────────────────
        # Move equation up and make room for 3D cube below
        top_group = VGroup(eq_energy, energy_labels)

        self.play(
            FadeOut(title), FadeOut(sep), FadeOut(energy_labels),
            eq_energy.animate.scale(0.85).to_edge(UP, buff=0.3),
            run_time=0.8,
        )

        # Create a small cube in the lower portion
        self.move_camera(phi=55 * DEGREES, theta=-40 * DEGREES, run_time=1.0)

        cube_viz = Cube(
            side_length=2.2, fill_color=GREY_E, fill_opacity=0.05,
            stroke_color=GREY_B, stroke_width=1,
        )
        cube_viz.shift(DOWN * 0.5)

        self.play(FadeIn(cube_viz), run_time=0.6)

        # Pulse magnetic (blue)
        blue_glow = cube_viz.copy()
        blue_glow.set_fill(C_H, opacity=0.35)
        blue_glow.set_stroke(C_H, width=2, opacity=0.8)

        lbl_mag_energy = MathTex(r"W_h", font_size=24, color=C_H)
        lbl_mag_energy.next_to(cube_viz, LEFT, buff=0.4)
        self.add_fixed_in_frame_mobjects(lbl_mag_energy)

        self.play(FadeIn(blue_glow), FadeIn(lbl_mag_energy), run_time=0.6)
        self.play(FadeOut(blue_glow), FadeOut(lbl_mag_energy), run_time=0.6)

        # Pulse electric (red)
        red_glow = cube_viz.copy()
        red_glow.set_fill(C_E, opacity=0.35)
        red_glow.set_stroke(C_E, width=2, opacity=0.8)

        lbl_elec_energy = MathTex(r"W_e", font_size=24, color=C_E)
        lbl_elec_energy.next_to(cube_viz, RIGHT, buff=0.4)
        self.add_fixed_in_frame_mobjects(lbl_elec_energy)

        self.play(FadeIn(red_glow), FadeIn(lbl_elec_energy), run_time=0.6)
        self.play(FadeOut(red_glow), FadeOut(lbl_elec_energy), run_time=0.6)

        self.wait(1.5)

        # Return to 2D
        self.play(FadeOut(cube_viz), run_time=0.4)
        self.move_camera(phi=0, theta=-PI / 2, run_time=0.6)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 4: O Pedágio da Matéria (Física Aplicada)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_4_pedagio_materia(self):
        title, sep = self.scene_header("O Pedágio da Matéria")
        self.add_fixed_in_frame_mobjects(title, sep)
        self.play(Write(title), Create(sep), run_time=0.8)

        # ── 4.1 Foco no termo σ|e|² ─────────────────────────────────────────
        term_focus = MathTex(
            r"\sigma\vec{e} \cdot \vec{e}",
            font_size=38, color=C_HEAT,
        )
        term_focus.next_to(sep, DOWN, buff=0.4)

        lbl_loss = Text("Termo de perda de energia", font_size=16, color=GREY_B)
        lbl_loss.next_to(term_focus, DOWN, buff=0.15)

        self.add_fixed_in_frame_mobjects(term_focus, lbl_loss)
        self.play(Write(term_focus), FadeIn(lbl_loss), run_time=0.8)
        self.wait(0.8)

        # Move term up to make room
        self.play(
            term_focus.animate.scale(0.75).to_corner(UL, buff=0.8).shift(DOWN * 0.4),
            FadeOut(lbl_loss),
            run_time=0.6,
        )

        # ── 4.2 O Fio Condutor (cilindro) ───────────────────────────────────
        # Switch to 3D for the conductor
        self.move_camera(phi=60 * DEGREES, theta=-55 * DEGREES, run_time=0.8)

        conductor = Cylinder(
            radius=0.5, height=3.5,
            direction=RIGHT,
            fill_color=C_CONDUCTOR, fill_opacity=0.3,
            stroke_color=C_CONDUCTOR, stroke_width=1.5,
            resolution=(12, 24),
        )
        conductor.shift(DOWN * 0.3)

        # Section labels
        lbl_S = MathTex(r"S", font_size=22, color=FG)
        lbl_S.next_to(conductor, LEFT, buff=0.3)
        lbl_l = MathTex(r"\ell", font_size=22, color=FG)
        lbl_l.next_to(conductor, DOWN, buff=0.3)

        self.play(FadeIn(conductor), run_time=0.8)
        self.add_fixed_in_frame_mobjects(lbl_S, lbl_l)
        self.play(FadeIn(lbl_S), FadeIn(lbl_l), run_time=0.5)
        self.wait(0.5)

        # ── 4.3 Campo E empurra elétrons ─────────────────────────────────────
        # E field arrow inside conductor
        e_arrow = Arrow3D(
            conductor.get_left() + np.array([0.3, 0, 0]),
            conductor.get_right() + np.array([-0.3, 0, 0]),
            color=C_E, thickness=0.025,
        )
        e_lbl3d = MathTex(r"\vec{e}", font_size=22, color=C_E)
        e_lbl3d.next_to(e_arrow, UP, buff=0.2)

        self.play(Create(e_arrow), run_time=0.6)
        self.add_fixed_in_frame_mobjects(e_lbl3d)
        self.play(FadeIn(e_lbl3d), run_time=0.3)

        # Electrons moving along the conductor
        electrons = VGroup()
        for i in range(8):
            dot = Dot3D(
                point=conductor.get_left() + np.array([0.4 + i * 0.4, 0, 0]),
                radius=0.06, color=BLUE_B,
            )
            electrons.add(dot)

        self.play(FadeIn(electrons, lag_ratio=0.1), run_time=0.6)

        # Animate electrons moving right
        self.play(
            electrons.animate.shift(RIGHT * 1.0),
            run_time=1.5, rate_func=linear,
        )

        # J = σE label
        j_eq = MathTex(
            r"\vec{j}", r"=", r"\sigma", r"\vec{e}",
            font_size=28,
        )
        j_eq[0].set_color(C_S)
        j_eq[3].set_color(C_E)
        j_eq.to_corner(UR, buff=0.5).shift(DOWN * 0.5)

        self.add_fixed_in_frame_mobjects(j_eq)
        self.play(Write(j_eq), run_time=0.6)
        self.wait(0.8)

        # ── 4.4 Integral de Volume ───────────────────────────────────────────
        self.play(
            FadeOut(e_arrow), FadeOut(e_lbl3d), FadeOut(electrons),
            FadeOut(lbl_S), FadeOut(lbl_l), FadeOut(j_eq),
            run_time=0.5,
        )
        self.move_camera(phi=0, theta=-PI / 2, run_time=0.6)

        # Fade out term_focus from corner, we'll rebuild equations
        self.play(FadeOut(term_focus), run_time=0.3)

        eq_volume = MathTex(
            r"\int_V", r"\sigma\vec{e} \cdot \vec{e}\;", r"dV",
            r"=",
            r"\int_V", r"\vec{j} \cdot \vec{e}\;", r"dV",
            font_size=30,
        )
        eq_volume[1].set_color(C_HEAT)
        eq_volume[5].set_color(C_S)
        eq_volume.next_to(sep, DOWN, buff=0.6)

        self.add_fixed_in_frame_mobjects(eq_volume)
        self.play(Write(eq_volume), run_time=1.0)
        self.wait(0.8)

        # ── 4.5 Condensar em potência dissipada ──────────────────────────────
        eq_power = MathTex(
            r"\int_V \vec{j} \cdot \vec{e}\; dV",
            r"=",
            r"\vec{i} \cdot \vec{v}",
            font_size=30,
        )
        eq_power[0].set_color(C_S)
        eq_power[2].set_color(C_HEAT)
        eq_power.next_to(eq_volume, DOWN, buff=0.4)

        lbl_power = Text("Potência dissipada (efeito Joule)", font_size=16, color=C_HEAT)
        lbl_power.next_to(eq_power, DOWN, buff=0.2)

        power_box = self.boxed(eq_power[2], color=C_HEAT)

        self.add_fixed_in_frame_mobjects(eq_power, lbl_power, power_box)
        self.play(Write(eq_power), run_time=0.8)
        self.play(FadeIn(lbl_power), Create(power_box), run_time=0.6)
        self.wait(0.8)

        # Conductor glow (incandescent)
        self.move_camera(phi=55 * DEGREES, theta=-50 * DEGREES, run_time=0.8)

        hot_conductor = Cylinder(
            radius=0.5, height=3.5, direction=RIGHT,
            fill_color=C_HEAT, fill_opacity=0.5,
            stroke_color=C_SPARK, stroke_width=2.5,
            resolution=(12, 24),
        )
        hot_conductor.shift(DOWN * 0.3 + DOWN * 1.5)

        self.play(
            conductor.animate.set_fill(C_HEAT, opacity=0.45).set_stroke(C_SPARK, width=2),
            run_time=1.5,
        )

        # Sparks
        sparks = VGroup()
        rng = np.random.default_rng(42)
        for _ in range(15):
            pos = conductor.get_center() + rng.uniform(-1.2, 1.2, 3) * np.array([1, 0.4, 0.4])
            spark = Dot3D(point=pos, radius=0.04, color=C_SPARK)
            sparks.add(spark)

        self.play(FadeIn(sparks, lag_ratio=0.05), run_time=0.8)
        self.play(FadeOut(sparks), run_time=1.0)
        self.wait(1.5)

        self.move_camera(phi=0, theta=-PI / 2, run_time=0.5)

    # ═════════════════════════════════════════════════════════════════════════
    # CENA 5: O Teorema Integral (A Grande Equação)
    # ═════════════════════════════════════════════════════════════════════════
    def cena_5_teorema_integral(self):
        title, sep = self.scene_header("O Teorema de Poynting")
        self.add_fixed_in_frame_mobjects(title, sep)
        self.play(Write(title), Create(sep), run_time=0.8)

        # ── 5.1 Equação diferencial completa (da Cena 3) ────────────────────
        eq_diff = MathTex(
            r"-", r"\nabla", r"\cdot",
            r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"=",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{h}\cdot\vec{b}}{2}\right)",
            r"+",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{e}\cdot\vec{d}}{2}\right)",
            r"+", r"\sigma|\vec{e}|^2",
            font_size=24,
        )
        eq_diff[1].set_color(C_NABLA)
        eq_diff[4].set_color(C_E)
        eq_diff[6].set_color(C_H)
        eq_diff[10].set_color(C_H)
        eq_diff[13].set_color(C_E)
        eq_diff[15].set_color(C_HEAT)
        eq_diff.next_to(sep, DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(eq_diff)
        self.play(Write(eq_diff), run_time=1.0)
        self.wait(0.5)

        # ── 5.2 Envolver tudo com integral de volume ─────────────────────────
        int_label = MathTex(r"\int_V(\;\cdots\;)dV", font_size=22, color=C_S)
        int_label.next_to(eq_diff, RIGHT, buff=0.25)
        self.add_fixed_in_frame_mobjects(int_label)
        self.play(FadeIn(int_label), run_time=0.5)
        self.wait(0.5)

        eq_integral = MathTex(
            r"-", r"\int_V",
            r"\nabla", r"\cdot",
            r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"\; dV",
            r"=",
            r"\int_V",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{h}\cdot\vec{b}}{2}\right)",
            r"dV",
            r"+",
            r"\int_V",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{e}\cdot\vec{d}}{2}\right)",
            r"dV",
            r"+",
            r"\int_V",
            r"\sigma|\vec{e}|^2",
            r"\; dV",
            font_size=22,
        )
        eq_integral[2].set_color(C_NABLA)
        eq_integral[5].set_color(C_E)
        eq_integral[7].set_color(C_H)
        eq_integral[13].set_color(C_H)
        eq_integral[18].set_color(C_E)
        eq_integral[22].set_color(C_HEAT)
        eq_integral.next_to(sep, DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(eq_integral)
        self.play(
            FadeOut(int_label),
            TransformMatchingTex(eq_diff, eq_integral),
            run_time=1.5,
        )
        self.wait(0.8)

        # ── 5.3 Teorema da Divergência (Gauss) ───────────────────────────────
        # Highlight the LHS volume integral
        hl_lhs = SurroundingRectangle(
            eq_integral[0:10], color=C_NABLA, buff=0.06, stroke_width=2,
        )
        self.add_fixed_in_frame_mobjects(hl_lhs)
        self.play(Create(hl_lhs), run_time=0.5)

        gauss_label = Text("Teorema da Divergência (Gauss):", font_size=15, color=C_NABLA)
        gauss_eq = MathTex(
            r"\int_V \nabla \cdot \vec{F}\; dV",
            r"=",
            r"\oint_S \vec{F} \cdot \hat{n}\; dS",
            font_size=22, color=C_NABLA,
        )
        gauss_group = VGroup(gauss_label, gauss_eq).arrange(DOWN, buff=0.1)
        gauss_panel = SurroundingRectangle(
            gauss_group, color=C_NABLA, buff=0.15,
            stroke_width=1.5, corner_radius=0.1,
        )
        gauss_panel.set_fill(C_PANEL, opacity=0.85)
        gauss_full = VGroup(gauss_panel, gauss_group)
        gauss_full.next_to(eq_integral, DOWN, buff=0.35).shift(LEFT * 2.5)

        self.add_fixed_in_frame_mobjects(gauss_full)
        self.play(FadeIn(gauss_full, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)

        # ── 5.4 Aplicar o teorema ao LHS ─────────────────────────────────────
        self.play(FadeOut(hl_lhs), FadeOut(gauss_full), run_time=0.5)

        eq_gauss_applied = MathTex(
            r"-", r"\oint_S",
            r"(", r"\vec{e}", r"\times", r"\vec{h}", r")",
            r"\cdot", r"\hat{n}\; dS",
            r"=",
            r"\int_V",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{h}\cdot\vec{b}}{2}\right)",
            r"dV",
            r"+",
            r"\int_V",
            r"\frac{\partial}{\partial t}",
            r"\left(\frac{\vec{e}\cdot\vec{d}}{2}\right)",
            r"dV",
            r"+",
            r"\int_V",
            r"\sigma|\vec{e}|^2",
            r"\; dV",
            font_size=22,
        )
        eq_gauss_applied[3].set_color(C_E)
        eq_gauss_applied[5].set_color(C_H)
        eq_gauss_applied[12].set_color(C_H)
        eq_gauss_applied[17].set_color(C_E)
        eq_gauss_applied[21].set_color(C_HEAT)
        eq_gauss_applied.next_to(sep, DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(eq_gauss_applied)
        self.play(
            TransformMatchingTex(eq_integral, eq_gauss_applied),
            run_time=1.5,
        )
        self.wait(0.8)

        # ── 5.5 Vetor de Poynting revelado ───────────────────────────────────
        # Highlight e × h and label it S
        hl_exh = SurroundingRectangle(
            eq_gauss_applied[2:7], color=C_S, buff=0.06, stroke_width=2.5,
        )
        poynting_def = MathTex(
            r"\vec{S}", r"\equiv",
            r"\vec{e}", r"\times", r"\vec{h}",
            font_size=26,
        )
        poynting_def[0].set_color(C_S)
        poynting_def[2].set_color(C_E)
        poynting_def[4].set_color(C_H)
        poynting_def.next_to(hl_exh, DOWN, buff=0.2)

        self.add_fixed_in_frame_mobjects(hl_exh, poynting_def)
        self.play(Create(hl_exh), Write(poynting_def), run_time=0.8)
        self.wait(1.0)

        # Replace e×h with S
        eq_poynting_final = MathTex(
            r"-", r"\oint_S",
            r"\vec{S}",
            r"\cdot", r"\hat{n}\; dS",
            r"=",
            r"\frac{\partial}{\partial t}",
            r"\int_V",
            r"\left(\frac{\vec{h}\cdot\vec{b}}{2}",
            r"+",
            r"\frac{\vec{e}\cdot\vec{d}}{2}\right)",
            r"dV",
            r"+",
            r"\int_V",
            r"\sigma|\vec{e}|^2",
            r"\; dV",
            font_size=24,
        )
        eq_poynting_final[2].set_color(C_S)
        eq_poynting_final[8].set_color(C_H)
        eq_poynting_final[10].set_color(C_E)
        eq_poynting_final[14].set_color(C_HEAT)
        eq_poynting_final.next_to(sep, DOWN, buff=0.45)

        final_box = self.boxed(eq_poynting_final, color=C_S, buff=0.18)

        self.add_fixed_in_frame_mobjects(eq_poynting_final, final_box)
        self.play(
            FadeOut(hl_exh), FadeOut(poynting_def),
            TransformMatchingTex(eq_gauss_applied, eq_poynting_final),
            run_time=1.8,
        )
        self.play(Create(final_box), run_time=0.6)
        self.wait(1.5)

        # ── 5.6 Visualização 3D final ────────────────────────────────────────
        # Push equation further up
        self.play(
            VGroup(eq_poynting_final, final_box).animate.scale(0.82).to_edge(UP, buff=0.2),
            FadeOut(title), FadeOut(sep),
            run_time=0.8,
        )

        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=1.0)

        # Wireframe cube with normal vectors
        cube_final = Cube(
            side_length=2.5, fill_opacity=0.0,
            stroke_color=GREY_B, stroke_width=1.5,
        )
        cube_final.shift(DOWN * 0.3)

        self.play(FadeIn(cube_final), run_time=0.6)

        # Normal vectors pointing outward from each face
        face_centers = [
            (RIGHT * 1.25, RIGHT),
            (LEFT * 1.25, LEFT),
            (UP * 1.25, UP),
            (DOWN * 1.25, DOWN),
            (OUT * 1.25, OUT),
            (IN * 1.25, IN),
        ]
        normals = VGroup()
        for center, direction in face_centers:
            n_vec = Arrow3D(
                cube_final.get_center() + center + DOWN * 0.3,
                cube_final.get_center() + center + direction * 0.6 + DOWN * 0.3,
                color=GREY_C, thickness=0.015,
            )
            normals.add(n_vec)

        self.play(FadeIn(normals, lag_ratio=0.1), run_time=0.8)

        # Poynting vectors (yellow arrows) entering through walls
        s_arrows = VGroup()
        rng = np.random.default_rng(123)
        for face_center, direction in face_centers:
            for _ in range(2):
                offset = rng.uniform(-0.5, 0.5, 3) * np.array([
                    1 if abs(direction[0]) < 0.5 else 0,
                    1 if abs(direction[1]) < 0.5 else 0,
                    1 if abs(direction[2]) < 0.5 else 0,
                ])
                start = cube_final.get_center() + face_center + direction * 0.8 + offset + DOWN * 0.3
                end = cube_final.get_center() + face_center + offset + DOWN * 0.3
                s_arr = Arrow3D(start, end, color=C_S, thickness=0.02)
                s_arrows.add(s_arr)

        self.play(FadeIn(s_arrows, lag_ratio=0.03), run_time=1.2)

        # Label: S arrows
        s_label = MathTex(r"\vec{S}", font_size=26, color=C_S)
        s_label.to_corner(DL, buff=0.5)
        s_text = Text("Fluxo de Energia", font_size=14, color=C_S)
        s_text.next_to(s_label, RIGHT, buff=0.15)
        self.add_fixed_in_frame_mobjects(s_label, s_text)
        self.play(FadeIn(s_label), FadeIn(s_text), run_time=0.5)

        # Interior pulsing (stored energy)
        blue_fill = cube_final.copy().set_fill(C_H, opacity=0.25).set_stroke(width=0)
        red_fill = cube_final.copy().set_fill(C_E, opacity=0.25).set_stroke(width=0)

        self.play(FadeIn(blue_fill), run_time=0.5)
        self.play(FadeOut(blue_fill), run_time=0.5)
        self.play(FadeIn(red_fill), run_time=0.5)
        self.play(FadeOut(red_fill), run_time=0.5)

        # Sparks inside (dissipated energy)
        sparks = VGroup()
        for _ in range(12):
            pos = cube_final.get_center() + rng.uniform(-0.8, 0.8, 3) + DOWN * 0.3
            spark = Dot3D(point=pos, radius=0.04, color=C_SPARK)
            sparks.add(spark)

        self.play(FadeIn(sparks, lag_ratio=0.05), run_time=0.6)
        self.play(FadeOut(sparks), run_time=1.0)

        # ── 5.7 Letreiros Finais ─────────────────────────────────────────────
        self.move_camera(phi=0, theta=-PI / 2, run_time=0.8)
        self.play(
            FadeOut(cube_final), FadeOut(normals), FadeOut(s_arrows),
            FadeOut(s_label), FadeOut(s_text),
            run_time=0.5,
        )

        # Move final equation to center
        self.play(
            VGroup(eq_poynting_final, final_box).animate.scale(1.15).move_to(UP * 1.5),
            run_time=0.6,
        )

        # Three pillars below the equation
        col_flux = VGroup(
            MathTex(r"-\oint_S \vec{S}\cdot\hat{n}\;dS", font_size=20, color=C_S),
            Text("=", font_size=14, color=GREY_B),
            Text("Fluxo de Energia", font_size=15, color=C_S, weight=BOLD),
        ).arrange(DOWN, buff=0.08)

        col_stored = VGroup(
            MathTex(
                r"\frac{\partial}{\partial t}\int_V\!\left(\frac{\vec{h}\cdot\vec{b}}{2}"
                r"+\frac{\vec{e}\cdot\vec{d}}{2}\right)dV",
                font_size=18,
            ),
            Text("+", font_size=14, color=GREY_B),
            Text("Variação de Energia\nArmazenada", font_size=14, color=BLUE_C,
                 weight=BOLD, line_spacing=0.8),
        ).arrange(DOWN, buff=0.08)

        col_diss = VGroup(
            MathTex(r"\int_V \sigma|\vec{e}|^2\;dV", font_size=20, color=C_HEAT),
            Text("+", font_size=14, color=GREY_B),
            Text("Energia Dissipada", font_size=15, color=C_HEAT, weight=BOLD),
        ).arrange(DOWN, buff=0.08)

        pillars = VGroup(col_flux, col_stored, col_diss).arrange(RIGHT, buff=0.6)
        pillars.next_to(eq_poynting_final, DOWN, buff=0.65)

        # Ensure pillars don't go off screen
        if pillars.get_bottom()[1] < -3.5:
            pillars.shift(UP * (pillars.get_bottom()[1] + 3.5) * (-1))

        self.add_fixed_in_frame_mobjects(pillars)
        self.play(FadeIn(pillars, shift=UP * 0.2, lag_ratio=0.15), run_time=1.5)

        # Connecting lines from equation parts to pillars
        line1 = DashedLine(
            eq_poynting_final[0:5].get_bottom(),
            col_flux[0].get_top(),
            color=C_S, stroke_width=1, dash_length=0.08,
        )
        line2 = DashedLine(
            eq_poynting_final[6:12].get_bottom(),
            col_stored[0].get_top(),
            color=BLUE_C, stroke_width=1, dash_length=0.08,
        )
        line3 = DashedLine(
            eq_poynting_final[13:16].get_bottom(),
            col_diss[0].get_top(),
            color=C_HEAT, stroke_width=1, dash_length=0.08,
        )
        conn_lines = VGroup(line1, line2, line3)
        self.add_fixed_in_frame_mobjects(conn_lines)
        self.play(Create(conn_lines), run_time=0.8)

        self.wait(4.0)

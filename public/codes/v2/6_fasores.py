from manim import *
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

# ── Paleta de cores ──────────────────────────────────────────────────────────
BG       = "#ece6e2"
FG       = "#5c5c5c"
INVIS    = [0.001, 0, 0] # Small non-zero vector to avoid Manim Point errors
C_EMAX   = "#e07b39"   # amplitude
C_OMEGA  = "#4a90d9"   # frequência angular
C_PHI    = "#8e44ad"   # fase
C_SIGMA  = "#c0392b"   # condutividade
C_EPS    = "#2980b9"   # permissividade
C_GOLD   = "#d4a017"   # caixas de destaque
C_GREEN  = "#27ae60"


class FasoresScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(color=FG)
        # Adicionar o pacote cancel ao template padrão do Manim
        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage{cancel}")
        MathTex.set_default(color=FG, tex_template=my_template)

        self.cena_1_variacao_harmonica()
        self.clean_up()

        self.cena_2_conducao_vs_deslocamento()
        self.clean_up()

        self.cena_3_razao_meio()
        self.clean_up()

        self.cena_4_fasores_euler()
        self.clean_up()

        self.cena_5_dominio_frequencia()
        self.clean_up()

        self.cena_6_exemplo_pratico()
        self.clean_up()

    # ── helpers ───────────────────────────────────────────────────────────────

    def clean_up(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.4)

    # ── Cena 1 ────────────────────────────────────────────────────────────────

    def cena_1_variacao_harmonica(self):
        titulo = Text("Campos Variantes no Tempo", font_size=42).to_edge(UP)
        self.play(Write(titulo))
        self.wait(0.5)

        # ---------- Gráfico 2D (cosseno) ----------
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": FG, "include_tip": False},
        ).shift(RIGHT * 2.5 + DOWN * 0.5)

        t_tracker = ValueTracker(0)

        wave_graph = always_redraw(
            lambda: axes.plot(
                lambda x: np.cos(x),
                x_range=[0, t_tracker.get_value()],
                color=C_EMAX,
                stroke_width=3,
            )
        )

        self.play(Create(axes))
        self.add(wave_graph)
        self.play(t_tracker.animate.set_value(4 * PI), run_time=3, rate_func=linear)
        self.wait(0.3)

        # ---------- Vetor oscilante (esquerda) ----------
        phase = ValueTracker(0)

        def get_vec():
            phi = phase.get_value()
            length = np.cos(phi)
            color = C_EMAX if length >= 0 else C_SIGMA
            
            # Create a line with length, but handle the near-zero case
            # Manim's Arrow/Line fails to render if length is exactly 0
            # We use a very small epsilon if it is close to 0 but we want to show it,
            # but if it's REALLY zero, we can just return a hidden point or small dot.
            
            if abs(length) < 0.001:
                return Vector(INVIS).move_to(LEFT * 4) # Almost null vector
            
            return Arrow(
                ORIGIN,
                UP * length * 1.8,
                color=color,
                buff=0,
                stroke_width=6,
            ).move_to(LEFT * 4)

        vec = always_redraw(get_vec)
        vec_label = MathTex(r"\vec{e}", font_size=36, color=C_EMAX).move_to(LEFT * 3.1 + UP * 0.3)
        self.add(vec) # add instead of FadeIn for always_redraw usually safer
        self.play(FadeIn(vec_label))
        self.play(phase.animate.set_value(4 * PI), run_time=3, rate_func=linear)
        self.wait(0.5)

        # ---------- Equação principal ----------
        eq = MathTex(
            r"\vec{e} = ",
            r"E_{max}",
            r"\cos(",
            r"\omega",
            r"t + ",
            r"\phi",
            r")",
            font_size=44,
        ).next_to(titulo, DOWN, buff=0.6)

        eq[1].set_color(C_EMAX)
        eq[3].set_color(C_OMEGA)
        eq[5].set_color(C_PHI)

        self.play(Write(eq))
        self.wait(0.5)

        # ---------- Anotações com cores ----------
        ann_emax = Text("Amplitude Máxima", font_size=22, color=C_EMAX).next_to(eq, DOWN, buff=0.6).shift(LEFT * 2)
        arrow_emax = Arrow(ann_emax.get_top(), eq[1].get_bottom(), color=C_EMAX, buff=0.05, stroke_width=3)

        ann_omega = Text("Frequência Angular", font_size=22, color=C_OMEGA).next_to(ann_emax, RIGHT, buff=1.2)
        arrow_omega = Arrow(ann_omega.get_top(), eq[3].get_bottom(), color=C_OMEGA, buff=0.05, stroke_width=3)

        ann_phi = Text("Fase Arbitrária", font_size=22, color=C_PHI).next_to(eq, RIGHT, buff=0.5)
        arrow_phi = Arrow(ann_phi.get_left(), eq[5].get_right(), color=C_PHI, buff=0.05, stroke_width=3)

        self.play(
            FadeIn(ann_emax, shift=UP * 0.3),
            GrowArrow(arrow_emax),
        )
        self.play(
            FadeIn(ann_omega, shift=UP * 0.3),
            GrowArrow(arrow_omega),
        )
        self.play(
            FadeIn(ann_phi, shift=LEFT * 0.3),
            GrowArrow(arrow_phi),
        )
        self.wait(2)

    # ── Cena 2 ────────────────────────────────────────────────────────────────

    def cena_2_conducao_vs_deslocamento(self):
        # Equação reduzida no topo
        eq_topo = MathTex(
            r"\vec{e} = E_{max}\cos(\omega t + \phi)",
            font_size=30,
        ).to_edge(UP).shift(DOWN * 0.1)
        self.play(FadeIn(eq_topo))
        self.wait(0.3)

        titulo = Text("Em um meio real, surgem duas correntes:", font_size=32).next_to(eq_topo, DOWN, buff=0.4)
        self.play(Write(titulo))
        self.wait(0.5)

        # ---------- Duas caixas lado a lado ----------
        box_left  = RoundedRectangle(corner_radius=0.2, width=5.2, height=3.2, color=C_SIGMA, stroke_width=3).shift(LEFT * 3.2 + DOWN * 1.0)
        box_right = RoundedRectangle(corner_radius=0.2, width=5.2, height=3.2, color=C_EPS,   stroke_width=3).shift(RIGHT * 3.2 + DOWN * 1.0)

        # Caixa 1 – Condução
        lbl1   = Text("1. Corrente de Condução", font_size=21, color=C_SIGMA).move_to(box_left.get_top() + DOWN * 0.35)
        eq_ohm = MathTex(r"\vec{J} = \sigma \cdot \vec{e}", font_size=40).move_to(box_left.get_center())
        sub1   = Text("(Acompanha o campo)", font_size=17, color=FG).next_to(eq_ohm, DOWN, buff=0.25)

        # Caixa 2 – Deslocamento
        lbl2      = Text("2. Corrente de Deslocamento", font_size=21, color=C_EPS).move_to(box_right.get_top() + DOWN * 0.35)
        eq_desloc = MathTex(r"\vec{J}_d = \epsilon \frac{\partial \vec{e}}{\partial t}", font_size=40).move_to(box_right.get_center())
        sub2      = Text("(Depende da variação)", font_size=17, color=FG).next_to(eq_desloc, DOWN, buff=0.25)

        self.play(Create(box_left), Create(box_right))
        self.play(Write(lbl1), Write(eq_ohm), FadeIn(sub1))
        self.play(Write(lbl2), Write(eq_desloc), FadeIn(sub2))
        self.wait(1.5)

        # ---------- Foco nas derivadas: encolhe ambas as caixas para os cantos ----------
        self.play(
            FadeOut(eq_topo),
            FadeOut(titulo),
            VGroup(box_left, lbl1, eq_ohm, sub1).animate.scale(0.55).to_corner(DL, buff=0.3),
            VGroup(box_right, lbl2, eq_desloc, sub2).animate.scale(0.55).to_corner(DR, buff=0.3),
        )
        self.wait(0.3)

        # Título de subetapa
        calc_title = Text("Como calcular essa derivada?", font_size=26, color=C_GOLD).to_edge(UP)
        self.play(Write(calc_title))

        # Substituir e no lugar adequado
        e_expandida = MathTex(
            r"\vec{J}_d = \epsilon \frac{\partial}{\partial t}\bigl[",
            r"E_{max}\cos(\omega t + \phi)",
            r"\bigr]",
            font_size=34,
        ).next_to(calc_title, DOWN, buff=0.5)

        self.play(Write(e_expandida))
        self.wait(0.8)

        # Indicar o termo a ser derivado
        label_deriv = Text("deriva aqui!", font_size=20, color=C_GOLD).next_to(e_expandida[1], DOWN, buff=0.25)
        self.play(Indicate(e_expandida[1], color=C_GOLD), FadeIn(label_deriv))
        self.wait(0.5)

        # Passo 1: derivada do cosseno → menos seno, ω desce
        step_res = MathTex(
            r"\vec{J}_d = -",
            r"\omega",
            r"\epsilon E_{max}\sin(\omega t + \phi)",
            font_size=36,
        ).next_to(e_expandida, DOWN, buff=0.6)
        step_res[1].set_color(C_OMEGA)

        self.play(FadeOut(label_deriv))
        self.play(TransformMatchingTex(e_expandida.copy(), step_res), run_time=1.2)
        self.wait(0.5)

        # Destaque no ω que "apareceu"
        omega_box = SurroundingRectangle(step_res[1], color=C_OMEGA, buff=0.08, stroke_width=3)
        omega_note = Text("ω nasceu da derivada!", font_size=20, color=C_OMEGA).next_to(step_res, DOWN, buff=0.3)
        self.play(Create(omega_box), Write(omega_note))
        self.wait(0.8)

        # Resultado final em caixa dourada
        result_box = SurroundingRectangle(step_res, color=C_GOLD, buff=0.2, stroke_width=3, corner_radius=0.1)
        result_label = Text("Esta é a Corrente de Deslocamento final!", font_size=22, color=C_GOLD).next_to(result_box, DOWN, buff=0.3)
        self.play(FadeOut(omega_box), FadeOut(omega_note))
        self.play(Create(result_box), Write(result_label))
        self.wait(2.5)

    # ── Cena 3 ────────────────────────────────────────────────────────────────

    def cena_3_razao_meio(self):
        titulo = Text("Como saber qual corrente domina?", font_size=36).to_edge(UP)
        self.play(Write(titulo))
        self.wait(0.5)

        sub = Text("Basta comparar os valores de pico!", font_size=26).next_to(titulo, DOWN, buff=0.4)
        self.play(FadeIn(sub))
        self.wait(0.5)

        # ---------- Amplitudes ----------
        jmax = MathTex(r"J_{max} = \sigma \cdot E_{max}", font_size=38, color=C_SIGMA).shift(LEFT * 3 + UP * 0.8)
        jdmax = MathTex(r"J_{d_{max}} = \omega \cdot \epsilon \cdot E_{max}", font_size=38, color=C_EPS).shift(RIGHT * 2.5 + UP * 0.8)

        self.play(Write(jmax), Write(jdmax))
        self.wait(0.7)

        # ---------- Fração e simplificação ----------
        frac_full = MathTex(
            r"\frac{\sigma \cdot \cancel{E_{max}}}{\omega \cdot \epsilon \cdot \cancel{E_{max}}}",
            font_size=44,
        ).shift(DOWN * 0.3)

        frac_result = MathTex(
            r"\frac{\sigma}{\omega \cdot \epsilon}",
            font_size=54, color=C_GOLD,
        ).next_to(frac_full, RIGHT, buff=0.6)

        self.play(Write(frac_full))
        self.wait(0.5)
        self.play(
            TransformFromCopy(frac_full, frac_result),
        )
        self.wait(0.5)

        # ---------- Diagrama de condições ----------
        brace_group = VGroup()

        conditions = [
            (r"> 100", "Meio Condutor",      C_SIGMA),
            (r"< \tfrac{1}{100}", "Meio Dielétrico",     C_EPS),
            (r"\tfrac{1}{100} < \cdot < 100", "Meio Quase Condutor", C_OMEGA),
        ]

        rows = VGroup()
        for cond_tex, label_str, color in conditions:
            cond = MathTex(cond_tex, font_size=30, color=color)
            label = Text(label_str, font_size=26, color=color)
            row = VGroup(cond, label).arrange(RIGHT, buff=0.5)
            rows.add(row)

        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(DOWN * 1.8 + RIGHT * 0.5)

        brace = Brace(rows, direction=LEFT, color=FG)
        brace_tex = MathTex(r"\frac{\sigma}{\omega\epsilon}", font_size=30, color=FG).next_to(brace, LEFT, buff=0.2)

        self.play(
            FadeOut(jmax), FadeOut(jdmax),
            frac_result.animate.move_to(ORIGIN + UP * 0.5).scale(0.9),
            FadeOut(frac_full),
        )
        self.play(GrowFromCenter(brace), Write(brace_tex))
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3))
        self.wait(2.5)

    # ── Cena 4 ────────────────────────────────────────────────────────────────

    def cena_4_fasores_euler(self):
        subtit = Text("Trabalhar com senos e cossenos é matematicamente exaustivo…", font_size=26).to_edge(UP)
        self.play(Write(subtit))
        self.wait(0.8)

        solucao = Text("A Solução: Identidade de Euler!", font_size=38, color=C_GOLD).next_to(subtit, DOWN, buff=0.5)
        self.play(Write(solucao))
        self.wait(0.3)

        # ---------- Identidade de Euler ----------
        # Split into parts so we can reference \cos(\theta) directly
        euler = MathTex(
            r"e^{i\theta}",
            r"=",
            r"\cos(\theta)",
            r"+",
            r"i\sin(\theta)",
            font_size=42,
        ).arrange(RIGHT, buff=0.15).shift(UP * 0.5)

        glow = SurroundingRectangle(euler, color=C_GOLD, buff=0.2, stroke_width=4, corner_radius=0.15)

        self.play(Write(euler), Create(glow))
        self.wait(1)

        # Isolar cosseno – agora euler[2] é exatamente \cos(\theta)
        box_cos = SurroundingRectangle(
            euler[2],
            color=C_EMAX, buff=0.1, stroke_width=3,
        )
        cos_re = MathTex(r"\cos(\theta) = \operatorname{Re}\!\left[e^{i\theta}\right]", font_size=36, color=C_EMAX).next_to(euler, DOWN, buff=0.6)

        self.play(Create(box_cos))
        self.play(Write(cos_re))
        self.wait(0.8)

        # ---------- Morphing da equação do tempo para a forma fasorial ----------
        eq_tempo = MathTex(
            r"u = U_{max}\cos(\omega t + \phi)",
            font_size=42,
        ).next_to(cos_re, DOWN, buff=0.7)

        eq_exp = MathTex(
            r"u = \operatorname{Re}\!\left\{U_{max} e^{i\phi} \cdot e^{i\omega t}\right\}",
            font_size=42,
        ).move_to(eq_tempo)

        self.play(Write(eq_tempo))
        self.wait(0.7)
        self.play(TransformMatchingTex(eq_tempo, eq_exp), run_time=1.5)
        self.wait(0.7)

        # Circular Umax e e^{iφ} e agrupar em \vec{U}
        fasor_box = SurroundingRectangle(
            eq_exp,
            color=C_PHI, buff=0.12, stroke_width=3,
        )
        self.play(Create(fasor_box))

        fasor_def = MathTex(
            r"\dot{U} = U_{max} e^{i\phi}",
            font_size=40, color=C_PHI,
        ).next_to(eq_exp, DOWN, buff=0.6)

        self.play(Write(fasor_def))

        texto_fasor = Text("Agrupamos amplitude e fase → FASOR (Ů)", font_size=24, color=C_PHI).next_to(fasor_def, DOWN, buff=0.35)
        self.play(FadeIn(texto_fasor, shift=UP * 0.2))
        self.wait(2.5)

    # ── Cena 5 ────────────────────────────────────────────────────────────────

    def cena_5_dominio_frequencia(self):
        titulo = Text("O Superpoder dos Fasores", font_size=42).to_edge(UP)
        self.play(Write(titulo))

        # ---------- Caixa dourada – regra central ----------
        regra = MathTex(r"\frac{\partial}{\partial t} \;\longrightarrow\; i\omega", font_size=52, color=FG)
        caixa_dourada = SurroundingRectangle(regra, color=C_GOLD, buff=0.3, stroke_width=5, corner_radius=0.2)
        caixa_dourada.set_fill(C_GOLD, opacity=0.08)
        grupo_regra = VGroup(caixa_dourada, regra).shift(UP * 0.8)

        self.play(Create(caixa_dourada), Write(regra))
        ann_regra = Text("Derivadas no tempo viram\nmultiplicações algébricas!", font_size=20, color=C_GOLD).next_to(grupo_regra, DOWN, buff=0.4)
        self.play(FadeIn(ann_regra, shift=UP * 0.2))
        self.wait(0.8)
        self.play(FadeOut(ann_regra))

        # ---------- Maxwell instantâneo → fasorial ----------
        eq_inst = MathTex(
            r"\nabla \times \vec{e} = -\frac{\partial}{\partial t}\vec{b}",
            font_size=44,
        ).shift(DOWN * 0.8)

        self.play(Write(eq_inst))
        self.wait(1)

        # Substituição visual
        eq_fasor = MathTex(
            r"\nabla \times \vec{E} = -i\omega\vec{B}",
            font_size=44, color=C_EPS,
        ).move_to(eq_inst)

        self.play(TransformMatchingTex(eq_inst, eq_fasor), run_time=1.5)
        self.wait(0.5)

        box_final = SurroundingRectangle(eq_fasor, color=C_EPS, buff=0.2, stroke_width=3, corner_radius=0.12)
        self.play(Create(box_final))

        # Mostrar as duas formas lado a lado
        lbl_tempo = Text("Domínio do Tempo", font_size=18, color=FG).to_edge(DOWN).shift(UP * 1.8 + LEFT * 3.2)
        eq_inst_ref = MathTex(
            r"\nabla \times \vec{e} = -\frac{\partial}{\partial t}\vec{b}",
            font_size=30,
        ).next_to(lbl_tempo, DOWN, buff=0.2)

        lbl_freq = Text("Domínio da Frequência", font_size=18, color=C_EPS).to_edge(DOWN).shift(UP * 1.8 + RIGHT * 3.2)
        eq_fasor_ref = MathTex(
            r"\nabla \times \vec{E} = -i\omega\vec{B}",
            font_size=30, color=C_EPS,
        ).next_to(lbl_freq, DOWN, buff=0.2)

        arrow_domain = Arrow(eq_inst_ref.get_right(), eq_fasor_ref.get_left(), color=C_GOLD, buff=0.15, stroke_width=3)

        self.play(
            FadeIn(lbl_tempo), Write(eq_inst_ref),
            FadeIn(lbl_freq), Write(eq_fasor_ref),
            GrowArrow(arrow_domain),
        )
        self.wait(2.5)

    # ── Cena 6 ────────────────────────────────────────────────────────────────

    def cena_6_exemplo_pratico(self):
        titulo = Text("Exemplo Prático: Retornando ao Domínio do Tempo", font_size=34).to_edge(UP)
        self.play(Write(titulo))
        self.wait(0.5)

        # ---------- Campo dado ----------
        campo_dado = MathTex(
            r"\vec{E} = (10\hat{x} + i20\hat{y})\,e^{-ikz}",
            font_size=42,
        ).next_to(titulo, DOWN, buff=0.5)

        self.play(Write(campo_dado))
        self.wait(0.7)

        separador = Line(LEFT * 6, RIGHT * 6, stroke_width=1, color=FG).next_to(campo_dado, DOWN, buff=0.4)
        self.play(Create(separador))

        # ---------- Passo 1 ----------
        p1_label = Text("1. Multiplicar pelo fator temporal", font_size=20, color=C_OMEGA).to_edge(LEFT, buff=0.5).shift(UP*0.5)
        eq_p1 = MathTex(
            r"\vec{e} = \operatorname{Re}\!\left\{(10\hat{x} + i20\hat{y})\,e^{-ikz} \cdot e^{i\omega t}\right\}",
            font_size=32,
        ).next_to(p1_label, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(p1_label))
        self.play(Write(eq_p1))
        self.wait(0.6)

        # ---------- Passo 2 ----------
        p2_label = Text("2. Expandir com Euler", font_size=20, color=C_PHI).next_to(eq_p1, DOWN, buff=0.3, aligned_edge=LEFT)
        eq_p2 = MathTex(
            r"e^{i(\omega t - kz)} = \cos(\omega t - kz) + i\sin(\omega t - kz)",
            font_size=28,
        ).next_to(p2_label, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(p2_label))
        self.play(Write(eq_p2))
        self.wait(0.6)

        # ---------- Passo 3 ----------
        p3_label = Text("3. Selecionar apenas a parte Real (Re)", font_size=20, color=C_SIGMA).next_to(eq_p2, DOWN, buff=0.3, aligned_edge=LEFT)

        # Termos complexos "apagados" visualmente
        eq_full = MathTex(
            r"10\hat{x}\cos(\omega t-kz)",
            r"+i10\hat{x}\sin(\dots)",
            r"+i20\hat{y}\cos(\dots)",
            r"-20\hat{y}\sin(\omega t-kz)",
            font_size=26,
        ).next_to(p3_label, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(p3_label))
        self.play(Write(eq_full))
        self.wait(0.5)

        # Apagar termos imaginários com FadeOut parcial e destacar a resposta
        eq_real_only = MathTex(
            r"\vec{e} = 10\hat{x}\cos(\omega t - kz) - 20\hat{y}\sin(\omega t - kz)",
            font_size=32, color=C_GREEN,
        ).move_to(eq_full, aligned_edge=LEFT)

        self.play(
            eq_full[1:3].animate.set_opacity(0).shift(DOWN*0.2),
            Transform(eq_full[0], eq_real_only[0][:21]), # 10x cos(...)
            Transform(eq_full[3], eq_real_only[0][21:]), # - 20y sin(...)
            run_time=1.5
        )
        self.wait(0.5)

        # ---------- Resultado final ----------
        # Limpa etapas intermédias, mantendo o campo original como referência
        self.play(
            FadeOut(p1_label), FadeOut(eq_p1),
            FadeOut(p2_label), FadeOut(eq_p2),
            FadeOut(p3_label), FadeOut(titulo),
            FadeOut(separador),
            FadeOut(eq_full),
            campo_dado.animate.to_edge(UP, buff=0.4),
        )

        # Monta a resposta final centralizada, próxima ao campo original
        res_eq = MathTex(
            r"\vec{e} = 10\hat{x}\cos(\omega t - kz) - 20\hat{y}\sin(\omega t - kz)",
            font_size=36, color=C_GREEN,
        ).next_to(campo_dado, DOWN, buff=0.5).set_x(0)  # centralizado

        res_unit_lbl = Text("[V/m]", font_size=24, color=C_GREEN).next_to(res_eq, RIGHT, buff=0.3)
        res_box_final = SurroundingRectangle(
            VGroup(res_eq, res_unit_lbl), color=C_GREEN, buff=0.3, stroke_width=3, corner_radius=0.15
        )
        texto_final = Text("Temos o nosso campo instantâneo!", font_size=28, color=C_GREEN).to_edge(DOWN, buff=0.5)

        self.play(Write(res_eq), Write(res_unit_lbl))
        self.play(Create(res_box_final))
        self.play(FadeIn(texto_final, shift=UP * 0.2))
        final_group = VGroup(res_box_final, res_eq, res_unit_lbl)
        self.play(final_group.animate.scale(1.08), run_time=0.5)
        self.play(final_group.animate.scale(1/1.08), run_time=0.3)
        self.wait(3.0)

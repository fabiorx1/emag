from manim import *

config.media_width = "75%"
config.verbosity = "WARNING"

class LorentzPermeabilidade(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # PARTE 1: A Carga e a Força de Lorentz (Recapitulando)
        # ---------------------------------------------------------
        
        # Texto inicial
        text_carga_q_1 = Tex(
            "Admitindo uma carga $q$ com massa desprezível...",
            font_size=26).to_corner(UL)
        
        self.play(Write(text_carga_q_1))
        
        # Criação da Carga
        circle = Circle(color=YELLOW, fill_opacity=0.9, radius=0.3)
        label_q = MathTex("q", font_size=24, color=BLACK).move_to(circle)
        
        # Vetor velocidade (inicialmente invisível/transparente)
        vec_v = Arrow(start=LEFT*0.5, end=RIGHT*0.5, color=RED, buff=0).next_to(circle, RIGHT, buff=0)
        label_v = MathTex(r"\vec{v}", font_size=24, color=RED).next_to(vec_v, UP, buff=0.1)
        
        vec_v.set_opacity(0)
        label_v.set_opacity(0)

        # Grupo da carga
        carga_q = VGroup(circle, label_q, vec_v, label_v)
        carga_q.shift(LEFT * 3)
        
        # Mostra a carga estática
        self.play(FadeIn(circle), FadeIn(label_q))
        self.wait(1)

        # Texto sobre movimento
        text_movimento = Tex(
            '...movimentando-se a uma velocidade $v$ numa região do espaço.',
            font_size=26).next_to(text_carga_q_1, DOWN, aligned_edge=LEFT)
        
        # Definição do movimento em loop
        def update_move(mob, dt):
            mob.shift(RIGHT * 2 * dt)
            # Se sair pela direita, volta para a esquerda
            if mob.get_left()[0] > config.frame_x_radius:
                mob.set_x(-config.frame_x_radius - mob.width)

        # Adiciona o grupo à cena e inicia animação
        self.add(carga_q)
        self.play(
            Write(text_movimento),
            vec_v.animate.set_opacity(1),
            label_v.animate.set_opacity(1)
        )
        carga_q.add_updater(update_move)
        self.wait(3)

        # Pergunta
        text_pergunta = Tex(
            'Se esta carga ficar sujeita a uma força, diz-se que ela está em uma região denominada região de campo eletromagnético. O nome dado a essa força é Força de Lorentz!',
            font_size=26).next_to(text_movimento, DOWN, aligned_edge=LEFT)
        self.play(Write(text_pergunta), run_time=3)
        self.wait(1)

        # Fórmula de Lorentz
        formula_lorentz = MathTex(
            r"\vec{F}", r"=", r"q", r"\vec{e}", r"+", r"q", r"(\vec{v} \times \vec{b})",
            font_size=34
        ).shift(UP * 0.5)
        
        # Retira o movimento da carga para focar na fórmula
        carga_q.remove_updater(update_move)
        self.play(
            FadeOut(carga_q),
            FadeOut(text_carga_q_1),
            FadeOut(text_movimento),
            FadeOut(text_pergunta),
            Write(formula_lorentz)
        )
        self.wait(1)

        # ---------------------------------------------------------
        # PARTE 2: Detalhando a Força de Lorentz
        # ---------------------------------------------------------

        # Destacando Força Elétrica
        # Indices: 0:F, 1:=, 2:q, 3:E, 4:+, 5:q, 6:(v x B)
        electric_part = VGroup(formula_lorentz[2], formula_lorentz[3])
        framebox1 = SurroundingRectangle(electric_part, buff = .1)
        label_letrica = Tex(r"Força Elétrica ($q\vec{e}$)", font_size=24, color=YELLOW)
        label_letrica.next_to(framebox1, UP)

        self.play(
            Create(framebox1),
            FadeIn(label_letrica)
        )
        self.wait(2)
        
        # Destacando Força Magnética
        magnetic_part = VGroup(formula_lorentz[5], formula_lorentz[6])
        framebox2 = SurroundingRectangle(magnetic_part, buff = .1)
        label_magnetica = Tex(r"Força Magnética ($q\vec{v} \times \vec{b}$)", font_size=24, color=RED)
        label_magnetica.next_to(framebox2, DOWN)

        self.play(
            ReplacementTransform(framebox1, framebox2),
            FadeOut(label_letrica),
            FadeIn(label_magnetica)
        )
        self.wait(2)

        explanation_vel = VGroup(
            Tex(r"Note que a componente magnética depende da velocidade $\vec{v}$.", font_size=24),
            Tex(r"Se $v=0$, apenas a força elétrica atua.", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula_lorentz, DOWN, buff=1.5)

        self.play(Write(explanation_vel))
        self.wait(3)

        # Limpar a cena para Permeabilidade
        self.play(
            FadeOut(formula_lorentz),
            FadeOut(framebox2),
            FadeOut(label_magnetica),
            FadeOut(explanation_vel)
        )

        # ---------------------------------------------------------
        # PARTE 3: Permeabilidade Magnética
        # ---------------------------------------------------------
        
        title_permeabilidade = Tex("Permeabilidade Magnética ($\mu$)", font_size=36, color=BLUE)
        title_permeabilidade.to_edge(UP)
        self.play(Write(title_permeabilidade))
        self.wait(1)

        text_perm_def = VGroup(
            Tex(r"A permeabilidade magnética mede a capacidade de um material", font_size=24),
            Tex(r"de permitir a formação de um campo magnético em seu interior.", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title_permeabilidade, DOWN, buff=0.5)
        self.play(Write(text_perm_def))
        self.wait(3)

        # Relação B e H
        eq_bh = MathTex(
            r"\vec{b} = \mu \vec{h}",
            font_size=40
        ).next_to(text_perm_def, DOWN, buff=1)
        
        text_b = Tex(r"$\vec{b}$: Densidade de Fluxo Magnético (Tesla)", font_size=22, color=YELLOW)
        text_h = Tex(r"$\vec{h}$: Intensidade de Campo Magnético (A/m)", font_size=22, color=GREEN)
        text_mu = Tex(r"$\mu$: Permeabilidade Magnética (H/m)", font_size=22, color=BLUE)

        definitions_group = VGroup(text_b, text_h, text_mu).arrange(DOWN, aligned_edge=LEFT).next_to(eq_bh, DOWN, buff=0.5)
        
        self.play(Write(eq_bh))
        self.play(
            FadeIn(text_b),
            FadeIn(text_h),
            FadeIn(text_mu)
        )
        self.wait(2)

        # Mu_0 e Mu_r
        eq_mu_breakdown = MathTex(
            r"\mu = \mu_0 \cdot \mu_r",
            font_size=36
        ).move_to(eq_bh) # Troca a equação anterior por esta

        text_mu0 = Tex(r"$\mu_0$: Permeabilidade do vácuo ($4\pi \cdot 10^{-7}$ H/m)", font_size=22)
        text_mur = Tex(r"$\mu_r$: Permeabilidade relativa do material", font_size=22)
        
        mu_defs_group = VGroup(text_mu0, text_mur).arrange(DOWN, aligned_edge=LEFT).next_to(eq_mu_breakdown, DOWN, buff=0.5)

        self.play(
            Transform(eq_bh, eq_mu_breakdown),
            FadeOut(text_b), FadeOut(text_h), FadeOut(text_mu),
            FadeIn(text_mu0), FadeIn(text_mur)
        )
        self.wait(3)
        
        final_note = Tex(
            "Materiais ferromagnéticos possuem $\mu_r$ muito alto!", font_size=24, color=ORANGE
        ).next_to(text_mur, DOWN, buff=0.5)
        self.play(Write(final_note))

        self.wait(3)

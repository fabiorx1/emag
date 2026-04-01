from manim import *

config.media_width = "75%"
config.verbosity = "WARNING"

class LorentzEConstitutivas(Scene):
    LIMIAR_TEXTO_LONGO = 70

    def esperar_texto(self, tempo_base: float, *textos: str):
        # Textos longos ganham +3s; textos curtos ganham +2s.
        total_caracteres = sum(len(texto) for texto in textos)
        tempo_extra = 3 if total_caracteres >= self.LIMIAR_TEXTO_LONGO else 2
        self.wait(tempo_base + tempo_extra)

    def parte_1_carga_e_forca(self):
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
        self.esperar_texto(1, "Admitindo uma carga q com massa desprezível")

        # Texto sobre movimento
        text_movimento = Tex(
            '...movimentando-se a uma velocidade $v$ numa região do espaço.',
            font_size=26).next_to(text_carga_q_1, DOWN, aligned_edge=LEFT)
        
        # Definição do movimento em loop
        def update_move(mob: Mobject, dt):
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
        self.esperar_texto(3, "movimentando-se a uma velocidade v numa região do espaço")

        # Pergunta
        text_pergunta = VGroup(
            Tex('Se esta carga ficar sujeita a uma força, diz-se \
                que ela está em uma região denominada região de campo eletromagnético.',
                font_size=26),
            Tex('O nome dessa força é Força de Lorentz.',font_size=26))\
                .arrange(DOWN, aligned_edge=LEFT)\
                .next_to(text_movimento, DOWN, aligned_edge=LEFT)
        self.play(Write(text_pergunta), run_time=3)
        self.esperar_texto(
            1,
            "Se esta carga ficar sujeita a uma força, diz-se que ela está em uma região denominada região de campo eletromagnético.",
            "O nome dessa força é Força de Lorentz."
        )
        
        # Retira o movimento da carga para focar na fórmula
        carga_q.remove_updater(update_move)
        self.play(
            FadeOut(carga_q),
            FadeOut(text_carga_q_1),
            FadeOut(text_movimento),
            FadeOut(text_pergunta),
        )
        self.wait(1)
    
    def parte_2_detalhando_forca(self):
        title_lorentz = Tex("Força de Lorentz", font_size=40, color=WHITE).to_edge(UP)
        formula_lorentz = MathTex(
            r"\vec{F}", r"=", r"q", r"\vec{e}", r"+", r"q", r"(\vec{v} \times \vec{b})",
            font_size=34).shift(UP * 0.2)
        self.play(Write(title_lorentz), Write(formula_lorentz))
        self.esperar_texto(
            1,
            "Força de Lorentz",
            "F = q e + q(v x b)"
        )
        electric_part = VGroup(formula_lorentz[2], formula_lorentz[3])
        framebox1 = SurroundingRectangle(electric_part, buff = .1)
        label_eletrica = Tex(r"Força Elétrica ($q\vec{e}$)", font_size=24, color=YELLOW)
        label_eletrica.next_to(framebox1, UP)
        self.play(
            Create(framebox1),
            FadeIn(label_eletrica)
        )
        self.esperar_texto(2, "Força Elétrica (q e)")
        
        # Destacando Força Magnética
        magnetic_part = VGroup(formula_lorentz[5], formula_lorentz[6])
        framebox2 = SurroundingRectangle(magnetic_part, buff = .1)
        label_magnetica = Tex(r"Força Magnética ($q\vec{v} \times \vec{b}$)", font_size=24, color=RED)
        label_magnetica.next_to(framebox2, DOWN)

        self.play(
            ReplacementTransform(framebox1, framebox2),
            FadeOut(label_eletrica),
            FadeIn(label_magnetica)
        )
        self.esperar_texto(2, "Força Magnética (q v x b)")

        explanation_vel = VGroup(
            Tex(r"Note que a componente magnética depende da velocidade $\vec{v}$.", font_size=24),
            Tex(r"Se $v=0$, apenas a força elétrica atua.", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula_lorentz, DOWN, buff=1.5)

        self.play(Write(explanation_vel))
        self.esperar_texto(
            3,
            "Note que a componente magnética depende da velocidade v.",
            "Se v=0, apenas a força elétrica atua."
        )

        # Limpar a cena para Permeabilidade
        self.play(
            FadeOut(title_lorentz),
            FadeOut(formula_lorentz),
            FadeOut(framebox2),
            FadeOut(label_magnetica),
            FadeOut(explanation_vel)
        )

    def parte_3_permeabilidade(self):
        title_permeabilidade = Tex("Permeabilidade Magnética ($\mu$)", font_size=36, color=BLUE)
        title_permeabilidade.to_edge(UP)
        self.play(Write(title_permeabilidade))
        self.esperar_texto(1, "Permeabilidade Magnética")

        text_perm_def = VGroup(
            Tex(r"A permeabilidade magnética mede a capacidade de um material", font_size=24),
            Tex(r"de permitir a formação de um campo magnético em seu interior.", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title_permeabilidade, DOWN, buff=0.5)
        self.play(Write(text_perm_def))
        self.esperar_texto(
            3,
            "A permeabilidade magnética mede a capacidade de um material",
            "de permitir a formação de um campo magnético em seu interior"
        )

        # Relação B e H
        eq_bh = MathTex(r"\vec{b} = \mu \vec{h}", font_size=40).next_to(text_perm_def, DOWN, buff=1)
        text_b = Tex(r"$\vec{b}$: Densidade de Fluxo Magnético (Tesla)", font_size=22, color=YELLOW)
        text_h = Tex(r"$\vec{h}$: Intensidade de Campo Magnético (A/m)", font_size=22, color=GREEN)
        text_mu = Tex(r"$\mu$: Permeabilidade Magnética (H/m)", font_size=22, color=BLUE)

        definitions_group = VGroup(text_b, text_h, text_mu)\
            .arrange(DOWN, aligned_edge=LEFT).next_to(eq_bh, DOWN, buff=0.5)
        
        self.play(Write(eq_bh))
        self.play(
            FadeIn(text_b),
            FadeIn(text_h),
            FadeIn(text_mu)
        )
        self.esperar_texto(
            2,
            "b: Densidade de Fluxo Magnético (Tesla)",
            "h: Intensidade de Campo Magnético (A/m)",
            "mu: Permeabilidade Magnética (H/m)"
        )

        # Mu_0 e Mu_r
        eq_mu_breakdown = MathTex(r"\mu = \mu_0 \cdot \mu_r",font_size=36).move_to(eq_bh) # Troca a equação anterior por esta
        text_mu0 = Tex(r"$\mu_0$: Permeabilidade do vácuo ($4\pi \cdot 10^{-7}$ H/m)", font_size=22)
        text_mur = Tex(r"$\mu_r$: Permeabilidade relativa do material", font_size=22)
        mu_defs_group = VGroup(text_mu0, text_mur).arrange(DOWN, aligned_edge=LEFT)\
            .next_to(eq_mu_breakdown, DOWN, buff=0.5)

        self.play(
            Transform(eq_bh, eq_mu_breakdown),
            FadeOut(text_b), FadeOut(text_h), FadeOut(text_mu),
            FadeIn(text_mu0), FadeIn(text_mur))
        self.esperar_texto(
            3,
            "mu = mu_0 x mu_r",
            "mu_0: Permeabilidade do vácuo",
            "mu_r: Permeabilidade relativa do material"
        )
        
        final_note = Tex(
            "Materiais ferromagnéticos possuem $\mu_r$ muito alto!",
            font_size=24, color=ORANGE).next_to(text_mur, DOWN, buff=0.5)
        self.play(Write(final_note))
        self.esperar_texto(3, "Materiais ferromagnéticos possuem mu_r muito alto")

        # Limpar a cena para Permissividade
        self.play(
            FadeOut(title_permeabilidade),
            FadeOut(text_perm_def),
            FadeOut(eq_bh),
            FadeOut(text_mu0),
            FadeOut(text_mur),
            FadeOut(final_note)
        )

    def parte_4_permissividade(self):
        title_permissividade = Tex("Permissividade Elétrica ($\epsilon$)", font_size=36, color=PURPLE)
        title_permissividade.to_edge(UP)
        self.play(Write(title_permissividade))
        self.esperar_texto(1, "Permissividade Elétrica")

        text_perm_def = VGroup(
            Tex(r"A permissividade elétrica mede a capacidade de um material", font_size=24),
            Tex(r"de permitir o armazenamento de energia em um campo elétrico.", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title_permissividade, DOWN, buff=0.5)
        self.play(Write(text_perm_def))
        self.esperar_texto(
            3,
            "A permissividade elétrica mede a capacidade de um material",
            "de permitir o armazenamento de energia em um campo elétrico"
        )

        # Relação D e E
        eq_de = MathTex(r"\vec{d} = \epsilon \vec{e}", font_size=40).next_to(text_perm_def, DOWN, buff=1)
        text_d = Tex(r"$\vec{d}$: Densidade de Fluxo Elétrico (C/m$^2$)", font_size=22, color=YELLOW)
        text_e = Tex(r"$\vec{e}$: Intensidade de Campo Elétrico (V/m)", font_size=22, color=GREEN)
        text_eps = Tex(r"$\epsilon$: Permissividade Elétrica (F/m)", font_size=22, color=PURPLE)

        definitions_group = VGroup(text_d, text_e, text_eps)\
            .arrange(DOWN, aligned_edge=LEFT).next_to(eq_de, DOWN, buff=0.5)
        
        self.play(Write(eq_de))
        self.play(
            FadeIn(text_d),
            FadeIn(text_e),
            FadeIn(text_eps)
        )
        self.esperar_texto(
            2,
            "d: Densidade de Fluxo Elétrico (C/m^2)",
            "e: Intensidade de Campo Elétrico (V/m)",
            "epsilon: Permissividade Elétrica (F/m)"
        )

        # Epsilon_0 e Epsilon_r
        eq_eps_breakdown = MathTex(r"\epsilon = \epsilon_0 \cdot \epsilon_r",font_size=36).move_to(eq_de)
        text_eps0 = Tex(r"$\epsilon_0$: Permissividade do vácuo ($\approx 8,85 \cdot 10^{-12}$ F/m)", font_size=22)
        text_epsr = Tex(r"$\epsilon_r$: Permissividade relativa do material", font_size=22)
        eps_defs_group = VGroup(text_eps0, text_epsr).arrange(DOWN, aligned_edge=LEFT)\
            .next_to(eq_eps_breakdown, DOWN, buff=0.5)

        self.play(
            Transform(eq_de, eq_eps_breakdown),
            FadeOut(text_d), FadeOut(text_e), FadeOut(text_eps),
            FadeIn(text_eps0), FadeIn(text_epsr))
        self.esperar_texto(
            3,
            "epsilon = epsilon_0 x epsilon_r",
            "epsilon_0: Permissividade do vácuo",
            "epsilon_r: Permissividade relativa do material"
        )
        
        final_note = Tex(
            "Materiais dielétricos possuem $\epsilon_r \ge 1$.",
            font_size=24, color=ORANGE).next_to(text_epsr, DOWN, buff=0.5)
        self.play(Write(final_note))
        self.esperar_texto(3, "Materiais dielétricos possuem epsilon_r maior ou igual a 1")

        self.play(
            FadeOut(title_permissividade),
            FadeOut(text_perm_def),
            FadeOut(eq_de),
            FadeOut(text_eps0),
            FadeOut(text_epsr),
            FadeOut(final_note)
        )
    
    def parte_5_condutividade(self):
        title_condutividade = Tex("Condutividade Elétrica ($\sigma$)", font_size=36, color=GREEN)
        title_condutividade.to_edge(UP)
        self.play(Write(title_condutividade))
        self.esperar_texto(1, "Condutividade Elétrica")

        text_cond_def = VGroup(
            Tex(r"A condutividade elétrica mede a facilidade com que", font_size=24),
            Tex(r"cargas elétricas se movem através de um material.", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title_condutividade, DOWN, buff=0.5)
        self.play(Write(text_cond_def))
        self.esperar_texto(
            3,
            "A condutividade elétrica mede a facilidade com que",
            "cargas elétricas se movem através de um material"
        )

        # Lei de Ohm Micro
        eq_je = MathTex(r"\vec{j} = \sigma \vec{e}", font_size=40).next_to(text_cond_def, DOWN, buff=1)
        text_j = Tex(r"$\vec{j}$: Densidade de Corrente (A/m$^2$)", font_size=22, color=YELLOW)
        text_e = Tex(r"$\vec{e}$: Intensidade de Campo Elétrico (V/m)", font_size=22, color=RED)
        text_sigma = Tex(r"$\sigma$: Condutividade Elétrica (S/m)", font_size=22, color=GREEN)

        definitions_group = VGroup(text_j, text_e, text_sigma)\
            .arrange(DOWN, aligned_edge=LEFT).next_to(eq_je, DOWN, buff=0.5)
        
        self.play(Write(eq_je))
        self.play(
            FadeIn(text_j),
            FadeIn(text_e),
            FadeIn(text_sigma)
        )
        self.esperar_texto(
            2,
            "j: Densidade de Corrente (A/m^2)",
            "e: Intensidade de Campo Elétrico (V/m)",
            "sigma: Condutividade Elétrica (S/m)"
        )

        # Resistividade
        eq_res_breakdown = MathTex(r"\sigma = \frac{1}{\rho}",font_size=36).move_to(eq_je)
        text_rho = Tex(r"$\rho$: Resistividade Elétrica ($\Omega \cdot$m)", font_size=22)
        
        rho_group = VGroup(text_rho).arrange(DOWN, aligned_edge=LEFT)\
            .next_to(eq_res_breakdown, DOWN, buff=0.5)

        self.play(
            Transform(eq_je, eq_res_breakdown),
            FadeOut(text_j), FadeOut(text_e), FadeOut(text_sigma),
            FadeIn(text_rho))
        self.esperar_texto(3, "sigma = 1/rho", "rho: Resistividade Elétrica")
        
        final_note = Tex(
            r"Condutores perfeitos teriam $\sigma \to \infty$.",
            font_size=24, color=ORANGE).next_to(text_rho, DOWN, buff=0.5)
        self.play(Write(final_note))
        self.esperar_texto(3, "Condutores perfeitos teriam sigma tendendo ao infinito")

        self.play(
            FadeOut(title_condutividade),
            FadeOut(text_cond_def),
            FadeOut(eq_je),
            FadeOut(text_rho),
            FadeOut(final_note)
        )

    def parte_6_relacoes_constitutivas(self):
        title_relacoes = Tex("Relações Constitutivas", font_size=36, color=WHITE)
        title_relacoes.to_edge(UP)
        self.play(Write(title_relacoes))
        self.esperar_texto(1, "Relações Constitutivas")

        # Equações
        eq_d = MathTex(r"\vec{d} = \epsilon \vec{e}", font_size=30)
        eq_b = MathTex(r"\vec{b} = \mu \vec{h}", font_size=30)
        eq_j = MathTex(r"\vec{j} = \sigma \vec{e}", font_size=30)

        # Labels
        label_d = Tex(r"Permissividade ($\epsilon$)", font_size=20, color=PURPLE).next_to(eq_d, UP)
        label_b = Tex(r"Permeabilidade ($\mu$)", font_size=20, color=BLUE).next_to(eq_b, UP)
        label_j = Tex(r"Condutividade ($\sigma$)", font_size=20, color=GREEN).next_to(eq_j, UP)
        
        group_d = VGroup(label_d, eq_d)
        group_b = VGroup(label_b, eq_b)
        group_j = VGroup(label_j, eq_j)
        
        all_eqs = VGroup(group_d, group_b, group_j).arrange(RIGHT, buff=1.5)
        
        self.play(
            FadeIn(group_d),
            FadeIn(group_b),
            FadeIn(group_j)
        )
        self.esperar_texto(
            2,
            "Permissividade (epsilon)",
            "Permeabilidade (mu)",
            "Condutividade (sigma)",
            "d = epsilon e",
            "b = mu h",
            "j = sigma e"
        )
        
        rect = SurroundingRectangle(all_eqs, buff=0.3, color=WHITE)
        text_summary = Tex(
            "Essas propriedades caracterizam o meio material.",
            font_size=26).next_to(rect, DOWN, buff=0.5)
            
        self.play(Create(rect), Write(text_summary))
        self.esperar_texto(3, "Essas propriedades caracterizam o meio material")

        self.play(
            FadeOut(title_relacoes),
            FadeOut(all_eqs),
            FadeOut(rect),
            FadeOut(text_summary)
        )

    def construct(self):
        self.parte_1_carga_e_forca()
        self.parte_2_detalhando_forca()
        self.parte_3_permeabilidade()
        self.parte_4_permissividade()
        self.parte_5_condutividade()
        self.parte_6_relacoes_constitutivas()

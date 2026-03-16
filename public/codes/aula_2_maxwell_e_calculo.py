from manim import *

config.media_width = "75%"
config.verbosity = "WARNING"

class MaxwellECalculo(Scene):
    LIMIAR_TEXTO_LONGO = 60

    def esperar_texto(self, tempo_base: float, *textos: str):
        total_caracteres = sum(len(texto) for texto in textos)
        tempo_extra = 3 if total_caracteres >= self.LIMIAR_TEXTO_LONGO else 2
        self.wait(tempo_base + tempo_extra)

    def construct(self):
        self.parte_1_equacoes_maxwell()
        self.parte_2_revisao_calculo()
        self.parte_3_lei_faraday()
        self.parte_4_lei_ampere()
        self.parte_5_lei_gauss_eletrica()
        self.parte_6_lei_gauss_magnetica()

    def parte_1_equacoes_maxwell(self):
        # Título
        titulo = Tex("Equações de Maxwell", font_size=40).to_edge(UP)
        self.play(Write(titulo))
        self.esperar_texto(1, "Equações de Maxwell")

        # As 4 equações na forma diferencial
        # Usaremos MathTex com substrings separadas para facilitar coloração
        # 1. Lei de Gauss (Elétrica)
        # \nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0}
        eq1 = MathTex(
            r"\nabla \cdot", r"\vec{E}", r"=", r"\frac{", r"\rho", r"}{", r"\varepsilon_0", r"}"
        )
        
        # 2. Lei de Gauss (Magnética)
        # \nabla \cdot \vec{B} = 0
        eq2 = MathTex(
            r"\nabla \cdot", r"\vec{B}", r"=", r"0"
        )
        
        # 3. Lei de Faraday
        # \nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}
        eq3 = MathTex(
            r"\nabla \times", r"\vec{E}", r"=", r"-", r"\frac{\partial ", r"\vec{B}", r"}{\partial t}"
        )
        
        # 4. Lei de Ampère-Maxwell
        # \nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t}
        eq4 = MathTex(
            r"\nabla \times", r"\vec{B}", r"=", r"\mu_0", r"\vec{J}", r"+", r"\mu_0", r"\varepsilon_0", r"\frac{\partial ", r"\vec{E}", r"}{\partial t}"
        )

        # Equações em grade 2x2
        equacoes = VGroup(eq1, eq2, eq3, eq4).arrange_in_grid(rows=2, cols=2, buff=1.0).shift(UP * 0.5)
        
        self.play(Write(equacoes), run_time=4)
        self.esperar_texto(2, "Essas são as quatro Equações de Maxwell na forma diferencial.")

        # --- Detalhando Componentes ---
        COR_E = BLUE
        COR_B = RED
        COR_FONTE = YELLOW # Rho e J
        COR_CONST = GREEN # Epsilon e Mi

        # Cores para os componentes
        self.play(
            eq1.animate.set_color_by_tex(r"\vec{E}", COR_E).set_color_by_tex(r"\rho", COR_FONTE).set_color_by_tex(r"\varepsilon_0", COR_CONST),
            eq2.animate.set_color_by_tex(r"\vec{B}", COR_B),
            eq3.animate.set_color_by_tex(r"\vec{E}", COR_E).set_color_by_tex(r"\vec{B}", COR_B),
            eq4.animate.set_color_by_tex(r"\vec{B}", COR_B).set_color_by_tex(r"\vec{J}", COR_FONTE).set_color_by_tex(r"\mu_0", COR_CONST).set_color_by_tex(r"\varepsilon_0", COR_CONST).set_color_by_tex(r"\vec{E}", COR_E)
        )
        
        # Legendas em grade 2x2 abaixo das equações
        legenda_E = Tex(r"$\vec{E}$: Campo Elétrico", color=COR_E, font_size=28)
        legenda_B = Tex(r"$\vec{B}$: Campo Magnético", color=COR_B, font_size=28)
        legenda_rho = Tex(r"$\rho$, $\vec{J}$: Fontes", color=COR_FONTE, font_size=28)
        legenda_const = Tex(r"$\varepsilon_0, \mu_0$: Meio", color=COR_CONST, font_size=28)
        
        legendas = VGroup(legenda_E, legenda_B, legenda_rho, legenda_const).arrange_in_grid(rows=2, cols=2, buff=0.8, cell_alignment=LEFT)
        legendas.next_to(equacoes, DOWN, buff=1.0)
        
        self.play(Write(legendas), run_time=3)
        self.esperar_texto(4, "Campos, Fontes e Constantes do Meio.")
        
        self.play(FadeOut(legendas), FadeOut(equacoes), FadeOut(titulo))

    def parte_2_revisao_calculo(self):
        # Título
        titulo = Tex("Operadores Diferenciais", font_size=40).to_corner(UL)
        self.play(Write(titulo))

        # Divergente
        label_div = MathTex(r"\nabla \cdot \vec{F}", color=YELLOW, font_size=48).shift(LEFT * 3 + UP * 2)
        texto_div = Tex('"Divergente"', font_size=32).next_to(label_div, UP)
        desc_div = Tex(r"Mede o fluxo saindo\\de um ponto", font_size=28).next_to(label_div, DOWN)

        # Rotacional
        label_rot = MathTex(r"\nabla \times \vec{F}", color=GREEN, font_size=48).shift(RIGHT * 3 + UP * 2)
        texto_rot = Tex('"Rotacional"', font_size=32).next_to(label_rot, UP)
        desc_rot = Tex(r"Mede a rotação\\em torno de um ponto", font_size=28).next_to(label_rot, DOWN)

        self.play(
            FadeIn(label_div), Write(texto_div), Write(desc_div),
            FadeIn(label_rot), Write(texto_rot), Write(desc_rot)
        )
        self.esperar_texto(3, "Vamos relembrar o Divergente e o Rotacional.")

        # --- Visualização Divergente ---
        centro_div = LEFT * 3 + DOWN * 1.5
        ponto_fonte = Dot(color=WHITE).move_to(centro_div)
        
        # Criar setas radiais
        setas_div = VGroup()
        for angulo in np.linspace(0, 360, 8, endpoint=False):
            direcao = np.array([np.cos(angulo*DEGREES), np.sin(angulo*DEGREES), 0])
            seta = Arrow(
                start=centro_div + direcao * 0.2, 
                end=centro_div + direcao * 1.0, # Setas menores para caber
                buff=0, 
                color=YELLOW,
                max_tip_length_to_length_ratio=0.25
            )
            setas_div.add(seta)
        
        # --- Visualização Rotacional ---
        centro_rot = RIGHT * 3 + DOWN * 1.5
        ponto_vortice = Dot(color=WHITE).move_to(centro_rot)
        
        setas_rot = VGroup()
        raio = 0.8
        for angulo in np.linspace(0, 360, 8, endpoint=False):
            # Posição no círculo
            pos = centro_rot + np.array([raio*np.cos(angulo*DEGREES), raio*np.sin(angulo*DEGREES), 0])
            # Tangente (-sin, cos)
            tangente = np.array([-np.sin(angulo*DEGREES), np.cos(angulo*DEGREES), 0])
            
            # Seta pequena tangente
            seta = Arrow(
                start=pos - tangente * 0.2,
                end=pos + tangente * 0.2,
                buff=0, 
                color=GREEN,
                max_tip_length_to_length_ratio=0.3
            )
            setas_rot.add(seta)
            
        self.play(
            Create(ponto_fonte), Create(setas_div),
            Create(ponto_vortice), Create(setas_rot)
        )
        
        # Animação de "pulso" para divergente e "rotação" para rotacional
        self.play(
            # Divergente pulsa (escala)
            setas_div.animate.scale(1.2).set_rate_func(there_and_back).set_run_time(2),
            # Rotacional gira
            Rotate(setas_rot, angle=2*PI, about_point=centro_rot, rate_func=linear, run_time=4)
        )

        self.esperar_texto(2, "O divergente associa-se a fontes e sorvedouros. O rotacional a vórtices e circulação.")
        
        # Finalização
        self.play(
            FadeOut(ponto_fonte), FadeOut(setas_div), FadeOut(label_div), FadeOut(texto_div), FadeOut(desc_div),
            FadeOut(ponto_vortice), FadeOut(setas_rot), FadeOut(label_rot), FadeOut(texto_rot), FadeOut(desc_rot),
            FadeOut(titulo)
        )
        self.wait(1)

    def parte_3_lei_faraday(self):
        # Título
        titulo = Tex("Lei de Faraday-Lenz", font_size=40).to_edge(UP)
        self.play(Write(titulo))
        
        # Equação de Faraday
        eq_faraday = MathTex(
            r"\nabla \times", r"\vec{E}", r"=", r"-", r"\frac{\partial \vec{B}}{\partial t}"
        )
        self.play(Write(eq_faraday))
        self.esperar_texto(2, "A Lei de Faraday relaciona o campo elétrico induzido à variação do campo magnético.")

        # Detalhando os componentes
        COR_E = BLUE
        COR_B = RED
        
        # Colorir componentes
        self.play(
            eq_faraday.animate.set_color_by_tex(r"\vec{E}", COR_E).set_color_by_tex(r"\vec{B}", COR_B)
        )

        # Mover equação para cima
        self.play(eq_faraday.animate.shift(UP * 2))

        # Texto Explicativo sobre Fontes e Meios (ou sua ausência)
        # Explicar que aqui a "fonte" não é carga/corrente, mas variação de campo
        texto_expl = Tex(
            r"Note a ausência de cargas ($\rho$) ou correntes ($\vec{J}$), que são as fontes convencionais.\\"
            r"E também das constantes do meio ($\varepsilon_0, \mu_0$).\\"
            r"Aqui, a 'fonte' do campo elétrico rotacional é puramente a variação temporal do campo magnético.",
            font_size=32
        ).next_to(eq_faraday, DOWN, buff=1)

        self.play(Write(texto_expl))
        self.esperar_texto(5, "A variação do campo magnético age como fonte para o campo elétrico induzido.")
        
        self.play(FadeOut(texto_expl))

        # Animação Visual da Indução
        # Mover para o centro-baixo para não bater na equação
        centro_anim = DOWN * 1.5
        
        # Vetor B no centro (crescendo)
        vetor_B = Arrow(start=DOWN, end=UP, color=COR_B, buff=0).scale(0.4).move_to(centro_anim)
        label_B = MathTex(r"\vec{B}(t)", color=COR_B, font_size=24).next_to(vetor_B, RIGHT, buff=0.1)
        
        # Campo E circulando (anéis de setas)
        grupo_E = VGroup()
        raio = 1.2 # Reduzido para não bater na equação ou bordas
        num_setas = 8
        for i in range(num_setas):
            angle = i * (360 / num_setas) * DEGREES
            # Posição no círculo
            pos = centro_anim + np.array([raio * np.cos(angle), raio * np.sin(angle), 0])
            # Tangente horária
            tangente = np.array([np.sin(angle), -np.cos(angle), 0])
            
            seta = Arrow(
                start=pos - tangente * 0.2, 
                end=pos + tangente * 0.2,
                buff=0, 
                color=COR_E,
                max_tip_length_to_length_ratio=0.3
            )
            grupo_E.add(seta)
            
        label_E = MathTex(r"\vec{E}_{ind}", color=COR_E, font_size=24).next_to(grupo_E, UP, buff=0.1)

        desc_anim = Tex("Variação de B gera E rotacional", font_size=26).to_edge(DOWN, buff=0.2)

        self.play(
            GrowArrow(vetor_B), Write(label_B),
            Create(grupo_E), Write(label_E),
            Write(desc_anim)
        )

        # Animação: B cresce, E gira
        self.play(
            vetor_B.animate.scale(1.8), # Escala reduzida para evitar sobreposição
            Rotate(grupo_E, angle=-2*PI, about_point=centro_anim, rate_func=linear), # Sentido horário
            run_time=4
        )
        self.esperar_texto(3, "Quanto mais rápida a variação do campo magnético, maior a intensidade do campo elétrico induzido.")

        self.play(
            FadeOut(vetor_B), FadeOut(label_B), 
            FadeOut(grupo_E), FadeOut(label_E), 
            FadeOut(desc_anim)
        )

        # Forma Integral
        titulo_integral = Tex("Forma Integral", font_size=36, color=YELLOW).next_to(titulo, DOWN)
        self.play(Write(titulo_integral))
        
        # Equação Integral
        # \oint \vec{E} \cdot d\vec{l} = - \frac{d}{dt} \int_S \vec{B} \cdot d\vec{S}
        eq_integral = MathTex(
            r"\oint", r"\vec{E}", r"\cdot d\vec{l}", r"=", r"-", r"\frac{d}{dt}", r"\int_S", r"\vec{B}", r"\cdot d\vec{S}"
        ).next_to(titulo_integral, DOWN, buff=1)

        self.play(ReplacementTransform(eq_faraday, eq_integral))
        self.esperar_texto(3, "Na forma integral, vemos que a circulação do campo elétrico é igual à variação do fluxo magnético.")

        # Relação Constitutiva
        # B = mu H
        # Texto do usuário: "campo magnético é a densidade do fluxo magnético x a permeabilidade magnética"
        # Assumindo B = mu H (Densidade = Permeabilidade * Intensidade) ou similar.
        # Mas a frase literal do usuário diz: "campo magnético (H?) = densidade (B) * permeabilidade (mu)"?
        # Ou "campo magnético (B) = densidade do fluxo (phi/A) * permeabilidade"?
        # Vamos usar a forma padrão: B = mu H, e citar o texto como "Relação entre B e H".
        
        note_text = Tex(r"Nota: Relação Constitutiva", font_size=30, color=BLUE).next_to(eq_integral, DOWN, buff=1.5)
        eq_constitutiva = MathTex(r"\vec{B} = \mu \vec{H}", font_size=36).next_to(note_text, DOWN)
        
        desc_constitutiva = Tex(
            r"$\vec{B}$: Densidade de Fluxo Magnético\\",
            r"$\vec{H}$: Intensidade de Campo Magnético\\",
            r"$\mu$: Permeabilidade Magnética",
            font_size=28
        ).next_to(eq_constitutiva, DOWN)

        self.play(Write(note_text), Write(eq_constitutiva))
        self.play(Write(desc_constitutiva))
        self.esperar_texto(4, "Lembrando que a densidade de fluxo B relaciona-se com a intensidade H pela permeabilidade do meio.")

        self.play(
            FadeOut(titulo), FadeOut(titulo_integral),
            FadeOut(eq_integral), 
            FadeOut(note_text), FadeOut(eq_constitutiva), FadeOut(desc_constitutiva)
        )
        self.wait(1)

    def parte_4_lei_ampere(self):
        # Título
        titulo = Tex("Lei de Ampère-Maxwell", font_size=40).to_edge(UP)
        self.play(Write(titulo))
        
        # Equação de Ampère-Maxwell de forma reduzida
        # \nabla \times \vec{H} = \vec{J} + \frac{\partial \vec{D}}{\partial t}
        # Mas vamos manter o padrão com B e E da Parte 1, ou usar H e D se for mais preciso?
        # Parte 1 usou E e B. Vamos manter E e B para consistência, mas expandir as constantes.
        
        # \nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t}
        
        eq_ampere = MathTex(
            r"\nabla \times", r"\vec{B}", r"=", r"\mu_0", r"\vec{J}", r"+", r"\mu_0 \varepsilon_0", r"\frac{\partial \vec{E}}{\partial t}"
        )
        self.play(Write(eq_ampere))
        self.esperar_texto(2, "A Lei de Ampère-Maxwell descreve como correntes e campos elétricos variáveis geram campo magnético.")

        COR_E = BLUE
        COR_B = RED
        COR_FONTE = YELLOW # J
        COR_CONST = GREEN  # Mu e Epsilon

        # Colorir
        self.play(
            eq_ampere.animate.set_color_by_tex(r"\vec{B}", COR_B).set_color_by_tex(r"\vec{J}", COR_FONTE).set_color_by_tex(r"\vec{E}", COR_E).set_color_by_tex(r"\mu_0", COR_CONST).set_color_by_tex(r"\varepsilon_0", COR_CONST)
        )
        
        self.play(eq_ampere.animate.shift(UP * 2))

        # Detalhar Termos
        termo_conducao = Tex("Corrente de Condução", color=COR_FONTE, font_size=30).next_to(eq_ampere, DOWN, buff=1).shift(LEFT*2)
        termo_deslocamento = Tex("Corrente de Deslocamento", color=COR_E, font_size=30).next_to(eq_ampere, DOWN, buff=1).shift(RIGHT*2)
        
        seta_cond = Arrow(start=termo_conducao.get_top(), end=eq_ampere[4].get_bottom(), color=COR_FONTE)
        seta_desl = Arrow(start=termo_deslocamento.get_top(), end=eq_ampere[7].get_bottom(), color=COR_E)
        
        self.play(
            FadeIn(termo_conducao), GrowArrow(seta_cond),
            FadeIn(termo_deslocamento), GrowArrow(seta_desl)
        )
        self.esperar_texto(4, "Temos a corrente de condução (J) e a corrente de deslocamento (variação de E).") # Force wait
        
        self.play(
            FadeOut(termo_conducao), FadeOut(seta_cond),
            FadeOut(termo_deslocamento), FadeOut(seta_desl)
        )

        # Animação Visual: Condução vs Deslocamento
        centro_anim = DOWN * 1.5
        
        # 1. Corrente de Condução (Fio)
        fio = Line(start=centro_anim + DOWN*2, end=centro_anim + UP*2, color=GREY, stroke_width=4)
        corrente_J = Arrow(start=centro_anim + DOWN*1, end=centro_anim + UP*1, color=COR_FONTE, buff=0)
        label_J = MathTex(r"\vec{J}", color=COR_FONTE, font_size=28).next_to(corrente_J, RIGHT, buff=0.1)
        
        grupo_B = VGroup()
        raio = 1.2
        num_setas = 8
        for i in range(num_setas):
            angle = i * (360 / num_setas) * DEGREES
            pos = centro_anim + np.array([raio * np.cos(angle), raio * np.sin(angle), 0])
            tangente = np.array([-np.sin(angle), np.cos(angle), 0])
            seta = Arrow(
                start=pos - tangente * 0.2, end=pos + tangente * 0.2,
                buff=0, color=COR_B, max_tip_length_to_length_ratio=0.3
            )
            grupo_B.add(seta)
            
        desc_anim_1 = Tex("Corrente de Condução gera B", font_size=26).to_edge(DOWN, buff=0.2)
        
        self.play(
            FadeIn(fio), GrowArrow(corrente_J), Write(label_J),
            Create(grupo_B), Write(desc_anim_1)
        )
        self.play(Rotate(grupo_B, angle=2*PI, about_point=centro_anim, run_time=2))
        self.esperar_texto(2, "Uma corrente elétrica convencional gera um campo magnético rotacional.")
        
        # 2. Corrente de Deslocamento (Capacitor)
        self.play(
            FadeOut(corrente_J), FadeOut(label_J), FadeOut(desc_anim_1),
            FadeOut(fio)
        )
        
        # Desenhar Capacitor
        gap = 1.0
        placa_esq = Rectangle(height=2, width=0.2, color=GREY, fill_opacity=0.5).move_to(centro_anim + LEFT*gap)
        placa_dir = Rectangle(height=2, width=0.2, color=GREY, fill_opacity=0.5).move_to(centro_anim + RIGHT*gap)
        
        # Campo E variável no gap
        vetor_E_gap = Arrow(start=centro_anim + LEFT*(gap-0.2), end=centro_anim + RIGHT*(gap-0.2), color=COR_E, buff=0)
        label_E_gap = MathTex(r"\frac{\partial \vec{E}}{\partial t}", color=COR_E, font_size=28).next_to(vetor_E_gap, UP)
        
        desc_anim_2 = Tex("Variação de E (Corrente de Deslocamento) também gera B", font_size=26).to_edge(DOWN, buff=0.2)
        
        self.play(
            FadeIn(placa_esq), FadeIn(placa_dir),
            GrowArrow(vetor_E_gap), Write(label_E_gap),
            Write(desc_anim_2)
        )
        
        # Animar variação de E e rotação de B
        # Vamos fazer E crescer e diminuir para simular dE/dt
        self.play(
            vetor_E_gap.animate.scale(1.2).set_opacity(1).set_rate_func(there_and_back),
            Rotate(grupo_B, angle=2*PI, about_point=centro_anim, rate_func=linear),
            run_time=4
        )
        self.esperar_texto(3, "No vácuo entre as placas, não há carga, mas a variação do campo elétrico cria um campo magnético.")

        self.play(
            FadeOut(placa_esq), FadeOut(placa_dir),
            FadeOut(vetor_E_gap), FadeOut(label_E_gap),
            FadeOut(grupo_B), FadeOut(desc_anim_2)
        )
        
        # Forma Integral
        titulo_integral = Tex("Forma Integral", font_size=36, color=YELLOW).next_to(titulo, DOWN)
        self.play(Write(titulo_integral))
        
        # \oint \vec{B} \cdot d\vec{l} = \mu_0 I + \mu_0 \varepsilon_0 \frac{d\Phi_E}{dt}
        # Simplificado para integrais
        eq_integral_ampere = MathTex(
            r"\oint", r"\vec{B}", r"\cdot d\vec{l}", r"=", r"\mu_0", r"\int_S \vec{J} \cdot d\vec{S}", r"+", r"\mu_0 \varepsilon_0", r"\frac{d}{dt} \int_S \vec{E} \cdot d\vec{S}"
        ).next_to(titulo_integral, DOWN, buff=0.5).scale(0.9)
        
        self.play(ReplacementTransform(eq_ampere, eq_integral_ampere))
        self.esperar_texto(3, "A circulação magnética depende da corrente total e da variação do fluxo elétrico.")
        
        # Relação Constitutiva (D = epsilon E)
        note_text = Tex(r"Nota: Relação Constitutiva", font_size=30, color=BLUE).next_to(eq_integral_ampere, DOWN, buff=1.0)
        eq_constitutiva_D = MathTex(r"\vec{D} = \varepsilon \vec{E}", font_size=36).next_to(note_text, DOWN)
        
        desc_constitutiva_D = Tex(
            r"$\vec{D}$: Densidade de Fluxo Elétrico\\",
            r"$\vec{E}$: Intensidade de Campo Elétrico\\",
            r"$\varepsilon$: Permissividade Elétrica",
            font_size=28
        ).next_to(eq_constitutiva_D, DOWN)

        self.play(Write(note_text), Write(eq_constitutiva_D))
        self.play(Write(desc_constitutiva_D))
        self.esperar_texto(4, "A densidade de fluxo elétrico D relaciona-se com o campo E pela permissividade do meio.")

        self.play(
            FadeOut(titulo), FadeOut(titulo_integral), FadeOut(eq_integral_ampere),
            FadeOut(note_text), FadeOut(eq_constitutiva_D), FadeOut(desc_constitutiva_D)
        )
        self.wait(1)

    def parte_5_lei_gauss_eletrica(self):
        # Título
        titulo = Tex("Lei de Gauss (Elétrica)", font_size=40).to_edge(UP)
        self.play(Write(titulo))

        # Equação de Gauss
        # \nabla \cdot \E = \frac{\rho}{\varepsilon_0}
        eq_gauss_E = MathTex(
            r"\nabla \cdot", r"\vec{E}", r"=", r"\frac{\rho}{ \varepsilon_0 }"
        )
        self.play(Write(eq_gauss_E))
        self.esperar_texto(2, "A Lei de Gauss para a Eletricidade relaciona o divergente do campo elétrico com sua fonte: a carga elétrica.")

        COR_E = BLUE
        COR_FONTE = YELLOW # Rho
        COR_CONST = GREEN  # Epsilon

        # Colorir componentes
        self.play(
            eq_gauss_E.animate.set_color_by_tex(r"\vec{E}", COR_E).set_color_by_tex(r"\rho", COR_FONTE).set_color_by_tex(r"\varepsilon_0", COR_CONST)
        )
        
        self.play(eq_gauss_E.animate.shift(UP * 2))

        # Texto Explicativo com componentes
        texto_expl = Tex(
            r"O divergente ($\nabla \cdot \vec{E}$) mede o quanto o campo 'brota' de um ponto.\\"
            r"$\rho$: Densidade volumétrica de carga elétrica (Fonte).\\"
            r"$\varepsilon_0$: Permissividade do meio.",
            font_size=32
        ).next_to(eq_gauss_E, DOWN, buff=1)
        
        self.play(Write(texto_expl))
        self.esperar_texto(4, "Cargas positivas são fontes de campo (divergente positivo), cargas negativas são sorvedouros (divergente negativo).")
        
        self.play(FadeOut(texto_expl))

        # Animação Visual
        # Carga positiva Q no centro -> Campo E divergente radialmente
        centro_anim = DOWN * 1.5
        
        carga_Q = Circle(radius=0.3, color=COR_FONTE, fill_opacity=0.8).move_to(centro_anim)
        sinal_mais = MathTex("+", color=BLACK).move_to(carga_Q)
        label_rho = MathTex(r"\rho > 0", color=COR_FONTE, font_size=30).next_to(carga_Q, UP)
        
        setas_E = VGroup()
        for angulo in np.linspace(0, 360, 12, endpoint=False):
            direcao = np.array([np.cos(angulo*DEGREES), np.sin(angulo*DEGREES), 0])
            seta = Arrow(
                start=centro_anim + direcao * 0.4, 
                end=centro_anim + direcao * 2.0,
                buff=0, 
                color=COR_E,
                max_tip_length_to_length_ratio=0.15
            )
            setas_E.add(seta)
            
        desc_anim = Tex("Campo E divergindo de uma carga positiva", font_size=26).to_edge(DOWN, buff=0.2)

        self.play(
            FadeIn(carga_Q), Write(sinal_mais), Write(label_rho),
            Create(setas_E), Write(desc_anim)
        )
        
        # Animação de fluxo saindo
        self.play(
            setas_E.animate.scale(1.1).set_rate_func(there_and_back).set_run_time(2)
        )
        self.esperar_texto(2, "As cargas elétricas atuam como fontes ou sumidouros do campo elétrico.")

        self.play(
            FadeOut(carga_Q), FadeOut(sinal_mais), FadeOut(label_rho),
            FadeOut(setas_E), FadeOut(desc_anim), FadeOut(eq_gauss_E)
        )

        # Forma Integral
        titulo_integral = Tex("Forma Integral", font_size=36, color=YELLOW).next_to(titulo, DOWN)
        self.play(Write(titulo_integral))
        
        # \oint_S \vec{D} \cdot d\vec{S} = Q_{L} (Carga Livre Envolvida)
        # Vamos usar a forma mais comum em livros de física básica primeiro: Integral E . dS = Q_int / eps0
        eq_integral_gauss = MathTex(
            r"\oint_S", r"\vec{E}", r"\cdot d\vec{S}", r"=", r"\frac{Q_{env}}{\varepsilon_0}"
        ).next_to(titulo_integral, DOWN, buff=1)

        self.play(Write(eq_integral_gauss))
        
        # Colorir Q_env para destaque
        self.play(eq_integral_gauss.animate.set_color_by_tex("Q_{env}", YELLOW))
        self.esperar_texto(3, "O fluxo elétrico total através de uma superfície fechada é proporcional à carga envolvida.")

        # Explicação mais detalhada de Q_env
        self.play(eq_integral_gauss.animate.to_edge(UP, buff=2))
        
        texto_qenv = Tex(
            r"$Q_{env}$: Carga Líquida dentro da superfície $S$.",
            font_size=32, color=YELLOW
        ).next_to(eq_integral_gauss, DOWN)
        
        subtexto_qenv = Tex(
            r"Cargas fora da superfície não alteram o fluxo líquido.",
            font_size=28
        ).next_to(texto_qenv, DOWN)

        self.play(Write(texto_qenv), Write(subtexto_qenv))
        self.esperar_texto(3, "Apenas as cargas dentro da superfície imaginária (Gaussiana) contribuem para o fluxo líquido.")

        # Visualização Carga Interna vs Externa
        centro_gauss = DOWN * 0.5
        
        # Superfície Gaussiana (Tracejada)
        superficie = Ellipse(width=4, height=2.5, color=WHITE).move_to(centro_gauss)
        superficie.set_stroke(opacity=0.5).set_style(stroke_width=2) # Tracejado manual não é nativo simples, usar opacidade baixa
        label_S = Tex("S", font_size=24).next_to(superficie, UL, buff=0)

        # Cargas
        q_in_1 = Circle(radius=0.15, color=YELLOW, fill_opacity=1).move_to(centro_gauss + LEFT*0.5)
        sign_in_1 = Tex("+", font_size=20, color=BLACK).move_to(q_in_1)
        
        q_in_2 = Circle(radius=0.15, color=YELLOW, fill_opacity=1).move_to(centro_gauss + RIGHT*0.8 + UP*0.3)
        sign_in_2 = Tex("+", font_size=20, color=BLACK).move_to(q_in_2)
        
        q_out = Circle(radius=0.15, color=RED, fill_opacity=1).move_to(centro_gauss + RIGHT*3)
        sign_out = Tex("+", font_size=20, color=BLACK).move_to(q_out)
        label_out = Tex("Carga Externa", font_size=24).next_to(q_out, DOWN)

        grupo_visual = VGroup(superficie, label_S, q_in_1, sign_in_1, q_in_2, sign_in_2, q_out, sign_out, label_out)
        
        self.play(Create(superficie), Write(label_S))
        self.play(FadeIn(q_in_1), FadeIn(q_in_2), FadeIn(sign_in_1), FadeIn(sign_in_2))
        self.play(FadeIn(q_out), FadeIn(sign_out), Write(label_out))
        
        self.esperar_texto(4, "Imagine uma superfície S. A lei conta apenas as cargas no interior dela.")
        
        self.play(
            FadeOut(texto_qenv), FadeOut(subtexto_qenv),
            FadeOut(grupo_visual)
        )
        
        # Nota sobre Densidade de Fluxo Elétrico (D)
        note_text = Tex(r"Nota: Relação Constitutiva", font_size=30, color=BLUE).next_to(eq_integral_gauss, DOWN, buff=1.0)
        eq_constitutiva_rho = MathTex(r"\nabla \cdot \vec{D} = \rho_v", font_size=36).next_to(note_text, DOWN)
        desc_constitutiva = Tex(
            r"$\vec{D} = \varepsilon \vec{E}$",
            font_size=30
        ).next_to(eq_constitutiva_rho, DOWN)

        self.play(Write(note_text), Write(eq_constitutiva_rho), Write(desc_constitutiva))
        self.esperar_texto(3, "Em muitos meios, usamos o vetor deslocamento elétrico D para incluir os efeitos de polarização.")

        self.play(
            FadeOut(titulo), FadeOut(titulo_integral), FadeOut(eq_integral_gauss),
            FadeOut(note_text), FadeOut(eq_constitutiva_rho), FadeOut(desc_constitutiva)
        )
        self.wait(1)

    def parte_6_lei_gauss_magnetica(self):
        # Título
        titulo = Tex("Lei de Gauss (Magnética)", font_size=40).to_edge(UP)
        self.play(Write(titulo))
        
        # Equação de Gauss Magnética
        # \nabla \cdot \vec{B} = 0
        eq_gauss_B = MathTex(
            r"\nabla \cdot", r"\vec{B}", r"=", r"0"
        )
        self.play(Write(eq_gauss_B))
        self.esperar_texto(2, "A Lei de Gauss para o Magnetismo afirma que não existem monopólos magnéticos.")

        COR_B = RED

        self.play(
            eq_gauss_B.animate.set_color_by_tex(r"\vec{B}", COR_B)
        )
        
        self.play(eq_gauss_B.animate.shift(UP * 2))

        # Texto Explicativo
        texto_expl = Tex(
            r"O divergente do campo magnético é sempre nulo.\\"
            r"Isso significa que não há fonte pontual magnética isolada (monopolo).\\"
            r"As linhas de campo magnético são sempre fechadas (loops).",
            font_size=32
        ).next_to(eq_gauss_B, DOWN, buff=1)
        
        self.play(Write(texto_expl))
        self.esperar_texto(4, "Diferente da eletricidade, onde podemos isolar cargas positivas e negativas, no magnetismo os polos norte e sul são inseparáveis.")
        
        self.play(FadeOut(texto_expl))

        # Animação Visual
        # Ímã dipolo -> Linhas saindo do N e entrando no S
        centro_anim = DOWN * 1.5
        
        # Ímã retangular
        ima = VGroup(
            Rectangle(width=0.5, height=2, color=BLUE, fill_opacity=0.8).shift(LEFT*0.25), # Sul
            Rectangle(width=0.5, height=2, color=RED, fill_opacity=0.8).shift(RIGHT*0.25)  # Norte
        ).move_to(centro_anim)
        label_N = Tex("N", color=WHITE, font_size=24).move_to(ima[1])
        label_S = Tex("S", color=WHITE, font_size=24).move_to(ima[0])
        
        # Linhas de campo (Simplificado: Arcos)
        linhas_campo = VGroup()
        for i in range(3):
            raio_x = 1.5 + i*0.5
            raio_y = 1.0 + i*0.5
            # Arco superior (N -> S)
            arco_sup = ArcBetweenPoints(
                start=centro_anim + RIGHT*0.25 + UP*0.8,
                end=centro_anim + LEFT*0.25 + UP*0.8,
                angle=PI/1.5,
                color=COR_B
            ).add_tip(tip_length=0.2)
            # Arco inferior (N -> S)
            arco_inf = ArcBetweenPoints(
                start=centro_anim + RIGHT*0.25 + DOWN*0.8,
                end=centro_anim + LEFT*0.25 + DOWN*0.8,
                angle=-PI/1.5,
                color=COR_B
            ).add_tip(tip_length=0.2)
            linhas_campo.add(arco_sup, arco_inf)
        
        # Linhas internas (S -> N) para fechar o loop
        linha_interna = Arrow(
            start=centro_anim + LEFT*0.2, end=centro_anim + RIGHT*0.2, 
            color=COR_B, buff=0, max_tip_length_to_length_ratio=0.5
        ).set_opacity(0.5)

        desc_anim = Tex("Linhas de campo B são contínuas e fechadas", font_size=26).to_edge(DOWN, buff=0.2)

        self.play(
            FadeIn(ima), Write(label_N), Write(label_S),
            Create(linhas_campo), FadeIn(linha_interna),
            Write(desc_anim)
        )
        self.esperar_texto(3, "Todo fluxo que sai do polo norte entra no polo sul, resultando em fluxo líquido nulo através de qualquer superfície fechada.")

        self.play(
            FadeOut(ima), FadeOut(label_N), FadeOut(label_S),
            FadeOut(linhas_campo), FadeOut(linha_interna),
            FadeOut(desc_anim), FadeOut(eq_gauss_B)
        )

        # Forma Integral
        titulo_integral = Tex("Forma Integral", font_size=36, color=YELLOW).next_to(titulo, DOWN)
        self.play(Write(titulo_integral))
        
        # \oint_S \vec{B} \cdot d\vec{S} = 0
        eq_integral_gauss_B = MathTex(
            r"\oint_S", r"\vec{B}", r"\cdot d\vec{S}", r"=", r"0"
        ).next_to(titulo_integral, DOWN, buff=1)

        self.play(Write(eq_integral_gauss_B))
        self.esperar_texto(3, "O fluxo magnético líquido através de qualquer superfície fechada é sempre zero.")
        
        # Nota final
        note_text = Tex("Não existe carga magnética isolada.", font_size=30, color=BLUE).next_to(eq_integral_gauss_B, DOWN, buff=1.0)
        self.play(Write(note_text))
        self.wait(2)

        # Encerramento
        self.play(
            FadeOut(titulo), FadeOut(titulo_integral), FadeOut(eq_integral_gauss_B),
            FadeOut(note_text)
        )
        final_text = Tex("Fim da Aula 2: Equações de Maxwell", font_size=40).move_to(ORIGIN)
        self.play(Write(final_text))
        self.wait(3)

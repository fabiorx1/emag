from manim import *
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

class PropagacaoMeiosScene(Scene):
    def construct(self):
        # Global configuration
        self.camera.background_color = "#ece6e2"
        Text.set_default(color="#5c5c5c")
        MathTex.set_default(color="#5c5c5c")
        
        self.parte_1_identidade_material()
        self.clean_up()
        
        self.parte_2_origem_quimica()
        self.clean_up()
        
        self.parte_3_balanca_perdas()
        self.clean_up()

        self.parte_3_5_permeabilidade_magnetica()
        self.clean_up()
        
        self.parte_4_propagacao_ondas()
        self.clean_up()
        
        self.parte_5_fechamento()
        self.clean_up()

    def clean_up(self):
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(0.5)

    def parte_1_identidade_material(self):
        # Título
        titulo = Text("A Batalha dos Meios", font_size=48).to_edge(UP)
        self.play(Write(titulo))
        self.wait()

        # Identidade do Material
        epsilon_sym = MathTex(r"\epsilon", color=BLUE, font_size=96)
        mu_sym = MathTex(r"\mu", color=RED, font_size=96)
        sigma_sym = MathTex(r"\sigma", color=GOLD_E, font_size=96) 
        
        # Position them
        group_syms = VGroup(epsilon_sym, mu_sym, sigma_sym).arrange(RIGHT, buff=2).shift(UP*0.5)
        
        epsilon_desc = Text("Armazena (C)", font_size=24, color=BLUE).next_to(epsilon_sym, DOWN)
        mu_desc = Text("Magnetiza (L)", font_size=24, color=RED).next_to(mu_sym, DOWN)
        sigma_desc = Text("Dissipa (R)", font_size=24, color=GOLD_E).next_to(sigma_sym, DOWN)
        
        self.play(
            FadeIn(epsilon_sym, shift=UP),
        )
        self.play(Write(epsilon_desc))
        
        self.play(
            FadeIn(mu_sym, shift=UP),
        )
        self.play(Write(mu_desc))

        self.play(
            FadeIn(sigma_sym, shift=UP),
        )
        self.play(Write(sigma_desc))
        
        self.wait(2)

    def parte_2_origem_quimica(self):
        t1 = Text("Dielétrico (Isolante)", font_size=32).move_to(LEFT*3.5 + UP*2.5)
        t2 = Text("Condutor (Metal)", font_size=32).move_to(RIGHT*3.5 + UP*2.5)
        
        self.play(Write(t1), Write(t2))
        
        # -- Lado Dieletrico (Esquerda) --
        dipoles = VGroup()
        for i in range(3):
            for j in range(3):
                oval = Ellipse(width=0.8, height=0.4, color=BLUE_D).set_fill(BLUE_A, opacity=0.5)
                # Sinais pretos para contraste dentro do oval azul claro
                plus = MathTex("+", font_size=16, color=BLACK).move_to(oval.get_right()*0.6)
                minus = MathTex("-", font_size=16, color=BLACK).move_to(oval.get_left()*0.6)
                dipole = VGroup(oval, plus, minus).move_to(LEFT*3.5 + (i-1)*1.2*UP + (j-1)*1.5*RIGHT)
                dipoles.add(dipole)
                
        self.play(Create(dipoles))
        
        # -- Lado Condutor (Direita) --
        atoms = VGroup()
        electrons = VGroup()
        
        for i in range(3):
            for j in range(3):
                atom = Circle(radius=0.2, color=GREY).set_fill(GREY_B, 0.5)
                atom.move_to(RIGHT*3.5 + (i-1)*1.2*UP + (j-1)*1.5*RIGHT)
                atoms.add(atom)
                
        # Elétrons livres
        for k in range(8):
            e = Dot(color=GOLD_E, radius=0.08)
            # Posição inicial aleatória na área direita
            e.move_to(RIGHT*3.5 + np.random.uniform(-1.5, 1.5)*RIGHT + np.random.uniform(-1.5, 1.5)*UP)
            electrons.add(e)
            
        self.play(Create(atoms), Create(electrons))
        
        t1_sub = Text("Energia Armazenada", font_size=24, color=BLUE).next_to(dipoles, DOWN, buff=0.5)
        t2_sub = Text("Energia Dissipada (Calor)", font_size=24, color=RED).next_to(atoms, DOWN, buff=0.5)
        
        self.play(Write(t1_sub), Write(t2_sub))

        # Adicionar vetor Campo Elétrico Externo
        e_field_tracker = ValueTracker(0) # Fase do campo
        
        # Vetor oscilante no centro
        def get_e_field_vector():
            val = np.sin(e_field_tracker.get_value())
            color = BLUE if val > 0 else RED
            return Arrow(
                start=ORIGIN, 
                end=UP * val * 2, 
                color=color, 
                buff=0,
                stroke_width=6
            ).move_to(ORIGIN)
            
        e_vec = always_redraw(get_e_field_vector)
        # Rótulo fixo à direita do centro para não pular com o tamanho da seta
        e_label = Text("Campo E Externo", font_size=20).next_to(ORIGIN, RIGHT, buff=0.4).shift(UP*0.5)
        
        self.play(FadeIn(e_vec), FadeIn(e_label))

        # Loop de animação
        # Executar por alguns ciclos
        
        steps = 20
        dt = (2*PI) / steps
        
        for _ in range(2 * steps): # 2 ciclos completos
            # Atualizar tracker
            e_field_tracker.increment_value(dt)
            current_phase = e_field_tracker.get_value()
            force = np.sin(current_phase)
            
            # Movimento dos elétrons com "Sparks" (colisões)
            electron_anims = []
            sparks = VGroup()
            
            for e in electrons:
                # Movimento aleatório + força do campo
                # Se campo pra cima (+), elétron (-) vai pra baixo
                drift = -force * 0.15 # Intensidade do drift
                
                new_pos = e.get_center() + np.array([
                    np.random.uniform(-0.1, 0.1), # Agitação térmica
                    drift + np.random.uniform(-0.05, 0.05), # Drift elétrico
                    0
                ])
                
                # Manter na caixa (Boundaries)
                center_x = 3.5
                if new_pos[0] > center_x + 1.5: new_pos[0] = center_x - 1.5
                if new_pos[0] < center_x - 1.5: new_pos[0] = center_x + 1.5
                if new_pos[1] > 1.5: new_pos[1] = -1.5
                if new_pos[1] < -1.5: new_pos[1] = 1.5
                
                electron_anims.append(e.animate.move_to(new_pos))
                
                # Chance de colisão e spark (apenas se velocidade for alta)
                if abs(drift) > 0.05 and np.random.random() > 0.90:
                    spark = Star(color=YELLOW, outer_radius=0.15, inner_radius=0.05).move_to(new_pos)
                    sparks.add(spark)

            # Dipolos giram
            rotation_step = (PI/4) * np.cos(current_phase) * dt # Derivada do sin é cos
            
            self.play(
                dipoles.animate.rotate(rotation_step),
                *electron_anims,
                run_time=0.1,
                rate_func=linear
            )
            
            # Mostrar sparks rapidinho
            if len(sparks) > 0:
                self.add(sparks)
                self.wait(0.05)
                self.remove(sparks)
            
        self.play(FadeOut(e_vec), FadeOut(e_label))
        self.wait()

    def parte_3_balanca_perdas(self):
        # A Tangente de Perdas como uma balança
        
        eq_tan = MathTex(
            r"\tan(\delta) = \frac{\sigma}{\omega \epsilon}",
            font_size=48
        ).to_edge(UP)
        
        meaning = Text("Condutividade vs Armazenamento", font_size=24).next_to(eq_tan, DOWN)
        
        self.play(Write(eq_tan))
        self.play(FadeIn(meaning))
        self.wait()
        
        # Desenho da balança
        triangle = Triangle().scale(0.5).set_fill(GREY, 1).to_edge(DOWN).shift(UP*1.5)
        pivot_point = triangle.get_top()
        beam = Line(LEFT*3.5, RIGHT*3.5, stroke_width=8, color="#5c5c5c").move_to(pivot_point)
        
        # Pratos
        plate_left = Line(LEFT*1, RIGHT*1, color="#5c5c5c").move_to(beam.get_left())
        plate_right = Line(LEFT*1, RIGHT*1, color="#5c5c5c").move_to(beam.get_right())

        # Strings segurando os pratos
        string_left = Line(beam.get_left(), plate_left.get_center(), color="#5c5c5c")
        string_right = Line(beam.get_right(), plate_right.get_center(), color="#5c5c5c")
        
        # Texto nos pratos
        # Esquerda: Sigma (Perdas)
        label_sigma = MathTex(r"\sigma", font_size=60, color=RED).next_to(plate_left, UP, buff=0.2)
        # Direita: Omega Epsilon (Armazenamento)
        label_omegaeps = MathTex(r"\omega \epsilon", font_size=60, color=BLUE).next_to(plate_right, UP, buff=0.2)
        
        group_balance = VGroup(triangle, beam, plate_left, plate_right, label_sigma, label_omegaeps)
        balance_arm = VGroup(beam, plate_left, plate_right, label_sigma, label_omegaeps, string_left, string_right)
        
        self.play(Create(triangle), Create(balance_arm))
        self.wait()
        
        # --- CASO 1: BOM DIELETRICO (Vidro) ---
        # Omega Epsilon >> Sigma (Pende para direita)
        
        t_case1 = Text("Bom Isolante (Vidro)", font_size=32, color=BLUE).next_to(meaning, DOWN, buff=1)
        
        self.play(Transform(meaning, t_case1))
        
        # Calcular rotação e offsets
        angle = -PI/8
        
        self.play(
            Rotate(balance_arm, angle, about_point=pivot_point),
            label_omegaeps.animate.scale(1.3),
            label_sigma.animate.scale(0.7),
        )
        self.wait(2)
        
        # --- CASO 2: BOM CONDUTOR (Cobre) ---
        # Sigma >> Omega Epsilon
        
        t_case2 = Text("Bom Condutor (Cobre)", font_size=32, color=RED).move_to(t_case1)
        
        # Reset rápido primeiro ou transform direto? Transform direto
        self.play(Transform(meaning, t_case2))
        
        self.play(
            Rotate(balance_arm, -2 * angle, about_point=pivot_point), # Voltar e ir para o outro lado
            label_omegaeps.animate.scale(0.7/1.3),
            label_sigma.animate.scale(1.3/0.7),
        )
        self.wait(2)

        # --- CASO 3: EFEITO DA FREQUÊNCIA ---
        # Voltar ao meio (Quase condutor)
        t_case3 = Text("Aumentando Frequência (ω sobe)", font_size=32, color=PURPLE).move_to(t_case1)
        self.play(Transform(meaning, t_case3))
        
        # Resetar para neutro primeiro
        self.play(
            Rotate(balance_arm, angle, about_point=pivot_point), # Volta para 0
            label_omegaeps.animate.scale(1/0.7),
            label_sigma.animate.scale(1/1.3),
        )
        self.wait(0.5)
        
        # Agora omega aumenta -> termo omega*epsilon aumenta -> balança pende para direita (Dielétrico)
        self.play(
            label_omegaeps.animate.scale(1.5).set_color(PURPLE),
            Rotate(balance_arm, angle, about_point=pivot_point), # Pende para direita (negativo)
            run_time=2
        )
        self.wait(2)


    def parte_3_5_permeabilidade_magnetica(self):
        # 1. A Constante "Invisível"
        mu_sym = MathTex(r"\mu", color=RED, font_size=96)
        t_title = Text("E o Magnetismo?", font_size=42, color="#5c5c5c").to_edge(UP)
        
        self.play(Write(t_title), FadeIn(mu_sym))
        self.wait()
        
        # Decomposição
        mu_eq = MathTex(r"\mu = \mu_r \cdot \mu_0", color=RED, font_size=64)
        self.play(Transform(mu_sym, mu_eq))
        self.wait()
        
        # Materiais Amagnéticos
        t_amag = Text("Materiais Amagnéticos (Água, Cobre, Ar)", font_size=28, color=BLUE).next_to(mu_eq, DOWN, buff=1)
        mu_r_val = MathTex(r"\mu_r \approx 1", color=BLUE).next_to(t_amag, DOWN)
        
        blocks = VGroup(*[Square(side_length=0.8, color=BLUE_A, fill_opacity=0.3) for _ in range(4)]).arrange(RIGHT, buff=0.5).next_to(mu_r_val, DOWN, buff=0.5)
        
        self.play(Write(t_amag), Write(mu_r_val), Create(blocks))
        # Fica cinza/transparente
        self.play(mu_sym.animate.set_color(GREY).set_opacity(0.3))
        self.wait(2)
        
        # Limpar para parte 2
        # Nova posição do título
        t_ferro = Text("Materiais Ferromagnéticos", font_size=32, color=RED).to_edge(UP)
        
        self.play(
            FadeOut(t_amag), FadeOut(mu_r_val), FadeOut(blocks), 
            FadeOut(t_title),
            # Mu volta a brilhar e vai para o canto superior esquerdo, abaixo da margem
            mu_sym.animate.set_color(RED).set_opacity(1).scale(1.2).to_corner(UL).shift(DOWN*0.5 + RIGHT*0.5)
        )
        
        # 2. O Mundo Ferromagnético
        self.play(Write(t_ferro))
        
        block_iron = Square(side_length=4, color=GREY, fill_opacity=0.2).move_to(DOWN*0.5)
        self.play(Create(block_iron))
        
        # Domínios
        domains = VGroup()
        arrows = []
        for i in range(5):
            for j in range(5):
                # Random direction
                angle = np.random.uniform(0, 2*PI)
                arrow = Arrow(ORIGIN, RIGHT*0.5, color=RED_B, buff=0).rotate(angle)
                arrow.move_to(block_iron.get_center() + (i-2)*0.7*RIGHT + (j-2)*0.7*UP)
                domains.add(arrow)
                arrows.append(arrow)
                
        self.play(Create(domains))
        
        lbl_domains = Text("Domínios Magnéticos", font_size=20, color=RED).next_to(block_iron, RIGHT).shift(UP)
        arrow_ptr = Arrow(lbl_domains.get_left(), block_iron.get_right(), color=RED)
        self.play(Write(lbl_domains), GrowArrow(arrow_ptr))
        
        # Campo Magnético Externo (Causa)
        h_field_val = ValueTracker(0) # 0=desligado, 1=cima, -1=baixo
        h_vector = always_redraw(lambda: Arrow(
            ORIGIN, UP * h_field_val.get_value() * 2, 
            color=BLUE, stroke_width=8
        ).next_to(block_iron, LEFT, buff=1))
        h_label = always_redraw(lambda: MathTex(r"\vec{H}", color=BLUE).next_to(h_vector, UP))
        
        self.play(FadeIn(h_vector), FadeIn(h_label))

        # Contador mu_r
        mu_counter = ValueTracker(1)
        mu_text = MathTex(r"\mu_r =", color=RED).next_to(block_iron, RIGHT).shift(DOWN*1.5)
        mu_num = always_redraw(lambda: DecimalNumber(mu_counter.get_value(), num_decimal_places=0).next_to(mu_text, RIGHT))
        
        self.play(Write(mu_text), Write(mu_num))
        self.play(mu_counter.animate.set_value(5000), run_time=3, rate_func=exponential_decay)
        self.wait()
        
        # 3. O Atrito Magnético (Histerese)
        self.play(FadeOut(lbl_domains), FadeOut(arrow_ptr), FadeOut(mu_text), FadeOut(mu_num))
        
        t_histerese = Text("Histerese: O Custo de Alinhar", font_size=32, color="#5c5c5c").to_edge(UP)
        self.play(Transform(t_ferro, t_histerese))
        
        # Loop de Histerese
        h_magnitude = 1.0
        for cycle in range(2):
            # 1. Campo Sobe (Causa)
            self.play(h_field_val.animate.set_value(h_magnitude), run_time=1)
            
            # 2. Domínios Alinham (Efeito)
            anims_up = []
            for arrow in arrows:
                anims_up.append(arrow.animate.set_color(YELLOW).rotate(
                    PI/2 - arrow.get_angle() + np.random.uniform(-0.1, 0.1)
                ))
            self.play(*anims_up, run_time=0.8)
            self.wait(0.2)
            
            # 3. Campo Desce (Inversão)
            self.play(h_field_val.animate.set_value(-h_magnitude), run_time=1)
            
            # 4. Flip Violento com Faíscas
            anims_down = []
            sparks = VGroup()
            for arrow in arrows:
                anims_down.append(arrow.animate.set_color(RED).rotate(PI))
                if np.random.random() > 0.6:
                    sparks.add(Star(color=YELLOW, outer_radius=0.12, inner_radius=0.04).move_to(arrow.get_center()))
            
            self.play(*anims_down, run_time=0.8)
            
            # 5. O Custo (Campo Encolhe devido às perdas)
            if len(sparks) > 0:
                self.add(sparks)
                h_magnitude *= 0.75 # Reduz 25% a cada flip
                self.play(h_field_val.animate.set_value(-h_magnitude), run_time=0.3)
                self.remove(sparks)
            
            self.wait(0.2)
            
        self.play(FadeOut(domains), FadeOut(block_iron), FadeOut(t_ferro), FadeOut(mu_sym), FadeOut(h_vector), FadeOut(h_label))
        
        # 4. O Freio Eletromagnético
        t_freio = Text("A Permeabilidade como Freio", font_size=32, color="#5c5c5c").to_edge(UP)
        self.play(Write(t_freio))
        
        # Quebramos a equação em 3 partes. O \mu será exatamente o índice [1]
        eq_v = MathTex(r"v = \frac{1}{\sqrt{", r"\mu", r" \epsilon}}", font_size=64, color="#5c5c5c").next_to(t_freio, DOWN, buff=0.5)
        self.play(Write(eq_v))
        
        # Agora você pode animar o índice 1 com total certeza de que é o \mu
        self.play(eq_v[1].animate.scale(2).set_color(RED))
        
        # Corrida
        start_x = -5
        end_x = 5
        
        # Pista 1 (Plastico)
        y1 = -0.5
        line1 = Line(LEFT*6 + UP*y1, RIGHT*6 + UP*y1, color="#5c5c5c")
        dot1 = Dot(color=BLUE).move_to(RIGHT*start_x + UP*y1)
        label1 = Tex(r"Plástico ($\mu$ pequeno)", font_size=24, color=BLUE).next_to(line1, UP)
        wave1 = TracedPath(dot1.get_center, stroke_color=BLUE, stroke_width=4)
        
        # Pista 2 (Ferro)
        y2 = -2.5
        line2 = Line(LEFT*6 + UP*y2, RIGHT*6 + UP*y2, color="#5c5c5c")
        dot2 = Dot(color=RED).move_to(RIGHT*start_x + UP*y2)
        label2 = Tex(r"Ferro ($\mu$ gigante $\to$ v baixo)", font_size=24, color=RED).next_to(line2, UP)
        wave2 = TracedPath(dot2.get_center, stroke_color=RED, stroke_width=4)
        
        self.add(wave1, wave2)
        self.play(
            Create(line1), Create(dot1), Write(label1),
            Create(line2), Create(dot2), Write(label2),
        )
        
        # Animar corrida com oscilação
        t_tracker = ValueTracker(0)
        
        def update_dot1(mob):
            t = t_tracker.get_value()
            v = 2.5
            x = start_x + v * t
            if x > 6: x = 6
            mob.move_to(np.array([x, y1 + 0.5*np.sin(5*x), 0]))
            
        def update_dot2(mob):
            t = t_tracker.get_value()
            # Muito lento no Ferro
            v = 0.4 
            x = start_x + v * t
            # lambda_compressed = v / f. Como v diminui muito, lambda encolhe (picos próximos)
            # 22*x cria uma oscilação visualmente muito mais densa (espremida)
            mob.move_to(np.array([x, y2 + 0.5*np.sin(22*x), 0])) 
            
        dot1.add_updater(update_dot1)
        dot2.add_updater(update_dot2)
        
        self.play(t_tracker.animate.set_value(4.8), run_time=5, rate_func=linear)
        
        dot1.remove_updater(update_dot1)
        dot2.remove_updater(update_dot2)
        
        self.wait(2)


    def parte_4_propagacao_ondas(self):
        # Efeito Skin e Atenuação
        
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": "#5c5c5c", "include_tip": False}
        ).shift(DOWN*0.5)
        
        axis_label = axes.get_x_axis_label(Text("Distância (z)", font_size=20, color="#5c5c5c"))
        
        title = Text("Propagação da Onda E(z,t) e H(z,t)", font_size=32).to_edge(UP)
        
        self.play(Create(axes), Write(axis_label), Write(title))
        
        # Variáveis
        alpha = ValueTracker(0.0)
        phase = ValueTracker(0.0)
        
        # A onda se propaga para direita: cos(kz - wt)
        # Vamos usar um k fixo e variar t (phase)
        k = 2.0
        w = 5.0
        
        # Updater para tempo contínuo
        def update_phase(mob, dt):
            mob.increment_value(w * dt)
            
        phase.add_updater(update_phase)
        self.add(phase)
        
        # Onda
        def get_E_wave():
            return axes.plot(
                lambda z: np.exp(-alpha.get_value() * z) * np.cos(k * z - phase.get_value()),
                color=RED,
                x_range=[0, 10]
            )

        E_wave = always_redraw(get_E_wave)
        
        # Onda Magnética (Azul - menor amplitude, em fase)
        def get_H_wave():
             return axes.plot(
                lambda z: 0.6 * np.exp(-alpha.get_value() * z) * np.cos(k * z - phase.get_value()),
                color=BLUE,
                x_range=[0, 10]
            )
        
        H_wave = always_redraw(get_H_wave)
        
        self.add(E_wave, H_wave) 
        
        # Envelope de decaimento (visual guide)
        def get_envelope():
            if alpha.get_value() < 0.05:
                return VGroup()
            
            # Pulsar opacidade com a onda (abs(cos) ou similar)
            pulse = 0.4 + 0.3 * np.abs(np.cos(phase.get_value()))

            return DashedVMobject(axes.plot(
                lambda z: np.exp(-alpha.get_value() * z),
                color=GREY,
                x_range=[0, 10]
            )).set_stroke(opacity=pulse)
        
        envelope = always_redraw(get_envelope)
        self.add(envelope)

        # Rótulos
        label_E = MathTex(r"\vec{E}", color=RED).move_to(axes.c2p(0.5, 1.2))
        label_H = MathTex(r"\vec{H}", color=BLUE).move_to(axes.c2p(0.5, 0.4))
        self.add(label_E, label_H)

        # 1. Meio Sem Perdas
        label_medium = Text("Ar / Vácuo (Sem Perdas)", font_size=28, color=BLUE).next_to(title, DOWN)
        self.play(Write(label_medium))
        self.wait(4)
        
        # 2. Meio com Perdas (Água do Mar)
        self.play(FadeOut(label_medium))
        label_medium = Text("Água do Mar (Atenuação)", font_size=28, color=ORANGE).next_to(title, DOWN)
        self.play(Write(label_medium))
        
        self.play(alpha.animate.set_value(0.25), run_time=3)
        self.wait(2)
        
        # 3. Bom Condutor (Efeito Skin)
        self.play(FadeOut(label_medium))
        label_medium = Text("Metal (Efeito Skin - Alta Atenuação)", font_size=28, color=RED).next_to(title, DOWN)
        self.play(Write(label_medium))
        
        self.play(alpha.animate.set_value(1.2), run_time=2)
        
        # Mostrar Profundidade Pelicular
        # Delta = 1/alpha
        current_alpha = alpha.get_value()
        delta = 1.0 / current_alpha
        
        line_skin = DashedLine(
            start=axes.c2p(delta, -1.5),
            end=axes.c2p(delta, 1.5),
            color="#5c5c5c"
        )
        label_skin = MathTex(r"\delta", color="#5c5c5c").next_to(line_skin, UP)
        annot_skin = Text("Profundidade Pelicular", font_size=20, color=GREY).next_to(line_skin, RIGHT, buff=0.1).shift(UP*1)
        
        self.play(Create(line_skin), Write(label_skin), FadeIn(annot_skin))
        self.wait(4)
        
        phase.remove_updater(update_phase) # Stop updater cleanly

    def parte_5_fechamento(self):
        t1 = Text("Resumo:", font_size=36, color="#5c5c5c").to_edge(UP)
        summary = VGroup(
            Text("1. Dielétricos armazenam energia (Dipolos)", font_size=24),
            Text("2. Condutores dissipam energia (Elétrons Livres)", font_size=24),
            Text("3. Tangente de Perdas mede essa disputa", font_size=24),
            Text("4. Ondas penetram pouco em condutores (Skin Effect)", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(t1, DOWN, buff=1)
        
        self.play(Write(t1))

        
        for item in summary:
            self.play(FadeIn(item, shift=RIGHT))
            self.wait(0.5)
            
        self.wait(2)

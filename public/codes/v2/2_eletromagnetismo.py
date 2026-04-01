from manim import *
import numpy as np
import warnings

# Suppress warnings from manim_voiceover about pkg_resources
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

class EletromagnetismoScene(Scene):
    def construct(self):
        self.parte_1_ima_estrutura_interna()
        self.clean_up()
        
        self.parte_2_ponte_movimento_logica()
        self.clean_up()
        
        self.parte_3_inducao_detalhada()
        self.clean_up()
        
        self.parte_4_ampere_bussolas()
        self.clean_up()
        
        self.parte_5_equacoes_maxwell()
        self.wait(1)

    def clean_up(self):
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.5)

    def create_atomic_dipole(self, point, color=WHITE):
        # A small arrow representing an atomic magnetic moment
        arrow = Arrow(start=LEFT*0.15, end=RIGHT*0.15, color=color, buff=0, stroke_width=2, tip_length=0.1)
        return arrow.move_to(point)

    def create_magnet_with_dipoles(self, width=3, height=1):
        # Create a bar magnet visually
        magnet_group = VGroup()
        
        north = Rectangle(width=width/2, height=height, color=RED, fill_opacity=0.3).shift(LEFT * width/4)
        south = Rectangle(width=width/2, height=height, color=BLUE, fill_opacity=0.3).shift(RIGHT * width/4)
        
        # Add atomic dipoles inside
        dipoles = VGroup()
        rows = int(height * 4)
        cols = int(width * 4)
        
        for i in range(rows):
            for j in range(cols):
                # Calculate position inside
                x = -width/2 + (j + 0.5) * (width/cols)
                y = -height/2 + (i + 0.5) * (height/rows)
                # Create arrow pointing N to S (Left? No, Magnet N is Left usually implies field OUT of N)
                # Let's Standardize: N on LEFT, S on RIGHT. Field Lines go OUT of N (Left) and INTO S (Right).
                # Inside magnet, B field goes S to N (Right to Left).
                # Atomic moments point S to N.
                dipole = self.create_atomic_dipole(np.array([x, y, 0]), color=YELLOW)
                dipole.rotate(PI) # Point Left
                dipoles.add(dipole)
                
        magnet_group.add(north, south, dipoles)
        return magnet_group

    def parte_1_ima_estrutura_interna(self):
        title = Tex("1. O Ímã: Por que não existem Monopolos?", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 1. Structure
        magnet = self.create_magnet_with_dipoles()
        magnet.shift(DOWN * 0.5)
        self.play(FadeIn(magnet))
        
        text_structure = Tex("Cada átomo é um micro-ímã alinhado", font_size=24).next_to(magnet, DOWN)
        self.play(Write(text_structure))
        self.wait(2)
        
        # 2. The Cut
        saw = Line(UP*1.2, DOWN*1.2, color=WHITE, stroke_width=4).move_to(magnet.get_center())
        self.play(Create(saw))
        self.play(saw.animate.shift(DOWN*0.5), run_time=0.5)
        self.play(FadeOut(saw))
        
        # Split behavior
        # Recreate smaller magnets to simulate split
        m1 = self.create_magnet_with_dipoles(width=1.4, height=1).shift(LEFT*1.5 + DOWN*0.5)
        m2 = self.create_magnet_with_dipoles(width=1.4, height=1).shift(RIGHT*1.5 + DOWN*0.5)
        
        self.play(
            FadeOut(magnet),
            FadeIn(m1), FadeIn(m2),
            FadeOut(text_structure)
        )
        
        text_cut = Tex("Cortar apenas separa as fileiras de átomos.", font_size=24, color=YELLOW).next_to(m1, DOWN).shift(RIGHT*1.5)
        self.play(Write(text_cut))
        self.wait(2)
        
        text_conclusion = Tex("O alinhamento continua: Novos Polos surgem instantaneamente!", font_size=24).next_to(text_cut, DOWN)
        self.play(Write(text_conclusion))
        self.wait(2)
        
        # 3. Formula
        formula = MathTex(r"\nabla \cdot \vec{b} = 0", font_size=40).to_edge(DOWN).shift(UP*1)
        self.play(Write(formula))
        self.wait(2)

    def parte_2_ponte_movimento_logica(self):
        title = Tex("2. A Força de Lorentz: Movimento é Chave", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Setup
        q = Dot(color=RED, radius=0.2).move_to(LEFT * 4 + DOWN * 0.5)
        label_q = MathTex("q").next_to(q, UP)
        
        # B Field (Blue Arrows UP)
        b_field = VGroup()
        for x in range(-6, 7, 1):
            for y in range(-2, 3, 1):
                arrow = Arrow(start=DOWN*0.2, end=UP*0.2, color=BLUE, stroke_width=2, tip_length=0.1).move_to([x, y - 0.5, 0])
                b_field.add(arrow)
        
        self.play(FadeIn(b_field), FadeIn(q), FadeIn(label_q))
        
        # Case 1: v = 0
        case1 = Tex("1. Carga Parada ($v=0$): Sem Força", color=GRAY).to_edge(UP, buff=1.2)
        self.play(Write(case1))
        self.wait(1)
        self.play(FadeOut(case1))

        # Case 2: v || B
        case2 = Tex("2. Movimento Paralelo ($v \parallel B$): Sem Força", color=GRAY).to_edge(UP, buff=1.2)
        vec_v_par = Arrow(q.get_center(), q.get_center() + UP * 1.5, color=GREEN, buff=0)
        
        self.play(Write(case2))
        self.play(GrowArrow(vec_v_par))
        self.play(q.animate.shift(UP * 2), vec_v_par.animate.shift(UP * 2), run_time=1.5)
        self.play(FadeOut(vec_v_par), FadeOut(case2))
        self.play(q.animate.move_to(LEFT * 4)) # Reset

        # Case 3: v perpendicular B
        case3 = Tex(r"3. Movimento Perpendicular: Força Máxima!", color=YELLOW).to_edge(UP, buff=1.2)
        self.play(Write(case3))
        
        vec_v = Arrow(q.get_center(), q.get_center() + RIGHT * 1.5, color=GREEN, buff=0)
        label_v = MathTex(r"\vec{v}", color=GREEN).next_to(vec_v, DOWN)
        
        self.play(GrowArrow(vec_v), Write(label_v))
        self.wait(0.5)
        
        # Show Cross Product Rule visually
        # v right, B up -> F out of screen (Z+)
        # Let's create a 3D-ish marker
        cross_prod = VGroup(
            Arrow(ORIGIN, RIGHT, color=GREEN), # v
            Arrow(ORIGIN, UP, color=BLUE), # B
            Dot(ORIGIN, color=YELLOW).scale(1.5), # F (coming out)
            Circle(radius=0.2, color=YELLOW) # Symbol for out of page
        ).next_to(q, UP, buff=1)
        
        rule_label = Tex("Regra da Mão Direita", font_size=20).next_to(cross_prod, UP)
        
        # Adjust position to not hide behind title
        cross_prod_group = VGroup(cross_prod, rule_label).to_edge(RIGHT, buff=1).shift(UP*1.5)
        
        self.play(FadeIn(cross_prod_group))
        self.wait(1)
        
        # Result: Circular Motion
        # Retcon B field to INTO PAGE so F is UP for simpler 2D curving
        self.play(FadeOut(b_field), FadeOut(cross_prod_group))
        b_field_in = VGroup()
        for x in range(-6, 7, 2):
            for y in range(-3, 4, 2):
                b_field_in.add(MathTex("\\times", color=BLUE).move_to([x, y, 0]))
        
        self.play(FadeIn(b_field_in))
        
        # New Rule: v Right, B In -> F Up
        vec_f = Arrow(q.get_center(), q.get_center() + UP * 1.5, color=YELLOW, buff=0)
        label_f = MathTex(r"\vec{F}", color=YELLOW).next_to(vec_f, LEFT)
        self.play(GrowArrow(vec_f), Write(label_f))
        
        path = Arc(radius=2, angle=PI, arc_center=q.get_center() + UP*2)
        
        self.play(
            MoveAlongPath(q, path),
            MoveAlongPath(label_q, path),
            FadeOut(vec_v), FadeOut(label_v), FadeOut(vec_f), FadeOut(label_f),
            run_time=2
        )
        
        formula = MathTex(r"\vec{F} = q(\vec{v} \times \vec{b})").to_edge(DOWN, buff=0.5).set_background_stroke(color=BLACK, width=5, opacity=1)
        self.play(Write(formula))
        self.wait(1)

    def parte_3_inducao_detalhada(self):
        title = Tex("3. Indução: O Corte das Linhas de Campo", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Wire Loop
        loop_radius = 1.5
        loop = Circle(radius=loop_radius, color=ORANGE).shift(RIGHT * 2 + DOWN * 0.5)
        loop_center = loop.get_center()
        self.play(Create(loop))
        
        # Magnet with visual field lines attached
        magnet = self.create_magnet_with_dipoles(width=2, height=0.6).shift(LEFT * 4 + DOWN * 0.5)
        
        # Create a group of lines that move with the magnet
        # These represent the B field projecting forward
        lines = VGroup()
        for i in np.linspace(-0.5, 0.5, 5):
            l = Line(start=magnet.get_right() + UP*i, end=magnet.get_right() + RIGHT*6 + UP*i, color=BLUE, stroke_opacity=0.5)
            lines.add(l)
            
        magnet_system = VGroup(magnet, lines)
        self.play(FadeIn(magnet_system))
        
        explanation = Tex("O segredo é a variação (corte) do fluxo", font_size=24).to_edge(DOWN)
        self.play(Write(explanation))

        # Electrons in the wire
        electrons = VGroup()
        num_electrons = 12
        for i in range(num_electrons):
            angle = 2*PI * i / num_electrons
            pos = loop_center + np.array([loop_radius*np.cos(angle), loop_radius*np.sin(angle), 0])
            e = Dot(color=YELLOW, radius=0.08).move_to(pos)
            electrons.add(e)
            
        self.play(FadeIn(electrons))

        # 1. Move Closer (Cutting lines)
        # Animate electrons rotating around the loop center
        self.play(
            magnet_system.animate.shift(RIGHT * 3),
            Rotate(electrons, angle=PI, about_point=loop_center), # Current flow
            loop.animate.set_stroke(color=YELLOW, width=6),
            run_time=2
        )
        
        # 2. Stop (No cutting)
        self.play(loop.animate.set_stroke(color=ORANGE, width=4)) # Electrons stop (no rotation)
        
        # 3. Move Away (Reverse cutting)
        self.play(
            magnet_system.animate.shift(LEFT * 3),
            Rotate(electrons, angle=-PI, about_point=loop_center), # Reverse flow
            loop.animate.set_stroke(color=YELLOW, width=6),
            run_time=2
        )
        
        self.play(loop.animate.set_stroke(color=ORANGE, width=4))
        
        final_eq = MathTex(r"fem = -\frac{\Delta \Phi_B}{\Delta t}").next_to(explanation, UP)
        self.play(Write(final_eq))
        self.wait(1)

    def parte_4_ampere_bussolas(self):
        title = Tex("4. Lei de Ampère: A Construção do Campo", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        wire = Line(DOWN*3, UP*2, color=WHITE, stroke_width=4).shift(DOWN*0.5)
        self.play(Create(wire))
        
        # Show "Compasses" (Little arrows)
        compasses = VGroup()
        angles = np.linspace(0, 2*PI, 12, endpoint=False)
        radius = 2
        
        for angle in angles:
            # Initially random
            rand_angle = np.random.uniform(0, 2*PI)
            arrow = Arrow(LEFT*0.3, RIGHT*0.3, color=RED, buff=0).rotate(rand_angle)
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle) - 0.5, 0])
            arrow.move_to(pos)
            compasses.add(arrow)
            
        self.play(FadeIn(compasses))
        
        step1 = Tex("Sem corrente: Bússolas aleatórias", font_size=24).to_edge(UP, buff=1.2)
        self.play(Write(step1))
        self.wait(1)
        
        # Turn on current
        electrons = VGroup(*[Dot(color=YELLOW).move_to(DOWN*3 + UP*i*0.5) for i in range(15)])
        self.play(FadeIn(electrons))
        
        step2 = Tex("Com corrente ($i$): Alinhamento Circular", font_size=24, color=YELLOW).to_edge(UP, buff=1.2)
        
        # Animate alignment
        anims = []
        for i, angle in enumerate(angles):
            # Target angle: tangent to circle (concentric)
            # Tangent at theta is theta + 90 deg (CCW)
            target_angle = angle + PI/2
            # Calculate rotation needed
            current_angle = compasses[i].get_angle()
            rotation = target_angle - current_angle
            anims.append(Rotate(compasses[i], angle=rotation))

        self.play(
            electrons.animate.shift(UP*3),
            Transform(step1, step2),
            *anims,
            run_time=2
        )
        
        # Reveal Field Lines
        field_circle = Circle(radius=2, color=BLUE, stroke_width=2).move_to(DOWN*0.5).set_opacity(0)
        self.play(Create(field_circle), field_circle.animate.set_opacity(1))
        
        # Add arrow heads on circle
        heads = VGroup() 
        for i in range(4):
            # Using simple triangles as arrow heads
            h = Triangle(color=BLUE, fill_opacity=1).scale(0.1)
            # Rotate to tangent
            # Points at 0, 90, 180, 270 (0, PI/2, PI, 3PI/2)
            # Tangents: 90, 180, 270, 0
            ang = i * PI/2
            h.rotate(ang + PI/2)
            h.move_to(field_circle.point_from_proportion(i/4))
            heads.add(h)
            
        self.play(FadeIn(heads))
        
        final_eq = MathTex(r"\oint \vec{h} \cdot dl = i_{total}").to_edge(DOWN, buff=0.5).set_background_stroke(color=BLACK, width=5, opacity=1)
        self.play(Write(final_eq))
        self.wait(2)

    def parte_5_equacoes_maxwell(self):
        # Grand Summary
        title = Tex("5. O Mapa do Eletromagnetismo (Maxwell)", font_size=38).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Position equations
        eq1 = MathTex(r"\nabla \cdot \vec{d} = \rho")
        eq2 = MathTex(r"\nabla \cdot \vec{b} = 0")
        eq3 = MathTex(r"\nabla \times \vec{e} = -\frac{\partial \vec{b}}{\partial t}")
        eq4 = MathTex(r"\nabla \times \vec{h} = \vec{j} + \frac{\partial \vec{d}}{\partial t}")
        
        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.6).shift(LEFT*2 + DOWN*0.3)
        
        # Explanations
        expls = [
            "Cargas Elétricas (Fontes)",
            "Sem Monopolos (Dipolos)",
            "Indução (Variação B cria E)",
            "Ampère (Corrente cria B)"
        ]
        
        expl_group = VGroup()

        for i in range(4):
            label = Tex(expls[i], color=YELLOW, font_size=28).next_to(eqs[i], RIGHT, buff=0.5)
            self.play(Write(eqs[i]), FadeIn(label))
            expl_group.add(label)
            self.wait(0.5)
            
        self.wait(3)

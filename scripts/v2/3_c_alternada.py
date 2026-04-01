from manim import *
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

class CorrenteAlternadaScene(Scene):
    def construct(self):
        self.parte_1_continuidade()
        self.clean_up()
        
        self.parte_2_ampere_paradoxo()
        self.clean_up()
        
        self.parte_3_solucao_maxwell()
        self.clean_up()
        
        self.parte_4_resolucao_exercicio()
        self.wait(1)

    def clean_up(self):
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.5)

    def parte_1_continuidade(self):
        title = Tex("1. A Equação da Continuidade: Carga não some", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Visualizing a volume (circle in 2D) - Moved UP to clear space for equations
        volume = Circle(radius=1.8, color=BLUE, fill_opacity=0.2).move_to(RIGHT * 1 + UP * 0.5)
        label_vol = MathTex(r"\rho").move_to(volume)
        
        self.play(DrawBorderThenFill(volume), Write(label_vol))
        
        # Charges entering
        charges = VGroup()
        arrows = VGroup()
        for i in range(8):
            angle = i * (2*PI/8)
            # Update center to match volume
            center = volume.get_center()
            start = center + np.array([2.8*np.cos(angle), 2.8*np.sin(angle), 0])
            end = center + np.array([1.9*np.cos(angle), 1.9*np.sin(angle), 0])
            arrow = Arrow(start, end, color=YELLOW)
            arrows.add(arrow)
            
        self.play(FadeIn(arrows))
        
        # Text on Left Column
        text = Tex("Se entra fluxo de carga...", font_size=28).to_corner(UL).shift(DOWN*1 + RIGHT*0.5)
        self.play(Write(text))
        
        # Density increases
        self.play(
            volume.animate.set_fill(opacity=0.6),
            label_vol.animate.scale(1.5),
            run_time=2
        )
        
        text2 = Tex("...a densidade interna aumenta.", font_size=28).next_to(text, DOWN)
        self.play(Write(text2))
        
        # Clean up texts before establishing the equation
        self.play(FadeOut(text), FadeOut(text2), FadeOut(arrows))

        # Equation
        # Position lower (buff=1.0) to ensure separation
        eq = MathTex(r"\nabla \cdot \vec{j} = -\frac{\partial \rho}{\partial t}", font_size=42).to_edge(DOWN, buff=1.0)
        self.play(Write(eq))
        
        explanation = Tex("O fluxo que sai (div) é igual à perda de densidade", font_size=24, color=GRAY).next_to(eq, UP, buff=0.2)
        self.play(FadeIn(explanation))
        self.wait(2)

    def parte_2_ampere_paradoxo(self):
        title = Tex("2. O Paradoxo do Capacitor", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))
        
        # Draw Circuit
        # Simplified Square Circuit: AC Source (Left), Capacitor (Right)
        
        # Coordinates
        LEFT_X = -3
        RIGHT_X = 3
        TOP_Y = 1.0
        BOT_Y = -2.0
        
        # Source
        source = Circle(radius=0.5, color=YELLOW).move_to([LEFT_X, (TOP_Y+BOT_Y)/2, 0])
        label_ac = MathTex(r"\sim").move_to(source)
        
        # Capacitor
        plate_top = Line([RIGHT_X-0.5, (TOP_Y+BOT_Y)/2 + 0.3, 0], [RIGHT_X+0.5, (TOP_Y+BOT_Y)/2 + 0.3, 0], color=BLUE, stroke_width=5)
        plate_bot = Line([RIGHT_X-0.5, (TOP_Y+BOT_Y)/2 - 0.3, 0], [RIGHT_X+0.5, (TOP_Y+BOT_Y)/2 - 0.3, 0], color=BLUE, stroke_width=5)
        
        # Wires
        wires = VGroup(
            Line([LEFT_X, TOP_Y, 0], [RIGHT_X, TOP_Y, 0]), # Top Horizontal
            Line([LEFT_X, BOT_Y, 0], [RIGHT_X, BOT_Y, 0]), # Bottom Horizontal
            Line([LEFT_X, TOP_Y, 0], source.get_top()), # Source Top
            Line([LEFT_X, BOT_Y, 0], source.get_bottom()), # Source Bot
            Line([RIGHT_X, TOP_Y, 0], plate_top.get_center() + UP*0.0), # Cap Top (connecting to plate center?? No, to wire above)
            # Actually standard schematic: wire goes to center of plate
            Line([RIGHT_X, TOP_Y, 0], [RIGHT_X, (TOP_Y+BOT_Y)/2 + 0.3, 0]), 
            Line([RIGHT_X, (TOP_Y+BOT_Y)/2 - 0.3, 0], [RIGHT_X, BOT_Y, 0])
        ).set_color(WHITE)
        
        circuit = VGroup(source, label_ac, plate_top, plate_bot, wires)
        self.play(Create(circuit))
        
        # Ampere Loop (Gamma) on Top Wire
        mid_wire = [0, TOP_Y, 0]
        loop = Ellipse(width=0.6, height=1.2, color=GREEN).rotate(PI/2).move_to(mid_wire)
        label_loop = Tex(r"Loop $\Gamma$", color=GREEN, font_size=24).next_to(loop, UP, buff=0.2)
        
        self.play(Create(loop), Write(label_loop))
        
        # Surface 1: Flat (cutting the wire)
        surf1 = loop.copy().set_fill(GREEN, opacity=0.3)
        label_s1 = Tex("S1: Corta o fio", color=GREEN, font_size=24).next_to(loop, DOWN, buff=0.4)
        
        current_arrow = Arrow(LEFT, RIGHT, color=YELLOW, buff=0).scale(0.5).move_to(mid_wire)
        # Position label ABOVE the loop clearly, not to the side where it might be clipped or hidden
        label_i = MathTex("i=I_{enc}", font_size=24, color=YELLOW).move_to(mid_wire).shift(UP*1.5)
        label_i.set_z_index(10)
        
        # Add surf1 first, then arrow and label on top
        self.play(FadeIn(surf1), Write(label_s1))
        self.play(FadeIn(current_arrow), Write(label_i))
        
        check = Tex(r"$\nabla \times \vec{h} \neq 0$", color=GREEN, font_size=32).to_corner(UL).shift(DOWN*1)
        self.play(Write(check))
        self.wait(2)
        
        # Surface 2: Balloon (passing through capacitor gap)
        # Clear S1 stuff to avoid clutter
        self.play(
            FadeOut(surf1), FadeOut(label_s1), 
            FadeOut(current_arrow), FadeOut(label_i),
            FadeOut(check)
        )
        
        label_s2 = Tex("S2: Passa no vão", color=RED, font_size=24).next_to(loop, DOWN, buff=0.2)
        
        # Visual balloon path
        p_start = loop.get_bottom() # approx
        p_end = [(RIGHT_X), (TOP_Y+BOT_Y)/2, 0] # Gap center
        
        # Dashed line representing the surface stretching
        balloon_line = DashedLine(p_start, p_end, color=RED)
        balloon_bulb = Circle(radius=0.3, color=RED, fill_opacity=0.3).move_to(p_end)
        
        self.play(Create(balloon_line), FadeIn(balloon_bulb), Write(label_s2))
        
        cross = Tex(r"$I_{enc} = 0 \implies \nabla \times \vec{h} = 0?$", color=RED, font_size=32).to_corner(UL).shift(DOWN*1)
        self.play(Write(cross))
        self.wait(2)
        
        paradox = Tex(r"Paradoxo! Resultados diferentes para o mesmo loop.", color=RED, font_size=32).to_edge(DOWN)
        self.play(Write(paradox))
        self.wait(3)

    def parte_3_solucao_maxwell(self):
        title = Tex("3. A Correção de Maxwell: Corrente de Deslocamento", font_size=32).to_edge(UP, buff=0.2)
        self.play(Write(title))

        # Capacitor mechanics
        plate_top = Line(LEFT*2, RIGHT*2, color=BLUE, stroke_width=5).shift(UP*1)
        plate_bot = Line(LEFT*2, RIGHT*2, color=BLUE, stroke_width=5).shift(DOWN*1)
        wire_top = Line(UP*3, UP*1, color=WHITE)
        wire_bot = Line(DOWN*3, DOWN*1, color=WHITE)
        
        plates = VGroup(plate_top, plate_bot, wire_top, wire_bot).shift(DOWN*0.5)
        self.play(Create(plates))
        
        # Oscillating Field Animation
        field_arrows = VGroup()
        for x in np.linspace(-1.5, 1.5, 6):
            arrow = Arrow(UP*0.8, DOWN*0.8, color=YELLOW, buff=0).move_to([x, -0.5, 0])
            field_arrows.add(arrow)
            
        # Label specifically positioned to not hit the future equation
        field_label = MathTex(r"\vec{E}(t)", color=YELLOW, font_size=32).next_to(plate_top, UP, buff=0.1).shift(RIGHT*2)
        
        self.play(FadeIn(field_arrows), FadeIn(field_label))
        
        t = ValueTracker(0)
        def update_field(mob):
            val = np.cos(t.get_value())
            mob.submobjects = []
            direction = DOWN if val > 0 else UP
            mag = abs(val)
            color = YELLOW if val > 0 else ORANGE
            if mag < 0.1: return 
            for x in np.linspace(-1.5, 1.5, 6):
                arr = Arrow(ORIGIN, direction * mag * 1.5, color=color, buff=0).move_to([x, -0.5, 0])
                mob.add(arr)
                
        field_arrows.add_updater(update_field)
        
        expl = Tex("Campo Variável gera Corrente!", font_size=28, color=YELLOW).to_corner(UL).shift(DOWN*0.5)
        self.play(Write(expl))
        
        self.play(t.animate.set_value(2*PI), run_time=4, rate_func=linear)
        field_arrows.remove_updater(update_field)
        
        # CLEAR FIRST before showing equation
        self.play(FadeOut(field_label), FadeOut(expl))

        # Introduce term
        # Position it explicitly relative to plates to avoid hitting arrows if they persist
        term = MathTex(r"\vec{j_d} = \epsilon \frac{\partial \vec{e}}{\partial t}", color=YELLOW, font_size=36).next_to(plates, RIGHT, buff=1.0)
        self.play(Write(term))
        
        # Now clear everything central to make room for final equation
        self.play(FadeOut(field_arrows), FadeOut(term), FadeOut(plates))
        
        final_eq = MathTex(r"\nabla \times \vec{h} = \vec{j} + \epsilon \frac{\partial \vec{e}}{\partial t}", font_size=40).move_to(ORIGIN)
        self.play(Write(final_eq))
        self.wait(2)

    def parte_4_resolucao_exercicio(self):
        title = Tex("4. A Prova Matemática: $i = i_d$", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Split screen
        line = Line(UP*2, DOWN*2, color=GRAY).shift(DOWN*0.5)
        self.play(Create(line))
        
        # Coordinates for cleaner layout
        LEFT_X = -3.5
        RIGHT_X = 3.5
        # Start higher to fit everything
        START_Y = 2.0
        STEP = 0.8  # Consistent step
        
        # Left Side
        header_l = Tex("Condução (Fio)", color=BLUE, font_size=32).move_to([LEFT_X, START_Y, 0])
        eq_q = MathTex(r"q = C v_0 \cos(wt)", font_size=28).move_to([LEFT_X, START_Y - STEP, 0])
        eq_i = MathTex(r"i = \frac{dq}{dt}", font_size=28).move_to([LEFT_X, START_Y - 2*STEP, 0])
        result_i = MathTex(r"i = - C v_0 w \sin(wt)", font_size=30, color=BLUE).move_to([LEFT_X, START_Y - 3*STEP, 0])
        
        # Right Side
        header_r = Tex("Deslocamento (Vão)", color=YELLOW, font_size=32).move_to([RIGHT_X, START_Y, 0])
        eq_e = MathTex(r"E = \frac{v_0}{d} \cos(wt)", font_size=28).move_to([RIGHT_X, START_Y - STEP, 0])
        eq_jd_def = MathTex(r"j_d = \epsilon \frac{\partial E}{\partial t}", font_size=28).move_to([RIGHT_X, START_Y - 2*STEP, 0])
        
        # Combine intermediate steps to save space
        step1 = MathTex(r"j_d = -\frac{\epsilon v_0 w}{d} \sin(wt)", font_size=26).move_to([RIGHT_X, START_Y - 3*STEP, 0])
        
        # Final result aligned with Left Final Result visually, but maybe lower?
        # Let's put the final i_d slightly lower
        result_id = MathTex(r"i_d = - \frac{\epsilon S}{d} v_0 w \sin(wt)", font_size=30, color=YELLOW).move_to([RIGHT_X, START_Y - 4*STEP, 0])

        
        self.play(Write(header_l), Write(header_r))
        self.play(Write(eq_q), Write(eq_e))
        self.play(Write(eq_i), Write(eq_jd_def))
        self.play(Write(result_i), Write(step1))
        self.play(Write(result_id))
        
        # Conclusion
        # Clear middle line to not obstruct arrow
        self.play(FadeOut(line))
        
        match_arrow = Arrow(result_i.get_right(), result_id.get_left(), color=GREEN, buff=0.1)
        conclusion = MathTex(r"C = \frac{\epsilon S}{d} \implies i = i_d", color=GREEN, font_size=36).to_edge(DOWN, buff=0.2)
        
        self.play(GrowArrow(match_arrow))
        self.play(Write(conclusion))
        self.wait(3)

from manim import *
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

class GeracaoOndaScene(Scene):
    def construct(self):
        self.parte_1_origem()
        self.clean_up()
        
        self.parte_2_mecanica()
        self.clean_up()
        
        self.parte_3_pwm()
        self.clean_up()

        self.parte_4_tanque_lc()
        self.clean_up()
        
        self.parte_5_encerramento()
        self.wait(1)

    def clean_up(self):
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.5)

    def parte_1_origem(self):
        # 1. Start Dark, White Dot appears
        dot = Dot(color=WHITE).scale(1.5)
        self.play(FadeIn(dot))
        
        # 2. Stretch to DC Line
        dc_line = Line(LEFT*4, RIGHT*4, color=WHITE, stroke_width=4)
        self.play(Transform(dot, dc_line))
        
        label_cc = Tex("Corrente Contínua (CC)", font_size=36).next_to(dc_line, UP)
        self.play(Write(label_cc))
        self.wait(1)
        
        # 3. Warp to AC Sine
        # Create sine path
        sine_path = FunctionGraph(lambda x: np.sin(x), x_range=[-4, 4], color=WHITE)
        
        label_ca = Tex("Corrente Alternada (CA)", font_size=36).next_to(sine_path, UP)
        
        self.play(
            ReplacementTransform(dot, sine_path), # dot was transformed to dc_line
            Transform(label_cc, label_ca)
        )
        self.wait(1)
        
        # 4. Freeze and Show 3 Icons
        # Gear (Mechanical)
        gear_body = Circle(radius=0.5, color=GREY, stroke_width=4)
        gear_teeth = VGroup(*[Line(start=ORIGIN, end=UP*0.7, color=GREY, stroke_width=6).rotate(angle=i*2*PI/8) for i in range(8)])
        gear_center = Circle(radius=0.2, color=BLACK, fill_opacity=1)
        gear = VGroup(gear_body, gear_teeth, gear_center).move_to(LEFT*3 + DOWN*1.5)
        
        # Microchip (Control)
        chip_body = Square(side_length=1.0, color=GREEN, fill_opacity=0.2)
        top_legs = VGroup(*[Line(UP*0.5, UP*0.7, color=GREEN).shift(RIGHT*offset) for offset in [-0.3, 0, 0.3]])
        bot_legs = VGroup(*[Line(DOWN*0.5, DOWN*0.7, color=GREEN).shift(RIGHT*offset) for offset in [-0.3, 0, 0.3]])
        chip_text = Text("CPU", font_size=16, color=GREEN)
        chip = VGroup(chip_body, top_legs, bot_legs, chip_text).move_to(DOWN*1.5)
        
        # Antena (High Freq)
        # Simple Y shape or dish
        ant_mast = Line(DOWN*0.5, UP*0.5, color=BLUE)
        ant_wave1 = Arc(radius=0.5, start_angle=PI/4, angle=PI/2, color=BLUE).shift(UP*0.5)
        ant_wave2 = Arc(radius=0.8, start_angle=PI/4, angle=PI/2, color=BLUE).shift(UP*0.5)
        antenna = VGroup(ant_mast, ant_wave1, ant_wave2).move_to(RIGHT*3 + DOWN*1.5)
        
        # Arrows pointing to wave
        arrows = VGroup(
            Arrow(gear.get_top(), sine_path.get_left() + DOWN*0.2, color=GREY),
            Arrow(chip.get_top(), sine_path.get_bottom(), color=GREEN),
            Arrow(antenna.get_top(), sine_path.get_right() + DOWN*0.2, color=BLUE)
        )
        
        title_center = Tex("Três caminhos para construir uma onda", font_size=32).to_edge(UP)
        
        self.play(FadeIn(gear), FadeIn(chip), FadeIn(antenna))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), GrowArrow(arrows[2]))
        self.play(Write(title_center))
        self.wait(2)

    def parte_2_mecanica(self):
        title = Tex("1. Geração Eletromecânica (Alternadores)", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Setup: Coil and Magnet
        coil = Ellipse(width=3, height=1.5, color=ORANGE, stroke_width=4).move_to(LEFT*3)
        coil_label = Tex("Espira ($S$)", font_size=24, color=ORANGE).next_to(coil, UP)
        
        # ValueTracker for rotation
        theta = ValueTracker(0)

        # Magnet defined with always_redraw to ensure proper rotation update
        def get_magnet():
            m = VGroup(
                Rectangle(width=2, height=0.4, color=RED, fill_opacity=0.8), # N
                Rectangle(width=2, height=0.4, color=BLUE, fill_opacity=0.8)  # S
            ).arrange(RIGHT, buff=0).move_to(coil.get_center())
            m.rotate(theta.get_value())
            return m

        magnet = always_redraw(get_magnet)
        
        magnet_label = Tex(r"Ímã ($\vec{B}$)", font_size=24).next_to(coil, DOWN)
        
        self.play(Create(coil), Write(coil_label), FadeIn(magnet), Write(magnet_label))
        
        # Equation 1: Flux
        eq_flux = MathTex(r"\varphi_b = \int_S \vec{b} \cdot \vec{n} \cdot dS", font_size=32).move_to(RIGHT*3 + UP*2)
        eq_faraday = MathTex(r"fem = -\frac{\partial \varphi_b}{\partial t}", font_size=36, color=YELLOW).next_to(eq_flux, DOWN, buff=0.5)
        
        self.play(Write(eq_flux))
        self.play(Write(eq_faraday))
        
        # Animation: Rotation and Graph
        # Axes for graph
        axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=5,
            y_length=2.5,
            axis_config={"color": GREY}
        ).move_to(RIGHT*3 + DOWN*1)
        
        graph_label = MathTex("fem(t)", color=YELLOW, font_size=24).next_to(axes, UP)
        self.play(Create(axes), Write(graph_label))
        
        # ValueTracker for rotation
        theta = ValueTracker(0)
        
        # Update Rotated Magnet is handled by always_redraw now
        
        # Update Graph Dot/Curve
        # We want to draw the sine wave as it rotates
        # fem = -d/dt (cos t) = sin t
        
        curve = always_redraw(lambda: 
            axes.plot(lambda x: np.sin(x), x_range=[0, theta.get_value()], color=YELLOW)
        )
        
        self.add(curve)
        
        # Run animation
        # Speed: 2 cycles (4 PI)
        self.play(theta.animate.set_value(4*PI), run_time=6, rate_func=linear)
        
        # magnet.clear_updaters() # Not needed with always_redraw
        
        freq_text = Tex("Rotação Física = $f$ (60 Hz)", font_size=28, color=GREY).next_to(axes, DOWN)
        self.play(FadeIn(freq_text))
        self.wait(2)

    def parte_3_pwm(self):
        title = Tex("2. Conversão Eletrônica (Inversores)", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 1. DC Line
        dc_line = Line(LEFT*4, RIGHT*4, color=YELLOW, stroke_width=4).shift(UP*1)
        dc_label = Tex("Fonte CC", font_size=24, color=YELLOW).next_to(dc_line, LEFT)
        self.play(Create(dc_line), Write(dc_label))
        
        # 2. Transistors Logic (The "Chopper")
        # Animate the chopping action
        chopper = Line(UP*2, DOWN*0.5, color=RED, stroke_width=2).move_to(LEFT*4)
        desc_chopper = Tex("Chaveamento Rápido", color=RED, font_size=24).next_to(chopper, UP)
        self.play(FadeIn(chopper), Write(desc_chopper))
        
        self.play(chopper.animate.move_to(RIGHT*4), run_time=1.5)
        self.play(FadeOut(chopper), FadeOut(desc_chopper))

        # Replace DC line with PWM Bars
        num_bars = 40 # More bars for better resolution
        pwm_group = VGroup()
        x_vals = np.linspace(-4, 4, num_bars)
        width_slot = 8.0 / num_bars
        
        # Visualize PWM: Width Modulation
        # Height is constant (Vcc), Width varies with sin(x)
        for x in x_vals:
            # Sine controls duty cycle
            sine_val = np.sin(x*1.5 + PI/2) # Frequency adjust
            is_pos = sine_val > 0
            
            bar_height = 1.5
            bar_width = width_slot * abs(sine_val) * 0.9 # Width prop to amplitude
            
            color = YELLOW if is_pos else ORANGE
            
            bar = Rectangle(width=bar_width, height=bar_height, color=color, fill_opacity=0.8)
            bar.move_to([x, 0, 0])
            
            if is_pos:
                bar.align_to(dc_line, DOWN).shift(UP*0.1)
            else:
                bar.align_to(dc_line, UP).shift(DOWN*0.1 + DOWN*2) # Shift below axis
                
            pwm_group.add(bar)

        center_axis = Line(LEFT*4, RIGHT*4, color=GREY).shift(DOWN*0)

        self.play(ReplacementTransform(dc_line, pwm_group), FadeIn(center_axis))
        
        pwm_label = Tex(r"Largura do Pulso $\propto$ Amplitude", font_size=24).next_to(pwm_group, DOWN, buff=1.5)
        self.play(Write(pwm_label))
        
        eq_pwm = MathTex(r"Media \approx Senoide", font_size=32, color=GREEN).next_to(pwm_group, UP, buff=0.2)
        self.play(Write(eq_pwm))
        
        # Filter (LC) sliding
        filter_box = RoundedRectangle(corner_radius=0.2, width=1.5, height=1, color=BLUE)
        filter_label = Tex("Filtro LC", font_size=20, color=BLUE).move_to(filter_box)
        filter_group = VGroup(filter_box, filter_label).move_to(LEFT*5)
        
        self.play(FadeIn(filter_group))
        
        # Sine wave to reveal
        sine_wave = FunctionGraph(lambda x: 1.5 * np.sin(x*1.5 + PI/2), x_range=[-4, 4], color=GREEN, stroke_width=4).shift(DOWN*1) # Correction

        # Animation: Filter slides, revealing sine wave behind it
        self.play(
            filter_group.animate.move_to(RIGHT*5),
            Create(sine_wave), # This just draws it, ideally we want a reveal mask
            run_time=4
        )
        
        final_text = Tex("Sem peças móveis. Apenas Matemática.", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

    def parte_4_tanque_lc(self):
        title = Tex("3. Osciladores (Circuito Tanque LC)", font_size=36).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Draw LC Circuit diagram
        # Capacitor Left, Inductor Right
        C_plate1 = Line(UP*0.8, DOWN*0.8, color=BLUE, stroke_width=5).move_to(LEFT*2)
        C_plate2 = Line(UP*0.8, DOWN*0.8, color=BLUE, stroke_width=5).move_to(LEFT*1.5)
        
        # Wires connecting top and bot
        wire_top = Line(LEFT*1.75 + UP*0.8, RIGHT*1.75 + UP*0.8)
        wire_bot = Line(LEFT*1.75 + DOWN*0.8, RIGHT*1.75 + DOWN*0.8)
        
        # Inductor (Spring shape)
        # Simplified as loops
        # Actually standard inductor symbol is usually vertical or bumps.
        # Let's make continuous spiral better positioned
        inductor = VGroup()
        for i in range(4):
            arc = Arc(radius=0.2, start_angle=-PI/2, angle=PI*1.5, color=RED).shift(UP * (i*0.4 - 0.6))
            inductor.add(arc)
        inductor.move_to(RIGHT*1.75)
        
        circuit = VGroup(C_plate1, C_plate2, wire_top, wire_bot, inductor).move_to(ORIGIN)
        self.play(Create(circuit))
        
        # Labels
        lbl_c = MathTex("C", color=BLUE).next_to(C_plate1, LEFT)
        lbl_l = MathTex("L", color=RED).next_to(inductor, RIGHT)
        self.play(Write(lbl_c), Write(lbl_l))
        
        # Energy Ball
        energy = Dot(color=BLUE, radius=0.3).move_to(LEFT*1.75 + UP*0.8) # Start at Capacitor Top
        
        # Energy Bars Display
        # Create axes for energy
        axes_energy = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 10, 2],
            x_length=2,
            y_length=3,
            axis_config={"include_numbers": False}
        ).to_edge(RIGHT).shift(DOWN*0.5)
        
        bar_E = Rectangle(width=0.5, color=BLUE, fill_opacity=1).move_to(axes_energy.c2p(0.5, 0), aligned_edge=DOWN)
        bar_B = Rectangle(width=0.5, color=RED, fill_opacity=1).move_to(axes_energy.c2p(1.5, 0), aligned_edge=DOWN) # Start empty
        # Start B at near zero
        bar_B.stretch_to_fit_height(0.1, about_edge=DOWN)
        bar_E.stretch_to_fit_height(3, about_edge=DOWN)

        label_UE = Tex("$U_E$", color=BLUE, font_size=24).next_to(bar_E, DOWN)
        label_UB = Tex("$U_B$", color=RED, font_size=24).next_to(bar_B, DOWN)
        
        self.play(Create(axes_energy), FadeIn(bar_E), FadeIn(bar_B), Write(label_UE), Write(label_UB))
        
        # Animation Loop
        
        # 1. Cap to Inductor (Current Flow)
        # E drops, B rises
        self.play(
            MoveAlongPath(energy, wire_top),
            energy.animate.set_color(RED),
            bar_E.animate.stretch_to_fit_height(0.1, about_edge=DOWN),
            bar_B.animate.stretch_to_fit_height(3, about_edge=DOWN),
            run_time=1.5
        )
        
        # 2. Inductor to Cap (Back flow bottom)
        # B drops, E rises
        self.play(
            MoveAlongPath(energy, Line(RIGHT*1.75 + DOWN*0.8, LEFT*1.75 + DOWN*0.8)), # Bottom wire back
            energy.animate.set_color(BLUE),
            bar_B.animate.stretch_to_fit_height(0.1, about_edge=DOWN),
            bar_E.animate.stretch_to_fit_height(3, about_edge=DOWN),
            run_time=1.5
        )
        
        # Faster loop
        for _ in range(3):
            self.play(
                MoveAlongPath(energy, wire_top, rate_func=linear), 
                energy.animate.set_color(RED),
                bar_E.animate.stretch_to_fit_height(0.1, about_edge=DOWN),
                bar_B.animate.stretch_to_fit_height(3, about_edge=DOWN),
                run_time=0.5
            )
            self.play(
                MoveAlongPath(energy, Line(RIGHT*1.75 + DOWN*0.8, LEFT*1.75 + DOWN*0.8), rate_func=linear), 
                energy.animate.set_color(BLUE),
                bar_B.animate.stretch_to_fit_height(0.1, about_edge=DOWN),
                bar_E.animate.stretch_to_fit_height(3, about_edge=DOWN),
                run_time=0.5
            )

        # Resonance Freq
        freq_eq = MathTex(r"f = \frac{1}{2\pi \sqrt{L \cdot C}}", font_size=42).to_edge(DOWN, buff=1)
        self.play(Write(freq_eq))
        
        expl = Tex("Alta Frequência (GHz)", color=GRAY, font_size=28).next_to(freq_eq, DOWN)
        self.play(Write(expl))
        self.wait(2)

    def parte_5_encerramento(self):
        # Summary scene
        # 1. Faraday (Left)
        # 2. PWM (Center)
        # 3. LC (Right) - represented by icons or simplified views
        
        # Just text headers and merge
        t1 = Tex("Mecânica", font_size=24).move_to(LEFT*4)
        t2 = Tex("Eletrônica", font_size=24).move_to(ORIGIN)
        t3 = Tex("Oscilação", font_size=24).move_to(RIGHT*4)
        
        self.play(Write(t1), Write(t2), Write(t3))
        
        # Merge to big wave
        big_wave = FunctionGraph(lambda x: np.sin(3*x), x_range=[-6, 6], color=WHITE, stroke_width=6)
        
        self.play(
            FadeOut(t1), FadeOut(t2), FadeOut(t3),
            Create(big_wave)
        )
        
        final_msg = Tex("A Física moldando a Frequência.", font_size=36).to_edge(DOWN)
        self.play(Write(final_msg))
        self.wait(3)

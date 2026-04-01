from manim import *
import numpy as np

config.media_width = "75%"
config.verbosity = "WARNING"

class CargaEletricaScene(Scene):
    def construct(self):
        self.parte_1_unidade_elementar()
        self.clean_up()
        
        self.parte_2_interacao()
        self.clean_up()
        
        self.parte_3_meio_fisico()
        self.clean_up()
        
        self.parte_4_densidades()
        self.clean_up()
        
        self.parte_5_origem_e_fluxo()
        # self.clean_up()

        # self.parte_6_potencial_padrao()
        # self.clean_up()

        # self.parte_7_origem_termodinamica()
        self.wait(1)

    def clean_up(self):
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.5)

    def create_charge(self, point, sign="+", color=RED, radius=0.3):
        circle = Circle(radius=radius, color=color, fill_opacity=0.8).move_to(point)
        label = MathTex(sign, color=WHITE).move_to(point)
        glow = circle.copy().set_fill(color, opacity=0.2).scale(1.5)
        return VGroup(glow, circle, label)

    def parte_1_unidade_elementar(self):
        # Title
        title = Tex("1. A Carga Elétrica ($Q$)", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Atom representation - Zooming into matter
        proton = self.create_charge(ORIGIN, "+", RED, 0.1)
        electron = self.create_charge(RIGHT * 1.5, "-", BLUE, 0.05)
        orbit = Circle(radius=1.5, color=WHITE, stroke_opacity=0.3)
        
        atom_group = VGroup(orbit, proton, electron)
        
        self.play(FadeIn(atom_group))
        self.play(Rotate(electron, angle=2*PI, about_point=ORIGIN, run_time=2))
        
        text_atom = Tex("Unidade fundamental: Prótons e Elétrons", font_size=24).next_to(atom_group, DOWN)
        self.play(Write(text_atom))
        self.wait(1)

        # Transition to Coulomb concept
        self.play(FadeOut(text_atom), FadeOut(orbit), FadeOut(proton))
        self.play(electron.animate.move_to(ORIGIN).scale(2))
        
        # Explosion to many electrons to represent Coulomb
        electrons = VGroup(*[
            Dot(color=BLUE, radius=0.05).move_to(
                np.array([np.random.uniform(-4, 4), np.random.uniform(-3, 3), 0])
            ) for _ in range(80)
        ])
        
        self.play(Transform(electron, electrons, lag_ratio=0.05))
        
        text_coulomb = MathTex("1 \\text{ Coulomb (C)} \\approx 6.24 \\times 10^{18} \\text{ elétrons}", font_size=36)
        text_coulomb.add_background_rectangle()
        text_coulomb.to_edge(DOWN)
        
        self.play(Write(text_coulomb))
        self.wait(2)
        
        self.play(FadeOut(electrons), FadeOut(text_coulomb), FadeOut(title))

        # Electric Field Visualization
        center_charge = self.create_charge(ORIGIN, "+", RED, 0.3)
        self.play(FadeIn(center_charge))
        
        def electric_field_func(p):
            dist = np.linalg.norm(p)
            if dist < 0.5:
                return np.array([0, 0, 0])
            return 0.8 * p / (dist**3)

        field = ArrowVectorField(electric_field_func, x_range=[-5, 5], y_range=[-3.5, 3.5])
        
        text_field = Tex("Campo Elétrico: Estado de prontidão", font_size=30).next_to(center_charge, UP, buff=0.5)
        text_field.add_background_rectangle()
        
        self.play(Create(field), Write(text_field))
        self.wait(2)

    def parte_2_interacao(self):
        title = Tex("2. A Interação (Força Elétrica)", font_size=40).to_edge(UP)
        self.play(Write(title))

        q1 = self.create_charge(LEFT * 2, "+", RED)
        q2 = self.create_charge(RIGHT * 2, "-", BLUE)
        
        l1 = always_redraw(lambda: MathTex("q_1").next_to(q1, UP))
        l2 = always_redraw(lambda: MathTex("q_2").next_to(q2, UP))

        self.play(FadeIn(q1), FadeIn(l1))
        self.play(FadeIn(q2), FadeIn(l2))

        # Dynamic Force Vectors
        # Using always_redraw to update vectors as objects move
        def get_force_vector(obj, target, color=YELLOW):
            direction = target.get_center() - obj.get_center()
            dist = np.linalg.norm(direction)
            if dist == 0: return Vector([0,0,0])
            unit_dir = direction / dist
            # Visual magnitude: inversely proportional to distance
            # Clamped to avoid huge vectors
            mag = 3.0 / (dist + 0.1) 
            mag = min(max(mag, 0.5), 2.5) 
            
            start_point = obj.get_center() + unit_dir * 0.4 # Start a bit outside the charge
            return Arrow(start=start_point, end=start_point + unit_dir * mag, color=color, buff=0, max_stroke_width_to_length_ratio=5)

        f1 = always_redraw(lambda: get_force_vector(q1, q2))
        f2 = always_redraw(lambda: get_force_vector(q2, q1))
        
        f_label = MathTex("\\vec{F}", color=YELLOW).next_to(f1, UP)

        self.play(GrowArrow(f1), GrowArrow(f2), Write(f_label))

        # Coulomb Law Formula
        formula = MathTex("F = k \\frac{|q_1 q_2|}{r^2}", font_size=36).to_edge(DOWN)
        self.play(Write(formula))

        # Dynamics Animation: Move closer (force grows)
        self.play(
            q1.animate.move_to(LEFT * 1),
            q2.animate.move_to(RIGHT * 1),
            run_time=2
        )
        self.wait(0.5)
        
        # Move Further (force shrinks)
        self.play(
            q1.animate.move_to(LEFT * 3),
            q2.animate.move_to(RIGHT * 3),
            run_time=2
        )
        self.wait(1)

        # Repulsion Case
        self.play(FadeOut(f1), FadeOut(f2), FadeOut(f_label))
        
        # Change q2 to positive
        q2_new = self.create_charge(q2.get_center(), "+", RED)
        
        self.play(
            Transform(q2, q2_new),
        )
        
        # Repulsion vectors (pointing away)
        def get_repulsion_vector(obj, target, color=YELLOW):
            direction = obj.get_center() - target.get_center() # Direction AWAY from target
            dist = np.linalg.norm(direction)
            if dist == 0: return Vector([0,0,0])
            unit_dir = direction / dist
            mag = 3.0 / (dist + 0.1)
            mag = min(max(mag, 0.5), 2.5)
            
            start_point = obj.get_center() + unit_dir * 0.4
            return Arrow(start=start_point, end=start_point + unit_dir * mag, color=color, buff=0)
            
        f1_rep = always_redraw(lambda: get_repulsion_vector(q1, q2))
        f2_rep = always_redraw(lambda: get_repulsion_vector(q2, q1))
        
        self.play(GrowArrow(f1_rep), GrowArrow(f2_rep))
        
        # Charges move away due to repulsion
        self.play(
            q1.animate.shift(LEFT * 0.5),
            q2.animate.shift(RIGHT * 0.5),
            run_time=1
        )
        self.wait(2)
        
    def parte_3_meio_fisico(self):
        title = Tex("3. O Meio Físico: Movimento vs. Tensão", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Scenario A: Vacuum (Action/Motion)
        case_a_text = Tex("Vácuo / Condutor $\\rightarrow$ Movimento", font_size=30, color=GREEN).to_corner(UL).shift(DOWN*1)
        self.play(Write(case_a_text))

        q_pos = self.create_charge(LEFT * 3, "+", RED)
        q_neg = self.create_charge(RIGHT * 3, "-", BLUE)
        
        self.add(q_pos, q_neg)
        
        # Charges accelerate towards each other
        self.play(
            q_pos.animate.move_to(LEFT * 0.3),
            q_neg.animate.move_to(RIGHT * 0.3),
            rate_func=lambda t: t**4, # Accelerate
            run_time=1.5
        )
        self.play(Flash(ORIGIN, color=WHITE, line_length=0.5))
        self.play(FadeOut(q_pos), FadeOut(q_neg), FadeOut(case_a_text))
        
        # Scenario B: Dielectric (Tension)
        case_b_text = Tex("Isolante $\\rightarrow$ Tensão", font_size=30, color=ORANGE).to_corner(UL).shift(DOWN*1)
        self.play(Write(case_b_text))

        # Reset charges
        q_pos = self.create_charge(LEFT * 3, "+", RED)
        q_neg = self.create_charge(RIGHT * 3, "-", BLUE)
        self.add(q_pos, q_neg)

        # Insert Obstacle
        obstacle = Rectangle(width=1.5, height=4, color=GRAY, fill_opacity=0.5).move_to(ORIGIN)
        label_dielectric = Tex("Dielétrico", font_size=24).move_to(obstacle)
        
        self.play(FadeIn(obstacle), Write(label_dielectric))
        
        # Charges try to move but act elastic/springy
        self.play(
            q_pos.animate.move_to(LEFT * 1.5),
            q_neg.animate.move_to(RIGHT * 1.5),
            run_time=0.8
        )
        
        # Wiggle to show constrained energy
        self.play(
            q_pos.animate.shift(RIGHT * 0.1),
            q_neg.animate.shift(LEFT * 0.1),
            rate_func=wiggle,
            run_time=1
        )
        
        # Tension visualization
        brace = Brace(obstacle, UP)
        tension_text = Tex("Tensão Elétrica ($V$)", color=ORANGE).next_to(brace, UP)
        
        self.play(Create(brace), Write(tension_text))
        self.wait(1)
        
        # Transition to Capacitor
        self.play(
            FadeOut(q_pos), FadeOut(q_neg), 
            FadeOut(label_dielectric), FadeOut(brace), FadeOut(tension_text),
            obstacle.animate.stretch_to_fit_width(2)
        )
        
        plate_l = Rectangle(width=0.2, height=3, color=RED, fill_opacity=1).next_to(obstacle, LEFT, buff=0)
        plate_r = Rectangle(width=0.2, height=3, color=BLUE, fill_opacity=1).next_to(obstacle, RIGHT, buff=0)
        
        self.play(FadeIn(plate_l), FadeIn(plate_r))
        
        # Field lines inside
        lines = VGroup()
        for i in np.linspace(-1.5, 1.5, 6):
            lines.add(Arrow(start=LEFT*1 + UP*i, end=RIGHT*1 + UP*i, color=YELLOW, stroke_width=2, tip_length=0.15))
            
        self.play(Create(lines))
        
        cap_label = Tex("Capacitor: Energia Armazenada em Tensão").to_edge(DOWN)
        self.play(Write(cap_label))
        self.wait(2)

    def parte_4_densidades(self):
        title = Tex("4. Densidades de Carga", font_size=40).to_edge(UP)
        self.play(Write(title))

        # 1. Linear
        wire = Line(LEFT*2.5, RIGHT*2.5, color=WHITE).shift(UP*2)
        charges_lin = VGroup(*[MathTex("+", color=RED, font_size=20).move_to(wire.point_from_proportion(p)) for p in np.linspace(0, 1, 15)])
        
        f_lin = MathTex(r"\rho_L = \frac{Q}{L}", color=YELLOW).next_to(wire, RIGHT)
        lbl_lin = Tex("Densidade Linear", font_size=24).next_to(wire, UP)
        
        self.play(Create(wire), FadeIn(charges_lin))
        self.play(Write(f_lin), Write(lbl_lin))
        self.wait(1)

        # 2. Superficial
        # Represented as a tilted plane
        plate = Rectangle(width=4, height=2, color=BLUE, fill_opacity=0.3).shift(DOWN * 0.5)
        # Add slight perspective
        plate_grp = VGroup(plate) 
        
        charges_surf = VGroup()
        for x in np.linspace(-1.5, 1.5, 8):
            for y in np.linspace(-0.6, 0.6, 3):
                charges_surf.add(MathTex("+", color=RED, font_size=16).move_to(plate.get_center() + [x, y, 0]))

        f_surf = MathTex(r"\rho_S = \frac{Q}{A}", color=YELLOW).next_to(plate, RIGHT)
        lbl_surf = Tex("Densidade Superficial", font_size=24).next_to(plate, UP)
        
        self.play(Create(plate), FadeIn(charges_surf))
        self.play(Write(f_surf), Write(lbl_surf))
        self.wait(1)

        # 3. Volumetric
        # Represented as a box
        box = Rectangle(width=1.5, height=1.5, color=GREEN, fill_opacity=0.3).shift(DOWN * 2.8)
        charges_vol = VGroup()
        for _ in range(20):
             charges_vol.add(Dot(radius=0.04, color=RED).move_to(box.get_center() + [np.random.uniform(-0.6,0.6), np.random.uniform(-0.6,0.6), 0]))
             
        f_vol = MathTex(r"\rho_V = \frac{Q}{V}", color=YELLOW).next_to(box, RIGHT)
        lbl_vol = Tex("Densidade Volumétrica", font_size=24).next_to(box, LEFT)
        
        self.play(Create(box), FadeIn(charges_vol))
        self.play(Write(f_vol), Write(lbl_vol))
        self.wait(2)

    def parte_5_origem_e_fluxo(self):
        title = Tex("5. A Origem Química e Corrente", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Battery Electrodes
        anode = Rectangle(width=1, height=2.5, color=GRAY, fill_opacity=0.6).shift(LEFT * 3)
        cathode = Rectangle(width=1, height=2.5, color=ORANGE, fill_opacity=0.6).shift(RIGHT * 3)
        
        l_zn = Tex("Zn").move_to(anode)
        l_cu = Tex("Cu").move_to(cathode)
        
        # Potentials
        pot_zn = MathTex("E^{\\circ} = -0.76 V").next_to(anode, DOWN)
        pot_cu = MathTex("E^{\\circ} = +0.34 V").next_to(cathode, DOWN)
        
        self.play(Create(anode), Create(cathode), Write(l_zn), Write(l_cu))
        self.play(Write(pot_zn), Write(pot_cu))
        
        # ddp / Voltage Arrow
        diff_arrow = DoubleArrow(start=anode.get_right(), end=cathode.get_left(), color=YELLOW, buff=0.1)
        diff_text = Tex("d.d.p (Volts)", color=YELLOW, font_size=28).next_to(diff_arrow, UP)
        
        self.play(GrowArrow(diff_arrow), Write(diff_text))
        self.wait(1)
        
        # Conductor Wire connection
        # Path: Anode Top -> Up -> Right -> Cathode Top
        p1 = anode.get_top()
        p2 = p1 + UP * 1.5
        p3 = cathode.get_top() + UP * 1.5
        p4 = cathode.get_top()
        
        wire = VGroup(
            Line(p1, p2),
            Line(p2, p3),
            Line(p3, p4)
        ).set_color(WHITE).set_stroke(width=4)
        
        self.play(Create(wire))
        
        # Current Flow Animation
        # We simulate electrons flowing
        electrons = VGroup()
        path = VMobject()
        path.set_points_as_corners([p1, p2, p3, p4])
        
        for _ in range(15):
            e = Dot(color=YELLOW, radius=0.08)
            electrons.add(e)
            
        # Create a continuous flow animation
        # MoveAlongPath gives total run_time for one object.
        # We need LaggedStart of many MoveAlongPath
        
        anims = [MoveAlongPath(Dot(color=YELLOW, radius=0.08), path, run_time=4, rate_func=linear) for _ in range(20)]
        
        current_text = Tex("Corrente Elétrica ($I$): Fluxo de Cargas", font_size=32).next_to(wire, DOWN).shift(UP*1)
        
        self.play(
            AnimationGroup(
                *anims,
                lag_ratio=0.15
            ),
            Write(current_text)
        )
        self.wait(1)

    def parte_6_potencial_padrao(self):
        title = Tex(r"6. Definindo o Potencial Padrão ($E^\circ$)", font_size=40).to_edge(UP)
        self.play(Write(title))

        # 1. The Reference: Standard Hydrogen Electrode (SHE)
        # Simplified drawing: Container, Solution, Electrode
        she_container = Rectangle(width=3, height=2.5, color=BLUE, fill_opacity=0.3).shift(RIGHT * 3)
        # Move electrode slightly up so it sticks out
        she_electrode = Rectangle(width=0.4, height=3, color=GRAY).move_to(she_container.get_top() + UP*0.2 + DOWN*1.5) 
        # Corrected positioning: Container top is at y=1.25. height=3 means electrode goes from -0.25 to 2.75.
        # Let's fix positioning relative to container center
        she_electrode.move_to(she_container.get_center() + UP*0.5)

        she_label = Tex("Eletrodo Padrão\nde Hidrogênio (EPH)", font_size=24).next_to(she_container, DOWN)
        she_val = MathTex(r"E^\circ = 0.00 V", color=YELLOW).move_to(she_container).shift(DOWN*0.5)
        
        self.play(Create(she_container), FadeIn(she_electrode), Write(she_label))
        self.play(Write(she_val))
        self.wait(1)

        # 2. Test Element: Zinc
        zn_container = Rectangle(width=3, height=2.5, color=GREEN, fill_opacity=0.3).shift(LEFT * 3)
        zn_electrode = Rectangle(width=0.4, height=3, color=GRAY_BROWN).move_to(zn_container.get_center() + UP*0.5)
        zn_label = Tex("Zinco (Zn)", font_size=24).next_to(zn_container, DOWN)
        
        self.play(Create(zn_container), FadeIn(zn_electrode), Write(zn_label))
        
        # 3. Connection and Voltmeter
        voltmeter = Circle(radius=0.5, color=WHITE).move_to(UP * 1)
        v_text = Tex("V").move_to(voltmeter)
        
        wire_left = Line(zn_electrode.get_top(), voltmeter.get_left())
        wire_right = Line(she_electrode.get_top(), voltmeter.get_right())
        
        self.play(Create(voltmeter), Write(v_text), Create(wire_left), Create(wire_right))
        
        # 4. Measurement
        reading = MathTex("-0.76 V", color=RED).next_to(voltmeter, UP)
        explanation = Tex("O voltímetro mede a diferença\nentre Zn e o Zero (H)", font_size=28).to_edge(DOWN)
        
        self.play(Write(reading), Write(explanation))
        self.wait(2)
        
        # 5. Formula
        self.play(FadeOut(explanation))
        
        def_text = MathTex(
            "E^\circ_{\\text{Zn}}", "=",  "V_{\\text{medido}}", "=", "-0.76 V"
        ).scale(1.2).shift(DOWN * 2.5)
        
        self.play(Write(def_text))
        self.wait(2)

    def parte_7_origem_termodinamica(self):
        title = Tex("7. Origem Termodinâmica do Potencial", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Zinc solid lattice
        lattice_dots = VGroup(*[
            Dot(color=GRAY, radius=0.15).move_to([x, y, 0])
            for x in np.linspace(-5, -3, 3)
            for y in np.linspace(-1, 1, 3)
        ])
        lattice_label = Tex("Rede Cristalina (Sólido)", font_size=24).next_to(lattice_dots, DOWN)
        
        self.play(FadeIn(lattice_dots), Write(lattice_label))
        
        # Step 1: Sublimation
        atom = lattice_dots[4].copy() # Middle dot
        self.play(atom.animate.move_to(LEFT * 1).set_color(WHITE).scale(1.2))
        
        step1_lbl = Tex("1. Sublimação ($+\Delta H_{sub}$)", color=RED, font_size=28).next_to(atom, UP)
        sub_energy = MathTex("+130 \\text{ kJ/mol}", color=RED, font_size=24).next_to(step1_lbl, DOWN)
        
        self.play(Write(step1_lbl), Write(sub_energy))
        self.wait(1)
        
        # Step 2: Ionization
        electrons = VGroup(
            Dot(color=YELLOW, radius=0.08).move_to(atom.get_left() + LEFT*0.2),
            Dot(color=YELLOW, radius=0.08).move_to(atom.get_right() + RIGHT*0.2)
        )
        
        self.play(
            atom.animate.set_color(GREEN), # Becomes ion
            FadeIn(electrons)
        )
        
        self.play(electrons.animate.shift(UP * 2), run_time=1.5) # Electrons leave
        
        step2_lbl = Tex("2. Ionização ($+IE$)", color=RED, font_size=28).next_to(atom, UP).shift(RIGHT * 2.5)
        ion_energy = MathTex("+2640 \\text{ kJ/mol}", color=RED, font_size=24).next_to(step2_lbl, DOWN)
        
        self.play(FadeOut(step1_lbl), FadeOut(sub_energy))
        self.play(Write(step2_lbl), Write(ion_energy))
        self.wait(1)
        
        # Step 3: Hydration
        water_mols = VGroup()
        for i in range(6):
            angle = i * (2*PI/6)
            pos = atom.get_center() + 0.6 * np.array([np.cos(angle), np.sin(angle), 0])
            water = Circle(radius=0.1, color=BLUE, fill_opacity=0.5).move_to(pos)
            water_mols.add(water)
            
        self.play(
            FadeIn(water_mols),
            atom.animate.scale(0.8) # Ions are smaller
        )
        
        step3_lbl = Tex("3. Hidratação ($-\Delta H_{hid}$)", color=BLUE, font_size=28).next_to(atom, DOWN).shift(DOWN*0.5)
        hyd_energy = MathTex("-2046 \\text{ kJ/mol}", color=BLUE, font_size=24).next_to(step3_lbl, DOWN)
        
        self.play(FadeOut(step2_lbl), FadeOut(ion_energy), FadeOut(electrons))
        self.play(Write(step3_lbl), Write(hyd_energy))
        self.wait(1)
        
        # Total Balance
        balance_box = Rectangle(width=5, height=3, color=WHITE).shift(RIGHT * 3.5)
        b_title = Tex("Balanço Energético", font_size=32).move_to(balance_box.get_top() + DOWN*0.5)
        
        line1 = MathTex("\Delta G \propto E^\circ", color=YELLOW).next_to(b_title, DOWN)
        line2 = MathTex("= \Delta H_{sub} + IE + \Delta H_{hid} - T\Delta S", font_size=24).next_to(line1, DOWN)
        line3 = Tex("Essa soma define a tendência!", font_size=26, color=ORANGE).next_to(line2, DOWN, buff=0.5)
        
        self.play(Create(balance_box), Write(b_title))
        self.play(Write(line1))
        self.play(Write(line2))
        self.play(Write(line3))
        self.wait(3)

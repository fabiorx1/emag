from manim import *
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

config.media_width = "75%"
config.verbosity = "WARNING"

BG = "#ece6e2"
FG = "#5c5c5c"
DARK_BG = "#101010"
C_GOLD = "#d4a017"
C_OMEGA = "#d9a441"
C_SIGMA = "#c0392b"
C_EPS = "#2980b9"
C_GREEN = "#27ae60"
C_RED = "#a93226"
C_PURPLE = "#8e44ad"
C_PANEL = "#f7f2ee"

EPS0 = 8.854e-12


class ExerciciosScene(Scene):
	def construct(self):
		self.camera.background_color = BG
		Text.set_default(color=FG)
		tex_template = TexTemplate()
		tex_template.add_to_preamble(r"\usepackage{cancel}")
		MathTex.set_default(color=FG, tex_template=tex_template)

		self.cena_0_abertura()
		self.clean_up()

		self.cena_1_base_exercicios()
		self.clean_up()

		self.cena_2_exercicios_1_2_3()
		self.clean_up()

		self.cena_1_5_espectro_materiais()
		self.clean_up()

		self.cena_3_exercicio_5()
		self.clean_up()

		self.cena_4_exercicio_6()
		self.clean_up()

		self.cena_5_exercicio_4()
		self.wait(1)

	def clean_up(self):
		self.play(*[FadeOut(mob) for mob in self.mobjects])
		self.wait(0.3)

	def cena_0_abertura(self):
		title = Text("Eletromagnetismo Aplicado", font_size=48, weight=BOLD)
		subtitle = Text("Resolução de Exercícios: Razão de Correntes e Campos", font_size=28, color=C_GOLD)
		VGroup(title, subtitle).arrange(DOWN, buff=0.5)
		
		line = Line(LEFT * 4, RIGHT * 4, color=FG, stroke_width=2).next_to(subtitle, DOWN, buff=0.4)
		
		self.play(Write(title), run_time=1.5)
		self.play(FadeIn(subtitle, shift=UP * 0.2), Create(line), run_time=1.2)
		self.wait(2)

	def formula_box(self, mob, color=C_GOLD, buff=0.18):
		box = SurroundingRectangle(mob, color=color, buff=buff, stroke_width=3, corner_radius=0.12)
		box.set_fill(color, opacity=0.05)
		return VGroup(box, mob)

	def caption(self, text, color=FG, font_size=24):
		return Text(text, font_size=font_size, color=color)

	def make_limit_card(self, title, ratio_tex, result_tex, color, width=4.0, height=2.55):
		rect = RoundedRectangle(
			corner_radius=0.16,
			width=width,
			height=height,
			color=color,
			stroke_width=3,
		)
		rect.set_fill(C_PANEL, opacity=0.92)
		title_mob = Text(title, font_size=26, color=color).move_to(rect.get_top() + DOWN * 0.38)
		ratio_mob = MathTex(ratio_tex, font_size=34, color=FG).move_to(rect.get_center() + UP * 0.2)
		result_mob = MathTex(result_tex, font_size=28, color=color).move_to(rect.get_center() + DOWN * 0.55)
		return VGroup(rect, title_mob, ratio_mob, result_mob)

	def scene_title(self, title, subtitle=None, color=FG):
		title_mob = Text(title, font_size=38, color=color).to_edge(UP)
		if subtitle is None:
			return VGroup(title_mob)
		subtitle_mob = Text(subtitle, font_size=22, color=color).next_to(title_mob, DOWN, buff=0.2)
		return VGroup(title_mob, subtitle_mob)

	def format_frequency(self, value_hz):
		if value_hz >= 1e9:
			return rf"{value_hz / 1e9:.2f}\,\text{{GHz}}"
		if value_hz >= 1e6:
			return rf"{value_hz / 1e6:.2f}\,\text{{MHz}}"
		if value_hz >= 1e3:
			return rf"{value_hz / 1e3:.1f}\,\text{{kHz}}"
		return rf"{value_hz:.1f}\,\text{{Hz}}"

	def build_case_cards(self, epsilon_r, sigma, override=None):
		limit_cond = sigma / (2 * PI * epsilon_r * EPS0 * 100)
		limit_diel = sigma / (2 * PI * epsilon_r * EPS0 * 0.01)

		cond_tex = rf"f < {self.format_frequency(limit_cond)}"
		diel_tex = rf"f > {self.format_frequency(limit_diel)}"
		quasi_tex = rf"{self.format_frequency(limit_cond)} < f < {self.format_frequency(limit_diel)}"

		if override:
			cond_tex = override.get("cond", cond_tex)
			diel_tex = override.get("diel", diel_tex)
			quasi_tex = override.get("quasi", quasi_tex)

		left = self.make_limit_card("Condutor", r"\text{Razão}=100", cond_tex, C_SIGMA)
		center = self.make_limit_card("Quase Condutor", r"\dfrac{1}{100}<\text{Razão}<100", quasi_tex, C_GOLD)
		right = self.make_limit_card("Dielétrico", r"\text{Razão}=\dfrac{1}{100}", diel_tex, C_EPS)
		cards = VGroup(left, center, right).arrange(RIGHT, buff=0.35).scale(0.82)
		return cards

	def cena_1_base_exercicios(self):
		overlay = FullScreenRectangle(fill_color=DARK_BG, fill_opacity=1, stroke_opacity=0)
		self.add(overlay)

		eq_ratio = MathTex(
			r"\frac{J_{\max}}{J_{d_{\max}}}",
			r"=",
			r"\frac{\sigma}{",
			r"\omega",
			r"\epsilon}",
			font_size=54,
			color=WHITE,
		)
		eq_ratio[3].set_color(YELLOW)

		self.play(FadeIn(eq_ratio, shift=UP * 0.2), run_time=1.2)
		self.wait(0.3)

		eq_expanded = MathTex(
			r"\frac{J_{\max}}{J_{d_{\max}}}",
			r"=",
			r"\frac{\sigma}{2\pi f\epsilon}",
			font_size=52,
			color=WHITE,
		).move_to(eq_ratio)
		eq_expanded.set_color_by_tex("f", YELLOW)

		self.play(TransformMatchingTex(eq_ratio, eq_expanded), run_time=1.2)
		self.wait(0.3)

		eq_frequency = MathTex(
			r"f = \frac{\sigma}{2\pi\epsilon\cdot \text{Razão}}",
			font_size=50,
			color=WHITE,
		).move_to(eq_expanded)
		eq_frequency.set_color_by_tex("f", C_OMEGA)

		note = self.caption(
			"A classificação do meio depende da frequência de operação f.",
			color=WHITE,
			font_size=26,
		).next_to(eq_frequency, DOWN, buff=0.55)

		self.play(TransformMatchingTex(eq_expanded, eq_frequency), run_time=1.3)
		self.play(FadeIn(note, shift=UP * 0.15))
		self.wait(0.6)

		eq_corner = eq_frequency.copy().set_color(FG).scale(0.72).to_corner(UL, buff=0.45)
		eq_box = self.formula_box(eq_corner)
		eq_box[0].set_color(C_GOLD)

		self.play(FadeOut(overlay, run_time=1.0))
		self.play(
			FadeOut(note),
			TransformFromCopy(eq_frequency, eq_corner),
			Create(eq_box[0]),
			FadeOut(eq_frequency),
			run_time=1.0,
		)
		self.add(eq_box)
		self.wait(0.8)

	def cena_2_exercicios_1_2_3(self):
		eq_ref = MathTex(
			r"f = \frac{\sigma}{2\pi\epsilon\cdot \text{Razão}}",
			font_size=34,
		).to_corner(UL, buff=0.45)
		eq_box = self.formula_box(eq_ref)
		header = self.scene_title("Exercícios 1, 2 e 3", "Calculando limites e frequência de equilíbrio")
		self.play(FadeIn(eq_box), Write(header[0]), FadeIn(header[1]))

		data_ex1 = MathTex(
			r"\epsilon = 81\epsilon_0",
			r"\qquad",
			r"\sigma = 4\,S/m",
			font_size=38,
		)
		data_ex1[0].set_color(C_EPS)
		data_ex1[2].set_color(C_SIGMA)
		data_ex1.next_to(header, DOWN, buff=0.85)

		ex1_label = Text("Ex. 1: Água do mar", font_size=24, color=FG).next_to(data_ex1, UP, buff=0.3)
		self.play(FadeIn(ex1_label, shift=UP * 0.1), Write(data_ex1))

		self.play(
			Indicate(data_ex1[2], color=C_SIGMA),
			Indicate(data_ex1[0], color=C_EPS),
			Indicate(eq_ref, color=C_GOLD),
			run_time=1.1,
		)

		cards_ex1 = self.build_case_cards(
			epsilon_r=81,
			sigma=4,
			override={
				"cond": r"f < 888\,\text{kHz}\,\text{aprox.}",
				"quasi": r"888\,\text{kHz} < f < 888\,\text{MHz}",
				"diel": r"f > 888\,\text{MHz}\,\text{aprox.}",
			},
		).move_to(DOWN * 1.1)

		self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards_ex1], lag_ratio=0.15), run_time=1.4)
		self.wait(1.0)

		data_ex2 = MathTex(
			r"\epsilon = 10\epsilon_0",
			r"\qquad",
			r"\sigma = 10^{-2}\,S/m",
			font_size=38,
		)
		data_ex2[0].set_color(C_EPS)
		data_ex2[2].set_color(C_SIGMA)
		data_ex2.move_to(data_ex1)
		ex2_label = Text("Ex. 2: Novo material", font_size=24, color=FG).move_to(ex1_label)
		cards_ex2 = self.build_case_cards(epsilon_r=10, sigma=1e-2).move_to(cards_ex1)

		self.play(
			TransformMatchingTex(data_ex1, data_ex2),
			Transform(ex1_label, ex2_label),
			TransformMatchingShapes(cards_ex1, cards_ex2),
			run_time=1.6,
		)
		self.wait(1.0)

		balance_base = Line(LEFT * 1.2, RIGHT * 1.2, color=FG, stroke_width=6).move_to(DOWN * 0.3)
		balance_pivot = Triangle(color=FG, fill_opacity=0.3).scale(0.22).next_to(balance_base, DOWN, buff=0.0)
		left_plate = Line(LEFT * 0.45, RIGHT * 0.45, color=FG).next_to(balance_base.get_left(), DOWN, buff=0.45)
		right_plate = Line(LEFT * 0.45, RIGHT * 0.45, color=FG).next_to(balance_base.get_right(), DOWN, buff=0.45)
		left_string = Line(balance_base.get_left(), left_plate.get_center(), color=FG)
		right_string = Line(balance_base.get_right(), right_plate.get_center(), color=FG)
		current_c = Text("Jc", font_size=18, color=C_SIGMA).next_to(left_plate, DOWN, buff=0.1)
		current_d = Text("Jd", font_size=18, color=C_EPS).next_to(right_plate, DOWN, buff=0.1)
		balance = VGroup(balance_base, balance_pivot, left_plate, right_plate, left_string, right_string, current_c, current_d)

		ratio_one = MathTex(r"\text{Razão}=1", font_size=38, color=C_GOLD)
		eq_balance = MathTex(r"f = \frac{\sigma}{2\pi\epsilon}", font_size=46, color=C_GOLD)
		text_balance = self.caption(
			"Frequência de equilíbrio:\nCorrente de condução = corrente de deslocamento",
			color=C_GOLD,
			font_size=20,
		).to_edge(DOWN, buff=0.35)
		balance.scale(0.92)
		balance_group = VGroup(ratio_one, balance, eq_balance).arrange(DOWN, buff=0.45).move_to(DOWN * 0.05)

		ex3_label = Text("Ex. 3: Equilíbrio de Correntes", font_size=24, color=FG).move_to(ex2_label)

		self.play(
			FadeOut(cards_ex2),
			FadeOut(data_ex2),
			Transform(ex1_label, ex3_label),
			FadeIn(balance_group, shift=UP * 0.15),
			run_time=1.0,
		)
		self.play(FadeIn(text_balance, shift=UP * 0.1))
		self.wait(1.4)

	def cena_3_exercicio_5(self):
		title = Text("Exercício 5: Do Domínio da Frequência para o Tempo", font_size=34, color=FG).to_edge(UP)
		note = MathTex(
			r"\text{Multiplicamos por } e^{i\omega t}\text{, expandimos e guardamos apenas a parte real.}",
			color=C_GOLD,
			font_size=18,
		).next_to(title, DOWN, buff=0.22)
		self.play(Write(title), FadeIn(note, shift=UP * 0.1))

		phasor = MathTex(
			r"\vec{E} = (10\hat{x} + i20\hat{y})e^{-ikz}",
			font_size=48,
		).move_to(UP * 1.25)
		self.play(Write(phasor))
		self.wait(1.0)

		step1 = MathTex(
			r"\vec{e} = \operatorname{Re}\left\{(10\hat{x} + i20\hat{y})e^{-ikz}\cdot e^{i\omega t}\right\}",
			font_size=34,
		).move_to(phasor)
		mult = MathTex(r"\cdot e^{i\omega t}", font_size=40, color=C_OMEGA).next_to(phasor, RIGHT, buff=0.35)
		self.play(FadeIn(mult, shift=LEFT * 0.1))
		self.play(TransformMatchingTex(phasor, step1), FadeOut(mult), run_time=1.5)
		self.wait(0.8)

		step2 = MathTex(
			r"\vec{e} = \operatorname{Re}\left\{(10\hat{x} + i20\hat{y})e^{i(\omega t-kz)}\right\}",
			font_size=34,
		).move_to(step1)
		self.play(TransformMatchingTex(step1, step2), run_time=1.2)
		self.wait(1.0)

		trig = MathTex(
			r"e^{i(\omega t-kz)} = \cos(\omega t-kz) + i\sin(\omega t-kz)",
			font_size=28,
			color=C_PURPLE,
		).move_to(ORIGIN + UP * 0.1)
		self.play(Write(trig))
		self.wait(0.8)

		terms = VGroup(
			MathTex(r"10\cos(\omega t-kz)\hat{x}", font_size=24),
			MathTex(r"+i10\sin(\omega t-kz)\hat{x}", font_size=24),
			MathTex(r"+i20\cos(\omega t-kz)\hat{y}", font_size=24),
			MathTex(r"-20\sin(\omega t-kz)\hat{y}", font_size=24),
		).arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.3)).move_to(DOWN * 1.4)
		self.play(FadeIn(terms, shift=UP * 0.1))
		self.wait(1.2)

		imag_box_1 = SurroundingRectangle(terms[1], color=C_RED, buff=0.1, stroke_width=3)
		imag_box_2 = SurroundingRectangle(terms[2], color=C_RED, buff=0.1, stroke_width=3)
		self.play(Create(imag_box_1), Create(imag_box_2))
		self.wait(1.0)
		self.play(
			FadeOut(terms[1], shift=RIGHT * 0.2),
			FadeOut(terms[2], shift=RIGHT * 0.2),
			FadeOut(imag_box_1),
			FadeOut(imag_box_2),
			run_time=1.2,
		)
		self.wait(0.8)

		result = MathTex(
			r"\vec{e} = 10\cos(\omega t-kz)\hat{x} - 20\sin(\omega t-kz)\hat{y}",
			font_size=34,
			color=C_GREEN,
		).move_to(DOWN * 0.7)
		unit = Text("[V/m]", font_size=22, color=C_GREEN).next_to(result, RIGHT, buff=0.25)

		self.play(
			FadeOut(terms[0]),
			FadeOut(terms[3]),
			FadeOut(trig),
			FadeOut(step2),
			FadeIn(result, shift=UP * 0.12),
			FadeIn(unit),
			run_time=1.4,
		)
		self.play(Create(self.formula_box(VGroup(result, unit), color=C_GREEN)[0]))
		self.wait(2.5)

	def cena_1_5_espectro_materiais(self):
		header = self.scene_title("Espectro de Frequências", "Visualizando a transição entre comportamentos")
		self.play(Write(header))

		# Configuração Logarítmica dos Eixos
		# Eixo X mapeado linearmente nas potências de 10 (f_exp variando de 3 a 11)
		# Eixo Y mapeado linearmente nas potências de 10 da Razão de Correntes (y de -4 a 10)
		ax = Axes(
			x_range=[3, 11, 2],
			y_range=[-4, 10, 2],
			x_length=9.5,
			y_length=5.5,
			axis_config={"include_tip": True, "color": FG},
		).shift(DOWN * 0.1 + RIGHT * 0.2)

		# Adicionar valores formatados como potências de 10 para ambos os eixos
		x_dict = {x: MathTex(rf"10^{{{x}}}", font_size=20, color=FG) for x in range(3, 12, 2)}
		ax.x_axis.add_labels(x_dict)
		
		y_dict = {y: MathTex(rf"10^{{{y}}}", font_size=20, color=FG) for y in range(-4, 11, 2)}
		ax.y_axis.add_labels(y_dict)

		x_label = ax.get_x_axis_label(Text("f [Hz]", font_size=18, color=FG), edge=DOWN, direction=DOWN, buff=0.1)
		y_label = ax.get_y_axis_label(MathTex(r"J_c/J_d", font_size=26, color=FG).rotate(90*DEGREES), edge=LEFT, direction=LEFT, buff=0.2)

		# Regiões de Comportamento
		region_cond = ax.get_area(
			ax.plot(lambda x: 2, x_range=[3, 11]),
			[3, 11],
			bounded_graph=ax.plot(lambda x: 10, x_range=[3, 11]),
			color=C_SIGMA, opacity=0.12
		)
		region_quasi = ax.get_area(
			ax.plot(lambda x: -2, x_range=[3, 11]),
			[3, 11],
			bounded_graph=ax.plot(lambda x: 2, x_range=[3, 11]),
			color=C_GOLD, opacity=0.08
		)
		region_diel = ax.get_area(
			ax.plot(lambda x: -4, x_range=[3, 11]),
			[3, 11],
			bounded_graph=ax.plot(lambda x: -2, x_range=[3, 11]),
			color=C_EPS, opacity=0.12
		)

		# Títulos de cada área alinhados por dentro do gráfico para não dar overflow horizontal
		labels_regioes = VGroup(
			Text("CONDUTOR", font_size=18, color=C_SIGMA, weight=BOLD).move_to(ax.c2p(9, 6)),
			Text("QUASE-CONDUTOR", font_size=18, color=C_OMEGA, weight=BOLD).move_to(ax.c2p(9, 0)),
			Text("DIELÉTRICO", font_size=18, color=C_EPS, weight=BOLD).move_to(ax.c2p(9, -3)),
		)

		self.play(Create(ax), Write(x_label), Write(y_label))
		self.play(FadeIn(region_cond), FadeIn(region_quasi), FadeIn(region_diel), FadeIn(labels_regioes))

		# Funções para plotagem: Ratio = sigma / (2 * pi * f * eps0 * epsr)
		def get_ratio_log(f_exp, sigma, eps_r):
			constant_part = np.log10(sigma / (2 * PI * eps_r * EPS0))
			return constant_part - f_exp

		# Ex 1: Água do mar (sigma=4, eps_r=81)
		graph_mar = ax.plot(
			lambda x: get_ratio_log(x, 4, 81),
			x_range=[3, 11],
			color=C_SIGMA,
			stroke_width=5
		)
		# Colocando os labels próximos das curvas em posições visíveis
		y_mar_label = get_ratio_log(4.5, 4, 81)
		label_mar = Text("Água do Mar", font_size=18, color=C_SIGMA).next_to(ax.c2p(4.5, y_mar_label), UR, buff=0.15)

		# Ex 2: Novo Material (sigma=1e-2, eps_r=10)
		graph_novo = ax.plot(
			lambda x: get_ratio_log(x, 1e-2, 10),
			x_range=[3, 11],
			color=C_EPS,
			stroke_width=5
		)
		y_novo_label = get_ratio_log(4.5, 1e-2, 10)
		label_novo = Text("Novo Material", font_size=18, color=C_EPS).next_to(ax.c2p(4.5, y_novo_label), DL, buff=0.15)

		self.play(Create(graph_mar), Write(label_mar), run_time=2)
		self.play(Create(graph_novo), Write(label_novo), run_time=2)
		self.wait(2.5)

	def cena_4_exercicio_6(self):
		title = Text("Exercício 6: Encontrando H e deduzindo k", font_size=34, color=FG).to_edge(UP)
		self.play(Write(title))

		medium = MathTex(
			r"\sigma=0,\quad \epsilon=\epsilon_0,\quad \mu=\mu_0",
			font_size=24,
			color=C_EPS,
		).to_corner(UL, buff=0.4).shift(DOWN * 0.95)
		e_field = MathTex(r"\vec{E}=10e^{-ikz}\hat{x}", font_size=28).next_to(medium, RIGHT, buff=0.8)
		self.play(Write(medium), Write(e_field))
		self.wait(0.8)

		faraday_text = self.caption("Aplicando o Rotacional 1 (Lei de Faraday)...", color=C_GOLD, font_size=20).to_edge(DOWN, buff=0.25)
		faraday = MathTex(r"\nabla \times \vec{E} = -i\omega\mu_0\vec{H}", font_size=30).move_to(UP * 0.7)
		self.play(FadeIn(faraday_text, shift=RIGHT * 0.1), Write(faraday))
		self.wait(0.5)

		det_e = MathTex(
			r"\nabla\times\vec{E}=\begin{vmatrix}",
			r"\hat{x}&\hat{y}&\hat{z}\\",
			r"\frac{\partial}{\partial x}&\frac{\partial}{\partial y}&\frac{\partial}{\partial z}\\",
			r"10e^{-ikz}&0&0",
			r"\end{vmatrix}",
			font_size=24,
		).move_to(DOWN * 0.35)
		self.play(Write(det_e), run_time=1.5)
		self.wait(0.8)

		surviving_e = MathTex(
			r"\nabla\times\vec{E}=\hat{y}\frac{\partial}{\partial z}(10e^{-ikz})",
			font_size=26,
			color=C_GOLD,
		).move_to(det_e)
		deriv_e = MathTex(
			r"\nabla\times\vec{E}=-i10ke^{-ikz}\hat{y}",
			font_size=28,
			color=C_GOLD,
		).move_to(det_e)
		equal_h = MathTex(
			r"-i10ke^{-ikz}\hat{y}=-i\omega\mu_0\vec{H}",
			font_size=28,
		).move_to(det_e)
		h_result = MathTex(
			r"\vec{H}=\frac{10k}{\omega\mu_0}e^{-ikz}\hat{y}",
			font_size=26,
			color=C_GREEN,
		).to_corner(UR, buff=0.4).shift(DOWN * 0.45)

		self.play(TransformMatchingTex(det_e, surviving_e), run_time=1.2)
		self.play(TransformMatchingTex(surviving_e, deriv_e), run_time=1.2)
		self.play(TransformMatchingTex(deriv_e, equal_h), run_time=1.2)
		self.wait(0.5)
		self.play(TransformMatchingTex(equal_h, h_result), run_time=1.4)
		self.play(Create(self.formula_box(h_result, color=C_GREEN, buff=0.12)[0]))
		self.wait(1.5)

		ampere_text = self.caption("Substituindo H na Lei de Ampère...", color=C_GOLD, font_size=20).move_to(faraday_text)
		ampere = MathTex(r"\nabla \times \vec{H} = i\omega\epsilon_0\vec{E}", font_size=30).move_to(UP * 0.7)
		det_h = MathTex(
			r"\nabla\times\vec{H}=\begin{vmatrix}",
			r"\hat{x}&\hat{y}&\hat{z}\\",
			r"\frac{\partial}{\partial x}&\frac{\partial}{\partial y}&\frac{\partial}{\partial z}\\",
			r"0&\frac{10k}{\omega\mu_0}e^{-ikz}&0",
			r"\end{vmatrix}",
			font_size=24,
		).move_to(DOWN * 0.35)
		surviving_h = MathTex(
			r"\nabla\times\vec{H}=-\hat{x}\frac{\partial}{\partial z}\left(\frac{10k}{\omega\mu_0}e^{-ikz}\right)",
			font_size=24,
			color=C_GOLD,
		).move_to(det_h)
		deriv_h = MathTex(
			r"\nabla\times\vec{H}=i\frac{10k^2}{\omega\mu_0}e^{-ikz}\hat{x}",
			font_size=26,
			color=C_GOLD,
		).move_to(det_h)
		equal_e = MathTex(
			r"i\frac{10k^2}{\omega\mu_0}e^{-ikz}\hat{x}=i\omega\epsilon_0(10e^{-ikz}\hat{x})",
			font_size=24,
		).move_to(det_h)

		self.play(Transform(faraday_text, ampere_text), FadeOut(faraday[0]), FadeIn(ampere), run_time=0.7)
		self.play(Write(det_h), run_time=1.5)
		self.wait(0.8)
		self.play(TransformMatchingTex(det_h, surviving_h), run_time=1.2)
		self.play(TransformMatchingTex(surviving_h, deriv_h), run_time=1.2)
		self.play(TransformMatchingTex(deriv_h, equal_e), run_time=1.2)
		self.wait(0.8)

		deduce_text = self.caption("Igualando com o campo E inicial...", color=C_GOLD, font_size=20).move_to(faraday_text)
		step_k1 = MathTex(r"\frac{k^2}{\omega\mu_0}=\omega\epsilon_0", font_size=30).move_to(equal_e)
		step_k2 = MathTex(r"k^2=\omega^2\mu_0\epsilon_0", font_size=32).move_to(equal_e)
		step_k3 = MathTex(r"k=\omega\sqrt{\mu_0\epsilon_0}", font_size=36, color=C_GREEN).move_to(equal_e).shift(UP*0.2)
		euler_note = self.caption(
			"Para a forma instantânea, aplicamos a conversão de Euler",
			color=C_PURPLE,
			font_size=16,
		).next_to(faraday_text, UP, buff=0.15)

		self.play(Transform(faraday_text, deduce_text), run_time=0.8)
		self.play(TransformMatchingTex(equal_e, step_k1), run_time=1.2)
		self.play(TransformMatchingTex(step_k1, step_k2), run_time=1.2)
		self.play(TransformMatchingTex(step_k2, step_k3), run_time=1.2)
		self.play(Create(self.formula_box(step_k3, color=C_GREEN, buff=0.15)[0]), FadeIn(euler_note, shift=UP * 0.1))
		self.wait(2.0)

	def cena_5_exercicio_4(self):
		header = self.scene_title("Exercício 4: Aplicando os mesmos princípios")
		guide = self.caption("Representação fasorial direta do campo H.", color=C_GOLD, font_size=18).next_to(header, DOWN, buff=0.2)
		self.play(Write(header[0]), FadeIn(guide, shift=UP * 0.1))
		self.wait(0.5)

		definitions = VGroup(
			Text("Dados:", font_size=22, color=C_GOLD),
			MathTex(r"\text{Meio não-magnético: } \mu = \mu_0", font_size=24),
			MathTex(r"\text{Dielétrico perfeito: } \sigma = 0", font_size=24),
			MathTex(r"\epsilon = 4\epsilon_0", font_size=24),
			MathTex(r"\omega = 3109 \, \text{rad/s}", font_size=24)
		).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4).shift(DOWN * 1.5)
		
		defs_box = SurroundingRectangle(definitions, color=C_GOLD, buff=0.2, stroke_width=2, corner_radius=0.1)
		defs_box.set_fill(C_GOLD, opacity=0.05)
		defs_group = VGroup(defs_box, definitions)
		
		self.play(FadeIn(defs_group, shift=RIGHT * 0.2))
		self.wait(1.0)

		inst = MathTex(
			r"h = 50\cos(\omega t-kz)\hat{x} + 100\sin(\omega t-kz)\hat{y}",
			font_size=32,
		).next_to(guide, DOWN, buff=0.45)
		self.play(Write(inst))
		self.wait(0.8)

		phasor_h_simple = MathTex(
			r"\vec{H} = (50\hat{x} - i100\hat{y})e^{-ikz}",
			font_size=32,
			color=C_GREEN,
		).move_to(inst).shift(DOWN * 0.8)

		self.play(TransformFromCopy(inst, phasor_h_simple), run_time=1.2)
		self.wait(1.0)

		summary = RoundedRectangle(corner_radius=0.12, width=10.5, height=1.5, color=C_EPS, stroke_width=2)
		summary.set_fill(C_PANEL, opacity=0.92)
		summary.move_to(DOWN * 2.2)
		summary_text = VGroup(
			Text("Para achar E, aplicamos a Lei de Ampère no dielétrico", font_size=20, color=C_EPS),
			MathTex(r"\sigma=0,\quad \epsilon=4\epsilon_0,\quad \nabla\times\vec{H}=i\omega(4\epsilon_0)\vec{E}", font_size=26),
		).arrange(DOWN, buff=0.15).move_to(summary.get_center())

		fast_label = Text("fast-forward", font_size=20, color=C_RED)
		fast_label.move_to(RIGHT * 4.4 + DOWN * 0.8)
		fast_arrow = Arrow(LEFT, RIGHT * 0.9, color=C_RED, buff=0.0, stroke_width=5).next_to(fast_label, DOWN, buff=0.1)
		matrix_fast = MathTex(
			r"\begin{vmatrix}\hat{x}&\hat{y}&\hat{z}\\ \partial_x&\partial_y&\partial_z\\ 50&-i100&0\end{vmatrix}",
			font_size=22,
			color=C_GOLD,
		).move_to(DOWN * 0.8 + LEFT * 2.2)
		e_fast = MathTex(
			r"\vec{E}=\left(-i\frac{100k}{4\omega\epsilon_0}\hat{x}-\frac{50k}{4\omega\epsilon_0}\hat{y}\right)e^{-ikz}",
			font_size=26,
			color=C_GREEN,
		).move_to(DOWN * 0.8 + LEFT * 1.55)
		e_fast.scale_to_fit_width(6)

		self.play(Create(summary), FadeIn(summary_text, shift=UP * 0.1))
		self.wait(0.5)
		self.play(FadeIn(fast_label), GrowArrow(fast_arrow))
		self.play(FadeIn(matrix_fast, shift=RIGHT * 0.2), run_time=0.6)
		self.play(TransformMatchingTex(matrix_fast, e_fast), run_time=1.2)
		e_fast_box = self.formula_box(e_fast, color=C_GREEN, buff=0.12)[0]
		self.play(Create(e_fast_box))
		self.wait(2.0)

		# Continuação: Determinando k e e(t)
		self.play(
			*[FadeOut(m) for m in [header, defs_group, guide, inst, phasor_h_simple, summary, summary_text, fast_label, fast_arrow, e_fast_box]],
			run_time=1.2
		)

		self.play(e_fast.animate.to_edge(UP, buff=0.4).scale(0.85))
		e_fast_box_small = self.formula_box(e_fast, color=C_GREEN, buff=0.1)[0]
		self.add(e_fast_box_small)
		self.wait(0.5)

		calc_k_title = self.caption("1. Calculando a constante de fase k", color=C_GOLD, font_size=20).next_to(e_fast, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
		eq_k = MathTex(r"k = \omega\sqrt{\mu_0(4\epsilon_0)} = \frac{2\omega}{c}", font_size=28).next_to(calc_k_title, DOWN, buff=0.2).align_to(calc_k_title, LEFT).shift(RIGHT * 0.3)
		eq_k_val = MathTex(r"k = \frac{2(3109)}{3\cdot 10^8} \approx 2.07\cdot 10^{-5}\,\text{rad/m}", font_size=28, color=C_OMEGA).next_to(eq_k, DOWN, buff=0.2).align_to(eq_k, LEFT)

		self.play(FadeIn(calc_k_title, shift=RIGHT * 0.2))
		self.play(Write(eq_k), run_time=1.2)
		self.play(Write(eq_k_val), run_time=1.2)
		self.wait(1.0)

		calc_e_title = MathTex(r"\text{2. Substituindo os valores em }\vec{E}", font_size=20, color=C_GOLD).next_to(eq_k_val, DOWN, buff=0.6).align_to(calc_k_title, LEFT)
		eq_e_final = MathTex(r"\vec{E} = (-i6000\pi\hat{x} - 3000\pi\hat{y})e^{-i 2.07\cdot 10^{-5} z}", font_size=28).next_to(calc_e_title, DOWN, buff=0.2).align_to(calc_e_title, LEFT).shift(RIGHT * 0.3)
		eq_e_approx = MathTex(r"\vec{E} \approx (-i18850\hat{x} - 9425\hat{y})e^{-i 2.07\cdot 10^{-5} z}\,\,[\text{V/m}]", font_size=28, color=C_GREEN).next_to(eq_e_final, DOWN, buff=0.2).align_to(eq_e_final, LEFT)

		self.play(FadeIn(calc_e_title, shift=RIGHT * 0.2))
		self.play(Write(eq_e_final), run_time=1.2)
		self.play(Write(eq_e_approx), run_time=1.2)
		self.wait(1.0)

		time_title = self.caption("3. Convertendo para a forma instantânea (Tempo)", color=C_GOLD, font_size=20).next_to(eq_e_approx, DOWN, buff=0.6).align_to(calc_k_title, LEFT)
		eq_time = MathTex(
			r"\vec{e}(z, t) = 18850\sin(3109 t - 2.07\cdot 10^{-5}z)\hat{x} - 9425\cos(3109 t - 2.07\cdot 10^{-5}z)\hat{y}\,\,[\text{V/m}]",
			font_size=24,
			color=C_PURPLE
		).next_to(time_title, DOWN, buff=0.2).align_to(time_title, LEFT).shift(RIGHT * 0.3)

		self.play(FadeIn(time_title, shift=RIGHT * 0.2))
		self.play(Write(eq_time), run_time=1.5)
		self.wait(2.5)
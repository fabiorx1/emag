import manim as mn
from manim import *        

config.media_width = "75%"
config.verbosity = "ERROR"
print(mn.__version__)

class ForcaLorentz(Scene):
    def construct(self):
        text_carga_q_1 = Tex(
            "Admitindo uma carga $q$ com massa desprezível...",
            font_size=26, color=WHITE)
        self.play(text_carga_q_1.animate.to_corner(UL))
        self.wait()
        
        # Criação dos componentes da carga
        circle = Circle(color=YELLOW, fill_opacity=0.9, radius=0.5)
        label_q = MathTex("q", font_size=24, color=BLACK)
        
        # Vetor velocidade e rótulo (invisíveis inicialmente)
        vec_v = Arrow(start=RIGHT*0.5, end=RIGHT*1.5, color=RED, buff=0).set_opacity(0)
        label_v = MathTex(r"\vec{v}", font_size=24, color=RED).next_to(vec_v, UP, buff=0.1).set_opacity(0)
        
        # Agrupando tudo em um VGroup
        carga_q = VGroup(circle, label_q, vec_v, label_v)
        carga_q.shift(LEFT*2)
        
        # Iniciar o movimento
        def animacao_movimento(mob, dt):
            mob.shift(RIGHT * 2 * dt)
            if mob.get_left()[0] > config.frame_x_radius:
                mob.set_x(-config.frame_x_radius - mob.width)
        
        # Mostra a carga parada na posição inicial definida anteriormente
        self.play(FadeIn(circle), FadeIn(label_q))
        self.wait()
        
        # Adiciona o grupo à cena para gerenciar os vetores e movimento subsequente
        self.add(carga_q)

        text_carga_q_2 = Tex(
            '...movimentando-se a uma velocidade $v$ numa região do espaço.',
            font_size=26, color=WHITE).next_to(text_carga_q_1, DOWN, aligned_edge=LEFT)
        
        self.play(
            Write(text_carga_q_2),
            vec_v.animate.set_opacity(1),
            label_v.animate.set_opacity(1)
        )
        carga_q.add_updater(animacao_movimento)
        self.wait(2)

        text_carga_q_3 = Tex(
            'O que acontece com a carga $q$?',
            font_size=26, color=WHITE).next_to(text_carga_q_2, DOWN, aligned_edge=LEFT)
        self.play(Write(text_carga_q_3))
        self.wait()

        text_carga_q_4 = Tex(
            'A resposta é dada pela força de Lorentz!',
            font_size=26, color=WHITE).next_to(text_carga_q_3, DOWN, aligned_edge=LEFT)
        self.play(Write(text_carga_q_4))
        self.wait()

        formula_forca_lorentz = MathTex(
            r"\vec{F} = q \cdot (\vec{e} + \vec{v} \times \vec{b})",
            font_size=30, color=WHITE).to_edge(DOWN)
        self.play(Write(formula_forca_lorentz))
        self.wait(3)
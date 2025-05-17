
from manim import *
from math import sin, cos, tan, exp, log, sqrt, pi, e, acos, asin, atan, sinh, cosh, tanh

class MyScene(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0.1, 10], 
            y_range=[-4, 4], 
            axis_config={"include_numbers": True}
        )
        try:
            graph = ax.plot(lambda x: log(x), color=BLUE)
            self.play(Create(ax), Create(graph))
        except Exception as e:
            error_text = Text(f"Error: {str(e)}", color=RED)
            self.play(Write(error_text))
        self.wait(2)

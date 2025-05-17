import os
import subprocess
import uuid
import re
from pathlib import Path
from math import sin, cos, tan, exp, log, sqrt, pi, e, acos, asin, atan, sinh, cosh, tanh

# Directory setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MANIM_SCRIPTS_DIR = os.path.join(BASE_DIR, "manim_scripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")

os.makedirs(MANIM_SCRIPTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Allowed functions and constants
ALLOWED_FUNCTIONS = {
    'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'pi', 'e', 
    'acos', 'asin', 'atan', 'sinh', 'cosh', 'tanh'
}
ALLOWED_OPERATORS = set("0123456789+-*/().^x ")

def parse_prompt_to_script(prompt: str) -> str:
    """
    Parses mathematical expressions from the prompt to generate a Manim scene.
    Supports functions like sin, cos, tan, exp, log, sqrt, etc.
    """
    # Extract the mathematical expression from the prompt
    match = re.search(r'y\s*=\s*([a-zA-Z0-9\*\+\-/\(\)\s\.^]+)', prompt, re.IGNORECASE)
    expression = match.group(1).strip() if match else None

    if expression:
        # Replace ^ with ** for exponentiation
        expression = expression.replace("^", "**")

        # Validate the expression
        tokens = re.findall(r'[a-zA-Z_]+|[0-9.]+|[+\-*/^()]', expression)
        for token in tokens:
            if token.isalpha() and token not in ALLOWED_FUNCTIONS and token != 'x':
                raise ValueError(f"Unsupported function or variable: {token}")
            if not all(c in ALLOWED_OPERATORS for c in token) and not token.isalpha():
                raise ValueError(f"Unsupported character in expression: {token}")

        # Adjust x-axis range for functions with restricted domains
        if "log" in expression or "sqrt" in expression:
            x_min = 0.1  # Small positive number to avoid log(0) and sqrt(negative)
            x_max = 10
        else:
            x_min = -4
            x_max = 4

        # Generate the Manim scene code
        return f"""
from manim import *
from math import sin, cos, tan, exp, log, sqrt, pi, e, acos, asin, atan, sinh, cosh, tanh

class MyScene(Scene):
    def construct(self):
        ax = Axes(
            x_range=[{x_min}, {x_max}], 
            y_range=[-4, 4], 
            axis_config={{"include_numbers": True}}
        )
        try:
            graph = ax.plot(lambda x: {expression}, color=BLUE)
            self.play(Create(ax), Create(graph))
        except Exception as e:
            error_text = Text(f"Error: {{str(e)}}", color=RED)
            self.play(Write(error_text))
        self.wait(2)
"""
    else:
        # Fallback for non-mathematical prompts
        return f"""
from manim import *

class MyScene(Scene):
    def construct(self):
        text = Text("{prompt}", color=WHITE)
        self.play(Write(text))
        self.wait(2)
"""


def generate_manim_output(prompt: str, output_type: str) -> str:
    """
    Generates a Manim output (video or image) and returns the relative file path for the web frontend.
    Supports both mathematical and text-based prompts.
    """
    try:
        scene_code = parse_prompt_to_script(prompt)
    except ValueError as e:
        raise RuntimeError(f"Invalid expression in prompt: {str(e)}")

    scene_id = str(uuid.uuid4())[:8]
    script_path = os.path.join(MANIM_SCRIPTS_DIR, f"{scene_id}.py")

    # Save the generated script to the file
    with open(script_path, "w") as f:
        f.write(scene_code)

    # Render command
    render_cmd = [
        "manim",
        script_path,
        "MyScene",
        "-pql",  # Low quality for faster generation
        f"--output_file={scene_id}"
    ]

    if output_type == "image":
        render_cmd.append("--save_last_frame")

    try:
        # Run the rendering command
        result = subprocess.run(render_cmd, cwd=OUTPUT_DIR, capture_output=True, text=True)

        # Check if there was an error during rendering
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            raise RuntimeError(f"Manim rendering failed: {result.stderr}")

    except Exception as e:
        print(f"Error during rendering: {e}")
        raise RuntimeError(f"Failed to render the output: {str(e)}")

    # Find the output file
    media_path = Path(OUTPUT_DIR)
    ext = "png" if output_type == "image" else "mp4"
    output_file = None

    for root, dirs, files in os.walk(media_path):
        for file in files:
            if file.endswith(ext) and scene_id in file:
                output_file = os.path.relpath(os.path.join(root, file), BASE_DIR).replace("\\", "/")
                break

    if not output_file:
        raise FileNotFoundError(f"Could not find generated {ext} file for {scene_id}")

    return f"/{output_file}",

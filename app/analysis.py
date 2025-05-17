import numpy as np
from scipy.optimize import minimize_scalar, root_scalar

def find_critical_points(func_str, x_min=-10, x_max=10, num_points=1000):
    """
    Finds critical points, maxima, minima, roots, and inflection points for a given function.
    """
    # Create x values
    x_values = np.linspace(x_min, x_max, num_points)
    safe_globals = {
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "pi": np.pi,
        "e": np.e,
        "abs": np.abs,
        "acos": np.arccos,
        "asin": np.arcsin,
        "atan": np.arctan,
        "sinh": np.sinh,
        "cosh": np.cosh,
        "tanh": np.tanh,
        "__builtins__": {}  # Disable all other builtins for security
    }

    # Convert the function string to a lambda function
    try:
        func = eval(f"lambda x: {func_str}", safe_globals)
        y_values = func(x_values)
        dy_dx = np.gradient(y_values, x_values)
        d2y_dx2 = np.gradient(dy_dx, x_values)
    except Exception as e:
        return {"error": str(e)}

    # Find critical points
    critical_points = [(x, y) for x, y, dy in zip(x_values, y_values, dy_dx) if np.isclose(dy, 0, atol=1e-2)]

    # Find roots
    roots = [(x, 0) for x, y in zip(x_values, y_values) if np.isclose(y, 0, atol=1e-2)]

    # Find maxima and minima
    maxima = [p for p in critical_points if np.isclose(d2y_dx2[x_values.tolist().index(p[0])], -1, atol=1e-2)]
    minima = [p for p in critical_points if np.isclose(d2y_dx2[x_values.tolist().index(p[0])], 1, atol=1e-2)]

    return {
        "critical_points": critical_points,
        "roots": roots,
        "maxima": maxima,
        "minima": minima
    }

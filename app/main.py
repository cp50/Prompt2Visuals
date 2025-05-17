from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.utils import generate_manim_output
from app.analysis import find_critical_points  # Import the analysis module
from .websocket import manager
import os
import numpy as np

app = FastAPI()

# Enable CORS for WebSocket support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/generated", StaticFiles(directory=os.path.join(BASE_DIR, "generated")), name="generated")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Route for the main home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route for the 2D interactive plot
@app.get("/interactive")
async def get_interactive_plot(request: Request):
    return templates.TemplateResponse("interactive_plot.html", {"request": request})

# Route for the 3D interactive plot
@app.get("/interactive3d")
async def get_interactive_3d_plot(request: Request):
    return templates.TemplateResponse("interactive_plot_3d.html", {"request": request})

# Route for Manim file generation
@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, prompt: str = Form(...), output: str = Form(...)):
    file_url = generate_manim_output(prompt, output)
    
    # Make the file URL relative to the server root
    if isinstance(file_url, tuple):
        file_url = file_url[0]
    
    # Ensure the URL starts with /generated/
    if not file_url.startswith("/generated/"):
        file_url = f"/generated/{file_url}"
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "prompt": prompt,
        "output": output,
        "file_url": file_url
    })

# WebSocket endpoint for 2D plotting and analysis
@app.websocket("/ws/plot")
async def websocket_endpoint_2d(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("📝 Received from client (2D):", data)

            # Extract function and parameters
            func = data['function']
            params = data['parameters']
            A = params.get('amplitude', 1)
            f = params.get('frequency', 1)
            phi = params.get('phase', 0)
            analyze = params.get('analyze', False)

            try:
                safe_globals = {
                    "sin": np.sin,
                    "cos": np.cos,
                    "tan": np.tan,
                    "exp": np.exp,
                    "log": np.log,
                    "sqrt": np.sqrt,
                    "pi": np.pi,
                    "e": np.e,
                    "acos": np.arccos,
                    "asin": np.arcsin,
                    "atan": np.arctan,
                    "sinh": np.sinh,
                    "cosh": np.cosh,
                    "tanh": np.tanh,
                    "abs": np.abs,
                    "__builtins__": {}  # Disable all other builtins for security
                }

                # Generate the 2D data
                x = np.linspace(-10, 10, 1000)
                expression = f"{A} * ({func.replace('x', f'({f} * x + {phi})')})"
                print("🔍 Evaluating expression:", expression)

                # Evaluate function
                y = eval(f"lambda x: {expression}", safe_globals)(x)

                # Prepare the response
                response = {
                    'type': '2d',
                    'x': x.tolist(),
                    'y': y.tolist()
                }

                # Perform analysis if requested
                if analyze:
                    analysis_result = find_critical_points(expression)
                    response["analysis"] = analysis_result
                    print("🔍 Analysis results:", analysis_result)

                # Send the data back to the client
                await websocket.send_json(response)
                print("✅ Data sent to client")

            except Exception as e:
                print("❌ Error (2D):", e)
                await websocket.send_json({
                    'error': str(e)
                })

    except WebSocketDisconnect:
        print("🔌 Client disconnected (2D)")
        manager.disconnect(websocket)

# WebSocket endpoint for 3D plotting
@app.websocket("/ws/plot3d")
async def websocket_endpoint_3d(websocket: WebSocket):
    try:
        # Accept the WebSocket connection
        await websocket.accept()
        print("🟢 3D WebSocket connection accepted")

        while True:
            data = await websocket.receive_json()
            print("📝 Received from client (3D):", data)

            # Extract function and parameters
            func = data['function']
            params = data['parameters']
            A = params.get('amplitude', 1)
            f = params.get('frequency', 1)
            phi = params.get('phase', 0)

            try:
                safe_globals = {
                    "sin": np.sin,
                    "cos": np.cos,
                    "tan": np.tan,
                    "exp": np.exp,
                    "log": np.log,
                    "sqrt": np.sqrt,
                    "pi": np.pi,
                    "e": np.e,
                    "acos": np.arccos,
                    "asin": np.arcsin,
                    "atan": np.arctan,
                    "sinh": np.sinh,
                    "cosh": np.cosh,
                    "tanh": np.tanh,
                    "abs": np.abs,
                    "__builtins__": {}  # Disable all other builtins for security
                }

                x = np.linspace(-10, 10, 50)
                y = np.linspace(-10, 10, 50)
                X, Y = np.meshgrid(x, y)
                Z = eval(f"lambda x, y: {A} * ({func.replace('x', '(x)').replace('y', '(y)')})", safe_globals)(X, Y)

                # Send data back to client
                await websocket.send_json({
                    'type': '3d',
                    'x': X.tolist(),
                    'y': Y.tolist(),
                    'z': Z.tolist()
                })
                print("✅ 3D plot data sent")

            except Exception as e:
                print("❌ Error (3D):", e)
                await websocket.send_json({
                    'error': str(e)
                })

    except WebSocketDisconnect:
        print("🔌 3D Client disconnected")

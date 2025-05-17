
# 🌐 Prompt2Visuals

An **AI-powered** interactive math visualization and animation generator built with **FastAPI**, **Manim**, and **Plotly**. This project allows you to create stunning 2D and 3D math visualizations, generate animations, and export them as **videos** or **images** using simple mathematical expressions.

---

## 📌 **Features**
- **Real-time 2D and 3D Plot Visualization:** Explore mathematical functions in real-time.
- **AI-Powered Function Analysis:** Automatically find critical points, roots, maxima, and minima.
- **Dynamic Plot Controls:** Adjust amplitude, frequency, and phase for precise function tuning.
- **Generate Animations:** Create **MP4** videos and **PNG** images from prompts.
- **Responsive and Modern UI:** Clean, professional design with dark mode support.
- **Interactive Modes:** Switch between 2D and 3D visualizations seamlessly.
- **Customizable Themes:** Light and dark modes with smooth transitions.

---

## 🚀 **Getting Started**

### **Prerequisites**
Make sure you have the following installed:
- Python 3.9 or higher
- **Manim** (Community Edition)
- **Node.js** (for frontend development, optional)

### **Installation Steps**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Prompt2Visuals.git
   cd Prompt2Visuals
   ```

2. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the Web App:**
   - Open **http://localhost:8000** in your browser.

---

## 📦 **Directory Structure**
```
Prompt2Visuals/
│
├── app/
│   ├── main.py           # FastAPI server
│   ├── utils.py          # Manim file generator
│   ├── analysis.py       # AI-powered function analysis
│   └── websocket.py      # WebSocket management
│
├── templates/
│   ├── index.html        # Main landing page
│   ├── interactive_plot.html   # 2D interactive plot page
│   ├── interactive_plot_3d.html # 3D interactive plot page
│   └── result.html       # Output result display
│
├── static/
│   └── css/
│       └── style.css     # Custom styles
│
├── generated/            # Generated videos and images
│
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Ignored files and directories
```

---

## 🖼️ **Screenshots**
- **Landing Page:** ![Landing Page](./screenshots/landing_page.png)
- **2D Interactive Mode:** ![2D Mode](./screenshots/2d_mode.png)
- **3D Interactive Mode:** ![3D Mode](./screenshots/3d_mode.png)
- **AI Analysis Results:** ![Analysis](./screenshots/analysis_results.png)

---

## 📚 **Usage Examples**
- **2D Function:** `y = sin(x)`
- **3D Function:** `z = sin(x) * cos(y)`
- **Advanced Expression:** `y = exp(-x**2) * sin(5*x)`

---

## 🛠️ **Future Improvements**
- Enhanced AI function analysis
- Support for multi-variable functions
- Mobile application (React Native)
- Plugin support for additional math libraries

---

## 🤝 **Contributing**
Contributions are welcome! Feel free to fork the repo and submit a pull request. 😊

---

## 📬 **Contact**
For any queries or feedback, please reach out at **chrispaul68002@gmail.com**.

---

### ⭐ **Don't forget to star the repo if you find it useful!**

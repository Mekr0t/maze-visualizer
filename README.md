![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

# Maze Visualizer

A Python-based application for **generating and solving mazes** with different algorithms.  
Includes a graphical user interface (GUI) built with Tkinter for interactive visualization.

---

## ✨ Features
- Multiple **maze generation algorithms**
- Multiple **maze solving algorithms**
- Adjustable **speed control** for generation and solving.
- Start and goal selection.
- Visual feedback of maze paths and solutions.


---

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/Mekr0t/maze-visualizer.git
cd maze-visualizer
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python main.py
```

---

## ⚙️ Project Structure
```
maze-visualizer/
│── algorithms         # Maze generation and solver algorithms
│── gui/               # Tkinter GUI controls and canvas
│── maze/              # Plug-in registry and core data container
│── utils/             # Helper functions, colors, etc.
│── main.py            # Entry point
│── requirements.txt   # Dependencies
│── README.md
```

---

## 📚 Algorithms Implemented
### Maze Generation
- Depth-First Search (Recursive Backtracker)
- Prim’s Algorithm
- Recursive Division
- Kruskal Algorithm

### Maze Solving
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- A* Search
- Dijkstra (Uniform-cost search solver)

---

## 🛠️ Requirements
- Python 3.10+
- Tkinter (comes with standard Python installation)
- Numpy 1.24+

---

## 📜 License
MIT License – free to use and modify.

---

## 👨‍💻 Author
Developed by [Mekr0t](https://github.com/Mekr0t).

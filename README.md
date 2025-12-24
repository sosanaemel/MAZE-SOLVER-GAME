# 🌀 Dual Path Maze Challenge 🌀

## Project Description
This project is a **random maze game** where the player competes against an **AI** to reach the maze's end first.  
Key features include:

- Randomly generated maze for each round.
- **Start point with two or more paths** to choose from.
- Player movement using keyboard arrows (`Up`, `Down`, `Left`, `Right`).
- AI uses **Breadth-First Search (BFS)** to find the shortest path to the end.
- Graphical display using **Tkinter Canvas**.
- Tracks both player and AI paths, highlighting **shared cells** in yellow.
- User interface shows **stats, results, and game state messages**.
- Supports **multiple rounds** with score tracking for both player and AI.

---

## 🛠️ Requirements

- Python **3.10.0** (required for full compatibility)
- `tkinter` (comes pre-installed with Python)
- `queue` (standard Python library)
- Any Python-supported editor/IDE (e.g., VS Code, PyCharm)

---

## ⚡ How to Run

1. Make sure **Python 3.10.0** is installed.
2. Clone the repository or copy the project files.
3. Open terminal inside the project folder.
4. Run the main file:

```bash
python main.py
The game window will appear. Use the arrow keys to move the player.

🖌️ Game Controls
Move Player: Arrow keys ↑ ↓ ← →

New Maze Button: Generate a new maze.

Reset Round Button: Restart the current round with the same maze.

🧩 Technical Notes
Maze represented as a matrix (List[List[str]]):

# = Wall

O = Start point

X = End point

= Open path

AI uses Breadth-First Search (BFS) to find the shortest path.

Player loses immediately if hitting a wall.

Cells shared by both player and AI are highlighted in yellow with an ✕.

🎨 Interface Colors
Walls: Dark Blue (#1E3A8A)

Player Path: Light Blue (#60A5FA)

AI Path: Light Red (#FCA5A5)

End Point: Coral Red (#FF6B6B)

Start Point: Light Blue (#3B82F6)

Shared Cells: Yellow (#FBBF24)

📚 Gameplay Instructions
Choose a path from the start point.

Avoid walls to reach the end.

Try to beat the AI to the finish line.

Track your steps and compare with the AI.

⚙️ Future Improvements
Add multiple difficulty levels.

Implement A* algorithm to optimize AI.

Mouse controls for path selection.

Add sound effects for moves, wins, and losses.

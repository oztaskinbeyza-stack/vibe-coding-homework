# Python Tetris Game (Pygame)

A fully functional Tetris game implemented in Python using the Pygame library. This project explores the "Vibe Coding" paradigm by using AI-powered development tools for logic and UI structure.

## 🚀 Project Features
* **Grid Layout**: Standard 10x20 game grid.
* **Classic Pieces**: Includes all 7 Tetrominoes (I, O, T, S, Z, J, L) with distinct colors.
* **Scoring & Levels**: 100 points per line with multipliers for multiple lines (3x, 5x, 8x).
* **Progression**: Difficulty levels increase every 10 lines cleared.
* **Enhanced UI**: Includes real-time score, level tracker, lines cleared counter, and a "Next Piece" preview.

## 🛠️ Technologies Used
* **Python**: Core programming language.
* **Pygame**: Library used for graphics and input handling.
* **Cursor**: AI-first code editor used for development.

## 🕹️ Controls
* **Left/Right Arrows**: Move piece horizontally.
* **Down Arrow**: Fast drop.
* **Up Arrow / Space**: Rotate piece.
* **P Key**: Pause / Unpause the game.
* **R Key**: Restart game after Game Over.

---

# 🐳 Tetris (Pygame) — Dockerization (Homework Section)

This section provides instructions on how to build and run the Tetris game within a Docker container, as required for the dockerization assignment.

## ⚙️ Quick Start

### 1. Build the Image
Open your terminal in the project directory and run:
```bash
docker build -t tetris-pygame .
(This command uses the provided Dockerfile to install dependencies and package the app.)

2. Run the Container (GUI Support)
Windows (WSLg) — Simplest on Windows:

Bash

docker run --rm -it -e DISPLAY=$DISPLAY tetris-pygame
Linux (X11):

Bash

xhost +local:docker
docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  tetris-pygame
xhost -local:docker
🛠️ Technical Details (What the Dockerfile does)
Base Image: Uses python:3.11-slim to minimize image size.

SDL2 Dependencies: Installs libsdl2, libgl1, and other runtime libraries required for Pygame graphics/audio.

Non-root User: Runs the game as appuser instead of root for better security practices.

Optimization: Includes a .dockerignore file to exclude unnecessary files like __pycache__ and venv from the build.

Dependency Management: Uses requirements.txt to pin the pygame version to 2.5.2.

✅ Submission Checklist
[x] Dockerfile properly configured.

[x] requirements.txt with dependencies.

[x] .dockerignore to keep image clean.

[x] README.md updated with Docker run instructions.

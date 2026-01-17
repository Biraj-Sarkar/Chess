# ♟️ Chess ML Engine – CNN + Minimax

A playable chess engine that uses a **Convolutional Neural Network (CNN)** to evaluate board positions and a **Minimax search algorithm** to choose moves.  
The project demonstrates how a learned evaluation function can be integrated into a classical game-playing engine.

---

## 🚀 Features

- Play a full game of chess against an AI
- CNN-based position evaluation (White better / Equal / Black better)
- Minimax search with configurable depth
- Legal move generation using `python-chess`
- Interactive UI built with Streamlit
- Clean separation between ML, engine logic, and UI

---

## 🧠 Architecture Overview
Chess/  
├── engine/ # Chess engine (Minimax + move selection)  
├── ml/ # ML inference + board encoding  
├── models/ # Trained CNN model (.keras)  
├── ui/ # Streamlit UI  
├── chess.ipynb # Training & experimentation notebook  
└── requirements.txt


### Core Components

- **CNN Evaluator**
  - Input: 8×8×17 tensor representation of the board
  - Output: Probabilities for {Black better, Equal, White better}

- **Engine**
  - Uses Minimax search
  - CNN provides evaluation at leaf nodes
  - Supports adjustable depth

- **UI**
  - Streamlit-based interactive chess interface
  - Dropdown-based move selection (legal moves only)
  - Real-time board updates

---

## 📊 Board Representation

Each position is encoded as a tensor with:
- 12 planes for piece types (6 white + 6 black)
- 1 plane for side to move
- 4 planes for castling rights

---

## 🏋️ Model Training

Training and experimentation are done in `chess.ipynb`:
- PGN parsing
- Stockfish-based position labeling
- Handling class imbalance
- CNN training and evaluation
- Confusion matrix analysis

The notebook outputs a trained model:  
> models/chess_cnn_evaluator.keras

---

## 🚀 Live Demo
👉 https://aichess.streamlit.app/

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run ui/app.py
```

### 3. Play
* Select a legal move from the dropdown
* Click Play Move
* The AI responds automatically

---

## ⚙️ Configuration
* Minimax depth can be adjusted in app.py
* Lower depth → faster, weaker play
* Higher depth → slower, stronger play

--- 

## 📌 Limitations (v1)
* UI uses Streamlit (no drag-and-drop board)
* CNN predicts coarse evaluation categories, not centipawn values
* No alpha–beta pruning (yet)
* These are intentional design choices for clarity and learning.

---

## 🔮 Future Improvements
* Alpha–beta pruning for faster search
* Regression-based evaluator (centipawn prediction)
* Clickable/drag-and-drop UI
* Full-stack deployment (React + FastAPI)
* Self-play training

---

## 👨‍💻 Author

Built as a learning-focused ML + systems project to explore how neural networks can be combined with classical algorithms in game AI.

---
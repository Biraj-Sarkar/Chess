# ♟️ Chess Engine with CNN Evaluation & Negamax Search

A full-stack chess engine that combines a Convolutional Neural Network (CNN) for position evaluation with a classical Negamax search algorithm.
The project focuses on integrating machine learning into a traditional game-search pipeline rather than competing with professional engines.

---

## 🚀 Features

- Play a full game of chess against an AI
- CNN-based position evaluation
- Negamax search with:
  - Alpha–beta pruning
  - Quiescence search
  - Transposition table
  - Iterative deepening
- Legal move generation using `python-chess`
- FastAPI backend with REST API
- React-based frontend chessboard UI
- Interactive UI built with Streamlit (v1.0)
- Clean separation between ML, engine logic, and UI

---

## 🧠 Architecture Overview
Backend/  
├── api/ # FastAPI server  
├── engine/ # Chess engine (Negamax + quiescence search + move selection + Game flow logic)  
├── ml/ # ML inference + board encoding  (Tensorflow)  
├── models/ # Trained CNN model (.keras)  
├── ui/ # Streamlit UI (v1.0)  
├── utils/ # Normalize FEN  
├── chess.ipynb # Training & experimentation notebook  
└── requirements.txt


### Core Components

**CNN Evaluator**
  - Input: 8×8×17 tensor representation of the board
  - Encodes:
    - 12 piece planes (6 white + 6 black)
    - 1 side-to-move plane
    - 4 castling-rights planes
  - Output: Scalar evaluation
    - Positive → White is better
    - Negative → Black is better

The CNN is only used at leaf nodes (and in quiescence), not during the full search.

**Engine**
  - Negamax formulation (single-perspective minimax)
  - Alpha–beta pruning
  - Quiescence search for capture stability
  - Transposition table with normalized FEN keys
  - Iterative deepening with time control
  
This design mirrors how real chess engines are structured, though simplified.

**Backend (FastAPI)**
- Endpoint:
  ```bash
  POST /move
  ```
- Input:
  ```bash
  {
    "fen": "...",
    "move": "e2e4",
    "max_time": 1.0
  }
  ```
- Output:
  ```bash
  {
    "fen": "...",
    "ai_move": "c7c5"
  }
  ```
- CNN model is lazy-loaded
- Evaluation results are cached for performance

**UI**
  - Streamlit-based interactive chess interface
  - Dropdown-based move selection (legal moves only)
  - Real-time board updates

**Frontend (React)**
- Interactive chessboard
- Legal-move enforcement
- Promotion handling
- AI responds automatically after user move
- Communicates with backend via REST API

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
👉 https://aichess.streamlit.app/  

---

## ▶️ How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Run the streamlit application
```bash
cd backend
streamlit run ui/app.py
```

### Run the frontend application
```bash
cd frontend
npm install
npm run dev
```

---

## ⚙️ Configuration
* AI thinking time is configurable per move
* Longer time → deeper search → stronger play
* Shorter time → faster but weaker play

--- 

## 📌 Limitations (v2)
* Written in Python, not C++
* CNN evaluation is slower than NNUE-style models
* No opening book or endgame tablebases
* Not intended to compete with Stockfish or Chess.com engines

This project prioritizes clarity, correctness, and learning over raw playing strength.

---

## 🔮 Future Improvements
* Opening book integration
* Killer moves & history heuristics
* NNUE-style evaluator
* Endgame tablebases
* C++ engine core
* Self-play training
* Stronger evaluation targets (centipawn regression)

---

## 👨‍💻 Author

Built as a learning-focused project to explore how machine learning models can be integrated into classical game-search algorithms, with an emphasis on clean architecture and correctness.

---
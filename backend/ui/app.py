import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import chess
import chess.svg
import base64

from engine import choose_move

st.set_page_config(page_title="Chess ML Engine", layout="centered")

st.title("♟️ Play Chess vs ML Engine")

# ---------------------------
# Session state initialization
# ---------------------------
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "awaiting_ai" not in st.session_state:
    st.session_state.awaiting_ai = False

# ---------------------------
# Helper to render SVG board
# ---------------------------
def render_board(board):
    svg = chess.svg.board(board, size=350)
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/svg+xml;base64,{b64}"/>
    </div>
    """
    st.write(html, unsafe_allow_html=True)

# ---------------------------
# Display board
# ---------------------------
render_board(st.session_state.board)

# ---------------------------
# Game status
# ---------------------------
if st.session_state.board.is_game_over():
    st.success(f"Game Over: {st.session_state.board.result()}")
    if st.button("Reset Game"):
        st.session_state.board = chess.Board()
        st.rerun()
    st.stop()

# ---------------------------
# Human move input
# ---------------------------
st.write("### Your Move (UCI format)")

board = st.session_state.board
legal_moves = list(board.legal_moves)

# Convert to SAN for display
move_map = {board.san(move): move for move in legal_moves}

selected_san = st.selectbox(
    "Select a move",
    options=list(move_map.keys()),
    key=board.fen()
)

if st.button("Play Move"):
    board = st.session_state.board

    move = move_map[selected_san]
    board.push(move)

    # Check game over after human move
    if board.is_game_over():
        st.session_state.board = board
        st.success(f"Game Over: {board.result()}")
        st.rerun()
        st.stop()

    st.session_state.board = board
    st.session_state.awaiting_ai = True
    st.rerun()

# ---------------------------
# AI move
# ---------------------------
if st.session_state.awaiting_ai:
    board = st.session_state.board

    with st.spinner("AI is thinking..."):
        ai_move = choose_move(board, 1.0)

    if ai_move is not None:
        board.push(ai_move)

    st.session_state.board = board
    st.session_state.awaiting_ai = False
    st.rerun()

# ---------------------------
# Reset button
# ---------------------------
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    st.rerun()

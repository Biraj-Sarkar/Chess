import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js'
import { useState, useRef } from 'react';
import { playMove } from "./services/api.js";

export default function App() {
    // ---------------------------
    // Chess state
    // ---------------------------
    const gameRef = useRef(new Chess())
    const game = gameRef.current

    const [fen, setFen] = useState(game.fen());
    const [isThinking, setIsThinking] = useState(false);

    // Click-move helpers
    const [moveFrom, setMoveFrom] = useState('');
    const [optionSquares, setOptionSquares] = useState({});

    // Promotion state
    const [pendingPromotion, setPendingPromotion] = useState(null);     // { from, to, fenBeforeMove }

    // Game Result
    const [gameResult, setGameResult] = useState(null);                 // 'win', 'lose', 'draw'

    // Difficulty
    const [difficulty, setDifficulty] = useState("medium");

    // AI time based on difficulty
    const difficultyTime = {
        easy: 0.3,
        medium: 0.8,
        hard: 1.5
    }

    // ---------------------------
    // Check Game Result
    // ---------------------------
    function checkGameOver() {
        if (game.isCheckmate()) {
            setGameResult(game.turn() === 'w' ? 'lose' : 'win');
        } else if (game.isDraw() || game.isStalemate() || game.isThreefoldRepetition()) {
            setGameResult('draw');
        }
    }

    // ---------------------------
    // Helpers
    // ---------------------------
    function getPromotionPosition(square) {
        const squareEl = document.querySelector(
            `[data-square="${square}"]`
        );

        if (!squareEl) {
            // Fallback positioning
            const col = square.charCodeAt(0) - 'a'.charCodeAt(0);
            const squareSize = 60; // approximate
            return { left: col * squareSize, top: 0 };
        }

        const boardEl = squareEl.closest('[class*="chessboard"]');
        if (!boardEl) return { left: 0, top: 0 };

        const squareRect = squareEl.getBoundingClientRect();
        const boardRect = boardEl.getBoundingClientRect();

        return {
            left: squareRect.left - boardRect.left,
            top: squareRect.top - boardRect.top,
            width: squareRect.width
        };
    }

    function isPromotionMove(from, to) {
        const piece = game.get(from);
        if (!piece || piece.type !== "p") return false;

        const rank = to[1];
        return (
            (piece.color === "w" && rank === "8") ||
            (piece.color === "b" && rank === "1")
        );
    }

    function getPromotionSquareStyle(square) {
        return {
            background: "rgba(255,255,255,0.95)",
            display: "grid",
            gridTemplateRows: "repeat(4, 1fr)",
            zIndex: 10,
        };
    }

    // ---------------------------
    // Backend AI call
    // ---------------------------
    const handleAIMove = async (humanMoveUci, fenBeforeMove) => {
        setIsThinking(true)

        try {
            const data = await playMove(fenBeforeMove, humanMoveUci, difficultyTime[difficulty])
            gameRef.current.load(data.fen)
            setFen(data.fen)
            checkGameOver()
        } catch (err) {
            console.error(err);
            alert("AI move failed");
        } finally {
            setIsThinking(false)
        }
    }

    // ---------------------------
    // Drag & drop
    // ---------------------------
    function onPieceDrop({sourceSquare, targetSquare}) { 
        if (!targetSquare) {
            return false;
        }

        if (isThinking || pendingPromotion) return false;

        const fenBeforeMove = game.fen();

        if (isPromotionMove(sourceSquare, targetSquare)) {
            setPendingPromotion({
                from: sourceSquare,
                to: targetSquare,
                fenBeforeMove,
            });
            return true;
        }

        const move = game.move({
            from: sourceSquare,
            to: targetSquare,
            promotion: "q",
        })

        if (move === null) {
            return false;
        }

        setFen(game.fen());
        setMoveFrom('');
        setOptionSquares({});

        checkGameOver();

        handleAIMove(sourceSquare + targetSquare, fenBeforeMove);

        return true;
    }

    // ---------------------------
    // Click to move
    // ---------------------------
    function getMoveOptions(square) {
        const piece = game.get(square);
        
        if (!piece || piece.color !== game.turn()) {
            setOptionSquares({});
            return false;
        }

        const moves = game.moves({
            square,
            verbose: true
        })

        if (moves.length === 0) {
            setOptionSquares({});
            return false;
        }

        const newSquares = {};

        for (const move of moves) {
            newSquares[move.to] = {
                background: game.get(move.to) && game.get(move.to)?.color !== game.get(square)?.color 
                    ? 'radial-gradient(circle, rgba(0,0,0,.1) 85%, transparent 85%)'
                    : 'radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)',
                borderRadius: '50%'
            }
        }

        newSquares[square] = {background: 'rgba(255, 255, 0, 0.4)'};

        setOptionSquares(newSquares)
        return true;
    }

    function onSquareClick({square, piece}) {
        if (pendingPromotion || isThinking) return;

        if (!moveFrom && piece) {
            if (getMoveOptions(square)) setMoveFrom(square);
            return;
        }

        if (!moveFrom && !piece) {
            setOptionSquares({});
            return;
        }

        const moves = game.moves({
            square: moveFrom,
            verbose: true
        })

        const foundMove = moves.find(m => m.from === moveFrom && m.to === square);

        if (!foundMove) {
            const hasMoveOptions = getMoveOptions(square);
            setMoveFrom(hasMoveOptions ? square : '');
            return;
        }

        const fenBeforeMove = game.fen();

        if (isPromotionMove(moveFrom, square)) {
            setPendingPromotion({
                from: moveFrom,
                to: square,
                fenBeforeMove
            });
            setMoveFrom("");
            setOptionSquares({});
            return;
        }
        
        const move = game.move({
            from: moveFrom,
            to: square,
            promotion: 'q'
        })

        if (move === null) {
            const hasMoveOptions = getMoveOptions(square);
            if (hasMoveOptions) {
                setMoveFrom(square);
            }
            return;
        }

        setFen(game.fen());
        setMoveFrom('');
        setOptionSquares({});

        checkGameOver();

        handleAIMove(moveFrom + square, fenBeforeMove);
    }

    // ---------------------------
    // Promotion choice handler
    // ---------------------------
    function handlePromotionChoice(piece) {
        const { from, to, fenBeforeMove } = pendingPromotion;

        game.load(fenBeforeMove);

        const move = game.move({
            from,
            to,
            promotion: piece,
        });

        if (!move) {
            setPendingPromotion(null);
            return;
        }

        setFen(game.fen());
        setPendingPromotion(null);

        checkGameOver();

        const uciMove = from + to + piece;
        handleAIMove(uciMove, fenBeforeMove);
    }

    // ---------------------------
    // Chess Board Options
    // ---------------------------
    const chessboardOptions = {
        onPieceDrop,
        onSquareClick,
        position: fen,
        squareStyles: optionSquares,
        arePiecesDraggable: !isThinking && !pendingPromotion,
    };

    const pieceSymbols = {
        w: { q: "♕", r: "♖", b: "♗", n: "♘" },
        b: { q: "♛", r: "♜", b: "♝", n: "♞" }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 p-4">
            <div className="w-full max-w-2xl">
                <div className="flex justify-center gap-4 mb-4">
                    <label className="text-white font-semibold">
                        Difficulty:
                    </label>

                    <select
                        value={difficulty}
                        onChange={(e) => setDifficulty(e.target.value)}
                        className="px-3 py-1 rounded bg-gray-800 text-white border border-gray-600"
                    >
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                </div>
                <div className="bg-white p-4 rounded-xl shadow-xl relative"> 
                    <Chessboard options={chessboardOptions} />
                    
                    {/* Promotion UI */}
                    {pendingPromotion && (
                        <>
                            {/* Semi-transparent overlay */}
                            <div
                                className="absolute inset-0 z-40 rounded-xl"
                                onClick={() => setPendingPromotion(null)}
                                onContextMenu={(e) => {
                                    e.preventDefault();
                                    setPendingPromotion(null);
                                }}
                            />

                            {/* Promotion selector - positioned at target square */}
                            <div
                                className="absolute z-50 bg-white rounded-lg shadow-2xl border-4 border-blue-500"
                                style={{
                                    left: `${getPromotionPosition(pendingPromotion.to).left}px`,
                                    top: `${getPromotionPosition(pendingPromotion.to).top}px`,
                                    width: `${getPromotionPosition(pendingPromotion.to).width || 60}px`,
                                }}
                            >
                                {["q", "r", "b", "n"].map((p) => {
                                    const color = game.get(pendingPromotion.from)?.color || 'w';
                                    return (
                                        <button
                                            key={p}
                                            className="w-full aspect-square flex items-center justify-center hover:bg-blue-100 transition-colors border-b last:border-b-0 border-gray-200"
                                            onClick={() => handlePromotionChoice(p)}
                                            onContextMenu={(e) => e.preventDefault()}
                                        >
                                            <span className="text-5xl text-black">
                                                {pieceSymbols[color][p]}
                                            </span>
                                        </button>
                                    );
                                })}
                            </div>
                        </>
                    )}

                    {/* Thinking indicator */}
                    {isThinking && (
                        <div className="absolute inset-0 flex items-center justify-center rounded-xl z-30">
                            <div className="bg-white px-6 py-3 rounded-lg shadow-lg">
                                <p className="text-lg text-yellow-700 font-semibold">AI is thinking ({difficulty})...</p>
                            </div>
                        </div>
                    )}

                    {/* Game Result Overlay */}
                    {gameResult && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center bg-opacity-50 rounded-xl z-30">
                            <div className="bg-white px-12 py-8 rounded-2xl shadow-2xl text-center">
                                {gameResult === 'win' && (
                                    <>
                                        <div className="text-6xl mb-4">🎉</div>
                                        <h2 className="text-4xl font-bold text-green-600 mb-2">You Win!</h2>
                                        <p className="text-gray-600 mb-6">Congratulations on your victory!</p>
                                    </>
                                )}
                                {gameResult === 'lose' && (
                                    <>
                                        <div className="text-6xl mb-4">😔</div>
                                        <h2 className="text-4xl font-bold text-red-600 mb-2">You Lost!</h2>
                                        <p className="text-gray-600 mb-6">Better luck next time!</p>
                                    </>
                                )}
                                {gameResult === 'draw' && (
                                    <>
                                        <div className="text-6xl mb-4">🤝</div>
                                        <h2 className="text-4xl font-bold text-blue-600 mb-2">Draw!</h2>
                                        <p className="text-gray-600 mb-6">Well played by both sides!</p>
                                    </>
                                )}
                                <button
                                    onClick={() => {
                                        gameRef.current.reset();
                                        setFen(gameRef.current.fen());
                                        setGameResult(null);
                                        setMoveFrom('');
                                        setOptionSquares({});
                                    }}
                                    className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors"
                                >
                                    New Game
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
const API_URL = "https://chess-d5p9.onrender.com";

export async function playMove(fen, move, max_time = 1.0) {
    const res = await fetch(`${API_URL}/move`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({fen, move, max_time})
    })

    if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || "Backend error")
    }

    return res.json();
}
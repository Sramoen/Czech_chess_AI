# Czech Chess AI Engine

## Introduction
As an chess enthusiast, I have always wanted to try building a chess engine. However, since many high-quality engines already exist for classical chess, I decided to build an AI engine for a lesser-known variant — Czech Chess — for which, to the best of my knowledge, no engine currently exists.

## What is Czech Chess?
Czech Chess (also known as "folky") is a chess variant that was introduced to the public in 2019 at the Czech Open chess festival in Pardubice. It was invented by Petr Doubek from Jaroměř.

In Czech Chess, only the following pieces are used: rooks, knights, bishops, and pawns. Kings and queens are absent from the game. The initial setup of the rooks, knights, and pawns is the same as in classical chess. However, unlike in classical chess, pieces cannot capture one another.

A pawn can only be placed on a square that is attacked by three of the player's pieces. Once placed, pawns cannot move or be captured. The goal of the game is to place eight pawns on the board. A draw can occur if the same position repeats three times, or by mutual agreement.

## Methods Used
The engine is built around the **minimax algorithm**. Minimax searches the game tree in depth-first order and alternates between maximizing (white's turn) and minimizing (black's turn) the evaluation of positions.

To improve efficiency, **alpha-beta pruning** is applied. This technique stores two additional parameters, α and β, to track the best values for maximizing and minimizing nodes respectively. When α ≥ β, the branch is pruned.

I also implemented a **transposition table** using **Zobrist hashing** to avoid redundant evaluations of previously seen positions. Zobrist hashing assigns random numbers to each piece-square combination and computes the position hash using XOR operations. This allows fast updates after moves.

To improve alpha-beta pruning, **move ordering** is critical. I experimented with several heuristics, including prioritizing moves already in the transposition table. Ultimately, a simple manually defined order gave the best results:
1. Pawn placements (high impact)
2. Rook moves (high mobility)
3. Bishop moves
4. Knight moves (low mobility)

Unlike classical chess, moves that deliver checks or captures aren't relevant, but future improvements could implement heuristics like the **killer move heuristic** (favoring moves that previously caused a cutoff).

### Evaluation Function
In classical chess, material is often the basis of evaluation. However, this doesn't apply in Czech Chess. Instead, my evaluation is especially based on:
1. **Number of placed pawns** (the win condition)
2. **Mobility** — since blocked pieces (especially rooks and bishops) become ineffective, ensuring they have room to move is crucial.

## Project Structure
The engine is implemented in **Python**. The board state is represented using **bitboards**, which allow for efficient move generation using bitwise operations like shift and XOR. I tested multiple libraries (`numpy`, `bitarray`, `gmpy2`) for speed, but native Python integers proved fastest. I also attempted to use `numba` to speed up computation, though this was not successful.

A basic GUI was created using **pygame**, so users can comfortably play against the engine.

### Instalation
The libraries needed for running the project are specified in requirements. To run the GUI (and play against the computer) you can just run the `Czech_chess.py` script.

---

Enjoy exploring this project, and feel free to contribute or suggest improvements!

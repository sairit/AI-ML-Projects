# Artificial Intelligence & Machine Learning Portfolio

This repository contains a collection of foundational Artificial Intelligence and Machine Learning projects implemented in Python. Each project focuses on a specific algorithm or logical concept, serving as a practical demonstration of how systems can be programmed to search, reason, optimize, and learn.

## Repository Overview

Below is a technical breakdown of each project included in this repository, highlighting the primary AI concepts and logic utilized to solve its respective problem.

### 1. Attention[cite: 1]
*   **Logical Concept:** Natural Language Processing (NLP) & Masked Language Modeling
*   **Project Overview:** Inspired by modern transformer models like BERT, this project implements an attention mechanism to predict missing (masked) words in a text sequence. It demonstrates how AI learns contextual relationships between words by assigning different "attention" weights to surrounding tokens, allowing the model to understand syntax and semantics[cite: 1].

### 2. Crossword[cite: 1]
*   **Logical Concept:** Constraint Satisfaction Problems (CSP) & Backtracking Search
*   **Project Overview:** An AI that automatically generates crossword puzzles. It treats the crossword grid as a constraint satisfaction problem, where variables are the blank spaces and the domain is a given dictionary of words. The algorithm uses node consistency, arc consistency (AC-3), and backtracking search with heuristics to efficiently fill the board without violating constraints[cite: 1].

### 3. Degrees[cite: 1]
*   **Logical Concept:** Graph Search Algorithms (Breadth-First Search)
*   **Project Overview:** Based on the "Six Degrees of Kevin Bacon" game, this AI finds the shortest path between any two actors based on the movies they have co-starred in. It models the data as a graph and uses Breadth-First Search (BFS) to guarantee that the path found represents the fewest possible degrees of separation[cite: 1].

### 4. Heredity[cite: 1]
*   **Logical Concept:** Bayesian Networks & Probabilistic Inference
*   **Project Overview:** This project calculates the probability of individuals possessing a certain genetic trait. By constructing a Bayesian Network that maps out family relationships and known genetic mutation rates, the AI infers the hidden joint probabilities of gene inheritance and trait expression across multiple generations[cite: 1].

### 5. Knights[cite: 1]
*   **Logical Concept:** Propositional Logic & Model Checking
*   **Project Overview:** An AI program designed to solve classic "Knights and Knaves" logic puzzles (where Knights always tell the truth and Knaves always lie). By encoding the puzzle's constraints into a Knowledge Base of propositional logic formulas, the AI uses model-checking algorithms to definitively deduce the identity of each character[cite: 1].

### 6. Minesweeper[cite: 1]
*   **Logical Concept:** Knowledge-Based Agents & Propositional Logic
*   **Project Overview:** An AI that plays the classic game of Minesweeper optimally. Instead of guessing, the AI maintains a Knowledge Base of logical sentences representing the board state. As it clicks on safe cells, it infers new safe cells and flags hidden mines by logically resolving overlapping subsets of data[cite: 1].

### 7. Nim[cite: 1]
*   **Logical Concept:** Reinforcement Learning (Q-Learning)
*   **Project Overview:** An AI that learns to play the mathematical game of Nim perfectly. Using Q-Learning, the agent trains by playing thousands of simulated games against itself. It updates its Q-values (rewards/penalties) based on the actions taken in specific states, eventually learning the optimal strategy to force a win without explicit hardcoding[cite: 1].

### 8. PageRank[cite: 1]
*   **Logical Concept:** Markov Chains & Iterative Mathematical Algorithms
*   **Project Overview:** A Python implementation of Google’s foundational PageRank algorithm[cite: 1]. The AI determines the importance of a set of web pages by using two methods: simulating a Random Surfer (Markov Chain) navigating between links, and applying an iterative mathematical formula to calculate the exact probability distribution of landing on any given page.

### 9. Parser[cite: 1]
*   **Logical Concept:** Natural Language Processing (CFG parsing)
*   **Project Overview:** This AI parses standard English sentences to understand their grammatical structure. Using Context-Free Grammar (CFG) rules and the NLTK library, the parser generates syntax trees to ensure sentences are structurally valid and successfully extracts specific "noun phrase chunks" from the text[cite: 1].

### 10. Shopping[cite: 1]
*   **Logical Concept:** Supervised Machine Learning (Classification)
*   **Project Overview:** A machine learning model that predicts whether an online shopping customer will complete a purchase. Using the k-Nearest Neighbors (k-NN) classification algorithm, the AI is trained on user session data (e.g., pages visited, time spent, browser type) to categorize future users into buyers or non-buyers, evaluating its performance via sensitivity and specificity metrics[cite: 1].

### 11. Tic-Tac-Toe[cite: 1]
*   **Logical Concept:** Adversarial Search (Minimax Algorithm)
*   **Project Overview:** An AI that plays Tic-Tac-Toe flawlessly. The engine uses the Minimax algorithm to explore all possible future game states, assuming the human opponent plays optimally. The AI will logically maximize its own score while minimizing the opponent's, ensuring that it never loses[cite: 1].

---

## Technical Stack
*   **Language:** Python 3
*   **Key Libraries:** Pygame, NLTK, Scikit-learn (implied based on standard AI coursework implementations)
*   **Concepts Demonstrated:** Search Algorithms, Propositional Logic, Probabilistic Inference, Supervised Learning, Reinforcement Learning, and NLP.

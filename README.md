# Telugu Chandassu as a Finite-State Digital Logic Architecture
[![DOI](https://zenodo.org)](https://doi.org/10.5281/zenodo.24304302)


A formal mathematical and computational framework mapping ancient Indian prosody (*Chandaḥśāstra* and Telugu *Vrutha Padyalu*) to modern digital logic, Karnaugh map minimization, combinatorics, and error-detection architectures.

---

## Overview

This repository summarizes the core mathematical theorems, discrete algorithms, and Boolean logic proofs demonstrating that classical **Telugu Chandassu** operates as a base-2 finite-state computational system.

---

## Core Mathematical Theorems & Formulations

### 1. Base-2 Acoustic State Space
Every spoken syllable in a poetic meter is quantized by its durational weight (*Matra*) into a binary state $x \in \{0, 1\}$:
* **Laghu ($\text{I}$):** Short duration ($1\text{ Matra}$) $\rightarrow \mathbf{0}$ (Low State)
* **Guru ($\text{U}$):** Long duration ($2\text{ Matras}$) $\rightarrow \mathbf{1}$ (High State)

A 3-syllable metric foot (*Gana*) forms an ordered 3-bit vector $V = [A, B, C] \in \{0, 1\}^3$, generating $2^3 = 8$ distinct states.

---

### 2. De Bruijn Shift Register Theorem (*Yamātārājabhānasalagām*)
**Theorem:** The 10-character mnemonic sequence $\text{య-మా-తా-రా-జ-భా-న-స-ల-గాం}$ forms a 3-bit cyclic shift register (a De Bruijn sequence of order $n=3$ over alphabet $k=2$).

$$S = [0, 1, 1, 1, 0, 1, 0, 0, 0, 1]$$

Every sliding window $W_i = [S_i, S_{i+1}, S_{i+2}]$ for $i \in \{0, 1, \dots, 7\}$ uniquely resolves the 3-bit binary representation of the $i$-th Master Gana without collisions.

---

### 3. Combinatorial Expansion Theorem (*Meru Prastara*)
**Theorem:** The distribution of *Laghu* ($L$) and *Guru* ($G$) permutations across a poetic line of length $n$ follows the **Binomial Expansion Theorem** (historically formulated as *Meru Prastara* / Pascal's Triangle):

$$(L + G)^n = \sum_{k=0}^{n} \binom{n}{k} L^{n-k} G^k$$

For $n = 3$:

$$(L + G)^3 = \binom{3}{0}L^3 + \binom{3}{1}L^2G + \binom{3}{2}LG^2 + \binom{3}{3}G^3 = 1L^3 + 3L^2G + 3LG^2 + 1G^3$$

Total system states: $1 + 3 + 3 + 1 = 8$.

---

### 4. Priority Encoder & Decoder Algorithms (*Uddiṣṭa* & *Naṣṭa*)

#### A. *Uddiṣṭa* (Binary-to-Decimal Encoder)
Given a syllable sequence $s_1, s_2, \dots, s_n$ scanned **right-to-left** (from $s_n$ down to $s_1$, aligning LSB-to-MSB) with initial state $I_0 = 1$:

$$I_k = \begin{cases} 2I_{k-1} & \text{if } s_{n-k+1} = \text{Guru } (1) \\ 2I_{k-1} - 1 & \text{if } s_{n-k+1} = \text{Laghu } (0) \end{cases}$$

The final value $I_n \in \{1, \dots, 2^n\}$ gives the exact 1-indexed matrix row address in $O(n)$ time complexity.

#### B. *Naṣṭa* (Decimal-to-Binary Decoder)
Given a 1-indexed row address $N_0$, bits are extracted left-to-right (from $s_1$ to $s_n$) over $n$ iterations:

$$s_k = \begin{cases} \text{Guru } (1), \quad N_k = \dfrac{N_{k-1} + 1}{2} & \text{if } N_{k-1} \text{ is odd} \\[8pt] \text{Laghu } (0), \quad N_k = \dfrac{N_{k-1}}{2} & \text{if } N_{k-1} \text{ is even} \end{cases}$$

---

### 5. Boolean Minimization & Karnaugh Map Adjacency Theorem
**Theorem:** Metrical constraints in Telugu *Vrutha Padyalu* (such as *Utpalamala*) act as minimized Boolean logic gates.

Let the target gate accept the four high-energy Ganas beginning with a *Guru*: **Bha ($m_4$), Ra ($m_5$), Ta ($m_6$), and Ma ($m_7$)**.

$$F(A, B, C) = \sum m(4, 5, 6, 7) = A\bar{B}\bar{C} + A\bar{B}C + AB\bar{C} + ABC$$

#### Algebraic Proof:
$$\begin{aligned}
F &= A\bar{B}(\bar{C} + C) + AB(\bar{C} + C) && \text{(Distributive Law)} \\
F &= A\bar{B}(1) + AB(1) && \text{(Complement Law: } X + \bar{X} = 1\text{)} \\
F &= A(\bar{B} + B) && \text{(Distributive Law)} \\
F &= A(1) = \mathbf{A} && \text{(Identity Law)}
\end{aligned}$$

**Prosodic Interpretation:** Because *Yati* (caesura rhyme) and *Prasa* (second-syllable consonant rhyme) force syllables $B$ and $C$ to vary dynamically across words, the K-map reduces the 4-term filter to a single-bit check ($F = A$). The metrical gate validates solely whether the opening audio frame is a *Guru* ($A = 1$).

---

### 6. Error-Detection & Parity Theorems

1. **Matra Checksum:** Each line of a meter must satisfy a fixed durational weight constraint:
   $$\sum_{k=1}^{n} w(s_k) = M_{\text{target}}, \quad w(s_k) \in \{1, 2\}$$
   Any syllable insertion, deletion, or vowel-length corruption alters the sum and fails the rhythmic checksum.
2. **Cyclic Redundancy Permutation (*Ghana Patha*):** Text streams are interleaved recursively forward and backward:
   $$W_1 W_2 \rightarrow W_2 W_1 \rightarrow W_1 W_2 W_3 \rightarrow W_3 W_2 W_1 \rightarrow W_1 W_2 W_3$$
   This enforces two-dimensional parity verification across oral transmission.

---

## Master Reference Truth Table

| Gana (గణం) | Syllable Pattern | Pingala Binary (LSB $\rightarrow$ MSB) | Standard 3-Bit Binary ($ABC$) | Standard Decimal | *Uddiṣṭa* Row Index |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Na (న)** | `I I I` | `000` | `000` | 0 | 1 |
| **Bha (భ)** | `U I I` | `100` | `100` | 4 | 5 |
| **Ja (జ)** | `I U I` | `010` | `010` | 2 | 3 |
| **Sa (స)** | `I I U` | `001` | `001` | 1 | 2 |
| **Ma (మ)** | `U U U` | `111` | `111` | 7 | 8 |
| **Ya (య)** | `I U U` | `011` | `011` | 3 | 4 |
| **Ra (ర)** | `U I U` | `101` | `101` | 5 | 6 |
| **Ta (త)** | `U U I` | `110` | `110` | 6 | 7 |

---

## Verification & Preprint

* **Automated Proof Suite:** Run `python chandassu_logic.py` to verify all theorems exhaustively across the 8-state space.
* **Preprint PDF (Zenodo):** https://doi.org/10.5281/zenodo.24304302

---

## Citation

If you reference these mathematical formulations or proofs in academic work, please cite:

```bibtex
@misc{chandassu_digital_logic_2026,
  title  = {Formalizing Telugu Chandassu as a Finite-State Digital Logic Architecture},
  author = {Muddasani Vaishali},
  year   = {2026},
  note   = {Computational Prosody and Digital Logic Research Repository}
}
```

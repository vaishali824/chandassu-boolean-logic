"""
Formal Verification of Telugu Chandassu Prosody via Boolean Logic & K-Map Minimization.

This module establishes a computational isomorphism between classical Indian prosody
(Telugu Chandassu / Pingala's Chandaḥśāstra) and modern digital logic:
  1. Laghu (|) and Guru (U) syllable weights -> Binary state space {0, 1}.
  2. Tri-syllabic Ganas -> 3-bit combinational encoder/decoder circuits.
  3. Pingala's Prastara sequence -> Gray code single-bit adjacency (Hamming distance = 1).
  4. Karnaugh map (K-map) minimization -> Canonical logic gate reduction (F = A).
  5. Yati & Prasa structural rules -> Formal parity/equivalence verification gates.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class GanaState:
    """Represents a 3-syllable prosodic state in binary and decimal domains."""
    name: str
    symbols: str          # '|' = Laghu, 'U' = Guru
    bits_msb: Tuple[int, int, int]  # Standard MSB-to-LSB binary (Laghu=0, Guru=1)
    pingala_index: int    # 1-indexed position in Pingala's Prastara (right-to-left)

    @property
    def decimal_msb(self) -> int:
        """Standard base-2 to base-10 conversion (MSB first)."""
        a, b, c = self.bits_msb
        return (a << 2) | (b << 1) | c

    @property
    def decimal_pingala(self) -> int:
        """Pingala's 1-indexed right-to-left positional decoding."""
        a, b, c = self.bits_msb
        return 1 + (a * 1) + (b * 2) + (c * 4)


# Canonical mapping of the 8 Tri-Syllabic Ganas (Laghu='|' -> 0, Guru='U' -> 1)
TRI_GANA_TABLE: Dict[Tuple[int, int, int], GanaState] = {
    (0, 1, 1): GanaState("Ya-gana", "|UU", (0, 1, 1), 7),
    (1, 1, 1): GanaState("Ma-gana", "UUU", (1, 1, 1), 8),
    (1, 1, 0): GanaState("Ta-gana", "UU|", (1, 1, 0), 4),
    (1, 0, 1): GanaState("Ra-gana", "U|U", (1, 0, 1), 6),
    (0, 1, 0): GanaState("Ja-gana", "|U|", (0, 1, 0), 3),
    (1, 0, 0): GanaState("Bha-gana", "U||", (1, 0, 0), 2),
    (0, 0, 0): GanaState("Na-gana", "|||", (0, 0, 0), 1),
    (0, 0, 1): GanaState("Sa-gana", "||U", (0, 0, 1), 5),
}


def encode_prosody_to_binary(syllable_pattern: str, laghu_is_zero: bool = True) -> List[int]:
    """
    Encodes a string of Laghu ('|') and Guru ('U') markers into a binary vector.

    Args:
        syllable_pattern: String containing '|' (Laghu) and 'U' (Guru).
        laghu_is_zero: If True, '|' -> 0 and 'U' -> 1 (standard convention).
                       If False, '|' -> 1 and 'U' -> 0 (Pingala Guru-first convention).
    """
    cleaned = syllable_pattern.replace(" ", "")
    valid_chars = {"|", "U"}
    if not set(cleaned).issubset(valid_chars):
        raise ValueError(f"Invalid prosodic symbols found in: {syllable_pattern}")

    if laghu_is_zero:
        return [0 if ch == "|" else 1 for ch in cleaned]
    return [1 if ch == "|" else 0 for ch in cleaned]


def decode_binary_to_gana(bits: Tuple[int, int, int]) -> GanaState:
    """Combinational 3-to-8 decoder mapping a 3-bit tuple to its corresponding Gana."""
    if bits not in TRI_GANA_TABLE:
        raise ValueError(f"Input must be a 3-bit tuple of 0s and 1s, got {bits}")
    return TRI_GANA_TABLE[bits]


def verify_pingala_prastara_indexing() -> None:
    """
    Theorem 1: Verifies that Pingala's 1-indexed right-to-left Prastara formula
    bijectively maps all 8 Ganas onto the integer range.
    """
    indices = [state.decimal_pingala for state in TRI_GANA_TABLE.values()]
    assert sorted(indices) == list(range(1, 9)), "Prastara bijection failed!"
    for state in TRI_GANA_TABLE.values():
        assert state.decimal_pingala == state.pingala_index, (
            f"Index mismatch for {state.name}: expected {state.pingala_index}, "
            f"got {state.decimal_pingala}"
        )


def hamming_distance(seq_a: Tuple[int, ...], seq_b: Tuple[int, ...]) -> int:
    """Computes the Hamming distance between two equal-length binary tuples."""
    assert len(seq_a) == len(seq_b), "Bit vectors must be of equal length"
    return sum(bit_a != bit_b for bit_a, bit_b in zip(seq_a, seq_b))


def verify_kmap_gray_code_adjacency() -> List[Tuple[int, int, int]]:
    """
    Theorem 2: Verifies 3-variable Karnaugh Map single-bit adjacency (Gray code).
    In a 3-variable K-map (A vs BC), columns follow Gray code order: 00, 01, 11, 10.
    Every adjacent cell (including cyclic wrap-around) must have Hamming distance = 1.
    """
    gray_columns = [(0, 0), (0, 1), (1, 1), (1, 0)]
    kmap_states: List[Tuple[int, int, int]] = []

    for a in (0, 1):
        row = [(a, b, c) for (b, c) in gray_columns]
        # Check horizontal adjacency and cyclic wrap-around in each K-map row
        for i in range(len(row)):
            curr_cell = row[i]
            next_cell = row[(i + 1) % len(row)]
            dist = hamming_distance(curr_cell, next_cell)
            assert dist == 1, f"K-map adjacency violated between {curr_cell} and {next_cell}"
        kmap_states.extend(row)

    return kmap_states


def verify_kmap_minimization_f_equals_a() -> None:
    """
    Theorem 3: Exhaustive Truth-Table Verification of K-Map Reduction F = A.
    When minterms m4, m5, m6, m7 (all states where MSB A = 1, i.e., Guru-initial
    Ganas: Bha, Ra, Ta, Ma) are grouped as a quad on a 3-variable K-map:
        F(A, B, C) = A*B'*C' + A*B'*C + A*B*C' + A*B*C
                   = A * (B' + B) * (C' + C)
                   = A
    """
    guru_initial_ganas = {"Bha-gana", "Ra-gana", "Ta-gana", "Ma-gana"}

    for bits, state in TRI_GANA_TABLE.items():
        a, b, c = bits
        # Unminimized sum-of-products (SOP) form
        sop_output = (
            (a and (not b) and (not c))
            or (a and (not b) and c)
            or (a and b and (not c))
            or (a and b and c)
        )
        # Minimized Boolean gate output
        minimized_output = bool(a)

        assert bool(sop_output) == minimized_output, f"Minimization mismatch at {bits}"
        if minimized_output:
            assert state.name in guru_initial_ganas, f"Unexpected Gana in group: {state.name}"


def verify_prasa_and_yati_parity(
    line1_second_syllable: str,
    line2_second_syllable: str,
    yati_maitri_group_a: int,
    yati_maitri_group_b: int,
) -> Dict[str, bool]:
    """
    Theorem 4: Structural Prosodic Constraints as Digital Error-Detection Gates.
      - Prasa Check: Exact equivalence (XNOR gate) on the 2nd syllable base consonant across lines.
      - Yati Check: Equivalence class parity verification between start syllable and caesura syllable.
    """
    prasa_valid = (line1_second_syllable == line2_second_syllable)
    yati_valid = (yati_maitri_group_a == yati_maitri_group_b)
    return {
        "prasa_xnor_pass": prasa_valid,
        "yati_equivalence_pass": yati_valid,
        "meter_integrity_valid": prasa_valid and yati_valid,
    }


def run_all_verifications() -> None:
    """Executes all formal proofs and prints a verification summary."""
    print("=== Telugu Chandassu <-> Digital Logic Verification Suite ===\n")

    # 1. Verify Pingala's Prastara Bijection
    verify_pingala_prastara_indexing()
    print("[PASS] Theorem 1: Pingala's 1-indexed Prastara bijection verified across all 8 Ganas.")

    # 2. Verify K-Map Gray Code Adjacency
    kmap_cells = verify_kmap_gray_code_adjacency()
    print(f"[PASS] Theorem 2: 3-Variable K-Map Gray Code single-bit adjacency verified ({len(kmap_cells)} cells).")

    # 3. Verify Boolean Minimization (F = A)
    verify_kmap_minimization_f_equals_a()
    print("[PASS] Theorem 3: K-Map Quad Reduction F(A,B,C) = Σm(4,5,6,7) = A verified exhaustively.")

    # 4. Verify Prasa & Yati Error-Detection Gates
    check = verify_prasa_and_yati_parity("క", "క", yati_maitri_group_a=1, yati_maitri_group_b=1)
    assert check["meter_integrity_valid"] is True
    print("[PASS] Theorem 4: Yati & Prasa structural parity/XNOR verification passed.\n")

    # Display Truth Table & Gana Decoder Mapping
    print(f"{'Gana':<10} | {'Prosody':<8} | {'Binary (A,B,C)':<15} | {'Std Dec':<8} | {'Pingala Index'}")
    print("-" * 62)
    for bits in sorted(TRI_GANA_TABLE.keys()):
        st = decode_binary_to_gana(bits)
        print(f"{st.name:<10} | {st.symbols:<8} | {str(st.bits_msb):<15} | {st.decimal_msb:<8} | {st.decimal_pingala}")

    # Example Line Decoding (e.g., Utpalamala opening: Bha, Ra, Na, Bha, Bha, Ra, Va)
    sample_pattern = "U|| U|U ||| U|| U|| U|U |U"
    bitstream = encode_prosody_to_binary(sample_pattern)
    ganas = [
        decode_binary_to_gana(tuple(bitstream[i : i + 3])).name  # type: ignore
        for i in range(0, 18, 3)
    ]
    print("\nSample Prosodic Stream:", sample_pattern)
    print("Encoded Bitstream:     ", "".join(map(str, bitstream)))
    print("Decoded Tri-Ganas:     ", " -> ".join(ganas))


if __name__ == "__main__":
    run_all_verifications()

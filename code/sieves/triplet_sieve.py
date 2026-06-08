#!/usr/bin/env python3
"""
triplet_sieve.py — Memory-efficient segmented sieve for prime triplets up to 10^9.

Finds both triplet patterns simultaneously:
  Pattern A: (p, p+2, p+6)   — primes with gaps (2,4)
  Pattern B: (p, p+4, p+6)   — primes with gaps (4,2)

Processes segments sequentially to keep memory at ~1GB even at 10^9.
Tracks only boundary primes between segments to detect cross-segment triplets.

Usage:
    python3 triplet_sieve.py [--limit 1000000000] [--output triplets.txt]
"""
import math
import time
import sys
import json
import argparse

def segmented_triplet_sieve(limit, segment_size=1 << 22):
    """Segmented sieve up to limit, finding all prime triplets.

    Returns: (pattern_A list, pattern_B list, total prime count)
    where patterns store the pivot p for each triplet found.
    """
    sqrt_lim = int(math.isqrt(limit))

    # Small sieve for base primes up to sqrt(limit)
    small_sieve = bytearray([True]) * (sqrt_lim + 1)
    small_sieve[0] = small_sieve[1] = False
    for i in range(2, int(math.isqrt(sqrt_lim)) + 1):
        if small_sieve[i]:
            slice_start = i * i
            small_sieve[slice_start:sqrt_lim + 1:i] = bytearray(
                [False] * ((sqrt_lim - slice_start) // i + 1)
            )

    base_primes = [i for i, is_p in enumerate(small_sieve) if is_p]
    print(f"Base primes up to sqrt({limit:,})={sqrt_lim:,}: {len(base_primes):,}")

    pattern_a = []  # (p, p+2, p+6) pivots
    pattern_b = []  # (p, p+4, p+6) pivots
    total_primes = 0
    prev_primes = []  # Last few primes from previous segment for boundary detection
    num_segments = (limit + segment_size - 1) // segment_size

    for seg_idx, seg_start in enumerate(range(0, limit + 1, segment_size)):
        seg_end = min(seg_start + segment_size, limit + 1)
        seg = bytearray([True]) * (seg_end - seg_start)

        for p in base_primes:
            start = max(p * p, ((seg_start + p - 1) // p) * p)
            for multiple in range(start - seg_start, seg_end - seg_start, p):
                seg[multiple] = False

        if seg_start == 0:
            seg[0] = seg[1] = False

        primes_in_seg = [seg_start + i for i, is_p in enumerate(seg) if is_p]
        total_primes += len(primes_in_seg)

        # Combine with boundary primes from previous segment
        candidates = prev_primes + primes_in_seg
        # Keep only primes we need for cross-segment triplet detection
        # A triplet can span at most 6 numbers, so we need primes within 6 of the boundary
        prev_primes = [p for p in candidates if p > seg_end - 7]

        # Find triplets in combined candidates
        prev_set = set(prev_primes)
        for p in candidates:
            if p + 6 > limit:
                break
            # Pattern A: (p, p+2, p+6)
            if (p + 2) in prev_set and (p + 6) in prev_set:
                pattern_a.append(p)
            # Pattern B: (p, p+4, p+6)
            elif (p + 4) in prev_set and (p + 6) in prev_set:
                pattern_b.append(p)

        if (seg_idx + 1) % max(1, num_segments // 10) == 0:
            elapsed = time.time() - tic
            print(f"  Segment {seg_idx+1}/{num_segments} — primes: {total_primes:,}, "
                  f"A: {len(pattern_a):,}, B: {len(pattern_b):,}, {elapsed:.1f}s")

    return pattern_a, pattern_b, total_primes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prime triplet segmented sieve")
    parser.add_argument("--limit", type=int, default=10**9, help="Upper bound")
    parser.add_argument("--output", type=str, default="triplets.txt", help="Output file")
    args = parser.parse_args()

    print(f"=== Prime Triplet Sieve to {args.limit:,} ===")
    tic = time.time()
    pattern_a, pattern_b, total = segmented_triplet_sieve(args.limit)
    toc = time.time()

    print(f"\nResults:")
    print(f"  Total primes: {total:,}")
    print(f"  Pattern A (p, p+2, p+6): {len(pattern_a):,}")
    print(f"  Pattern B (p, p+4, p+6): {len(pattern_b):,}")
    print(f"  Total triplets: {len(pattern_a) + len(pattern_b):,}")
    print(f"  Time: {toc - tic:.1f}s")

    with open(args.output, "w") as f:
        json.dump({
            "limit": args.limit,
            "total_primes": total,
            "pattern_A_count": len(pattern_a),
            "pattern_B_count": len(pattern_b),
            "pattern_A_first_20": pattern_a[:20],
            "pattern_B_first_20": pattern_b[:20],
            "runtime_seconds": round(toc - tic, 2),
        }, f, indent=2)
    print(f"  Saved to {args.output}")

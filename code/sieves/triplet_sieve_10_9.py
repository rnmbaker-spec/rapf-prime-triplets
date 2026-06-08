#!/usr/bin/env python3
"""
triplet_sieve_10_9.py - Segmented sieve for prime triplets up to 10^9.

Finds both triplet patterns simultaneously:
  Pattern A: (p, p+2, p+6)   — gaps (2, 4)
  Pattern B: (p, p+4, p+6)   — gaps (4, 2)

Memory-efficient segmented design ~1GB buffer.
Cross-segment boundary detection via overlap window.

Usage:
    python3 triplet_sieve_10_9.py [--limit 1000000000] [--segment-size 4194304]
"""
import math
import time
import argparse
import json


def segmented_triplet_sieve(limit, segment_size=1 << 22):
    """Segmented sieve collecting triplet pivots up to limit."""
    sqrt_lim = int(math.isqrt(limit))

    # Base primes up to sqrt(limit)
    small_sieve = bytearray([True]) * (sqrt_lim + 1)
    small_sieve[0] = small_sieve[1] = False
    for i in range(2, int(math.isqrt(sqrt_lim)) + 1):
        if small_sieve[i]:
            small_sieve[i * i:sqrt_lim + 1:i] = bytearray(
                [False] * ((sqrt_lim - i * i) // i + 1)
            )
    base_primes = [i for i, b in enumerate(small_sieve) if b]
    print(f"Base primes to {sqrt_lim:,}: {len(base_primes):,}")

    pattern_a = []  # (p, p+2, p+6)
    pattern_b = []  # (p, p+4, p+6)
    total_primes = 0

    overlap = 6  # Max gap span for triplets
    prev_segment_primes = []  # Primes from end of previous segment

    seg_start = 0
    seg_count = 0
    while seg_start <= limit:
        seg_end = min(seg_start + segment_size, limit + 1)
        seg_len = seg_end - seg_start
        seg = bytearray([True]) * seg_len

        # Mark composites
        for p in base_primes:
            start = max(p * p, ((seg_start + p - 1) // p) * p)
            seg[start - seg_start:seg_len:p] = bytearray(
                [False] * ((seg_len - 1 - (start - seg_start)) // p + 1)
            )

        if seg_start == 0:
            seg[0] = seg[1] = False

        # Extract primes from this segment
        primes = [seg_start + i for i, b in enumerate(seg) if b]
        total_primes += len(primes)

        # Combine with overlap window from previous segment
        window = [p for p in prev_segment_primes if p >= seg_start - overlap]
        combined = window + primes

        # Find triplets
        prime_set = set(combined)
        for p in combined:
            if p + 6 > limit:
                break
            if (p + 2) in prime_set and (p + 6) in prime_set:
                pattern_a.append(p)
            elif (p + 4) in prime_set and (p + 6) in prime_set:
                pattern_b.append(p)

        # Save overlap for next segment boundary
        prev_segment_primes = [p for p in primes if p > seg_end - overlap - 1]

        seg_count += 1
        if seg_count % max(1, ((limit + segment_size) // segment_size) // 10) == 0:
            elapsed = time.time() - t0
            print(f"  up to {seg_end:,}: {total_primes:,} primes, "
                  f"A={len(pattern_a):,}, B={len(pattern_b):,}, {elapsed:.1f}s")

        seg_start += segment_size

    return pattern_a, pattern_b, total_primes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10**9)
    parser.add_argument("--segment-size", type=int, default=1 << 22)
    parser.add_argument("--output", default="data/triplet_census.json")
    args = parser.parse_args()

    print(f"=== Triplet sieve to {args.limit:,} ===")
    t0 = time.time()

    a, b, total = segmented_triplet_sieve(args.limit, args.segment_size)
    elapsed = time.time() - t0

    print(f"\nTotal primes: {total:,}")
    print(f"Pattern A (0,2,6): {len(a):,}")
    print(f"Pattern B (0,4,6): {len(b):,}")
    print(f"Total triplets: {len(a) + len(b):,}")
    print(f"A/B ratio: {len(a)/len(b):.6f}" if b else "A/B ratio: inf")
    print(f"Time: {elapsed:.1f}s")

    results = {
        "limit": args.limit,
        "total_primes": total,
        "pattern_A_count": len(a),
        "pattern_B_count": len(b),
        "pattern_A_ratio_vs_expected": round(len(a) / (len(a) + len(b)), 6) if (a or b) else 0,
        "pattern_B_ratio_vs_expected": round(len(b) / (len(a) + len(b)), 6) if (a or b) else 0,
        "elapsed_seconds": round(elapsed, 2),
        "pattern_A_first_20": a[:20],
        "pattern_B_first_20": b[:20],
    }

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {args.output}")

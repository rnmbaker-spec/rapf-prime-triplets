# RAPF Extended: Prime Triplets and Higher-Order Constellations

Research extending RAPF to $k=3$ prime constellations.

## Overview

Paper 4 of the RAPF program. Where Papers 1-3 established the framework for twin primes ($k=2$), this work generalizes admissibility classes, polynomial certificates, and equidistribution analysis to:
- **Pattern A:** $(p, p+2, p+6)$
- **Pattern B:** $(p, p+4, p+6)$

## Key Questions

1. Does the discrete geometry extend from 1D (twins) to 2D (triplets)?
2. Do polynomial certificates remain computationally tractable at $k=3$?
3. Is primorial equidistribution preserved — or does triplet structure reveal new biases?
4. Are $(0,2,6)$ and $(0,4,6)$ equidistributed relative to each other, or is there structural asymmetry?

## Repository Structure

```
papers/          LaTeX source(s)
pdfs/            Compiled output
code/sieves/     Segmented sieves for triplets (basic + GPU)
code/analysis/   Fisher tests, gap distributions, bias measures
data/            Census results (n=6,7,8)
docs/            Supplementary materials
```

## Relationship to v1

Extends https://github.com/rnmbaker-spec/rapf-prime-framework:
- Lemma 1 (Recursive Density) → generalized to $k$-tuples
- Lemma 2 (Class Occupancy) → extended to 2D admissibility classes
- Polynomial Certificates → complexity analysis at $k=3$

## Citation

@misc{miller2026rapf-triplets,
  title={RAPF Extended: Prime Triplets and Higher-Order Constellations},
  author={Rob Miller},
  year={2026},
  url={https://github.com/rnmbaker-spec/rapf-prime-triplets}
}

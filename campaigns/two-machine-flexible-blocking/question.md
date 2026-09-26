# Partition → Two-machine flexible blocking

Category: Complexity open

## Source

The source gives positive binary integer weights. A valid output is a subset whose sum is half the total, or NO-SOLUTION if no such subset exists.

## Target

The target allows a variable job order. Each job has a mandatory first operation on machine one, flexible intermediate operations, and a final operation on machine two, with positive processing times, no buffer, and no overtaking. Seek an order and legal splits meeting the deadline.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question asks whether assignment flexibility causes hardness even with just two machines.

## Difficulty

The order itself is free, so soundness must exclude schedules that evade the intended partition by reordering jobs.

## Literature context

The target permits variable job order but fixes two machines and bufferless blocking. Other flexibility and buffering models require separate reductions.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Flow shop scheduling with inter-stage flexibility and blocking constraints](https://doi.org/10.1016/j.cor.2025.107219): Nicosia et al., Flow shop scheduling with inter-stage flexibility and blocking constraints, Computers & Operations Research 184 (2025), 107219, Table 3 and conclusion, explicitly leave this two-machine variable-order case open. The primary preprint, Sections 2 and 3.2, Table 1 and Theorem 2, specifies the model and proves polynomial solvability when the two-machine order is fixed. Preemptive hardness cited there has a different operation model and is not assumed to transfer. Its original proof was not inspected in this screening, so any proposed adaptation must check it.
- [primary preprint](https://arxiv.org/html/2411.18381v1): Nicosia et al., Flow shop scheduling with inter-stage flexibility and blocking constraints, Computers & Operations Research 184 (2025), 107219, Table 3 and conclusion, explicitly leave this two-machine variable-order case open. The primary preprint, Sections 2 and 3.2, Table 1 and Theorem 2, specifies the model and proves polynomial solvability when the two-machine order is fixed. Preemptive hardness cited there has a different operation model and is not assumed to transfer. Its original proof was not inspected in this screening, so any proposed adaptation must check it.

Fixed from board record `website/questions/two-machine-flexible-blocking.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.

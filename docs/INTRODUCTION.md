# Introduction: Reading Connectome Motifs Carefully

## What a connectome is

A **connectome** is a map of connections in a nervous system. In a directed connectome, a neuron is a node and a connection is an arrow from a source neuron to a target neuron. Modern *Drosophila* wiring diagrams make it possible to ask system-scale questions about these arrows, including questions about small recurring patterns of connectivity.[1] Earlier reconstructions of the adult central brain, an adult visual pathway, and the larval brain show that this work can be done at different anatomical scales and developmental stages.[8] [9] [10]

This repository focuses on the structure of selected directed patterns. It does not claim that a pattern proves what a circuit computes, whether an animal learns, or what causes behavior. A wiring diagram is a powerful constraint on possible mechanisms, but it is not a functional experiment.[2] Understanding circuit function additionally requires information such as neuronal dynamics, modulation, and experimental measurements of activity or perturbation effects.[12] [13]

## What a network motif is

A **network motif** is a small arrangement of connections, such as several sources converging on one target, two nodes connected in both directions, or a feed-forward triangle. Counting a motif is descriptive. Calling it enriched or depleted requires a comparison against an explicit randomized reference network.[3]

That reference is often called a **null model**. One useful null model rewires connections while preserving every node’s number of incoming and outgoing edges. It asks whether a pattern is unusual once those connection totals are held fixed. A more constrained null can also preserve coarse totals between designated cell classes. These models ask different scientific questions, so they can legitimately give different answers.[4] [5]

For directed binary graphs, the sampling procedure is part of that specification: naive accept-all edge swaps can be biased, whereas methods that enforce detailed balance can target a stated distribution while conserving in- and out-degrees.[11]

## Why this matters in *Drosophila*

Connectomic studies of the adult fly have shown that network statistics and motifs can be evaluated under multiple reference families. This makes the reference model part of the interpretation, not a technical afterthought.[6] The mushroom body is an important learning-related fly circuit, but an anatomical pattern within it is still not proof of a learning mechanism.[7] [12] [13]

Different reconstructions have distinct coverage and developmental scope, so a motif analysis should identify its source graph rather than treat fly connectomes as interchangeable.[8] [9] [10] The FlyWire whole-brain annotation study and the associated Codex resource make cell labels, connectivity views, and data access available for an identified dataset.[14] [15]

## What this project found

The project completed two predefined structural diagnostics on a fixed labelled directed representation. The convergence diagnostic was **non-discriminative** under both reference families. The reciprocal-pair diagnostic changed direction when the reference family changed. Neither result supports a robust enrichment, depletion, learning-computation, functional, mechanistic, or causal conclusion.

The durable methodological result is narrower: the reciprocal-pair statistic is sensitive to the assumed reference architecture. The ordered feed-forward-triangle definition is implemented and tested on synthetic graphs only; no empirical triangle calculation or null comparison has been run.

## How to use the code

The public code builds caller-supplied in-memory directed graphs, performs degree-preserving and class-block-constrained rewiring, and counts defined motifs. Its tests check graph and rewiring invariants on synthetic fixtures. They validate software behavior, not a biological hypothesis.

## Citation provenance

No valid prior GenSpark citation was recoverable from this repository’s reachable history. The verified references below explain the topic and null-model logic; they are not evidence for a new claim in this repository.

## References

[1]: https://doi.org/10.1038/s41586-024-07558-y "Dorkenwald et al. and the FlyWire Consortium (2024), Neuronal wiring diagram of an adult brain"
[2]: https://doi.org/10.7554/eLife.66039 "Hulse et al. (2021), A connectome of the Drosophila central complex reveals network motifs suitable for flexible navigation and context-dependent action selection"
[3]: https://doi.org/10.1126/science.298.5594.824 "Milo et al. (2002), Network motifs: Simple building blocks of complex networks"
[4]: https://doi.org/10.1137/16M1087175 "Fosdick et al. (2018), Configuring random graph models with fixed degree sequences"
[5]: https://doi.org/10.1371/journal.pbio.0020369 "Sporns and Kötter (2004), Motifs in brain networks"
[6]: https://doi.org/10.1038/s41586-024-07968-y "Lin et al. (2024), Network statistics of the whole-brain connectome of Drosophila"
[7]: https://doi.org/10.7554/eLife.62576 "Li et al. (2021), The connectome of the adult Drosophila mushroom body provides insights into function"
[8]: https://doi.org/10.7554/eLife.57443 "Scheffer et al. (2020), A connectome and analysis of the adult Drosophila central brain"
[9]: https://doi.org/10.1126/science.add9330 "Winding et al. (2023), The connectome of an insect brain"
[10]: https://doi.org/10.7554/eLife.24394 "Takemura et al. (2017), The comprehensive connectome of a neural substrate for ‘ON’ motion detection in Drosophila"
[11]: https://doi.org/10.1103/PhysRevE.85.046103 "Roberts and Coolen (2012), Unbiased degree-preserving randomization of directed binary networks"
[12]: https://doi.org/10.1038/nmeth.2451 "Bargmann and Marder (2013), From the connectome to brain function"
[13]: https://doi.org/10.1242/jeb.164954 "Meinertzhagen (2018), Of what use is connectomics? A personal perspective on the Drosophila connectome"
[14]: https://doi.org/10.1038/s41586-024-07686-5 "Schlegel et al. (2024), Whole-brain annotation and multi-connectome cell typing of Drosophila"
[15]: https://codex.flywire.ai/ "FlyWire Codex (accessed 2026), Connectome Data Explorer"

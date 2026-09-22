# Extended Introduction: Connectomes, Learning Circuits, and Null Models from Scratch

This document assumes **zero neuroscience background**. It explains every idea in plain language with analogies, then shows how each idea maps onto the actual code in this repository. For a shorter version with the full literature list, see [Introduction](INTRODUCTION.md); for what the project concluded, see [Current Results and Discussion](CURRENT_RESULTS_AND_DISCUSSION.md).

There is no single correct mental model for the core ideas, so each major concept below is followed by a **"many roads"** subsection: several independent mathematical lenses on the same idea, each with a tiny fully-worked example you can check by hand. Take whichever road matches how you think; skip the rest. None require calculus or differential equations — only counting, sets, and tables.

**Concept figure.** The repository's whole method — wiring diagram to directed graph, motif counting, and the degree-preserving shuffle that decides whether a count is surprising — is drawn in [concept_figure.md](concept_figure.md) as an embedded Mermaid diagram. (The release boundary does not allow image files in the tracked tree, so the figure lives as text.) Parts 5 and 6 below work through the same pipeline as explicit hand-countable arithmetic.

## Part 1: What is a connectome?

Your brain contains billions of nerve cells, called **neurons**, and they talk to each other through connections called **synapses**. A **connectome** is the complete wiring diagram of a nervous system: a list of every neuron and every connection between them.

Here is the most useful analogy: a connectome is like a **road map** of a country. The map tells you which towns are connected by roads and which direction each road runs. But a road map does *not* tell you the **traffic** — which roads are busy at rush hour, which ones are closed for repairs, or where any particular car is going. In the same way, a connectome tells you which neurons *could* signal to which other neurons, but not what signals actually flow when an animal learns, decides, or acts (references [12] and [13] in the introduction). Understanding traffic requires additional experiments: recordings of neural activity, perturbations, behavioral measurements. This repository works only with the road map, and it is careful — deliberately — not to claim anything about traffic.

## Part 2: Why the fruit fly?

Mapping every connection in a human brain is far beyond current technology. The fruit fly *Drosophila melanogaster* has a brain small enough — roughly a hundred thousand neurons — that researchers have actually reconstructed the whole adult wiring diagram in a community electron-microscopy effort (reference [1]). Think of it this way: if the human brain is the road network of an entire planet, the fly brain is one well-mapped city. It is small enough to study completely, yet still complex enough to be interesting — flies learn, remember, navigate, and make decisions. Earlier reconstructions covered the adult central brain (reference [8]), a visual pathway (reference [10]), and the larval brain (reference [9]), so each study must state which map it uses rather than treating fly connectomes as interchangeable. Annotation work and a public connectivity explorer provide cell labels and views for the whole-brain dataset (references [14] and [15]).

```mermaid
flowchart LR
    A["A fly brain<br/>~100k neurons"] --> B["Electron microscopy<br/>+ proofreading"]
    B --> C["Wiring diagram:<br/>neurons + directed synapses"]
    C --> D["Directed graph<br/>(this repository's format)"]
    D --> E["Structural questions:<br/>motifs, degrees, convergence"]
```

### The many roads to "a wiring diagram"

**Road 1: set theory.** A connectome is two sets and a membership test: a set of nodes N and a set of edges E, where each edge is an ordered pair (source, target) drawn from N × N. "Is neuron 17 connected to neuron 42?" is the question "is the pair (17, 42) a member of E?" Worked example: N = {A, B, C, D}, E = {(A,B), (A,C), (B,C), (C,A), (D,A)}. Then (A,B) ∈ E — connected; (B,A) ∉ E — not connected, because edges are *ordered* pairs. Direction is nothing more mysterious than the difference between (A,B) and (B,A). *What this buys you:* total precision with zero machinery; every graph question is a membership question. *What it costs you:* membership is silent about strengths, dynamics, and meaning.

**Road 2: linear algebra as weight tables.** Write the wiring as a table with one row and one column per neuron, where the cell (row i, column j) holds the total synaptic weight from i to j (0 if no edge). The whole connectome is then a single inspectable table. Worked example on the same four nodes, edges with weights 2, 1, 3, 1, 4: the table has row A = (0, 2, 1, 0), row B = (0, 0, 3, 0), row C = (1, 0, 0, 0), row D = (4, 0, 0, 0). Tracing one cell: row C, column A holds 1, meaning "C→A carries weight 1." Weighted sums down a column give each neuron's total incoming drive — column A sums to 0 + 0 + 1 + 4 = 5. *What this buys you:* arithmetic on the wiring — total inputs, total outputs, common partners — becomes row and column sums. *What it costs you:* a table of 100,000 neurons is 10^10 cells, so the table is a way of thinking, not a way of storing.

**Road 3: automata and computation.** Read the wiring as the transition graph of a state machine: each neuron is a state-holder, each edge a wire that lets one state's activity influence the next. "Activity flows through the connectome" becomes: put a token on node A, and at each step move copies of the token along every outgoing arrow. Worked example on the four-node graph: start with a token on D (out-edges: D→A). Step 1: token on A (out-edges: A→B, A→C). Step 2: tokens on B and C. Step 3: B→C and C→A give tokens on C and A. Three steps showed that D can influence C within 3 hops — a reachability fact you read off by hand. *What this buys you:* signal flow as token-passing you can simulate on paper. *What it costs you:* real synapses are not tokens; this road says nothing about timing, strength, or inhibition.

**Road 4: geometry.** Give each neuron coordinates and let "close together" mean "likely to be related." Worked example: place A at (0,0), B at (1,0), C at (0,1), D at (5,5). Distances: A–B is 1, A–C is 1, A–D is about 7. The wiring A→B and A→C now *looks* local while D→A looks long-range — geometry turns the abstract edge list into a picture with near and far. *What this buys you:* spatial intuition — neighborhoods, clusters, long-range shortcuts. *What it costs you:* the coordinates are a choice (real anatomy, or an invented layout), and a bad layout can make the same wiring look random or ordered.

## Part 3: What does "learning architecture" mean?

Flies can learn: for example, they can learn that a particular smell predicts a small electric shock, and they will avoid that smell afterward. The brain region most associated with this kind of learning is the **mushroom body**. In plain terms, the mushroom body is the fly's classroom. Simplified, it works like this (reference [7]):

- **Kenyon cells (KCs)** are a large population of neurons that each receive a sparse, somewhat random mixture of smell inputs — like many students each writing down a different partial sketch of the same lecture.
- **MBONs (mushroom body output neurons)** read the KCs' combined activity and turn it into behavior-relevant output, such as "approach" or "avoid" — like the class jointly reaching a verdict.
- **MBINs (mushroom body input neurons, including dopaminergic neurons)** deliver teaching signals — "that went well" or "that went badly" — that adjust how strongly KCs influence MBONs, like feedback changing which notes the class trusts next time.

The word **architecture** means the *pattern of connections*: who connects to whom, in what direction, with what convergence and feedback. A natural question is whether the mushroom body's wiring contains distinctive structural patterns — for instance, particular small circuits — that might support learning. That kind of question is what motivated this project. But the project is equally emphatic about what wiring *cannot* tell you: a structural pattern is not proof of a learning mechanism (reference [2]).

### The many roads to a learning circuit

**Road 1: linear algebra as weight tables.** Learning, in this circuit, is editing one table: the KC→MBON weight table. Before learning, the smell "apple" might drive an MBON with weighted sum 0.2 + 0.3 + 0.1 = 0.6; after the teaching signal arrives, the rule lowers the active cells' weights, say halving them: 0.1 + 0.15 + 0.05 = 0.3 — the same smell now drives the output half as much. Tracing one cell: the weight from KC #2 to the MBON went 0.3 → 0.15, and that single cell's edit is "a synapse changed." *What this buys you:* learning as auditable arithmetic on a table — you can watch exactly which cells moved. *What it costs you:* the table hides *why* the teaching signal arrived when it did; it records consequences, not reasons.

**Road 2: information theory by counting.** The sparse KC layer is an expander: a smell described by, say, 4 active inputs out of 20 is recoded into many more KC combinations. Count the options: the number of ways to choose 4 active inputs from 20 is (20×19×18×17)/(4×3×2×1) = 4845, so the input layer can name fewer than 5000 smells; if the KC layer has 2000 cells with 40 active per smell, the number of nameable patterns is astronomically larger — that expansion is *why* similar smells can be told apart. *What this buys you:* a counting argument for why the architecture is built wide and sparse. *What it costs you:* counts of possible patterns are not counts of usable ones; real discriminability depends on the readout, not just the combinatorics.

**Road 3: game theory as teacher-versus-synapse.** View learning as a repeated game: the teaching signal punishes synapses that voted wrong. Each KC→MBON synapse is a player whose "move" is its weight; after each outcome, players who voted with the losing side lose points and must shrink. Worked example as a 2×2 table — synapse votes "avoid," outcome was "safe": penalty 2; synapse votes "avoid," outcome was "dangerous": reward 1; votes "approach" with "safe": reward 1; votes "approach" with "dangerous": penalty 3. A synapse that keeps its ears open drifts toward voting with the outcome-correlated side — nobody needs to understand the whole circuit for the table of local payoffs to push weights the right way. *What this buys you:* credit assignment as local incentives, no central accountant. *What it costs you:* the payoff table is imposed by the experimenter or the world; the lens does not explain where it comes from.

**Road 4: discrete iterated maps.** Circuit activity is a step-by-step map: the MBON's activity at the next step is a fixed rule of the KCs' current activities (a weighted sum, possibly thresholded). Worked example: rule "MBON_next = sum of active KC weights, keep only if ≥ 0.5." With weights 0.2, 0.3, 0.1 the sum is 0.6 → output 1 (avoid). After learning halves the weights, the same inputs give 0.3 → output 0. The entire behavioral change is one rule evaluated twice with different table entries. *What this buys you:* the before/after of learning as two rows of one table. *What it costs you:* real neurons do not tick in synchrony; the step view is a deliberate simplification.

## Part 4: What are directed-graph methods?

Mathematically, a wiring diagram becomes a **directed graph**: each neuron is a **node** (a dot), and each synaptic connection is a **directed edge** (an arrow) from the source neuron to the target neuron. Direction matters because synapses are one-way: neuron A signaling to neuron B does not mean B signals to A.

This repository represents such graphs in memory (`src/primary_graph.py`) using caller-supplied records: `Node` (an identifier plus a label like `"group_a"`), `Edge` (source, target, weight, kind), and `CollapsedEdge` (one aggregated arrow per source–target pair, with summed weight and a count of contributing raw edges). The function `collapse_edges` merges repeated arrows between the same pair of neurons and drops self-loops, producing a simple weighted directed graph. Null-model helpers (`src/null_models.py`, `src/class_constrained_null_models.py`) then build rewired comparison graphs, and motif helpers (`src/motif_counts.py`) count small patterns.

## Part 5: What is a network motif?

A **network motif** is a small recurring pattern of arrows — usually two or three nodes — that researchers count across a big network (references [3] and [5]). Three motifs appear directly in this repository's code:

- **Convergence** (`count_convergent_targets`): several source neurons all point at the same target — many roads feeding one town.
- **Reciprocal pairs** (`count_reciprocal_cross_group_pairs`): neuron A points to neuron B *and* B points back to A — a two-way street between specific addresses.
- **Feed-forward triangles** (`count_feed_forward_triangles`, also wrapped by `src/m3_feed_forward_triangle.py` for compatibility): a chain with a shortcut — A points to B, B points to C, and A also points directly to C, like an express road running alongside a two-stop route.

```mermaid
flowchart LR
    subgraph Conv["Convergence"]
      s1["S1"] --> t1["T"]
      s2["S2"] --> t1
      s3["S3"] --> t1
    end
    subgraph Recip["Reciprocal pair"]
      a1["A"] --> b1["B"]
      b1 --> a1
    end
    subgraph FFL["Feed-forward triangle"]
      x["A"] --> y["B"]
      y --> z["C"]
      x --> z
    end
```

Counting a motif is just **description**. The hard part is deciding whether the count is *surprising*.

**Counting by hand, once, so the idea is concrete.** Take a tiny four-node graph with five arrows: A→B, A→C, B→C, C→A, D→A. Now tally each motif by enumeration — this is literally what `src/motif_counts.py` does, just on graphs too big for a notebook margin:

- *Feed-forward triangles* (X→Y, Y→Z, X→Z): only one — A→B, B→C, A→C. The triple (C, A, B) fails because C→A and A→B exist but C→B does not.
- *Reciprocal pairs*: one — A→C and C→A.
- *Convergent targets* (nodes with at least two incoming arrows): A gets arrows from C and D, and C gets arrows from A and B — so two targets have convergence.

Nothing here is more than careful list-checking. Every motif count in this project is this procedure scaled up.

### The many roads to a motif count

**Road 1: set enumeration (the native road).** A motif count is the size of a set you can write out: the set of all triples (X, Y, Z) such that (X,Y), (Y,Z), and (X,Z) all belong to the edge set. In the four-node example that set is {(A,B,C)}, so the count is 1. Listing the set and counting its members are the same act — that is why motif counting is description, not inference. *What this buys you:* absolute transparency; every count can be re-derived by listing. *What it costs you:* the list grows cubically with node count, so the listing road is walked by code, not by hand.

**Road 2: information theory by counting.** How surprising is a count? Compare the questions needed. If a motif's presence in any given triple were a fair coin flip, one triple's status costs 1 yes/no question; if the real network shows triangles in 1 of every 16 triples, locating the triangle takes about log2(16) = 4 questions. The gap between "1 question if random" and "4 questions observed" is a counting-based measure of structure. *What this buys you:* surprise in units of yes/no questions, comparable across motifs. *What it costs you:* you must state the reference ("fair coin") explicitly — which is exactly the null-model question of Part 6.

**Road 3: geometry.** Think of each small pattern as a shape, and motif counting as asking how often each shape appears as a sub-shape of the big drawing. Feed-forward triangles are "open" shapes (a chain with a shortcut), reciprocal pairs are "closed" shapes (a two-way street); counting shapes is a visual habit humans are good at. Worked example: in the four-node graph, trace the shape A→B→C with A→C — it looks like a triangle missing its B–A side, which is exactly why it counts as feed-forward and not as a cycle. *What this buys you:* fast pattern recognition and memorable vocabulary (open vs closed shapes). *What it costs you:* pictures fail beyond a handful of nodes, and visual salience is not statistical importance.

**Road 4: automata.** Motif counting is a tiny machine scanning the edge list: for each ordered triple it runs a fixed checklist — "edge 1 present? edge 2 present? edge 3 present?" — and increments a counter. Worked example: triple (C, A, B) — is C→A present? yes; is A→B present? yes; is C→B present? no — checklist fails at step 3, counter unchanged. The counter's final value is the motif count, and the machine's state is just the three yes/no answers. *What this buys you:* the algorithm laid bare — there is no hidden cleverness in `motif_counts.py`. *What it costs you:* the machine view shows how counting works, not what the count means.

## Part 6: What is a null model?

Suppose you count 500 reciprocal pairs in the fly brain. Is that a lot? The honest answer is: **compared to what?** A null model is the "compared to what" made explicit. It is a way of generating randomized comparison networks, so you can ask whether your count is unusual for a network that shares some basic properties with the real one but is otherwise random.

The key idea used here is the **degree-preserving shuffle**. Each node's **degree** is its number of connections — in a directed graph, its **in-degree** (arrows in) and **out-degree** (arrows out). Imagine every neuron is a person holding a fixed number of outgoing and incoming rope ends. The degree-preserving shuffle repeatedly takes two arrows, A→B and C→D, and swaps their targets to get A→D and C→B. Every node keeps exactly the same number of ropes, so all the boring explanations for a motif count — "this neuron just talks a lot" — are held fixed. If a motif is *still* unusually common after thousands of these swaps, the pattern needs a better explanation than raw connectedness (reference [4]).

**One swap, done explicitly.** Use the four-node graph from Part 5: arrows A→B, A→C, B→C, C→A, D→A. Pick the arrows B→C and D→A and swap their targets: they become B→A and D→C. Check the degrees before and after:

| Node | In-degree before | Out-degree before | In-degree after | Out-degree after |
|---|---|---|---|---|
| A | 2 | 2 | 2 | 2 |
| B | 1 | 1 | 1 | 1 |
| C | 2 | 1 | 2 | 1 |
| D | 0 | 1 | 0 | 1 |

Identical columns, different graph — the reciprocal pair A↔C survived, but the feed-forward triangle A→B→C with A→C is gone (B→C no longer exists). That is the whole null-model engine: repeat this swap thousands of times, recount the motifs each time, and you get the reference distribution by brute enumeration rather than by any theorem. Whether the real brain's count sits oddly far out among the shuffled counts is the entire statistical question.

The code implements this in `degree_preserving_null` (`src/null_models.py`), built on a standard graph library's directed edge swap, and then *checks its own work*: after rewiring it raises an error if the degree signature changed or a self-loop appeared. The more constrained variant, `class_constrained_degree_preserving_null` (`src/class_constrained_null_models.py`), additionally preserves the number of edges between each pair of neuron classes — like shuffling road connections while keeping the total count of city-to-suburb, suburb-to-suburb, and suburb-to-city roads fixed. One subtlety the literature makes clear: naive edge swapping can sample some graphs more often than others, so unbiased directed rewiring needs care about how swaps are proposed and accepted (reference [11]).

Crucially, these two null models **ask different questions and can legitimately give different answers**. That is not a software bug; it is a scientific finding. Work on the whole-brain fly connectome shows that network statistics and motifs should be evaluated under multiple reference families (reference [6]), and this project's own headline result is that the reciprocal-pair statistic *changed direction* between its two reference families.

### The many roads to a null model

**Road 1: statistical mechanics by counting.** The set of all graphs with a fixed degree signature is a collection of "microstates," and the shuffle is a random walk among them. If a motif appears in most microstates, seeing it is unremarkable — it is like rolling a total of 7 with two dice, which has 6 of the 36 arrangements. Worked example on our 4-node, 5-edge graph: the degree signature (in/out per node) is A:2/2, B:1/1, C:2/1, D:0/1. Enumerating all 5-edge directed graphs with that signature is a small but real counting exercise; the fraction containing a reciprocal pair is the multiplicity of "reciprocal-pair worlds." Surprise = the real graph belonging to a low-multiplicity macrostate. *What this buys you:* "significant" rephrased as "rare among equally lawful arrangements" — no forces, no distributions to memorize, just counting. *What it costs you:* exact enumeration is feasible only for toy graphs; big connectomes need the sampling shortcut, which inherits the swap-bias subtlety of reference [11].

**Road 2: probability as frequencies.** Run the shuffle 1000 times, count the motif each time, and tally. If the real count exceeds 990 of the 1000 shuffled counts, the empirical frequency of "this extreme by chance" is about 10 in 1000. That fraction — a literal recount of the tally — is the p-value, with no formula in sight. Worked example: shuffled triangle counts: 0 (600 times), 1 (300), 2 (90), 3 (10). The real graph has 3 triangles; only 10 of 1000 shuffles reached 3, so the observed count is rare at the 1% level *by direct count*. *What this buys you:* every inferential claim is an auditable histogram. *What it costs you:* 1000 shuffles resolve frequencies no finer than about 1 in 1000; finer claims need proportionally more compute.

**Road 3: set theory and invariants.** The shuffle is defined by what it *refuses to change*: the degree signature (and, in the constrained variant, the class-block edge counts). An invariant partitions the set of all graphs into equivalence classes — graphs sharing the invariant — and the null model says "sample from the real graph's own class." Worked example: graphs {G1, G2, G3} all share signature A:2/2, B:1/1, C:2/1, D:0/1; G4 does not. The null set is {G1, G2, G3}; G4 is excluded *by membership*, not by distance or preference. Choosing a different invariant (add class-block counts) shrinks the set — a different question, a different class, legitimately a different answer. *What this buys you:* the reason the two null models can disagree, stated as pure set inclusion. *What it costs you:* set membership does not tell you which invariant is scientifically right; that judgment lives outside the formalism.

**Road 4: game theory as a skeptic's bet.** The null model is a skeptic who bets: "I can reproduce your impressive count using only degrees." If the skeptic's 1000 attempts match or beat the real count often, the skeptic wins and the count needs no special explanation. Worked example: skeptic's attempts at the triangle count: 0, 1, 0, 2, 1, … with best value 3 reached twice in 1000 tries; your claim "triangles are special" survives only if the skeptic rarely ties you. The degree constraint is the skeptic's handicap — tightening it (class constraints) gives the skeptic more help, which is why a statistic can flip direction when the handicap changes. *What this buys you:* an adversarial intuition for why a harsher null is a stronger test. *What it costs you:* the skeptic is only as informed as the invariant you grant; the lens does not choose the handicap for you.

## Part 7: Why data-free synthetic validation?

Every function in this repository is **data-free**: it operates only on records the caller supplies in memory. It never reads a file, downloads a connectome, or writes a result. The tests (`tests/`) build tiny synthetic graphs — a dozen nodes drawn by hand — and check invariants: does rewiring preserve degrees? Does the class-constrained rewiring preserve block counts? Does an empty input raise the documented error?

Why insist on this? Three reasons:

1. **Trust through simplicity.** If the code never touches data, reviewers can read and verify everything. There is no hidden preprocessing step that could quietly change the answer.
2. **Correctness before science.** A motif counter that miscounts on a 6-node graph will miscount on 100,000 neurons. Synthetic tests catch bugs at the scale where a human can count the arrows by hand.
3. **A clean release boundary.** Keeping empirical material out of the public tree means the repository can be shared, audited, and extended freely (see [Release Boundary](RELEASE_BOUNDARY.md)).

## Part 8: The pipeline end to end

```mermaid
flowchart TD
    A["Caller-supplied records:<br/>Node + Edge lists"] --> B["primary_graph.py<br/>select_nodes + collapse_edges"]
    B --> C["Simple weighted<br/>directed graph"]
    C --> D["null_models.py<br/>degree_preserving_null"]
    C --> E["class_constrained_null_models.py<br/>class-block-constrained null"]
    D --> F["motif_counts.py<br/>convergence, reciprocal, triangle"]
    E --> F
    F --> G["Compare observed vs. reference families<br/>(empirical comparison: outside this public tree)"]
```

```mermaid
flowchart LR
    subgraph repo["Repository layout"]
      src["src/<br/>graph, null models, motifs"]
      tests["tests/<br/>synthetic invariant tests"]
      tools["tools/<br/>release-boundary scanner"]
      docs["docs/<br/>status, scope, methods, intro"]
    end
```

## Part 9: The math, in one sentence each

Each concept below appears directly in the code. The named resources are free and beginner-friendly; search the quoted title.

- **Directed graph**: a set of dots connected by one-way arrows, the native data structure of connectomes — see 3Blue1Brown or search "graph theory introduction" on Khan Academy.
- **Degree (in/out)**: how many arrows enter and leave a node — the one property every null model here refuses to change (see `degree_signature` in `src/null_models.py`).
- **Edge swap / rewiring**: repeatedly exchanging arrow endpoints to build random graphs with identical degrees — the engine of `degree_preserving_null`; search StatQuest's resampling videos for intuition about shuffling.
- **Permutation test**: judging a statistic by comparing it with what shuffled versions of the same structure produce — the logic behind every null-model comparison; search StatQuest "p-values" and "permutation".
- **Motif count**: a tally of a small arrow pattern, treated as a summary statistic of the whole network — see `src/motif_counts.py` and reference [3].
- **Statistical power / multiple comparisons**: testing many motifs at once inflates the chance of a false "discovery" — search Seeing Theory's chapters on inference for an interactive treatment.

## Part 10: What this project actually found

To keep the introduction honest, it ends with the results, stated plainly: the **convergence diagnostic was non-discriminative** under both reference families; the **reciprocal-pair diagnostic changed direction** when the reference family changed; and the **feed-forward-triangle diagnostic has been defined and tested on synthetic graphs only — never run on real data**. The overall conclusion is *inconclusive for enrichment, mechanism, or causation*, with one durable methodological lesson: **the choice of null model is part of the scientific question, not a technical afterthought** (reference [6]).

## References

All references are the numbered list in [INTRODUCTION.md](INTRODUCTION.md), cited here by number only; no new sources were introduced. The entries used above are: [1] the adult-brain wiring diagram reconstruction; [2] the central-complex connectome and its motif analysis; [3] the founding network-motifs paper; [4] the reference on random graphs with fixed degree sequences; [5] the review of motifs in brain networks; [6] the whole-brain fly connectome network-statistics study; [7] the adult mushroom-body connectome; [8] the adult central-brain connectome; [9] the larval insect-brain connectome; [10] the visual-pathway connectome; [11] the study of unbiased degree-preserving randomization; [12] and [13] perspectives on what connectomes can and cannot deliver; [14] the whole-brain annotation study; [15] the public connectivity explorer.

## Choosing your road

If you think in dots, arrows, and shapes, take **graph theory** and **geometry** — a connectome is a drawing, a motif a sub-shape. If you think in membership tests and invariants, take **set theory** — a null model is an equivalence class, an edge an ordered pair. If you think in tables of numbers, take **linear algebra as weight tables** — wiring is a matrix and learning is editing cells. If you think in tallies and enumeration, take **statistical mechanics by counting** and **probability as frequencies** — surprise is low multiplicity, and a p-value is a recount. If you think in questions and answers, take **information theory** — structure is how many yes/no questions the network saves you. If you think in machines and checklists, take **automata** — a motif counter is a three-question checklist in a loop. If you think in incentives and adversaries, take **game theory** — a null model is a skeptic with a handicap, and a teaching signal is a payoff table. If you think in step-by-step rules, take **discrete iterated maps** — circuit activity is one rule evaluated row after row.

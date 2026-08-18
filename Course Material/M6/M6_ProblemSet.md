# Computational Statistics — Problem Sets

## Module 6 — Markov Chains as Computational Objects

### PS6.1 — Simulate, verify, and break: mixing, stationarity, and their absence
**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 1, 2
**Prerequisites:** None.

**Statement:**
Define a 4-state Markov chain — call it your **main chain** — on states $S_0, S_1, S_2, S_3$ with transition matrix
$$
P = \begin{pmatrix}
0.5 & 0.3 & 0.2 & 0.0 \\
0.2 & 0.4 & 0.3 & 0.1 \\
0.1 & 0.3 & 0.4 & 0.2 \\
0.0 & 0.2 & 0.3 & 0.5
\end{pmatrix}
$$
(row $i$ = current state $S_i$, column $j$ = next state $S_j$; each row sums to 1, confirm this). Before doing anything computational, look at the matrix and confirm two structural facts by inspection: (i) **irreducible** — every state can reach every other state in some number of steps (trace the nonzero entries); (ii) **aperiodic** — every state has a strictly positive self-transition probability, which alone rules out periodic behavior.

*Part A (simulate).* From primitives — your own uniform-RNG draw and a manual categorical-sampling step (do **not** call a library "sample from a discrete distribution" routine) — simulate a single trajectory of the main chain for $N \ge 200{,}000$ steps, starting at $S_0$. Set and report your seed. Record how often each state is visited and convert to occupancy frequencies (visits to $S_i$ divided by $N$).

*Part B (solve analytically).* Using library linear algebra (permitted here per R4(b) — this is verification machinery, not the algorithm the goal is about), solve for the stationary distribution $\pi^*$ satisfying $\pi^* P = \pi^*,\ \sum_i \pi^*_i = 1$ — e.g. by solving the linear system directly, or via the left eigenvector of $P$ for eigenvalue 1. If you have access to both methods, use them to cross-check each other.

*Part C (compare).* Compute the maximum absolute difference between your Part A occupancy vector and your Part B $\pi^*$, state-by-state.

*Part D (periodic contrast).* Now consider a second, much smaller chain — call it the **periodic chain** — with two states and transition matrix
$$
P_{\text{per}} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix},
$$
i.e. from either state the chain deterministically swaps to the other. Starting from $\mu_0 = (1, 0)$, compute the distribution $\mu_t = \mu_0 P_{\text{per}}^t$ for $t = 0, 1, \dots, 7$ by matrix powers — no simulation needed; this is exact and deterministic. Observe what happens: does $\mu_t$ ever settle down?

**Deliverable:** Your Part A occupancy-frequency vector; your Part B $\pi^*$; the Part C max absolute difference; the Part D sequence $\mu_0, \dots, \mu_7$ as a short table. In 5–6 sentences: (i) state what Parts A–C together confirm about your main chain reaching a stationary distribution; (ii) name, in your own words, what "mixing," "stationarity," and — by contrast — "failure to converge" each look like in the numbers you just produced (Parts A–C give you the first two; Part D gives you the third); (iii) explain what irreducibility and aperiodicity are each guaranteeing here — be specific about which guarantee (existence of a stationary distribution vs. convergence to it) each property is responsible for; (iv) explain in one or two sentences why $P_{\text{per}}$ never settles despite being a perfectly well-defined, irreducible chain — name the one structural property it lacks.

**Verification:** Part B's $\pi^*$ is a **tier-2** fact: the exact solution of $\pi^*P = \pi^*,\ \sum \pi^*_i = 1$ for the stated matrix — a fully determined linear-algebra computation, no simulation involved. Parts A vs. B (**tier 3**, executed and logged): at $N \ge 200{,}000$ steps, the max absolute difference between your Part A occupancy vector and your own Part B $\pi^*$ should be **less than 0.02** per state. Part D is a **tier-2** fact (exact matrix powers, no tolerance needed): $\mu_t$ must equal exactly $(1,0)$ at even $t$ and exactly $(0,1)$ at odd $t$, for every $t$ you compute — any other value indicates an implementation bug, not sampling noise.

**Discussion note:** (folded) If Parts A and B agree well but you're not sure your simulation is really "from primitives," the tell-tale sign of an accidental library shortcut is usually *too-good* agreement combined with suspiciously round timing — a hand-rolled categorical draw from a single uniform number (walk the cumulative-probability boundaries until you cross the drawn value) is slower and noisier than a compiled routine, and that noise is exactly what Part C's tolerance is sized to absorb. Irreducibility and aperiodicity are doing two genuinely different jobs, and it's worth being precise about which is which: irreducibility (together with finiteness) guarantees a stationary distribution *exists* — the periodic chain has one too, $\pi_{\text{per}} = (0.5, 0.5)$, exactly as irreducible as your main chain — while aperiodicity is what guarantees the chain actually *converges* to it from an arbitrary start. The periodic chain's stationary distribution is real; it's just a fixed point the chain approaches from nowhere except the fixed point itself, because starting anywhere off it, the chain oscillates around it forever rather than settling into it. This is the cleanest way to see why LPW's characterization of irreducibility — a chain is irreducible if and only if its associated state-transition graph is connected (LPW Ch. 1) — is necessary but not sufficient for what Goal 1 asks you to observe: connectivity alone buys you existence of $\pi$, not convergence to it. Zoom out on what you've actually done here: Parts A–C are Goal 1's first two phenomena (mixing and stationarity) made numeric — your simulated trajectory *mixes* toward $\pi^*$, and $\pi^*$ *is* the stationary distribution both by direct simulation and by exact linear algebra agreeing. Part D is the third phenomenon, failure to converge, built as a deliberate foil: same finite-state, well-defined, irreducible chain machinery, one missing property, qualitatively different long-run behavior. Hold onto both chains — a later problem in this module reuses your main chain (unchanged) to make the "how fast does it converge" question precise, and it will point back to this periodic chain again as a reminder of what "guaranteed to converge" was buying you all along.

---

### PS6.2 — Detailed balance: verifying it, and watching it fail
**Type:** I/D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 35 min | **Goals:** 3
**Prerequisites:** None.

**Statement:**
You'll build two small chains and put detailed balance to the numeric test on both.

*Chain 1 (reversible, by construction).* Define a **birth–death chain** on states $\{0,1,2,3\}$ — a chain that only moves to a neighboring state or stays put, never jumps more than one state in a single step:
$$
P^{(1)} = \begin{pmatrix}
0.6 & 0.4 & 0.0 & 0.0 \\
0.3 & 0.3 & 0.4 & 0.0 \\
0.0 & 0.2 & 0.3 & 0.5 \\
0.0 & 0.0 & 0.5 & 0.5
\end{pmatrix}.
$$
Compute its stationary distribution $\pi^{(1)}$ (library linear algebra, as in PS6.1 Part B). Then, for **every** pair of states $(i,j)$ — including the pairs with zero transition probability in one or both directions — numerically check whether
$$
\pi^{(1)}(i)\, P^{(1)}(i,j) \;=\; \pi^{(1)}(j)\, P^{(1)}(j,i).
$$

*Chain 2 (non-reversible, by construction).* Define a **biased directed 4-cycle** on the same 4 states — a chain that only ever moves "forward" around a cycle (or stays put), never backward:
$$
P^{(2)} = \begin{pmatrix}
0.3 & 0.7 & 0.0 & 0.0 \\
0.0 & 0.3 & 0.7 & 0.0 \\
0.0 & 0.0 & 0.3 & 0.7 \\
0.7 & 0.0 & 0.0 & 0.3
\end{pmatrix}
$$
(state 3 wraps forward to state 0). Compute its stationary distribution $\pi^{(2)}$ the same way. Then run the same pairwise check as Chain 1 on every **adjacent** pair in the cycle (i.e., $(0,1), (1,2), (2,3), (3,0)$), and compute the **net flow** for each pair,
$$
\text{net}(i \to j) = \pi^{(2)}(i)\,P^{(2)}(i,j) \;-\; \pi^{(2)}(j)\,P^{(2)}(j,i).
$$
Confirm separately that Chain 2 is still irreducible (every state reachable from every other, even though every move is "forward").

**Deliverable:** $\pi^{(1)}$ and, for every pair $(i,j)$, the two sides of the detailed-balance equation and their difference. $\pi^{(2)}$ and, for every adjacent pair, the two sides and the net-flow value. A short (3–5 sentence) interpretation: does Chain 1 satisfy detailed balance? Does Chain 2? Does Chain 2 still have a valid, well-defined stationary distribution despite the failure? What does "net flow" mean physically in terms of probability circulating around the cycle rather than sitting still — and why is detailed balance a *sufficient* but not *necessary* condition for stationarity (i.e. what does Chain 2 prove by existing)?

**Verification:** Both $\pi^{(1)}$ and $\pi^{(2)}$ are **tier-2** facts (exact linear-algebra solutions of the stated matrices). The pairwise comparisons are **tier 3** (executed and logged): for Chain 1, $|\pi^{(1)}(i)P^{(1)}(i,j) - \pi^{(1)}(j)P^{(1)}(j,i)|$ should be **less than $10^{-8}$** for every pair (an exact identity up to floating-point solver precision, not a statistical tolerance — if you see a larger gap, suspect a $\pi^{(1)}$ computation bug, not sampling noise, since nothing here is sampled). For Chain 2, every one of the 4 adjacent-pair net-flow values should be **clearly nonzero** (magnitude greater than 0.05) and should agree with each other in sign and to within a small relative tolerance, by the cycle's built-in symmetry.

**Discussion note:** (folded) Chain 1 is a birth–death chain — a chain whose only allowed moves are to a nearest neighbor (or staying put) on a path. This structure is not a coincidence: any such chain is reversible with respect to its own stationary distribution, essentially because there's only ever one "edge" of probability flow to balance between any two connected states, and the balance equation between neighbors, iterated along the path, is enough to pin down the whole distribution up to normalization. Chain 2 breaks that structure on purpose: it moves only forward around a cycle, so there is a direction of net probability circulation baked into the transition rule itself, and detailed balance — which asks the flow between *every pair* to cancel exactly — has no chance of holding, even though the chain still settles into a perfectly good, unique stationary distribution (uniform, here, by the cycle's symmetry). This is Goal 3's central point made concrete: detailed balance is a *sufficient* condition for a distribution to be stationary (if it holds, you're guaranteed $\pi P = \pi$), but it is not *necessary* — Chain 2 is living proof, since it has a valid $\pi^{(2)}$ without detailed balance ever holding on a single pair. The reason MCMC algorithms are built to enforce detailed balance anyway, rather than aiming for stationarity directly, is constructive: detailed balance gives you a *local*, pairwise condition you can engineer into a proposal-and-accept/reject rule (this is exactly what Module 7's Metropolis–Hastings acceptance ratio does), whereas "has the right stationary distribution" alone is a *global* property with no obvious local recipe for achieving it. Keep the net-flow number in mind, too — 0.175 units of probability mass circulating past any point on this cycle, every step, forever, at stationarity — as a concrete image of what "detailed balance fails" *means*, not just a checkbox that comes back false.

---

### PS6.3 — Spectral gap and mixing time on the lazy $n$-cycle
**Type:** V/D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 50 min | **Goals:** 4, 5 (Goal 1 also touched empirically, via the mixing observation in Part C)
**Prerequisites:** None.

**Statement:**
*Part A (build the family).* For each $n \in \{4,5,6,7,8,9,10\}$, construct the transition matrix $P_n$ of the **lazy random walk on the $n$-cycle**: from state $i \in \{0,\dots,n-1\}$ (indices taken mod $n$), stay at $i$ with probability $1/2$, move to $i+1$ with probability $1/4$, and move to $i-1$ with probability $1/4$. (The self-loop's "laziness" matters: the *non-lazy* random walk on an even cycle is periodic, and Goal 4's mixing-time question wouldn't even be well-posed for it — you're building on the aperiodicity point from PS6.1 directly.) Confirm that the uniform distribution $\pi_n = (1/n, \dots, 1/n)$ is stationary for $P_n$ (a quick exact check — $P_n$ is doubly stochastic, so this should hold for every $n$).

*Part B (spectral gap).* Using library eigendecomposition (linear algebra, permitted per R4(b)), compute the eigenvalues of each $P_n$ and record the **spectral gap** $\gamma_n = 1 - \lambda_2(P_n)$, where $\lambda_2$ is the second-largest eigenvalue (the largest, $\lambda_1$, is always 1 for a valid transition matrix).

*Part C (empirical mixing time).* Define the mixing time $\tau_n(\varepsilon)$, with $\varepsilon = 0.25$, as the smallest $t$ such that $\lVert \delta_0 P_n^t - \pi_n \rVert_{TV} \le \varepsilon$, where $\delta_0$ is the point mass at state 0 and $\lVert \cdot \rVert_{TV}$ is total variation distance. Compute $\tau_n(\varepsilon)$ **exactly** via matrix powers — feasible here because every $n$ in your sweep is $\le 10$ states, so no simulation or Monte Carlo estimate is needed at all.

*Part D (plot and connect).* Produce two plots: $\tau_n(\varepsilon)$ against $n$, and $\tau_n(\varepsilon)$ against $\gamma_n$ (or against $1/\gamma_n$, whichever relationship looks cleaner). In 3–5 sentences: describe the relationship between spectral gap and mixing time that you observe (does mixing time grow as the gap shrinks? roughly how — linearly in $1/\gamma_n$, or some other pattern?); then connect this to **Goal 5**, referencing your own PS6.1 Part A experience — explain concretely what a much smaller spectral gap (a much slower-mixing chain) would imply for the reliability of an occupancy-based estimate computed from a *fixed-length* simulated trajectory, and why you might need a substantially longer run on a slow-mixing chain to trust the same estimate you trusted after 200,000 steps in PS6.1.

*Part E (definitional anchor — one paragraph, hand-derived, not swept).* Separately from the $n$-cycle family above, consider the simplest possible chain that has a tunable spectral gap: the two-state chain with **switch probability** $p \in (0, 0.5]$,
$$
P = \begin{pmatrix} 1-p & p \\ p & 1-p \end{pmatrix}.
$$
By hand — this is the one place in this problem where you work the algebra directly rather than calling a library — show that the eigenvalues of $P$ are $1$ and $1-2p$ (hint: solve the characteristic equation $\det(P - \lambda I) = 0$ directly, or note that $P = (1-2p)I + 2p\,\bar P$ where $\bar P$ has every entry $1/2$), and hence that the spectral gap is $\gamma = 2p$. In one sentence, say what happens to mixing speed as $p \to 0$.

**Deliverable:** A table of $(n, \gamma_n, \tau_n(\varepsilon))$ for your sweep; the two plots from Part D; the Part E hand-derivation shown in your own algebra, plus your one-sentence answer about $p \to 0$; the 3–5 sentence write-up connecting Parts B–D to Goal 5 and to your PS6.1 experience.

**Verification:** The spectral gaps $\gamma_n$ are **tier-2** facts — exact library-computed eigenvalues of the fully specified matrices $P_n$ (this is verification/characterization machinery, not the "core algorithm from primitives" the module is built around). The mixing times $\tau_n(\varepsilon)$ are **tier 3** (executed and logged): each is an exact integer from a deterministic matrix-power computation (zero statistical tolerance — a mismatch against your own recomputation indicates a bug, not numerical noise), and across your swept range $\tau_n(\varepsilon)$ should be **non-decreasing** as $n$ increases, while $\gamma_n$ should be **strictly decreasing**. Part E's eigenvalues and gap formula are a **tier-2** self-verifying closed form: once derived, you can check them directly by confirming $Pv = \lambda v$ for your two eigenvectors.

**Discussion note:** (folded) The pattern you should see in Part D is that $\tau_n(\varepsilon)$ and $\gamma_n$ move in a roughly reciprocal relationship — their product stays close to a constant across most of your sweep (it drifts a little at the very smallest $n$, which is a small-number edge effect, not a sign of a bug), which is the signature of the well-known "diffusive" scaling for this family: the spectral gap of the lazy $n$-cycle shrinks like $1/n^2$ as $n$ grows, so mixing time grows like $n^2$ — a chain on twice as many states takes *roughly four times as long* to mix, not twice as long. This is the concrete content behind the geometric intuition Goal 4 is after: a longer cycle isn't just "more states to visit," it's a *worse-conditioned* chain in a precise, quantifiable sense, and the spectral gap is what quantifies it. (This is also this module's own conceptual question 33, if you want a second angle on the same relationship stated more qualitatively.) The Goal 5 connection is the practical payoff: your PS6.1 main chain had a comfortably large gap and 200,000 steps gave you an occupancy estimate accurate to a couple thousandths — but on a chain with a spectral gap ten or a hundred times smaller, that same run length would leave you far short of stationarity, and an occupancy-frequency "estimate" computed from it wouldn't actually be estimating $\pi$ yet; it would still be showing you the transient. This is precisely why "just run it longer" is not a free pass in practice — how much longer scales with $1/\gamma$, and a chain's spectral gap is not something you get to see just by watching a trace plot look stable for a while. Part E's two-state chain is the cleanest possible illustration of the gap itself: at $p=0.5$ the chain forgets its past state entirely in a single step ($\gamma=1$, fastest possible mixing), and as $p \to 0$ the chain becomes increasingly "sticky" — it almost never switches, the gap shrinks toward 0, and mixing time grows without bound. (Note, incidentally, that $p=1$ would reproduce PS6.1's periodic 2-cycle exactly — outside this problem's $p \in (0,0.5]$ domain on purpose, since $1-2p$ going negative changes what "gap" even means and that subtlety isn't this problem's job to resolve.) The chains you've just measured here are exactly the kind of object Module 7's samplers *are* — MH and Gibbs are Markov chains engineered to have a specific target as their stationary distribution, and everything this problem taught you about spectral gap and mixing time applies to them directly (preview).

---

### PS6.4 — Why mixing time is well-defined: TV contraction and monotonicity
**Type:** I | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 35 min | **Goals:** 4
**Prerequisites:** Requires the transition matrix $P$ you specified in PS6.1 (Parts A–C — the 4-state **main chain**, not the periodic chain), unchanged.

**Statement:**
Every mixing-time claim you made in PS6.3 quietly assumed something: that "distance to stationarity" only ever shrinks as $t$ grows, so that "the first $t$ where you're within $\varepsilon$" is a sensible, well-defined quantity rather than something that could flicker back above threshold later. This problem proves that assumption.

Let $\lVert \mu - \nu \rVert_{TV} = \frac{1}{2}\sum_x |\mu(x) - \nu(x)|$ denote total variation distance between two distributions $\mu, \nu$ on the same finite state space, and let $P$ be any transition matrix (rows summing to 1) on that space.

*Part A (TV contraction — reconstruct the proof).* Show that applying $P$ can only contract total variation distance, never increase it:
$$
\lVert \mu P - \nu P \rVert_{TV} \;\le\; \lVert \mu - \nu \rVert_{TV} \qquad \text{for all distributions } \mu, \nu.
$$
Work from the definition of TV distance and the fact that $P$'s rows sum to 1. (This is the TV-contraction result harvested from MIT OCW 18.445's LPW-based problem sets — Levin, Peres & Wilmer; a solved exercise, chapter-mapped to this module's assigned Ch. 4 reading. Its exercise number within the specific edition assigned to this program has not been independently confirmed, so no exercise or section number is cited here.) *Hint, if you want the shortest route*: bound $|(\mu P - \nu P)(y)|$ using the triangle inequality applied to the sum $\sum_x (\mu(x)-\nu(x))P(x,y)$, then sum over $y$ and swap the order of summation.

*Part B (monotonicity of $d(t)$ — derive as a corollary of Part A).* Let $\pi$ be a stationary distribution of $P$ (so $\pi P = \pi$), and define
$$
d(t) = \sup_{\mu} \lVert \mu P^t - \pi \rVert_{TV},
$$
the worst-case distance to stationarity over all possible starting distributions $\mu$, after $t$ steps. Using Part A — applied to the specific pair $(\mu P^t,\ \pi)$, and the fact that $\pi P = \pi$ — show that
$$
d(t+1) \;\le\; d(t) \qquad \text{for all } t \ge 0.
$$
(This is the companion harvested exercise — using the contraction result above, it proves $d(t)$ is non-increasing — likewise a solved MIT OCW 18.445 / LPW exercise, chapter-mapped but not exercise-number-verified; same citation-form caveat as Part A.)

*Part C (confirm it empirically, on your own chain).* Using your PS6.1 main-chain transition matrix $P$ (unchanged) and its stationary distribution $\pi^*$ (also from PS6.1), compute $d(t)$ **exactly** for $t = 0, 1, \dots, 20$. You can compute $d(t)$ tractably for a small chain like this one by using a fact worth noting explicitly: because $\lVert \mu P^t - \pi \rVert_{TV}$ is a convex function of $\mu$ (it's a linear map of $\mu$ composed with a norm), its supremum over the full probability simplex is attained at a vertex of the simplex — i.e., you only need to check point-mass starting distributions $\delta_0, \delta_1, \delta_2, \delta_3$ and take the max, not search over all possible $\mu$. Confirm your computed sequence is non-increasing.

*Part D (optional reinforcement — your discretion).* Repeat Part C's exact $d(t)$ computation for PS6.1's periodic chain. You should find it stays flat rather than decaying — monotonicity (Part B) still holds (trivially, since a constant sequence is non-increasing), but the chain never actually converges. This is the same aperiodicity point from PS6.1 Part D, now visible directly in $d(t)$ rather than in a single oscillating trajectory.

**Deliverable:** Parts A and B as short written derivations (a few lines of algebra/reasoning each — not a page of real analysis). Part C's $d(t)$ sequence for $t=0,\dots,20$, presented as a table or a plot on a log scale, with a one-line confirmation that it is non-increasing. If attempted, Part D's flat $d(t)$ sequence for the periodic chain, with a one- or two-sentence comparison to Part C.

**Verification:** Parts A and B are **tier 1**: the results being (re)proved are two solved exercises from MIT OCW 18.445's LPW-based problem sets (TV contraction; $d(t)$ monotonicity), chapter-mapped to this module's assigned Ch. 4 reading — your derivation should arrive at the boxed inequalities above via your own reasoning, not a transcription of the source's proof. Part C is **tier 3** (executed and logged): your computed $d(t)$ sequence must be **non-increasing** at every step you compute (any observed increase larger than floating-point noise, roughly $10^{-10}$, indicates an implementation bug); you should also see $d(0)$ well above $0.5$ and $d(t)$ shrinking to a very small number (below $10^{-4}$) by around $t \approx 15$–$20$ for this particular chain. Part D, if attempted, is an exact structural fact with zero tolerance: $d(t)$ must equal exactly $0.5$ for every $t$.

**Discussion note:** (folded) The proof strategy in Part A is the elementary route — triangle inequality plus the fact that $P$'s rows sum to 1 — and it's worth noticing that it needs nothing beyond definitions you already have; it does *not* go through a coupling construction. LPW's own exposition of this material (§4.2–§4.4) leans heavily on coupling — building two copies of the chain on a shared probability space and bounding TV distance by their meeting time — which is a genuinely illuminating alternative technique, but one this module does not assign as reading (coupling is LPW Ch. 5, out of scope here). If you're curious what that alternative route looks like conceptually: two chains started from $\mu$ and $\nu$ respectively, run so that once they land on the same state they move together forever after — the probability they *haven't* yet met by time $t$ turns out to upper-bound $\lVert \mu P^t - \nu P^t\rVert_{TV}$, which gives another way to see why repeated applications of $P$ can only bring distributions closer together. You are not asked to formalize that argument here; the elementary proof in Part A is complete on its own and is the one this problem holds you to. Part B's derivation is the satisfying payoff of Part A: monotonicity of $d(t)$ isn't a separate fact requiring separate machinery — it falls straight out of contraction applied to the single pair $(\mu P^t, \pi)$, using $\pi$'s defining property $\pi P = \pi$ to keep the "target" side of the inequality fixed at $\pi$ across the step. Part C closes the loop back to PS6.3: mixing time (the first $t$ with $d(t)$ below some threshold) is only a *well-defined, unambiguous* number because $d(t)$ can't un-shrink partway through — without Part B's result, "the first $t$ below $\varepsilon$" could in principle mean different things depending on how far out you were willing to search. Part D (if you did it) makes the distinction between "monotonic" and "convergent" impossible to blur: the periodic chain's $d(t)$ is perfectly non-increasing — it's constant — while never once getting closer to 0. Monotonicity is a weaker, more generally-true statement than convergence; aperiodicity is what upgrades one into the other, and now you've seen that fact from three different angles across this module (a single trajectory that won't settle, in PS6.1; a flat vs. decaying $d(t)$ curve, here).

---
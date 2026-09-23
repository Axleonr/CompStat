# Module 1
## Random Number Generation & Simulation

Every method in this program ultimately depends on the ability to generate random numbers. This module examines where those numbers come from. Computers are deterministic machines, so randomness must be constructed — through algorithms that produce **sequences with the right statistical properties**, even though they are entirely determined by an initial seed. Understanding this is not merely a technical curiosity: it shapes how you think about reproducibility, about the limits of simulation, and about what it means to say a result is "random."

From this foundation the module moves to basic stochastic simulation — turning uniform random numbers into samples from arbitrary distributions — which is the primitive operation on which Monte Carlo and MCMC are built.

### Reading Guide
The module has a natural two-stage structure: uniform generation first, then non-uniform. Read in the order given. Owen and L'Ecuyer cover the uniform layer in parallel — **read them together** before moving to the non-uniform material.

***
#### Uniform PRNGs
1. *Owen (2013) — Monte Carlo Theory, Methods and Examples*
**Ch 3: Uniform random numbers**
	- **Focus**: Focus on what properties a sequence must have to behave statistically as random, and why a deterministic algorithm can produce such a sequence. The statistical tests for uniformity in this chapter are important: they are the operational definition of "good" randomness at the uniform level.
	- **Builds toward**: This lays the uniform foundation that all non-uniform methods (Ch 4 and Devroye) take as given.

2. *L'Ecuyer (1998) — Random Number Generation*
**In *J. Banks (Ed.), Handbook of Simulation***
	- **Focus**: Focus on the internal mechanics of PRNG construction: LCGs, combined generators, period length, and what it means for a deterministic sequence to pass randomness tests. *Owen covers what properties are required; L'Ecuyer explains how they are achieved. Read these together, they address the same topic from complementary angles*. §4.3.5 through §4.4 (lacunary indices, matrix generators, LFSRs, nonlinear methods) go beyond what this module requires; read for awareness and move on.
	- **Builds toward**: Understanding generator mechanics is prerequisite to understanding reproducibility, period exhaustion, and the correlation artifacts that matter in Goal 1.6.

***

#### Non-uniform RN Generation

3. *Owen (2013) — Monte Carlo Theory, Methods and Examples*
**Ch 4: Non-uniform random numbers**
	- **Focus**: Read both **§4.1–4.2** (inversion principle and worked examples) and **§4.7** (acceptance-rejection) carefully. The intervening sections can be read selectively: 
		- **§4.3** introduces the practical challenge of inverting the normal CDF — the key point is that numerical inversion is feasible, not the implementation details of specific algorithms. 
		- **§4.6** (Box-Muller and other transformations) is interesting background but is not load-bearing for this module's goals; students pressed for time may treat it as optional. 
		- **§4.8** (gamma generators) illustrates acceptance-rejection proposal design in a realistic setting and is worth skimming; 
		- **§4.9** (automatic generators) is optional. Keep the connection back to Ch 3 explicit throughout: inversion and acceptance-rejection both take $U(0,1)$ draws as their input, and those draws come from the PRNG you just read about.
	- **Builds toward**: These two methods are the building blocks for every more complex sampling algorithm in the program; they reappear in Module 2 (importance sampling) and Module 7 (MCMC proposal design).

4. *Devroye (1986) — Non-Uniform Random Variate Generation*
**Ch II: §2.1–2.3 (inversion method); §3.1–3.3 (rejection method)**
*Read after Owen Ch 4, not in parallel.*
	- **Focus**:  Devroye's value is not coverage, but rigor and algorithmic design perspective. For the inversion method, note Devroye's Example 2.4 — the claim that inversion is "the only truly universal method" is the cleanest statement of when and why it applies. For acceptance-rejection, §3.2 is the essential section for this module: it works through the optimization of the proposal distribution explicitly, showing how to minimize the rejection constant $c$ by choosing the best $g$ within a parametric family. This is the formal treatment of what makes a proposal better or worse. Students pressed for time may treat §3.3 (generalizations) as a reference rather than a read-through.
	- **Builds toward**: Devroye's proposal optimization framework (§3.2) connects directly to Module 7's discussion of proposal distribution choice in Metropolis-Hastings.
***

5. *L'Ecuyer (1999), "Good Parameters and Implementations for Combined Multiple Recursive Random Number Generators"*, Operations Research 47(1). \
**[Optional]**
	For students who want to see the technical construction of combined generators in detail. Not required for any Goal.

> **Synthesis note:** After finishing all four readings, pause before beginning the self-assessment. Try to state in one paragraph the complete generative chain — from PRNG seed through uniform output through non-uniform transformation to a final sample from an arbitrary target distribution. Each link in that chain is covered in the readings, but no single source assembles all of them. Constructing that narrative yourself is what Goal 5 asks for.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Explain why a computer cannot generate true randomness, and describe what a pseudorandom number generator actually does? (Goal 1.1)
- Name and describe the key structural properties of a good uniform PRNG: period length, seed dependence, and the statistical tests used to evaluate output quality? (Goal 1.2)
- Implement the inverse transform method and state the conditions under which it applies? (Goal 1.3)
- Implement acceptance-rejection, explain where its efficiency comes from, and identify what makes a proposal distribution better or worse? (Goal 1.4)
- Trace a sample from an arbitrary target distribution back through the full generative chain to the PRNG output? (Goal 1.5)
- Describe at least two practical consequences of poor RNG choices in simulation? (Goal 1.6)

#### Conceptual Questions
1.	A pseudorandom number generator is entirely deterministic — given the same seed, it produces the exact same sequence every time. In what sense, then, can its output be called "random"? What does randomness mean here, and how is that meaning established? (Goal 1.1)
2.	The inverse transform and acceptance-rejection methods both produce draws from a target distribution, but they work in fundamentally different ways. What does each method require, and what does each assume about the target? When would you prefer one over the other? (Goal 1.3)
3.	Period exhaustion is rarely discussed in practice. Why does it matter, and under what conditions could it become a real problem rather than a theoretical concern? (Goal 1.6)
4.	Devroye treats the uniform generation problem as already solved and takes U(0,1) draws as given. Why is this a sensible division of labor? What would break if the uniform draws were not actually independent? (Goal 1.5)
5.	Module 2 builds Monte Carlo estimation on top of the simulation primitives from this module. What specific properties of your RNG output does the validity of a Monte Carlo estimate depend on? (Goal 1.6)
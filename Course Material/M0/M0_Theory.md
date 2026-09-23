# Module 0
## Computational Thinking & Statistical Algorithms
***

Statistics has traditionally been taught as a collection of formulas and decision rules. This module reframes the discipline from the ground up: statistical procedures are algorithms that take data as input and produce estimates, intervals, or decisions as output. That reframing has consequences. It means we can ask how fast an algorithm converges, how sensitive it is to its inputs, whether it can be made more efficient, and under what conditions it breaks.

This module establishes the vocabulary and mental habits that the rest of the program depends on. You will not write complex code here, but you will leave with a clearer picture of what it means to *compute* a statistical answer and why that question is different from simply *deriving* one.

### Reading Guide
Read in the order given.

1. *Tukey (1962) — The Future of Data Analysis*
**Read in full (~40 pages)**
	- **Focus**: Read as a disciplinary argument, not as historical background. Identify Tukey's central claim about the relationship between statistics and data analysis, and note where his critique is directed. The argument is short enough that every section earns attention; resist the urge to skim.
	- **Builds toward**: Efron & Hastie Ch 1 picks up directly from Tukey's framing — reading them together makes the progression from Tukey's critique to modern computational practice explicit.

2. *Efron & Hastie (2016) — Computer Age Statistical Inference*
**Ch 1: Algorithms and Inference**
	- **Focus**: Focus on the conceptual argument about what changed when computation entered statistical practice — what questions became askable, what the relationship between algorithms and inference looks like. Ch 2 (Frequentist Inference) is listed as optional orientation context; read it if you want a compact framing of classical inference as the foil for everything that follows, but it is not required.
	- **Builds toward**: This chapter's framing of statistics as a computational discipline is the lens through which every subsequent module should be read.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Describe a familiar statistical procedure (e.g., least squares, MLE) as an algorithm — specifying its inputs, the computational process, and its outputs? (Goal 0.1)
- Articulate the difference between deriving a statistical result analytically and computing one algorithmically, and explain why that distinction matters for how we evaluate methods? (Goal 0.2)
- Name the questions the computational framing opens up (convergence, sensitivity, efficiency, failure conditions) and give one concrete example of each? (Goal 0.3)
- Locate simulation, resampling, optimization, and MCMC within a unified algorithmic view of statistics? (Goal 0.4)
- State Tukey's central argument in one or two sentences and assess whether it has aged well? (Goal 0.5)

#### Conceptual Questions
1.	Tukey writes that “data analysis” is not the same as mathematical statistics. What is the substance of that distinction, and what does it imply about how statistical methods should be evaluated? (Goal 0.5)
2.	What does Efron & Hastie mean by an “algorithm” in the context of statistical inference? How is this different from a formula or a theorem? (Goal 0.2)
3.	The computational framing of statistics asks: how fast does this converge, how sensitive is it to its inputs, under what conditions does it fail? Pick one of these questions and explain why it could not be asked — or was much harder to answer — in a purely analytical framework. (Goal 0.3)
4.	Efron & Hastie describe a shift in statistical practice as computation became cheap. What was that shift, and what did it make possible that was not possible before? (Goal 0.4)
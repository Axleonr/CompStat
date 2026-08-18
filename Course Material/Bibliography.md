# Computational Statistics — Bibliography
 
*Internal version 1.4.*
 
## I. Disciplinary Orientation
 
**Tukey, J. W.** (1962). The future of data analysis. *Annals of Mathematical Statistics*, 33(1), 1–67.
*Role: Required reading, Module 0. Sets the disciplinary framing for the entire program.*
 
**Efron, B., & Hastie, T.** (2016). *Computer Age Statistical Inference: Algorithms, Evidence, and Data Science*. Cambridge University Press.
*Role: Primary text across multiple modules (0, 2, 10). The program's broadest conceptual anchor. Module 0 draws on Ch 1 (Algorithms and Inference) as the primary reading; Ch 2 (Frequentist Inference) is optional orientation context. Module 10 draws on the Epilogue as the primary disciplinary retrospective — a short timeline from 1900 to 2016 tracing the movement of statistical progress between Applications, Mathematics, and Computation, and discussing the rise of data science. Note: the previous program reference assigned "Chs 16–18" for synthesis; this was incorrect. Ch 16 is Sparse Modeling and the Lasso; Ch 18 is Neural Networks and Deep Learning — neither is a retrospective. The Epilogue is the correct synthesis reading for Goal 6.*
 
**Gelman, A., & Vehtari, A.** (2021). What are the most important statistical ideas of the past 50 years? *Journal of the American Statistical Association*, 116(536), 2087–2097.
*Role: Synthesis reading, Module 10. Directly supports Goal 6 — read as a disciplinary retrospective that situates the program's methods within the broader arc of modern statistical practice, and closes the frame opened by Tukey (1962) in Module 0. Pair with Efron & Hastie Epilogue.*
 
**Donoho, D.** (2017). 50 years of data science. *Journal of Computational and Graphical Statistics*, 26(4), 745–766. https://doi.org/10.1080/10618600.2017.1384734
*Role: Optional retrospective reading, Module 10. Opens explicitly with Tukey (1962) and examines what happened to his call for a reformation of academic statistics over the subsequent 50 years — situating computational statistics within the data science debate. A second perspective alongside Gelman & Vehtari (2021) for Goal 6; freely available online.*
 
---
 
## II. Random Number Generation & Simulation
 
**Owen, A. B.** (2013). *Monte Carlo Theory, Methods and Examples*. Self-published (freely available online).
*Role: Primary text, Modules 1–2. Covers pseudorandom generation, Monte Carlo integration, and variance reduction. Module 1 draws on Ch 3 (Uniform random numbers) and Ch 4 (Non-uniform random numbers). Module 2 draws on Ch 8 (Variance reduction, including antithetic variates, control variates, and stratification) and Ch 9 (Importance sampling); Ch 10 is "Advanced variance reduction" and is optional depth. Note: Ch 5 is "Random vectors and objects" — it is not assigned.*
 
**L'Ecuyer, P.** (1998). Random number generation. In J. Banks (Ed.), *Handbook of Simulation*. Wiley.
*Role: Required companion, Module 1. Accessible treatment of uniform pseudorandom generation mechanics.*
 
**L'Ecuyer, P.** (1999). Good parameters and implementations for combined multiple recursive random number generators. *Operations Research*, 47(1), 159–164.
*Role: Secondary depth, Module 1. For students seeking technical detail on generator construction.*
 
**Devroye, L.** (1986). *Non-Uniform Random Variate Generation*. Springer. (Freely available online.)
*Role: Secondary, Module 1. Ch II (General Principles): Sec 2.1–2.3 (inversion method) and Sec 3.1–3.3 (rejection method).*
 
**Asmussen, S., & Glynn, P. W.** (2007). *Stochastic Simulation: Algorithms and Analysis*. Springer.
*Role: Secondary reference, Module 2. Provides deeper theoretical grounding in simulation methods.*
 
**Nelson, B. L.** (2013). *Foundations and Methods of Stochastic Simulation*. Springer.
*Role: Secondary reference, Module 2. Applied complement to Owen; accessible treatment of simulation foundations.*
 
---
 
## III. Monte Carlo Estimation & Variance Reduction
 
*Module 2 has a two-stage structure. Robert & Casella Ch 3 is the error theory foundation and should be read first; Owen Chs 8–9 (variance reduction and importance sampling) follow. Owen is not the primary anchor for Module 2 error theory — R&C Ch 3 is.*
 
**Robert, C. P., & Casella, G.** (2004). *Monte Carlo Statistical Methods* (2nd ed.). Springer.
*Role: Primary, Module 2 (error theory foundation, Ch 3 read first); Primary, Module 7 (Chs 7, 9–10); Ch 6 is secondary depth for Module 8. Ch 3 provides the CLT-based estimator framework, variance as the controlling quantity, and confidence interval construction for Monte Carlo estimates — the conceptual architecture that Owen's variance reduction chapters presuppose. Also covers Rao-Blackwellization as a variance reduction strategy (later in Ch 3, read after Owen Chs 8–9). Ch 6 (Markov chains — stationarity, irreducibility, ergodicity, convergence) is secondary depth for Module 8: provides the ergodic theorem framing that connects chain convergence to the validity of MCMC time averages, complementing LPW Ch 12 Sec 12.7. Note: SIR does not appear as a standalone chapter in R&C; the primary SIR source for Module 7 is Givens & Hoeting Ch 6 Sec 6.3.1.*

**Robert, C. P., & Casella, G.** (2010). *Introducing Monte Carlo Methods with R*. Springer.
*Role: Problem-provenance only, not assigned reading (Modules 2, 7, 8). A distinct, separate volume from the 2004 *Monte Carlo Statistical Methods* entry immediately above — the R-implementation companion text, not an edition or revision of it. Several harvest-index files supporting Modules 2, 7, and 8 draw on this volume's exercises and worked examples as problem-provenance sources for original tier-3 drafting; it carries no student-facing reading assignment and is not to be conflated with the 2004 entry.*
 
**Glasserman, P.** (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
*Role: Optional companion, Module 2 (Stage 1 — error theory). Sec 1.1.1–1.1.3 and Appendix A cover the same error foundations as R&C Ch 3 Secs 3.1–3.2 with a more applied, example-driven presentation. Recommended as an entry point for students who find R&C's register demanding; read before R&C, then return to R&C for the formal development. Note: examples carry a financial engineering framing — the error theory is domain-agnostic.*

**Vehtari, A., Gelman, A., Simpson, D., Carpenter, B., & Bürkner, P.-C.** (2021). Rank-normalization, folding, and localization: An improved R̂ for assessing convergence of MCMC. *Bayesian Analysis*, 16(2), 667–718.
*Role: Problem-provenance, Module 8, optional depth only (PS8.3). Supports PS8.3's classic-vs-rank-normalized R-hat contrast (the published N(0,1)-vs-t₃ example: classic R̂ ≈ 1, rank-normalized R̂ = 1.39 against the 1.01 threshold). **Distinct from Gelman & Vehtari (2021)**, "What are the most important statistical ideas of the past 50 years?" (*JASA* 116(536), Section I above) — a different paper, with an overlapping but not identical author list, assigned as the Module 10 disciplinary retrospective. Do not conflate the two: this entry is the MCMC convergence-diagnostic methods paper; the Section I entry is the historical/retrospective essay.*
 
---
 
## IV. Bootstrap & Resampling
 
**Efron, B.** (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics*, 7(1), 1–26.
*Role: Required short reading, Module 3. Original paper introducing the bootstrap; read for the founding argument — what the empirical distribution is, why sampling from it simulates the sampling process, and what that substitution assumes. Analogous in function to Tukey (1962) for Module 0 and DLR (1977) for Module 4.*
*Access: Freely available via Project Euclid / the Annals of Statistics open archive: https://projecteuclid.org/journals/annals-of-statistics/volume-7/issue-1/Bootstrap-Methods-Another-Look-at-the-Jackknife/10.1214/aos/1176344552.full*
 
**Efron, B., & Tibshirani, R. J.** (1993). *An Introduction to the Bootstrap*. Chapman and Hall/CRC.
*Role: Primary text, Module 3. Chs 1–2 and 4 cover the bootstrap idea (introduction, accuracy of a sample mean, empirical distribution function, and the plug-in principle). Ch 3 (random samples and probabilities) is background probability review — optional for students who need the notation; not required for any Goal. Ch 6 covers the bootstrap estimate of standard error and the parametric bootstrap. Ch 8 (More complicated data structures) covers one-sample and two-sample bootstrap extensions, more general data structures (Sec 8.4), and the moving blocks bootstrap (Sec 8.6) — required for Goal 5. Ch 10 (Estimates of bias) covers bootstrap and jackknife bias estimation; optional secondary depth for students who want the bias-estimation foundation before reading Ch 11. Ch 11 covers the jackknife — its definition, relationship to the bootstrap, and failure conditions. Chs 12–13 cover bootstrap-t and percentile confidence intervals, establishing the accuracy hierarchy that Ch 14 builds on. Ch 14, Secs 14.1–14.3 cover the BCa method — required for Goal 2; Sec 14.4 (ABC method) is secondary depth; Sec 14.5 (tooth data example) is optional depth, flagged by the authors as skippable on first reading.*
 
**Davison, A. C., & Hinkley, D. V.** (1997). *Bootstrap Methods and Their Application*. Cambridge University Press.
*Role: Secondary, Module 3. Sec 2.6.1 (consistency and asymptotic accuracy) is the primary source for the theoretical conditions under which bootstrap confidence intervals are valid — Goal 3. Sec 2.6.2 (rough statistics) and Sec 2.6.4 (when might the bootstrap fail?) are the failure-mode content for Goal 4. Sec 2.6.3 (conditional properties) is outside the module's scope. The failure modes material is not supplemental — understanding when a method breaks is part of knowing the method. Remediation for the dependence failure mode (moving blocks bootstrap) is covered in Efron & Tibshirani Ch 8, Sec 8.6. Sec 3.8 (Hierarchical Data) is assigned as secondary reading for the clustered-data component of Goal 4 — it identifies why within-cluster correlation violates the resampling assumption behind the ordinary nonparametric bootstrap. This section's remediation content (cluster-aware resampling schemes) is not assigned; Goal 5's implementation requirement remains scoped to the moving blocks bootstrap only.*
 
---
 
## V. Optimization
 
**Lange, K.** (2010). *Numerical Analysis for Statisticians* (2nd ed.). Springer.
*Role: Primary text, Module 4. Chs 11 and 14 cover the gradient methods material: Ch 11 (Optimization Theory) provides the unconstrained optimization foundation (Secs 11.1–11.2); Ch 14 (Newton's Method and Scoring) covers Newton's method, ad hoc Hessian approximations, and quasi-Newton methods (Secs 14.1–14.4 and 14.9). Ch 13 (The EM Algorithm) covers derivation, ascent property, and the missing data framework (Secs 13.1–13.4). Note: metaheuristic methods (simulated annealing, genetic algorithms) are covered at the orientation level required by Goal 5 in Givens & Hoeting (see General Reference); no dedicated text is assigned for this component.*
 
**Nocedal, J., & Wright, S. J.** (2006). *Numerical Optimization* (2nd ed.). Springer.
*Role: Secondary reference, Module 4. Sec 3.1 (Wolfe conditions and step-length selection); Sec 6.1 (BFGS method and convergence); Sec 7.2 (L-BFGS). Appendix A (conditioning and numerical stability) is optional reference depth.*
 
**Dempster, A. P., Laird, N. M., & Rubin, D. B.** (1977). Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society: Series B*, 39(1), 1–22.
*Role: Required reading, Module 4 (EM). Original paper; read for the founding argument — missing data framing, E and M step construction, and the monotone likelihood claim.*
 
**Wu, C. F. J.** (1983). On the convergence properties of the EM algorithm. *Annals of Statistics*, 11(1), 95–103.
*Role: Secondary, Module 4 (EM). Provides the rigorous convergence proof that extended and corrected Dempster et al. (1977). Goal 4 requires students to articulate what Wu establishes over the original paper.*
 
---
 
## VI. Bayesian Modeling, Computation & Model Checking
 
**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B.** (2013). *Bayesian Data Analysis* (3rd ed.). Chapman and Hall/CRC.
*Role: Primary text, Modules 5, 7, 8, and 10. Module 5 draws on Chs 1–3 and Ch 5 — probability and inference, single-parameter models, multiparameter models (structural patterns, read selectively), and hierarchical models; Ch 11 (Basics of Markov chain simulation) is intentionally deferred to Module 7. Module 7 draws on Ch 10, Sec 10.4 (importance sampling) as background context for SIR, and Ch 11 (Gibbs sampler, Metropolis-Hastings, convergence) as the primary applied simulation reference; the primary SIR source is Givens & Hoeting Ch 6 Sec 6.3.1. Module 8 draws on Ch 11 (MCMC in practice and convergence diagnostics) as continued primary reading. Module 10 revisits Ch 6 (model checking and posterior predictive checks) — directly supports Goal 4 (demonstrating a posterior predictive check as a model criticism tool). Covers Bayesian modeling framework, MCMC in practice, and model checking.*
 
**Gamerman, D., & Lopes, H. F.** (2006). *Markov Chain Monte Carlo: Stochastic Simulation for Bayesian Inference* (2nd ed.). Chapman and Hall/CRC.
*Role: Secondary, Module 8. Provides an alternative treatment of MCMC from a Bayesian computation perspective.*
 
---
 
## VII. Markov Chains
 
**Levin, D. A., Peres, Y., & Wilmer, E. L.** (2009). *Markov Chains and Mixing Times*. American Mathematical Society. (2nd ed. freely available online.)
*Role: Primary, Module 6. Ch 1 is the core theory foundation: Secs 1.1 (Markov chains), 1.3 (irreducibility and aperiodicity), 1.5 (stationary distributions), and 1.6 (reversibility and time reversals — detailed balance). Ch 3 (Metropolis and Glauber chains) provides a concrete entry point — observe a chain on a simple target before formalizing the theory. Ch 4 (Introduction to Markov Chain Mixing) covers total variation distance, the convergence theorem, and mixing time. Ch 12 (Eigenvalues) covers the spectral representation, relaxation time, and spectral gap. Note: Ch 12, Sec 12.7 (Time Averages) is the LPW treatment closest to the ergodic theorem; see Module 8 for how this connects to ESS and the validity of MCMC estimates.*
 
---
 
## VIII. MCMC: Diagnostics & Supporting References
 
*Module 8 draws on BDA Ch 11 (Secs 11.4–11.5, continued primary reading) and R&C Ch 6 (secondary depth). Primary MCMC methods coverage for Module 7 is provided by Robert & Casella (Chs 7, 9–10) and Gelman et al. (Chs 10–11); see Sections III and VI. The SIR conceptual entry point for Module 7 is Givens & Hoeting Ch 6 Sec 6.3.1; see Section X.*
 
**Geyer, C. J.** (1992). Practical Markov chain Monte Carlo. *Statistical Science*, 7(4), 473–483.
*Role: Primary, Module 8. Foundational treatment of ESS, autocorrelation, and the ergodic theorem for MCMC — directly supports Goals 1–2 (ESS as central measure of output quality, autocorrelation interpretation) and Goal 6 (iterative workflow).*
 
**Flegal, J. M., Haran, M., & Jones, G. L.** (2008). Markov chain Monte Carlo: Can we trust the third significant figure? *Statistical Science*, 23(2), 250–260.
*Role: Secondary, Module 8. Monte Carlo standard errors and ESS for dependent samples.*
 
**Cowles, M. K., & Carlin, B. P.** (1996). Markov chain Monte Carlo convergence diagnostics: A comparative review. *Journal of the American Statistical Association*, 91(434), 883–904.
*Role: Secondary, Module 8. Survey of convergence diagnostics; read critically, not as a recipe.*
 
**Link, W. A., & Eaton, M. J.** (2012). On thinning of chains in MCMC. *Methods in Ecology and Evolution*, 3(1), 112–115.
*Role: Secondary, Module 8. Establishes that thinning is inefficient relative to keeping all samples.*
 
**Roberts, G. O., & Rosenthal, J. S.** (2001). Optimal scaling for various Metropolis-Hastings algorithms. *Statistical Science*, 16(4), 351–367.
*Role: Reference depth, Module 7. Proposal scaling and acceptance rate targets — directly supports Goal 3 (characterizing how proposal distribution choice governs the tradeoff between acceptance rate and autocorrelation).*
 
**VanDerwerken, D.** (2017). Not every Gibbs sampler is a special case of the Metropolis-Hastings algorithm. *Communications in Statistics — Theory and Methods*, 46(20), 10005–10009.
*Role: Reference, Module 7. Establishes that the deterministic-scan Gibbs sampler does not satisfy detailed balance in general — directly supports Goal 5 (distinguishing random-scan from deterministic-scan Gibbs and understanding why the latter requires its own treatment).*
 
---
 
## IX. Density Estimation
 
**Silverman, B. W.** (1986). *Density Estimation for Statistics and Data Analysis*. Chapman and Hall/CRC.
*Role: Primary text, Module 9. Ch 2 covers histograms and naive estimators — context for Goal 1 (articulating the density estimation problem). Ch 3 (The kernel method for univariate data) covers the kernel estimator, the full bias-variance analysis (Secs 3.2–3.3: MISE, optimal bandwidth derivation), and bandwidth selection in full (Sec 3.4: subjective choice, rule-of-thumb, least-squares cross-validation, likelihood cross-validation) — covers Goals 2–3. Ch 4 (The kernel method for multivariate data) is outside this module's scope. Ch 5, Sec 5.2 (nearest-neighbour estimator) is assigned as the primary source for Goal 5 — includes the formal bias-variance analysis (Eqs. 5.4–5.5) and the explicit comparison with the kernel method; Sec 5.3 (adaptive kernel estimates) is optional depth; Sec 5.4 (maximum penalized likelihood) is outside this module's scope. Concise and well-scoped for this module's goals; the standard reference for KDE at this level.*
*Access: Requires library access. Students without access can use Wasserman's* All of Nonparametric Statistics *(Springer, 2006), Ch 6, as a freely accessible alternative covering the core KDE material at comparable depth; available via Springer Link at most institutions.*
 
---
 
## X. General Reference
 
**Givens, G. H., & Hoeting, J. A.** (2013). *Computational Statistics* (2nd ed.). Wiley.
*Role: General reference across the program; targeted primary source for specific topics. Ch 3 (Combinatorial Optimization) covers simulated annealing (Sec 3.3) and genetic algorithms (Sec 3.4) at the orientation depth required by Module 4, Goal 5. Ch 6, Sec 6.3.1 (Sampling Importance Resampling Algorithm) is the primary source for SIR in Module 7 — a dedicated treatment with proof, worked examples, and practical guidance on envelope choice and failure modes. Ch 6, Sec 6.4.4 (Rao–Blackwellization) is secondary depth for Module 9, Goal 4 — complements the R&C Ch 3 treatment of Rao-Blackwellization as a variance reduction strategy by applying it specifically to density estimation in MCMC settings. Ch 10 (Nonparametric Density Estimation) provides secondary coverage for Module 9; Sec 10.4.3.1 (Nearest Neighbor Approaches) is the primary source for Goal 5 (nearest-neighbor density estimation and its bias-variance contrast with KDE). Ch 7 (MCMC) provides broad secondary coverage for Modules 7–8.*
 
**Stan Development Team.** *Stan Reference Manual.* https://mc-stan.org/docs/reference-manual
*Role: Reference, Module 8. Authoritative source on ESS, R-hat, and warm-up in practice — directly supports Goals 3 (trace plots, R-hat, ESS as diagnostics) and Goal 4 (warm-up).*
 
**Petersen, K. B., & Pedersen, M. S.** (2012). *The Matrix Cookbook*. Technical University of Denmark. (Freely available online.)
*Role: Lookup reference. Matrix identities as needed throughout the program.*
 
---

## XI. Provenance & Access Notes

*Access/license/URL metadata for sources already cited (or independently needing citation) elsewhere in this bibliography — not full citations. See Sections III–X above for the corresponding role assignments.*

**Vehtari — Aalto BDA course (CS-E5710) assignment templates.** \
Notebooks at `avehtari.github.io/BDA_course_Aalto/assignments/template{1,2,3,4,5}.html`, plus the companion quiz page `avehtari.github.io/BDA_course_Aalto/assignments/assignment5.html`. CC-BY-NC 4.0. One-time confirmation of fit (per `Tier1_SourceSurvey_1_0.md` §2.3's caveat, cited here as fact-basis, not re-edited): the license terms are compatible with this program's use — adaptation and target values only, no republication of complete author solutions or of the `markmyassignment`/`aaltobda` tooling itself.

**McElreath — *Statistical Rethinking* course-repo license note.** \
Course materials (`rmcelreath/stat_rethinking_2023` and related repos) are offered publicly for reuse. Verified source URLs: reedfrogs prompt `github.com/rmcelreath/stat_rethinking_2023/blob/main/homework/week06.pdf`; reedfrogs author solutions `.../week06_solutions.pdf`; Monks prompt `.../homework/week08.pdf`; Monks author solutions `.../week08_solutions.pdf`; Monks dataset (raw CSV) `github.com/rmcelreath/stat_rethinking_2022/blob/main/homework/week08_Monks.csv` (also `data(Monks)` in the `rethinking` package). Per project policy: adaptation and target values only, no republication of complete author solutions.

**Gelman et al. — BDA3 official partial solutions PDF.** \
`sites.stat.columbia.edu/gelman/book/solutions3.pdf` (24 June 2019 build), recorded as a primary, directly-inspected source — Ch 5's solution *content* (not merely the statements) was verified against this document — rather than a secondary or TOC-level index.

*Cross-reference: Robert & Casella, Introducing Monte Carlo Methods with R (2010) — problem-provenance role; see Section III.*
 









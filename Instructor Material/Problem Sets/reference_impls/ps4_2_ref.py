"""
PS4.2 reference implementation.
Model: two-component Gaussian mixture, known weight w=0.25, known common sigma=1,
       unknown (mu1, mu2). n=20 (chosen so the raw likelihood is a representable,
       nonzero double -- see Notes in the validation log for why n=400 will not work
       for the '1/like' encoding).
Part A: Newton-Raphson from scratch (finite-difference gradient/Hessian) on two
        objective encodings: g1 = -log L(theta) and g2 = 1/L(theta). Compare
        iterate paths and confirm limit-point agreement.
Part B: BFGS via its own update formula (inverse-Hessian form, backtracking line
        search), confirm it reaches the same optimum.
Part C: Step-size/stability failure -- an oversized Newton step (fixed multiplier
        alpha applied to the raw Newton step) causes the iterate sequence to fail
        to converge to the true optimum within a fixed iteration budget.
Run with: python3 ps4_2_ref.py
"""
import numpy as np

w, sigma = 0.25, 1.0


def gen_mixture_data(seed, n, w, mu1_true, mu2_true, sigma):
    rng = np.random.default_rng(seed)
    n1 = int(round(w * n))
    n2 = n - n1
    x1 = rng.normal(mu1_true, sigma, n1)
    x2 = rng.normal(mu2_true, sigma, n2)
    return np.concatenate([x1, x2]), n1, n2


x, n1, n2 = gen_mixture_data(seed=5, n=20, w=w, mu1_true=0.0, mu2_true=4.0, sigma=sigma)


def per_point_densities(theta, x):
    mu1, mu2 = theta
    phi1 = np.exp(-0.5 * ((x - mu1) / sigma) ** 2) / np.sqrt(2 * np.pi * sigma ** 2)
    phi2 = np.exp(-0.5 * ((x - mu2) / sigma) ** 2) / np.sqrt(2 * np.pi * sigma ** 2)
    return w * phi1 + (1 - w) * phi2


def g_negloglik(theta):
    f = per_point_densities(theta, x)
    return -np.sum(np.log(f + 1e-300))


def g_reciprocal(theta):
    f = per_point_densities(theta, x)
    L = np.prod(f)
    return 1.0 / L if L > 0 else np.inf


def finite_diff_grad(g, theta, h=1e-5):
    grad = np.zeros(2)
    for i in range(2):
        tp = theta.copy(); tp[i] += h
        tm = theta.copy(); tm[i] -= h
        grad[i] = (g(tp) - g(tm)) / (2 * h)
    return grad


def finite_diff_hess(g, theta, h=1e-4):
    H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            tpp = theta.copy(); tpp[i] += h; tpp[j] += h
            tpm = theta.copy(); tpm[i] += h; tpm[j] -= h
            tmp = theta.copy(); tmp[i] -= h; tmp[j] += h
            tmm = theta.copy(); tmm[i] -= h; tmm[j] -= h
            H[i, j] = (g(tpp) - g(tpm) - g(tmp) + g(tmm)) / (4 * h * h)
    return H


def newton(g, theta0, alpha=1.0, max_iter=50, tol=1e-8, verbose=True):
    theta = np.array(theta0, dtype=float)
    path = [theta.copy()]
    for it in range(max_iter):
        grad = finite_diff_grad(g, theta)
        H = finite_diff_hess(g, theta)
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            if verbose:
                print(f"  iter {it}: Hessian singular -- STOP")
            return theta, path, "singular_hessian"
        theta_new = theta - alpha * step
        if not np.all(np.isfinite(theta_new)) or np.linalg.norm(theta_new) > 1e5:
            if verbose:
                print(f"  iter {it}: blew up -- STOP")
            return theta, path, "blew_up"
        if verbose:
            print(f"  iter {it}: theta={np.round(theta,4)}, |grad|={np.linalg.norm(grad):.4e}, "
                  f"|step|={np.linalg.norm(step):.4e}")
        path.append(theta_new.copy())
        if np.linalg.norm(theta_new - theta) < tol:
            theta = theta_new
            return theta, path, "converged"
        theta = theta_new
    return theta, path, "max_iter_reached"


print("=== Part A: Newton-Raphson under two objective encodings ===")
theta0 = [1.0, 3.0]

print("--- Encoding 1: g1 = -log L(theta) ---")
theta1, path1, status1 = newton(g_negloglik, theta0, alpha=1.0)
print(f"Converged theta (encoding 1): {theta1}, n_iters={len(path1)-1}, status={status1}")

print()
print("--- Encoding 2: g2 = 1/L(theta) ---")
theta2, path2, status2 = newton(g_reciprocal, theta0, alpha=1.0)
print(f"Converged theta (encoding 2): {theta2}, n_iters={len(path2)-1}, status={status2}")

print()
print("Agreement between encodings (||theta1 - theta2||):", np.linalg.norm(theta1 - theta2))

# grid-search cross-check (same technique as PS4.1)
mu_grid = np.linspace(-4, 8, 241)
best = None
for m1 in mu_grid:
    for m2 in mu_grid:
        val = -g_negloglik((m1, m2))
        if best is None or val > best[2]:
            best = (m1, m2, val)
print("Grid-search cross-check (PS4.1-style) global max:", best)
print("Newton final vs grid-search optimum, ||diff|| =", np.linalg.norm(np.array(theta1) - np.array(best[:2])))

print()
print("=== Part B: BFGS via its own update formula ===")


def bfgs(g, theta0, max_iter=50, tol=1e-8, verbose=True):
    theta = np.array(theta0, dtype=float)
    n_ = len(theta)
    Hinv = np.eye(n_)
    grad = finite_diff_grad(g, theta)
    path = [theta.copy()]
    for it in range(max_iter):
        p = -Hinv @ grad
        alpha_ls = 1.0
        g0 = g(theta)
        while g(theta + alpha_ls * p) > g0 + 1e-4 * alpha_ls * np.dot(grad, p) and alpha_ls > 1e-10:
            alpha_ls *= 0.5
        s = alpha_ls * p
        theta_new = theta + s
        grad_new = finite_diff_grad(g, theta_new)
        yv = grad_new - grad
        sy = np.dot(s, yv)
        if sy > 1e-12:
            rho = 1.0 / sy
            I = np.eye(n_)
            Hinv = (I - rho * np.outer(s, yv)) @ Hinv @ (I - rho * np.outer(yv, s)) + rho * np.outer(s, s)
        path.append(theta_new.copy())
        if verbose:
            print(f"  iter {it}: theta={np.round(theta,4)}, step_len={alpha_ls:.4g}, "
                  f"g={g0:.6f}, |grad|={np.linalg.norm(grad):.4e}")
        if np.linalg.norm(theta_new - theta) < tol:
            theta = theta_new
            break
        theta, grad = theta_new, grad_new
    return theta, path


theta_bfgs, path_bfgs = bfgs(g_negloglik, theta0)
print(f"BFGS converged theta: {theta_bfgs}, n_iters={len(path_bfgs)-1}")
print("BFGS vs Newton (encoding 1) agreement:", np.linalg.norm(theta_bfgs - theta1))

print()
print("=== Part C: step-size/stability failure (oversized Newton step) ===")
for alpha in [1.0, 1.9]:
    print(f"--- alpha (step multiplier) = {alpha} ---")
    theta_a, path_a, status_a = newton(g_negloglik, theta0, alpha=alpha, max_iter=30, verbose=False)
    final_g = g_negloglik(theta_a) if np.all(np.isfinite(theta_a)) else float('nan')
    print(f"  final theta after 30 iters: {theta_a}, g={final_g:.4f}, status={status_a}")
    print(f"  distance from true optimum {np.round(theta1,4)}: {np.linalg.norm(theta_a - theta1):.4f}")

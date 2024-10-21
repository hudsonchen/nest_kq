from utils.kernels import *
import jax
import jax.numpy as jnp


def KQ_RBF_Gaussian(X, f_X, mu_X_theta, var_X_theta):
    """
    KQ, not Vectorized.

    \int f(x, theta) N(x|mu_X_theta, var_X_theta) dx

    Args:
        rng_key: random number generator
        X: shape (N, D)
        f_X: shape (N, )
        var_X_theta: (D, D)
        mu_X_theta: (D, )
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    # l = 1.0
    l = jnp.median(jnp.abs(X - X.mean(0)))  # Median heuristic
    A = 1.0

    K = A * my_RBF(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_RBF_Gaussian(mu_X_theta, var_X_theta, l, X)
    # varphi = A * kme_double_RBF_Gaussian(mu_X_theta, var_X_theta, l)

    I_NKQ = phi.T @ K_inv @ f_X
    # I_NKQ_std = jnp.sqrt(jnp.abs(varphi - phi.T @ K_inv @ phi))
    pause = True
    return I_NKQ


def KQ_RBF_Gaussian_Vectorized(X, f_X, mu_X_theta, var_X_theta):
    """
    KQ, Vectorized over the first indice of X, f_X, mu_X_theta and var_X_theta.

    Args:
        rng_key: random number generator
        X: shape (T, N, D)
        f_X: shape (T, N)
        mu_X_theta: (T, D)
        var_X_theta: (T, D, D)
    Returns:
        I_NKQ: (T, )
        I_NKQ_std: (T, )
    """
    vmap_func = jax.vmap(KQ_RBF_Gaussian, in_axes=(None, 0, 0, 0, 0))
    return vmap_func(X, f_X, mu_X_theta, var_X_theta)


def KQ_RBF_Uniform(X, f_X, a, b):
    """
    KQ, not Vectorized.

    \int f(x, theta) U(x|a,b) dx

    Args:
        rng_key: random number generator
        X: shape (N, D)
        f_X: shape (N, )
        a: float
        b: float
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    A = 1.
    l = jnp.median(jnp.abs(X - X.mean(0)))  # Median heuristic
    # l = 1.

    K = A * my_RBF(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_RBF_uniform(a, b, l, X)
    # varphi = A

    I_NKQ = phi.T @ K_inv @ f_X
    # I_NKQ_std = jnp.sqrt(jnp.abs(varphi - phi.T @ K_inv @ phi))
    pause = True
    return I_NKQ.squeeze()


def KQ_RBF_Uniform_Vectorized(X, f_X, a, b):
    """
    KQ, Vectorized over the first indice of X and f_X.
    a and b are scalars

    Args:
        rng_key: random number generator
        X: shape (T, N, D)
        f_X: shape (T, N)
        a: float
        b: float
    Returns:
        I_NKQ: (T, )
        I_NKQ_std: (T, )
    """
    vmap_func = jax.vmap(KQ_RBF_Uniform, in_axes=(0, 0, None, None))
    return vmap_func(X, f_X, a, b)


def KQ_Matern_32_Gaussian(X, f_X):
    """
    KQ, not Vectorized over theta.
    Only works for one-d and for standard normal distribution

    \int f(x) N(x|0,1) dx

    Args:
        rng_key: random number generator
        X: shape (N, D)
        f_X: shape (N, )
        a: float
        b: float
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    A = 1.
    l = jnp.median(jnp.abs(X - X.mean(0)))  # Median heuristic
    # l = 1.

    K = A * my_Matern_32(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_Matern_32_Gaussian(l, X)
    # varphi = A

    I_NKQ = phi.T @ K_inv @ f_X
    pause = True
    return I_NKQ.squeeze()


def KQ_Matern_32_Gaussian_Vectorized(X, f_X):
    """
    KQ, Vectorized over the first indice of X and f_X.
    Only works for one-d and for standard normal distribution
    Actually, every integral can be written as integration wrt to a standard normal distribution
    Args:
        rng_key: random number generator
        X: shape (T, N, D)
        f_X: shape (T, N)
    Returns:
        I_NKQ: (T, )
        I_NKQ_std: (T, )
    """
    vmap_func = jax.vmap(KQ_Matern_32_Gaussian, in_axes=(None, 0, 0))
    return vmap_func(X, f_X)


def KQ_Matern_12_Gaussian(X, f_X):
    """
    KQ, not Vectorized over theta.
    Only works for one-d and for standard normal distribution

    \int f(x) N(x|0,1) dx

    Args:
        rng_key: random number generator
        X: shape (N, D)
        f_X: shape (N, )
        a: float
        b: float
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    A = 1.
    # l = jnp.median(jnp.abs(X - X.mean(0)))  # Median heuristic
    l = 1. * jnp.ones(D)

    K = A * my_Matern_12_product(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_Matern_12_Gaussian(l, X)
    # varphi = A

    I_NKQ = phi.T @ K_inv @ f_X
    pause = True
    return I_NKQ.squeeze()


def KQ_Matern_12_Gaussian_Vectorized(X, f_X):
    """
    KQ, Vectorized over the first indice of X and f_X.
    Only works for one-d and for standard normal distribution
    Actually, every integral can be written as integration wrt to a standard normal distribution
    Args:
        rng_key: random number generator
        X: shape (T, N, D)
        f_X: shape (T, N)
    Returns:
        I_NKQ: (T, )
        I_NKQ_std: (T, )
    """
    vmap_func = jax.vmap(KQ_Matern_12_Gaussian, in_axes=(0, 0))
    return vmap_func(X, f_X)


def KQ_Matern_32_Uniform(X, f_X, a, b):
    """
    KQ, not Vectorized over theta.
    Only works for product Matern kernel

    \int f(x) U(x| a , b) dx

    Args:
        rng_key: random number generator
        X: shape (N, D)
        f_X: shape (N, )
        a: (D, )
        b: (D,)
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    A = 1.
    # l = jnp.median(jnp.abs(X - X.mean(0)), axis=0)  # Median heuristic
    l = jnp.ones(D) * 3.0
    # l = jnp.median(jnp.abs(X - X.mean(0))) * jnp.ones(D)

    K = A * my_Matern_32_product(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_Matern_32_Uniform(a, b, l, X)

    I_NKQ = phi.T @ K_inv @ f_X
    pause = True
    return I_NKQ.squeeze()



def KQ_Matern_32_Uniform_Vectorized(X, f_X, a, b):
    """
    KQ, Vectorized over the first indice of X and f_X.
    Only works for product Matern kernel

    Args:
        rng_key: random number generator
        X: shape (T, N, D)
        f_X: shape (T, N)
        a: (T, D)
        b: (T, D)
    Returns:
        I_NKQ: (T, )
        I_NKQ_std: (T, )
    """
    vmap_func = jax.vmap(KQ_Matern_32_Uniform, in_axes=(0, 0, 0, 0))
    return vmap_func(X, f_X, a, b)


def KQ_Matern_12_Uniform(X, f_X, a, b):
    """
    KQ, not Vectorized over theta.
    Only works for one-d, D = 1

    \int f(x) U(x| a , b) dx

    Args:
        X: shape (N, D)
        f_X: shape (N, )
        a: float
        b: float
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    A = 1.
    l = jnp.median(jnp.abs(X - X.mean(0)))  # Median heuristic
    # l = 1.

    K = A * my_Matern_12(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_Matern_12_Uniform(a, b, l, X)
    # varphi = A

    I_NKQ = phi.T @ K_inv @ f_X
    pause = True
    return I_NKQ.squeeze()

def KQ_Matern_12_Uniform_Vectorized(X, f_X, a, b):
    """
    KQ, Vectorized over the first indice of X and f_X.
    Only works for one-d D = 1 and for standard normal distribution

    Args:
        rng_key: random number generator
        X: shape (T, N, D)
        f_X: shape (T, N)
        a: float
        b: float
    Returns:
        I_NKQ: (T, )
        I_NKQ_std: (T, )
    """
    vmap_func = jax.vmap(KQ_Matern_12_Uniform, in_axes=(0, 0, None, None))
    return vmap_func(X, f_X, a, b)


def KQ_log_RBF_log_Gaussian(X, f_X, mu, std):
    """
    KQ, not Vectorized. Only works for one-d, D = 1

    \int f(x, theta) log N(x|mu_X_theta, var_X_theta) dx

    Args:
        rng_key: random number generator
        X: shape (N, 1)
        f_X: shape (N, )
        mu: float
        std: float
    Returns:
        I_NKQ: float
    """
    N, D = X.shape[0], X.shape[1]
    eps = 1e-6

    # l = 0.1
    l = 0.1
    # l = jnp.median(jnp.abs(jnp.log(X) - jnp.log(X).mean(0)))  # Median heuristic
    A = 1.0

    K = A * my_log_RBF(X, X, l)
    K_inv = jnp.linalg.inv(K + eps * jnp.eye(N))
    phi = A * kme_log_normal_log_RBF(mu, std, X, l)
    I_NKQ = phi.T @ K_inv @ f_X
    return I_NKQ


def KQ_log_RBF_log_Gaussian_Vectorized(X, f_X, mu, std):
    """
    KQ, not Vectorized. Only works for one-d, D = 1

    \int f(x, theta) log N(x|mu_X_theta, var_X_theta) dx

    Args:
        rng_key: random number generator
        X: shape (T, N, 1)
        f_X: shape (T, N)
        mu: (T,)
        std: (T, )
    Returns:
        I_NKQ: (T, )
    """
    vmap_func = jax.vmap(KQ_log_RBF_log_Gaussian, in_axes=(0, 0, 0, 0))
    return vmap_func(X, f_X, mu, std)
import numpy as np

from ..util import BaseCase, needs_deap

from pygsti.optimize import optimize as opt


class OptimizeTester(BaseCase):
    def setUp(self):
        self.f = lambda x: np.dot(x, x)
        self.x0 = np.array([10, 5], 'd')
        self.answer = np.array([0, 0], 'd')

    def test_minimize_methods(self):
        for method in ("simplex", "supersimplex", "customcg", "basinhopping", "CG", "BFGS", "L-BFGS-B"):  # "homebrew"
            result = opt.minimize(self.f, self.x0, method, maxiter=1000)
            self.assertArraysAlmostEqual(result.x, self.answer)

    def test_minimize_swarm(self):
        result = opt.minimize(self.f, self.x0, "swarm", maxiter=30)
        self.assertArraysAlmostEqual(result.x, self.answer)

    def test_minimize_brute_force(self):
        result = opt.minimize(self.f, self.x0, "brute", maxiter=10)
        self.assertArraysAlmostEqual(result.x, self.answer)

    @needs_deap
    def test_minimize_evolutionary(self):
        result = opt.minimize(self.f, self.x0, "evolve", maxiter=20)
        self.assertLess(np.linalg.norm(result.x - self.answer), 0.1)

    def test_checkjac(self):
        def f_vec(x):
            return np.array([np.dot(x, x)])

        def jac(x):
            return 2 * x[None, :]

        x0 = self.x0
        opt.check_jac(f_vec, x0, jac(x0), eps=1e-10, tol=1e-6, errType='rel')
        opt.check_jac(f_vec, x0, jac(x0), eps=1e-10, tol=1e-6, errType='abs')
        # TODO assert correctness

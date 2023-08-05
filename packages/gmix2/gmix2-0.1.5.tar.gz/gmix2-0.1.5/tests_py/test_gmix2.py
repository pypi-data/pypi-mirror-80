# Python modules
import unittest

# 3rd Party Modules
import numpy as np

# Project modules
from src.gmix2 import gmix2

np.set_printoptions(precision=12)


class TestGmix2(unittest.TestCase):
    rng = np.random.RandomState(31)

    w = np.array([
        [0.15, 0.10, 0.40, 0.05, 0.3],
        [0.05, 0.20, 0.10, 0.35, 0.3]
    ])
    m = np.array([
        [ 0.0,  1.0, 2.0, 3.0, 4.0],
        [-5.0, -2.0, 0.0, 1.0, 3.0]
    ])
    s = np.array([
        [0.9, 0.5, 2.0, 1.0, 3.0],
        [0.5, 10.0, 2.0, 5.0, 0.8]
    ])

    def test_pdf(self):
        # One value at a time
        exp_pdf = np.array([0.212963552378, 0.059730094961])
        act_pdf = gmix2.pdf(1, self.w, self.m, self.s)

        np.testing.assert_allclose(act_pdf, exp_pdf)

        exp_pdf = [[0.212963552378, 0.000335617249],
                   [0.059730094961, 0.044152358959]]
        act_pdf = gmix2.pdf(np.array([1, -5.5]), self.w, self.m, self.s)

        np.testing.assert_allclose(act_pdf, exp_pdf)

        act_pdf = gmix2.pdf([1, -5.5], self.w, self.m, self.s)

        np.testing.assert_allclose(act_pdf, exp_pdf)

    def test_cdf(self):
        exp_cdf = [0.000266662424, 0.11474477839]
        act_cdf = gmix2.cdf(-5.5, self.w, self.m, self.s)

        np.testing.assert_allclose(act_cdf, exp_cdf)

        exp_cdf = [[0.352160058832, 0.000266662424],
                   [0.419591430163, 0.11474477839]]
        act_cdf = gmix2.cdf(np.array([1, -5.5]), self.w, self.m, self.s)

        np.testing.assert_allclose(act_cdf, exp_cdf)

        act_cdf = gmix2.cdf([1, -5.5], self.w, self.m, self.s)

        np.testing.assert_allclose(act_cdf, exp_cdf)

    def test_ppf(self):
        exp_ppf = [0.753339733752, -1.185816277994]
        act_ppf = gmix2.ppf(0.3, self.w, self.m, self.s)

        np.testing.assert_allclose(act_ppf, exp_ppf)

        exp_ppf = [[0.753339733752, 5.673110996856],
                   [-1.185816277994, 5.916783093835]]
        act_ppf = gmix2.ppf(np.array([0.3, 0.9]), self.w, self.m, self.s)

        np.testing.assert_allclose(act_ppf, exp_ppf)

        act_ppf = gmix2.ppf([0.3, 0.9], self.w, self.m, self.s)

        np.testing.assert_allclose(act_ppf, exp_ppf)

    def test_mean(self):
        exp_mean = [2.25, 0.6]
        act_mean = gmix2.mean(self.w, self.m)

        np.testing.assert_allclose(act_mean, exp_mean)

    def test_median(self):
        exp_median = [1.79712881, 2.00299055]
        act_median = gmix2.median(self.w, self.m, self.s)

        np.testing.assert_allclose(act_median, exp_median)

    def test_mode(self):
        exp_mode = [[(0.9580152000982137, 0.21324093573952826)],
                    [(-4.970966372242318, 0.06205794913899075),
                     (2.96872434469676, 0.189013117805071)]]
        act_mode = gmix2.mode(self.w, self.m, self.s)

        for act_grp, exp_grp in zip(act_mode, exp_mode):
            for (act_x, act_p), (exp_x, exp_p) in zip(act_grp, exp_grp):
                self.assertAlmostEqual(act_x, exp_x)
                self.assertAlmostEqual(act_p, exp_p)

    def test_variance(self):
        exp_var = [6.384, 34.0945]
        act_var = gmix2.variance(self.w, self.m, self.s)

        np.testing.assert_allclose(act_var, exp_var)

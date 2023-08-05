//
// Created by reid on 8/13/20.
//

#pragma once

// System Includes
#include <cmath>
#include <exception>
#include <limits>
#include <memory>
#include <random>
#include <utility>

// Third Party Includes
#include <Eigen/Core>
#include <unsupported/Eigen/SpecialFunctions>

// Project Includes

// region Constants
const double SQRT_2 = std::sqrt(2.0);
const double SQRT_2_PI = 2.5066282746310005;
// endregion Constants

// region Procedural Interface --------------------------------------------------------------------------------------//
// Utility Methods
namespace {
/**
 * See https://bitbashing.io/comparing-floats.html
 * @param a
 * @param b
 * @return
 */
std::int32_t
ulps_distance(const float a, const float b) {
    // This code is licensed by CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
    // Copyright (c) 2017 Matt Kline

    // We can skip all the following work if they're equal.
    if (a == b) return 0;

    const auto max = std::numeric_limits<int32_t>::max();

    // We first check if the values are NaN.
    // If this is the case, they're inherently unequal;
    // return the maximum distance between the two.
    if (std::isnan(a) || std::isnan(b)) { return max; }

    // If one's infinite, and they're not equal,
    // return the max distance between the two.
    if (std::isinf(a) || std::isinf(b)) { return max; }

    // At this point we know that the floating-point values aren't equal and
    // aren't special values (infinity/NaN).
    // Because of how IEEE754 floats are laid out
    // (sign bit, then exponent, then mantissa), we can examine the bits
    // as if they were integers to get the distance between them in units
    // of least precision (ULPs).
    static_assert(sizeof(float) == sizeof(std::int32_t), "What size is float?");

    // memcpy to get around the strict aliasing rule.
    // The compiler knows what we're doing and will just transfer the float
    // values into integer registers.
    std::int32_t ia, ib;
    memcpy(&ia, &a, sizeof(float));
    memcpy(&ib, &b, sizeof(float));

    // If the signs of the two values aren't the same,
    // return the maximum distance between the two.
    // This is done to avoid integer overflow, and because the bit layout of
    // floats is closer to sign-magnitude than it is to two's complement.
    // This *also* means that if you're checking if a value is close to zero,
    // you should probably just use a fixed epsilon instead of this function.
    if ((ia < 0) != (ib < 0)) { return max; }

    // If we've satisfied all our caveats above, just subtract the values.
    // The result is the distance between the values in ULPs.
    std::int32_t distance = ia - ib;
    if (distance < 0) { distance = -distance; }
    return distance;
}
} // end anonymous namespace

// Some typedefs and aliases
namespace gmix {
template <typename Float>
using Pair = std::tuple<Float, Float>;

template <typename Float>
using PairVector = std::vector<Pair<Float>>;

template <typename Float>
using ModeVector = std::vector<PairVector<Float>>;

template <typename Float>
using Array = Eigen::Array<Float, 1, Eigen::Dynamic, Eigen::RowMajor>;

template <typename Float>
using Matrix = Eigen::Array<Float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

template <typename Float>
using ArrayConstRef = Eigen::Ref<const Array<Float>>;

template <typename Float>
using MatrixConstRef = Eigen::Ref<const Matrix<Float>>;
} // end namespace gmix

// Methods for Normal distributions
namespace normal {
template <typename Float>
using Array = Eigen::Array<Float, 1, Eigen::Dynamic, Eigen::RowMajor>;

template <typename Float>
using Matrix = Eigen::Array<Float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

template <typename Float>
using ArrayConstRef = Eigen::Ref<const Array<Float>>;

template <typename Float>
using MatrixConstRef = Eigen::Ref<const Matrix<Float>>;

/**
 *
 * @tparam Float
 * @param x
 * @param mean
 * @param std
 * @return
 */
template <typename Float>
Matrix<Float>
pdf(Float x, const MatrixConstRef<Float>& mean, const MatrixConstRef<Float>& std) {
    return (1.0 / (std * SQRT_2_PI)) * (-0.5 * ((x - mean) / std).pow(2)).exp();
}

template <typename Float>
Matrix<Float>
cdf(Float x, const MatrixConstRef<Float>& mean, const MatrixConstRef<Float>& std) {
    return 0.5 * (1.0 + ((x - mean) / (SQRT_2 * std)).erf());
}

template <typename Float>
Float
first_derivative(
    const Float x,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std
) {
    return (weight * -(x - mean) * pdf(x, mean, std) / (std * std)).sum();
}

template <typename Float>
Float
second_derivative(
    const Float x,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std
) {
    const auto variance = std * std;
    const auto variance_2 = variance * variance;
    const auto fx = pdf(x, mean, std);
    const auto diff_2 = (x - mean) * (x - mean);

    return (weight * ((-fx / variance) + (diff_2 * fx / variance_2))).sum();
}

} // end namespace normal

// Utility methods
namespace gmix {
/**
 * An implementation of Brent's algorithm based off the description on
 * <a href="https://en.wikipedia.org/wiki/Brent%27s_method">Wikipedia</a>.
 *
 * <em>Using Brent's method, returns the root of a function \p f known to lie between \p lower_bound and \p upper_bound.
 * The root will be refined until its accuracy is \p tol.</em> - <b>Numerical Recipes 3rd Edition</b>.
 *
 * @tparam F
 * @param f
 * @param lower_bound
 * @param upper_bound
 * @param tol
 * @param max_itr
 * @return
 */
template <typename F>
double
brent_root(
    F&& f,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const double eps = std::numeric_limits<double>::epsilon();
    bool mflag, c1, c2, c3, c4, c5;
    double a = lower_bound, b = upper_bound, c, d = 0;
    double fa = f(a), fb = f(b), fc, fs;
    double s;
    double lb = 0, ub = 0;

    if (fa * fb >= 0) {
        throw std::runtime_error("The root is not bracketed.");
    }

    if (std::abs(fa) < std::abs(fb)) {
        std::swap(a, b);
        std::swap(fa, fb);
    }

    c = a;
    fc = fa;
    mflag = true;

    for (int i = 0; i < max_itr; ++i) {
        if (fa != fc && fb != fc) {
            // inverse quadratic interpolation
            s =   (a * fb * fc) / ((fa - fb) * (fa - fc))
                + (b * fa * fc) / ((fb - fa) * (fb - fc))
                + (c * fa * fb) / ((fc - fa) * (fc - fb));
        } else {
            // Secant method
            s = b - fb * (b - a) / (fb - fa);
        }

        lb = (3.0 * a + b) / 4.0;
        ub = b;

        // I'm not sure if this can ever be true, but the description on Wikipedia is ambiguous.
        if (lb > ub) { std::swap(lb, ub); }

        c1 = lb <= s > ub;
        c2 = mflag && std::abs(s - b) >= std::abs(b - c) / 2.0;
        c3 = !mflag && std::abs(s - b) >= std::abs(c - d) / 2.0;
        c4 = mflag && std::abs(b - c) < std::abs(eps);
        c5 = !mflag && std::abs(c - d) < std::abs(eps);

        if (c1 || c2 || c3 || c4 || c5) {
            s = (a + b) / 2.0;
            mflag = true;
        } else {
            mflag = false;
        }

        fs = f(s);
        d = c;
        c = b;
        fc = fb;

        if (fa * fs < 0) {
            b = s;
            fb = fs;
        } else {
            a = s;
            fa = fs;
        }

        if (std::abs(fa) < std::abs(fb)) {
            std::swap(a, b);
            std::swap(fa, fb);
        }

        if (fb == 0 || std::abs(b - a) < tol) {
            return b;
        }
    }
    throw std::runtime_error("Unable to find root within maximum iterations.");
}
} // end namespace gmix

// Methods for Gaussian Mixture Distributions
namespace gmix {
/**
 *
 * @tparam Float
 * @param y
 * @param weight
 * @param mean
 * @param std
 * @return
 */
template <typename Float>
Matrix<Float>
pdf(Float x, const MatrixConstRef<Float>& weight, const MatrixConstRef<Float>& mean, const MatrixConstRef<Float>& std) {
    return (weight * normal::pdf(x, mean, std)).rowwise().sum();
}

/**
 *
 * @tparam Float
 * @tparam Iterable
 * @param points
 * @param weight
 * @param mean
 * @param std
 * @return
 */
template <typename Float>
Matrix<Float>
pdf(const ArrayConstRef<Float>& points, const MatrixConstRef<Float>& weight, const MatrixConstRef<Float>& mean, const MatrixConstRef<Float>& std) {
    Matrix<Float> result(weight.rows(), points.size());

    // There doesn't seem to be an obvious way to vectorize this.
    // However, doing the looping in C++ should be a lot faster than in Python.
    // C++11 range based iterators don't seem to work with my current version
    // of Eigen, so I'm doing it this way instead.
    for (int i = 0; i < points.size(); ++i) {
        result.col(i) = pdf(points(i), weight, mean, std);
    }

    return result;
}

/**
 *
 * @tparam Float
 * @param x
 * @param weight
 * @param mean
 * @param std
 * @return
 */
template <typename Float>
Matrix<Float>
cdf(
    Float x,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std
) {
    return (weight * normal::cdf(x, mean, std)).rowwise().sum();
}

/**
 *
 * @tparam Float
 * @tparam Iterable
 * @param points
 * @param weight
 * @param mean
 * @param std
 * @return
 */
template <typename Float>
Matrix<Float>
cdf(
    const ArrayConstRef<Float>& points,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std
) {
    Matrix<Float> result(weight.rows(), points.size());

    // There doesn't seem to be an obvious way to vectorize this.
    // However, doing the looping in C++ should be a lot faster than in Python.
    // C++11 range based iterators don't seem to work with my current version
    // of Eigen, so I'm doing it this way instead.
    for (int i = 0; i < points.size(); ++i) {
        result.col(i) = cdf(points(i), weight, mean, std);
    }

    return result;
}

/**
 *
 * @tparam Float
 * @param p
 * @param weight
 * @param mean
 * @param std
 * @param lower_bound
 * @param upper_bound
 * @param tol
 * @param max_itr
 * @return
 */
template <typename Float>
Matrix<Float>
ppf(
    Float p,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    // Unfortunately there is no way to vectorize this over the entire matrix.
    // Each row needs to be calculated individually.
    Matrix<Float> result(weight.rows(), 1);

    for (int i = 0; i < weight.rows(); ++i) {
        const Matrix<Float> w = weight.row(i);
        const Matrix<Float> m = mean.row(i);
        const Matrix<Float> s = std.row(i);

        auto f = [&](const Float x) -> Float { return cdf<Float>(x, w, m, s)(0, 0) - p; };
        result(i, 0) = brent_root(f, lower_bound, upper_bound, tol, max_itr);
    }

    return result;
}

template <typename Float>
Matrix<Float>
ppf(
    const ArrayConstRef<Float>& points,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    Matrix<Float> result(weight.rows(), points.size());

    // There doesn't seem to be an obvious way to vectorize this.
    // However, doing the looping in C++ should be a lot faster than in Python.
    // C++11 range based iterators don't seem to work with my current version
    // of Eigen, so I'm doing it this way instead.
    for (int i = 0; i < points.size(); ++i) {
        result.col(i) = ppf(points(i), weight, mean, std, lower_bound, upper_bound, tol, max_itr);
    }

    return result;
}

template <typename Float>
Matrix<Float>
mean(const MatrixConstRef<Float>& weight, const MatrixConstRef<Float>& mean) {
    return (weight * mean).rowwise().sum();
}

template <typename Float>
Matrix<Float>
median(
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    return ppf(0.5, weight, mean, std, lower_bound, upper_bound, tol, max_itr);
}

/**
 *
 * @tparam Float
 * @param weight
 * @param mean
 * @param std
 * @param max_itr
 * @param min_diff
 * @param min_grad
 */
template <typename Float>
ModeVector<Float>
mode(
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std,
    const int max_itr = 1000,
    const double min_diff = 1e-4,
    const double min_grad = 1e-9
) {
    // TODO validate the inputs are compatible
    const auto n_means = mean.cols();

    // The modes have to be found independently for each mixture.
    ModeVector<Float> result;

    for (int i = 0; i < weight.rows(); ++i) {
        const Matrix<Float> w = weight.row(i);
        const Matrix<Float> m = mean.row(i);
        const Matrix<Float> s = std.row(i);

        PairVector<Float> modes;
        for (int mean_idx = 0; mean_idx < n_means; ++mean_idx) {
            Float x_new = m(0, mean_idx);
            Float x_old = 0;

            for (int itr = 0; itr < max_itr; ++itr) {
                const auto g1 = normal::first_derivative<Float>(x_new, w, m, s);
                const auto g2 = normal::second_derivative<Float>(x_new, w, m ,s);

                if (ulps_distance(0, g2) < 4) { break; }

                x_old = x_new;
                x_new = x_old - (g1 / g2);

                if (std::abs(g1) < min_grad) { break; }
            }

            if (normal::second_derivative<Float>(x_new, w, m, s) < 0) {
                // I'm not sure the move is doing anything that the compiler wouldn't
                // already do, but I don't think it can hurt.
                modes.push_back(std::move(std::make_tuple(x_new, pdf<Float>(x_new, w, m, s)(0, 0))));
            }
        }

        // Only keep unique modes (ones that are at least `min_diff` apart).
        std::sort(modes.begin(), modes.end());
        auto uniq_itr = std::unique(
            modes.begin(),
            modes.end(),
            [&](std::tuple<Float, Float> left, std::tuple<Float, Float> right) {
                return std::abs(std::get<0>(left) - std::get<0>(right)) < min_diff;
            }
        );

        modes.resize(std::distance(modes.begin(), uniq_itr));
        result.push_back(std::move(modes));
    }

    return result;
}

template <typename Float>
Matrix<Float>
variance(
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std
) {
    // See: https://stats.stackexchange.com/a/16609
    return
          (weight * std * std).rowwise().sum()
        + (weight * mean * mean).rowwise().sum()
        - (weight * mean).rowwise().sum().pow(2);
}

/**
 *
 * @tparam Float
 * @param n
 * @param weight
 * @param mean
 * @param std
 * @param seed
 * @return
 */
template <typename Float>
Matrix<Float>
random(
    size_t n,
    const MatrixConstRef<Float>& weight,
    const MatrixConstRef<Float>& mean,
    const MatrixConstRef<Float>& std,
    const int seed = -1
) {
    std::mt19937 generator(seed < 0 ? std::mt19937::default_seed : seed);
    std::uniform_real_distribution<Float> rng(0.0, 1.0);
    Matrix<Float> result(std.rows(), n);

    for (size_t i = 0; i < n; ++i) {
        result.col(i) = ppf<Float>(rng(generator), weight, mean, std);
    }

    return result;
}

} // end namespace gmix
// endregion Procedural Interface -----------------------------------------------------------------------------------//

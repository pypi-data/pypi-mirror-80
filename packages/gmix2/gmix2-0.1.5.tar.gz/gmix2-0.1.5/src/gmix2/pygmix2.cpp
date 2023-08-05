/*****************************************************************************
 * Copyright 2020 Reid Swanson
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*****************************************************************************/


#include <algorithm>
#include <iostream>

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <boost/python/docstring_options.hpp>
#include <Eigen/Core>

#include <Python.h>

#include "gmix2/gmix.hpp"

// See: https://stackoverflow.com/a/59694707/4971706
namespace bp = boost::python;
namespace np = boost::python::numpy;

//-- region Utility Functions ---------------------------------------------------------------------------------------//
template <typename Float>
Eigen::Map<gmix::Array<Float>>
ndarray_to_array(const np::ndarray& array) {
    // Assume it's 1D
    return Eigen::Map<gmix::Array<Float>>(reinterpret_cast<double*>(array.get_data()), 1, array.shape(0));
}

template <typename Float>
gmix::Array<Float>
list_to_array(const bp::list& list) {
    // Assume it's 1D
    const int size = bp::len(list);

    gmix::Array<Float> array(size);
    for (int i = 0; i < size; ++i) {
        array(i) = bp::extract<double>(list[i]);
    }
    return array;
}

template <typename Float>
Eigen::Map<gmix::Matrix<Float>>
ndarray_to_matrix(const np::ndarray& array) {
    const int n_rows = array.shape(0), n_cols = array.shape(1);

    return Eigen::Map<gmix::Matrix<Float>>(reinterpret_cast<double*>(array.get_data()), n_rows, n_cols);
}

template <typename Float>
np::ndarray
matrix_to_array(const gmix::Matrix<Float> &matrix) {
    // Unfortunately, I don't think there's a way around copying the data for the return result;
    const double * const data = matrix.data();
    np::ndarray result = np::zeros(bp::make_tuple(matrix.rows(), matrix.cols()), np::dtype::get_builtin<double>());
    std::copy(data, data + matrix.size(), reinterpret_cast<double*>(result.get_data()));

    return result;
}

template <typename Float>
bp::list
mode_vector_to_list(const gmix::ModeVector<Float>& modes) {
    bp::list result;
    for (int i = 0; i < modes.size(); ++i) {
        // For each mixture
        bp::list mixture_result;
        for (int j = 0; j < modes[i].size(); ++j) {
            // For each mode in the mixture
            const auto& tuple = modes[i][j];
            mixture_result.append(bp::make_tuple(std::get<0>(tuple), std::get<1>(tuple)));
        }
        result.append(std::move(mixture_result));
    }

    return result;
}
//-- endregion Utility Functions ------------------------------------------------------------------------------------//

//-- region Wrapper Functions ---------------------------------------------------------------------------------------//
//-- region Normal Distribution -------------------------------------------------------------------------------------//
np::ndarray
normal_pdf(double x, const np::ndarray& mean, const np::ndarray& std) {
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(normal::pdf<double>(x, m, s));
}
//-- endregion Normal Distribution ----------------------------------------------------------------------------------//

//-- region Mixture Distribution ------------------------------------------------------------------------------------//
/**
 *
 * @param x
 * @param weight
 * @param mean
 * @param std
 * @return
 */
np::ndarray
pdf(double x, const np::ndarray& weight, const np::ndarray& mean, const np::ndarray& std) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::pdf<double>(x, w, m, s)).reshape(bp::make_tuple(-1));
}

const char *pdf_docstring = "The `probability density function <https://en.wikipedia.org/wiki/Probability_density_function>`_ at x.\n\n"
                            "**x** (float, list of floats or 1d-ndarray): The point or points where the PDF will be evaluated.\n\n"
                            "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                            "Each row is a separate distribution. Each column is a weight for that distribution. "
                            "The weights in a row should sum to 1.0.\n\n"
                            "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                            "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                            "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                            "**returns** (1d or 2d-ndarray): For scalar values of ``x`` this returns a 1d array of values containing the PDF of ``x`` for each mixture. "
                            "When ``x`` is a list or array of values then a 2d-array is returned. "
                            "Each row corresponds to a mixture and each column contains the PDF for the corresponding ``x`` value";


np::ndarray
pdf_multi_array(const np::ndarray& x, const np::ndarray& weight, const np::ndarray& mean, const np::ndarray& std) {
    const auto& i = ndarray_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::pdf<double>(i, w, m, s));
}

np::ndarray
pdf_multi_list(const bp::list& x, const np::ndarray& weight, const np::ndarray& mean, const np::ndarray& std) {
    const auto& i = list_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::pdf<double>(i, w, m, s));
}

/**
 *
 * @param x
 * @param weight
 * @param mean
 * @param std
 * @return
 */
np::ndarray
cdf(double x, const np::ndarray& weight, const np::ndarray& mean, const np::ndarray& std) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::cdf<double>(x, w, m, s)).reshape(bp::make_tuple(-1));
}

const char *cdf_docstring = "The `cumulative distribution function <https://en.wikipedia.org/wiki/Cumulative_distribution_function>`_ at x.\n\n"
                            "**x** (float, list of floats or 1d-ndarray): The point or points where the CDF will be evaluated.\n\n"
                            "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                            "Each row is a separate distribution. Each column is a weight for that distribution. "
                            "The weights in a row should sum to 1.0.\n\n"
                            "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                            "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                            "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                            "**returns** (1 or 2d-ndarray): Returns the CDF value(s) for the input ``x`` in the same way as the :func:`.pdf`";

np::ndarray
cdf_multi_array(const np::ndarray& x, const np::ndarray& weight, const np::ndarray& mean, const np::ndarray& std) {
    const auto& i = ndarray_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::cdf<double>(i, w, m, s));
}

np::ndarray
cdf_multi_list(const bp::list& x, const np::ndarray& weight, const np::ndarray& mean, const np::ndarray& std) {
    const auto& i = list_to_array<double>(x);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::cdf<double>(i, w, m, s));
}

/**
 *
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
np::ndarray
ppf(
    double p,
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(
        gmix::ppf<double>(p, w, m, s, lower_bound, upper_bound, tol, max_itr)
    ).reshape(bp::make_tuple(-1));
}

const char *ppf_docstring = "The `percent point function <https://en.wikipedia.org/wiki/Quantile_function>`_ (aka quantile or inverse cumulative distribution function)_ for probability p. "
                            "This returns the value ``x`` such that its probability is less than or equal to ``p``. "
                            "There is no analytic solution to finding the ``ppf`` of a Gaussian mixture so a heuristic search is performed following the recipe in this `Stack Exchange solution <https://stats.stackexchange.com/a/14484>`_.\n\n"
                            "**p** (float, list of floats or 1d-ndarray): The desired probability of the resulting x value(s).\n\n"
                            "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                            "Each row is a separate distribution. Each column is a weight for that distribution. "
                            "The weights in a row should sum to 1.0.\n\n"
                            "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                            "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                            "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                            "**lower_bound** (float): The lower bound of the search.\n\n"
                            "**upper_bound** (float): The upper bound of the search.\n\n"
                            "**tol** (float): The accepted tolerance.\n\n"
                            "**max_itr** (int): The maximum number of iterations before giving up.\n\n"
                            "**returns** (1 or 2d-ndarray): Returns the PPF value(s) for the input ``p`` in the same way as the :func:`.pdf`";

np::ndarray
ppf_multi_array(
    const np::ndarray& p,
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& i = ndarray_to_array<double>(p);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::ppf<double>(i, w, m, s, lower_bound, upper_bound, tol, max_itr));
}

np::ndarray
ppf_multi_list(
    const bp::list& p,
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std,
    const double lower_bound = -1e4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& i = list_to_array<double>(p);
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::ppf<double>(i, w, m, s, lower_bound, upper_bound, tol, max_itr));
}

np::ndarray
mean(const np::ndarray& weight, const np::ndarray& mean) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);

    return matrix_to_array(gmix::mean<double>(w, m)).reshape(bp::make_tuple(-1));
}

const char *mean_docstring = "The mean <https://en.wikipedia.org/wiki/Mean>`_ value of the distribution(s).\n\n"
                             "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                             "Each row is a separate distribution. Each column is a weight for that distribution. "
                             "The weights in a row should sum to 1.0.\n\n"
                             "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                             "**returns** (1d-ndarray): The mean value for each mixture";


np::ndarray
median(
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std,
    const double lower_bound = 1e-4,
    const double upper_bound = 1e4,
    const double tol = 1e-12,
    const int max_itr = 100
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(
        gmix::median<double>(w, m, s, lower_bound, upper_bound, tol, max_itr)
    ).reshape(bp::make_tuple(-1));
}

const char *median_docstring = "The `median <https://en.wikipedia.org/wiki/Median>`_ value of the distribution. "
                               "This is simply a shortcut for calling :func:`ppf` with a ``p=1.0``.\n\n"
                               "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                               "Each row is a separate distribution. Each column is a weight for that distribution. "
                               "The weights in a row should sum to 1.0.\n\n"
                               "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                               "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                               "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                               "**returns** (1d-ndarray): The median value for each mixture";



bp::list
mode(
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std,
    const int max_itr = 1000,
    const double min_diff = 1e-4,
    const double min_grad = 1e-9
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return mode_vector_to_list(gmix::mode<double>(w, m, s, max_itr, min_diff, min_grad));
}

const char *mode_docstring = "The `mode(s) <https://en.wikipedia.org/wiki/Mode_(statistics)>`_ of the distribution. "
                             "This method uses a slightly simplified version of the approach described in `this paper <http://faculty.ucmerced.edu/mcarreira-perpinan/papers/cs-99-03.pdf>`_.\n\n"
                             "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                             "Each row is a separate distribution. Each column is a weight for that distribution. "
                             "The weights in a row should sum to 1.0.\n\n"
                             "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                             "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                             "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                             "**max_itr** (int): The maximum number of iterations before terminating regardless of convergence.\n\n"
                             "**min_diff** (float): Only keep modes whose values are at least ``min_diff`` apart.\n\n"
                             "**min_grad** (float): Stop iterating when the magnitude of the gradient falls below this value.\n\n"
                             "**returns** (a 2d list of tuples): For each mixture this returns a list of tuples. "
                             "The first value of each tuple is the ``x`` value of the mode and the second value is its density.";

np::ndarray
variance(
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::variance<double>(w, m, s)).reshape(bp::make_tuple(-1));
}

const char *variance_docstring = "The `variance <https://en.wikipedia.org/wiki/Variance>`_ of the distribution. "
                                 "`This StackExchange answer <https://stats.stackexchange.com/a/16609>` gives a concise derivation of the variance for a Gaussian mixture.\n\n"
                                 "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                                 "Each row is a separate distribution. Each column is a weight for that distribution. "
                                 "The weights in a row should sum to 1.0.\n\n"
                                 "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                                 "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                                 "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                                 "**returns** (1d-ndarray): The variance for each mixture.";

// Boost Python does not like the name random for some reason and will fail to build
// if the function has that name.
np::ndarray
gmix_random(
    size_t n,
    const np::ndarray& weight,
    const np::ndarray& mean,
    const np::ndarray& std,
    const int seed = -1
) {
    const auto& w = ndarray_to_matrix<double>(weight);
    const auto& m = ndarray_to_matrix<double>(mean);
    const auto& s = ndarray_to_matrix<double>(std);

    return matrix_to_array(gmix::random<double>(n, w, m, s, seed));
}

const char *random_docstring = "Generate `random <https://en.wikipedia.org/wiki/Inverse_transform_sampling>`_ values from the distribution using inverse transform sampling.\n\n"
                               "**n** (int): The number of random values to generate for each mixture.\n\n"
                               "**weights** (2d-ndarray): The weights of each Normal distribution in the mixture(s). "
                               "Each row is a separate distribution. Each column is a weight for that distribution. "
                               "The weights in a row should sum to 1.0.\n\n"
                               "**means** (2d-ndarray): The mean value for each Normal distribution in the mixture(s)\n\n"
                               "**stddevs** (2d-ndarray): The standard deviation for each Normal distribution in the mixture(s). "
                               "Note, Normal distributions are often characterized by their mean and variance, but the standard deviation is used in this toolkit.\n\n"
                               "**seed** (int): The seed to use if you would like reproducible random values.\n\n"
                               "**returns** (2d-ndarray): For each mixture (the rows) this returns ``n`` random values (the columns) drawn from that mixture.";
//-- endregion Mixture Distribution ---------------------------------------------------------------------------------//
//-- endregion Wrapper Functions ------------------------------------------------------------------------------------//

BOOST_PYTHON_FUNCTION_OVERLOADS(ppf_overloads, ppf, 4, 8)
BOOST_PYTHON_FUNCTION_OVERLOADS(ppf_array_overloads, ppf_multi_array, 4, 8)
BOOST_PYTHON_FUNCTION_OVERLOADS(ppf_list_overloads, ppf_multi_list, 4, 8)
BOOST_PYTHON_FUNCTION_OVERLOADS(median_overloads, median, 3, 7)
BOOST_PYTHON_FUNCTION_OVERLOADS(mode_overloads, mode, 3, 6)
BOOST_PYTHON_FUNCTION_OVERLOADS(rand_overloads, gmix_random, 4, 5)

BOOST_PYTHON_MODULE(cgmix2) {
    // NOTE: It is imperative that all numpy arrays created in gmix2
    // are in the default storage order ('C' / Row Major)
    Py_Initialize();
    np::initialize();

    bp::docstring_options doc_options(true, true, false);
    bp::scope().attr("__doc__") = "All the functions listed and documented below in the ``cgmix2`` module are actually made avaliable in python by importing the ``gmix2`` module."
                                        "I apologize for this confusion which is probably arising due to a misunderstanding of how to structure and name C++ extensions";

    bp::def("normal_pdf", normal_pdf);

    bp::def("pdf", pdf, bp::args("x", "weights", "means", "stddevs"), pdf_docstring);
    bp::def("pdf", pdf_multi_array, bp::args("x", "weights", "means", "stddevs"));
    bp::def("pdf", pdf_multi_list, bp::args("x", "weights", "means", "stddevs"));
    bp::def("cdf", cdf, bp::args("x", "weights", "means", "stddevs"), cdf_docstring);
    bp::def("cdf", cdf_multi_array, bp::args("x", "weights", "means", "stddevs"));
    bp::def("cdf", cdf_multi_list, bp::args("x", "weights", "means", "stddevs"));
    bp::def(
        "ppf",
        ppf,
        ppf_overloads(
            (
                bp::args("p"),
                bp::args("weight"),
                bp::args("mean"),
                bp::args("std"),
                bp::args("lower_bound") = -1e4,
                bp::args("upper_bound") = 1e4,
                bp::args("tol") = 1e-12,
                bp::args("max_itr") = 100
            ),
            ppf_docstring
        )
    );
    bp::def(
        "ppf",
        ppf_multi_array,
        ppf_array_overloads(
            (
                bp::args("p"),
                bp::args("weight"),
                bp::args("mean"),
                bp::args("std"),
                bp::args("lower_bound") = -1e4,
                bp::args("upper_bound") = 1e4,
                bp::args("tol") = 1e-12,
                bp::args("max_itr") = 100
            )
        )
    );
    bp::def(
        "ppf",
        ppf_multi_list,
        ppf_list_overloads(
            (
                bp::args("p"),
                bp::args("weight"),
                bp::args("mean"),
                bp::args("std"),
                bp::args("lower_bound") = -1e4,
                bp::args("upper_bound") = 1e4,
                bp::args("tol") = 1e-12,
                bp::args("max_itr") = 100
            )
        )
    );
    bp::def("mean", mean, bp::args("weights", "means"), mean_docstring);
    bp::def(
        "median",
        median,
        median_overloads(
            (
                bp::args("weight"),
                bp::args("mean"),
                bp::args("std"),
                bp::args("lower_bound") = -1e4,
                bp::args("upper_bound") = 1e4,
                bp::args("tol") = 1e-12,
                bp::args("max_itr") = 100
            ),
            median_docstring
        )
    );
    bp::def(
        "mode",
        mode,
        mode_overloads(
            (
                bp::args("weight"),
                bp::args("mean"),
                bp::args("std"),
                bp::args("max_itr") = 1000,
                bp::args("min_diff") = 1e-4,
                bp::args("min_grad") = 1e-9
            ),
            mode_docstring
        )
    );
    bp::def("variance", variance, bp::args("weignts", "means", "stddevs"), variance_docstring);
    bp::def(
        "random",
        gmix_random,
        rand_overloads(
            (
                bp::args("n"),
                bp::args("weight"),
                bp::args("mean"),
                bp::args("std"),
                bp::args("seed") = 1
            ),
            random_docstring
        )
    );
}

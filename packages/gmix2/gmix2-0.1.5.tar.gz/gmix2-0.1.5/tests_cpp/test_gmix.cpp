//
// Created by reid on 8/13/20.
//
#include "doctest.h"

// System Includes
#include <iostream>

// Third Party Includes
#include <Eigen/Core>

// Project Includes
#include "gmix2/gmix.hpp"

const int n_examples = 2;
const int n_components = 5;

typedef gmix::Array<double> Array;
typedef gmix::Matrix<double> Matrix;

TEST_CASE("Testing Gaussian Mixture Distributions") {
    Matrix weight(n_examples, n_components);
    Matrix mean(n_examples, n_components);
    Matrix std(n_examples, n_components);

    weight << 0.15, 0.10, 0.40, 0.05, 0.3,
              0.05, 0.20, 0.10, 0.35, 0.3;

    mean <<  0,  1, 2, 3, 4,
            -5, -2, 0, 1, 3;

    std <<  0.90,  0.50, 2.00, 1.00, 3.0,
            0.50, 10.00, 2.00, 5.00, 0.8;

    SUBCASE("Test root finding") {
        const double a1 = 27.0;
        const double a2 = 28.0;

        auto f1 = [=](const double x)-> double {return x * x * x - a1;};
        auto f2 = [=](const double x)-> double {return x * x * x - a2;};

        double exp_root_1 = 3.0;
        double exp_root_2 = 3.0365889718756625;
        auto act_root_1 = gmix::brent_root(f1);
        auto act_root_2 = gmix::brent_root(f2);

        CHECK(act_root_1 == doctest::Approx(exp_root_1));
        CHECK(act_root_2 == doctest::Approx(exp_root_2));
    }

    SUBCASE("Testing procedural interface") {
        // PDF
        Matrix exp_pdf(2, 1); exp_pdf << 0.21296355237789200, 0.059730094960613933;
        Matrix act_pdf = gmix::pdf<double>(1.0, weight, mean, std);

        CHECK(act_pdf.isApprox(exp_pdf));

        Matrix exp_pdf2(2, 2); exp_pdf2 << 0.21296355237789200, 0.000335617248627443,
                                           0.05973009496061393, 0.044152358958679160;

        Array points(2); points << 1.0, -5.5;
        Matrix act_pdf2 = gmix::pdf<double>(points, weight, mean ,std);

        CHECK(act_pdf2.isApprox(exp_pdf2));

        // CDF
        Matrix exp_cdf(2, 1); exp_cdf << 0.35216005883186496, 0.41959143016292472;
        Matrix act_cdf = gmix::cdf<double>(1.0, weight, mean, std);

        CHECK(act_cdf.isApprox(exp_cdf));

        Matrix exp_cdf2(2, 2); exp_cdf2 << 0.352160058832, 0.000266662424,
                                           0.419591430163, 0.11474477839;
        Matrix act_cdf2 = gmix::cdf<double>(points, weight, mean, std);

        CHECK(act_cdf2.isApprox(exp_cdf2));

        // PPF
        Matrix exp_ppf(2, 1); exp_ppf << 0.753339733752, -1.185816277994;
        Matrix act_ppf = gmix::ppf<double>(0.3, weight, mean, std);

        CHECK(act_ppf.isApprox(exp_ppf));

        // Mode
        gmix::ModeVector<double> exp_modes = {
            {gmix::Pair<double>(0.9580152000982137, 0.21324093573952826)},
            {
                gmix::Pair<double>(-4.970966372242318, 0.06205794913899075),
                gmix::Pair<double>(2.96872434469676, 0.189013117805071),
            }
        };
        gmix::ModeVector<double> act_modes = gmix::mode<double>(weight, mean, std);

        CHECK_EQ(act_modes.size(), exp_modes.size());
        CHECK_EQ(act_modes[0].size(), 1);
        CHECK_EQ(act_modes[1].size(), 2);
        CHECK_EQ(act_modes[0].size(), exp_modes[0].size());
        CHECK_EQ(act_modes[1].size(), exp_modes[1].size());

        CHECK(std::get<0>(act_modes[0][0]) == doctest::Approx(std::get<0>(exp_modes[0][0])));
        CHECK(std::get<1>(act_modes[0][0]) == doctest::Approx(std::get<1>(exp_modes[0][0])));
        CHECK(std::get<0>(act_modes[1][0]) == doctest::Approx(std::get<0>(exp_modes[1][0])));
        CHECK(std::get<1>(act_modes[1][0]) == doctest::Approx(std::get<1>(exp_modes[1][0])));
        CHECK(std::get<0>(act_modes[1][1]) == doctest::Approx(std::get<0>(exp_modes[1][1])));
        CHECK(std::get<1>(act_modes[1][1]) == doctest::Approx(std::get<1>(exp_modes[1][1])));

        // Variance
        Matrix exp_var(2, 1); exp_var << 6.38400000000000034106, 34.0944999999999964757;
        Matrix act_var = gmix::variance<double>(weight, mean, std);

        CHECK(act_var.isApprox(exp_var));

        // Random
        Matrix exp_random(2, 5);
        exp_random << 5.22846717120181558869,   1.15596613430513706078, -0.855235849534194958466,    3.9807712788443647689,   0.88644894142577013163,
                      5.02247578725460908089,  0.394091114545033371908,  -7.62489438958240217659,   3.67892633903988919286, -0.645765183607914239339;
        Matrix act_random = gmix::random<double>(5, weight, mean, std, 2177);

        CHECK(act_random.isApprox(exp_random));
    }
}
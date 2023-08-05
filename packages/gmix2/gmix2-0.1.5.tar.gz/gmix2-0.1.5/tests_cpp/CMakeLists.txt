find_package(Eigen3 3.3 REQUIRED NO_MODULE)

add_library(doctest INTERFACE)
add_library(gmix2 INTERFACE)

add_executable(test_gmix test_gmix.cpp test_main.cpp)

target_include_directories(test_gmix PUBLIC ../include)

target_compile_features(test_gmix PRIVATE cxx_std_17)

target_link_libraries(test_gmix PRIVATE gmix2 Eigen3::Eigen doctest)

add_test(test_gmix_test COMMAND test_gmix)

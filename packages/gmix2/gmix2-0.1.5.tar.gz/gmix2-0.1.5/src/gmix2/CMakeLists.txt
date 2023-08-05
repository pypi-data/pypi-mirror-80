find_package(Eigen3 3.3 REQUIRED NO_MODULE)
find_package(PythonLibs 3.7 REQUIRED)
find_package(PythonLibs 3.7 REQUIRED)
find_package(Boost 1.73.0 REQUIRED COMPONENTS system python37 numpy37)


set(GMIX_INCLUDE "${PROJECT_SOURCE_DIR}/include")

message("GMIX_INCLUDE: ${GMIX_INCLUDE}")

# include directories
include_directories("$GMIX_INCLUDE")
include_directories("${PYTHON_INCLUDE_DIRS}")
include_directories("${Boost_INCLUDE_DIRS}")

add_library(cgmix2 SHARED pygmix2.cpp)

target_include_directories(cgmix2 PUBLIC ${Boost_INCLUDE_DIRS} ${GMIX_INCLUDE})
target_compile_features(cgmix2 PUBLIC cxx_std_17)

set_target_properties(
        cgmix2
        PROPERTIES
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS OFF
        PREFIX ""
        OUTPUT_NAME "cgmix2"
        LINKER_LANGUAGE CXX
)

target_link_libraries(cgmix2 PRIVATE ${Boost_LIBRARIES} Eigen3::Eigen)

#add_custom_command(
#    TARGET cgmix2 POST_BUILD
#    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:cgmix2> ../../../python-package/
#)

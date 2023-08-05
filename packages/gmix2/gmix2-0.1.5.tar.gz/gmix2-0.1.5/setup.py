import os
import pathlib
import subprocess

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


current_dir = pathlib.Path(__file__).parent
readme = (current_dir / "README.rst").read_text()


# See: https://www.benjack.io/2017/06/12/python-cpp-tests.html
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])

        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions)
            )

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        cwd = pathlib.Path().absolute()

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config
        ]

        # example of build args
        build_args = [
            '-v',
            '--config', config,
            '--', '-j2'
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        os.chdir(str(cwd))


if __name__ == '__main__':
    setup(name='gmix2',
          version='0.1.5',
          description='An implementation of Gaussian mixture distribution methods',
          long_description=readme,
          long_description_content_type='text/x-rst',
          install_requires=[
              'numpy',
          ],
          extras_require={
              'plotting': [
                  'pandas',
                  'plotnine',
                  'scipy'
              ]
          },
          author='Reid Swanson',
          maintainer='Reid Swanson',
          author_email='reid@reidswanson.com',
          maintainer_email='reid@reidswanson.com',
          zip_safe=False,
          package_dir={'': 'src/gmix2'},
          py_modules=['gmix2'],
          ext_modules=[CMakeExtension('cgmix2')],
          cmdclass={'build_ext': CMakeBuild},
          include_package_data=True,
          license='Apache-2.0',
          url='https://bitbucket.org/reidswanson/gmix2',
          classifiers=['Development Status :: 4 - Beta',
                       'Intended Audience :: Science/Research',
                       'License :: OSI Approved :: Apache Software License',
                       'Natural Language :: English',
                       'Operating System :: POSIX :: Linux',
                       'Programming Language :: Python :: 3.7',
                       'Topic :: Scientific/Engineering :: Mathematics'])

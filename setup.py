from setuptools import setup, find_packages
import os

# make sure users without cython can install our extensions
try:
    from Cython.Distutils.extension import Extension
    from Cython.Distutils import build_ext as _build_ext
    USE_CYTHON = True
except ImportError:
    from setuptools import Extension
    from setuptools.command.build_ext import build_ext as _build_ext
    USE_CYTHON = False

print('using cython', USE_CYTHON)


# If we compile cython extensions using numpy
# we have to include the numpy headers
# If we just import numpy here, people need to have it already
# installed.
# Placing the import here, makes sure it runs after the parsing
# of our requirements further down.
class build_ext(_build_ext):
    def finalize_options(self):
        super().finalize_options()
        import numpy
        self.include_dirs.append(numpy.get_include())


# if we have cython, use the cython file if not the c file
ext = '.pyx' if USE_CYTHON else '.c'
extensions = [
    Extension('cython_demo.fib', sources=['cython_demo/fib' + ext]),
]
cmdclass = {'build_ext': build_ext}

# give a nice error message if people cloned the
# repository and do not have cython installed
if ext == '.c':
    if not os.path.isfile('cython_demo/example.c'):
        raise ImportError('You need `Cython` to build this project locally')


with open('README.md') as f:
    long_description = f.read()

setup(
    name='cython_demo',
    version='0.1.0',
    description='Python read-only implementation of the EventIO file format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/maxnoe/cython-demo',
    author='Maximilian Noethe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',

    packages=find_packages(),

    ext_modules=extensions,
    cmdclass=cmdclass,

    # package the c files, then users downloading sdist
    # (e.g. from PyPI) don't need cython
    package_data={
        'cython_demo': ['*.c'],
    },
    install_requires=[
        'numpy',
    ],
    setup_requires=['numpy'],
)

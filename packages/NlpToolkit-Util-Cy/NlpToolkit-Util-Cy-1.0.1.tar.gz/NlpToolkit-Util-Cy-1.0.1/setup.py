from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Util/*.pyx", "Util/*.pxd"], compiler_directives={'language_level' : "3"}),
    name='NlpToolkit-Util-Cy',
    version='1.0.1',
    packages=['Util'],
    url='https://github.com/olcaytaner/Util-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Simple Utils'
)

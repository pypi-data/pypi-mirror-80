from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["PropBank/*.pyx", "PropBank/*.pxd"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-PropBank-Cy',
    version='1.0.0',
    packages=['PropBank'],
    url='https://github.com/olcaytaner/TurkishPropbank-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Turkish PropBank'
)

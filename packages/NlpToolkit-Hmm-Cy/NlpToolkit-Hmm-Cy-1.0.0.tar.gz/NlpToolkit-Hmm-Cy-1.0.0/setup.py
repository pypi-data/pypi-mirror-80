from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Hmm/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-Hmm-Cy',
    version='1.0.0',
    packages=['Hmm'],
    package_data={'Hmm': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/olcaytaner/Hmm-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Hidden Markov Model Library',
    install_requires=['NlpToolkit-Math-Cy', 'NlpToolkit-DataStructure-Cy']
)

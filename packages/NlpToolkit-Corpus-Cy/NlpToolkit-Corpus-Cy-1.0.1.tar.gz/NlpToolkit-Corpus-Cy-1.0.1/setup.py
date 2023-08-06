from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Corpus/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-Corpus-Cy',
    version='1.0.1',
    packages=['Corpus'],
    package_data={'Corpus': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/olcaytaner/Corpus-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Corpus library',
    install_requires=['NlpToolkit-Dictionary-Cy']
)

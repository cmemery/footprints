from distutils.core import setup

setup(
    name='footprints',
    version='1.0',
    author='Chris Emery',
    author_email='chris.emery@gmail.com',
    packages=['footprints',],
    license='GPL2',
    long_description=open('README.md').read(),
    install_requires=['zeep<3']
)

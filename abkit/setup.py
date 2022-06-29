from abkit import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='abkit',
    version=__version__,
    author='lee',
    author_email='leepand6@gmail.com',
    packages=['abkit', 'abkit.test'],
    #scripts=['bin/abkit', 'bin/abkit-web'],
    url='http://github.com/leepand/open-mlops',
    #license=open('LICENSE.txt').read(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    description='A/B testing framework under active development at bole/SEA',
    long_description=open('README.rst').read() + '\n\n' +
                     open('CHANGES.rst').read(),
    #tests_require=['nose'],
    #test_suite='nose.collector',
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
)
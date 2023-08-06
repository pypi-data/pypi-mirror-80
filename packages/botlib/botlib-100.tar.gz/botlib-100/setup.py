# setup.py
#
#

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read():
    return open("README", "r").read()

setup(
    name='botlib',
    version='100',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description=""" BOTLIB is a framework you can use to program bots. """,
    long_description=read(),
    license='Public Domain',
    install_requires=["olib"],
    packages=["bot", "bmod", "ol"],
    namespace_packages=["bot", "bmod"],
    scripts=["bin/bcmd", "bin/botd", "bin/bsh", "bin/birc"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

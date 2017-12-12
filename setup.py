from setuptools import setup

import retox

with open('README.rst') as readme:
    long_description = readme.read()
with open('requirements.txt') as req:
    requirements = req.readlines()

_version = retox.__version__

def main():
    setup(
        name='retox',
        description='distributing activities of the tox tool',
        long_description=long_description,
        version=_version,
        url='https://github.com/tonybaloney/retox',
        license='APACHE-2',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='Anthony Shaw',
        classifiers=['Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Utilities',
                     'Programming Language :: Python',
                     ],
        packages=['retox', ],
        install_requires=[requirements],
        entry_points={'console_scripts': 'retox=retox.main:main',
                      'tox': ['proclimit = retox.tox_proclimit']},
    )

if __name__ == '__main__':
    main()

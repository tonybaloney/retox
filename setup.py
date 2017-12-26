from setuptools import setup

import retox

with open('README.rst') as readme:
    long_description = readme.read()


_version = retox.__version__

requirements = [
    'tox==2.9.1',
    'eventlet==0.21.0',
    'asciimatics==1.9.0',
    'pathlib2==2.3.0',
]


def main():
    setup(
        name='retox',
        description='A parallel service for tox',
        long_description=long_description,
        version=_version,
        url='https://github.com/tonybaloney/retox',
        license='MIT',
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
        entry_points={'console_scripts': 'retox=retox.__main__:main',
                      'tox': ['exclude = retox.exclude',
                              'proclimit = retox.proclimit',
                              'watch = retox.watch']},
    )

if __name__ == '__main__':
    main()

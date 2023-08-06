#!/usr/bin/env python3

import re
import setuptools

with open('src/c10k/__init__.py') as f:
    version = re.search(r"__version__\s*=\s*'(.*)'", f.read()).group(1)
with open('README.rst') as f:
    readme  = f.read()

setuptools.setup(
                name='c10k',
             version=version,
         description=('Solving the C10K problem without '
                      'modifying the code'),
    long_description=readme,
             license='GPL',
            keywords='gevent asynchronous c10k',
              author='Wilhelm Shen',
        author_email='wilhelmshen@pyforce.com',
         package_dir={'': 'src'},
            packages=['c10k'],
         classifiers=
             [
                 'License :: OSI Approved :: GNU General Public License '+
                                                                 '(GPL) ',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: Implementation :: '+
                                                              'CPython',
                 'Operating System :: POSIX',
                 'Topic :: Internet',
                 'Topic :: Software Development :: Libraries :: '+
                                                 'Python Modules',
                 'Intended Audience :: Developers',
                 'Development Status :: 1 - Planning'
             ],
     python_requires='>=3.6',
        entry_points=
             {
                 'console_scripts': ['c10k=c10k.__main__:main']
             }
)

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='logmonitor',
    version='0.0.7a1',
    description='A simple log monitor application that parses an actively written log and outputs useful statistics.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FConstantinos/logmonitor',
    author='Konstantinos Fragkiadakis',
    author_email='fconstantinos@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='logging, monitoring, development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6.9, <4',
    install_requires=['sh', 'apachelogs'],
    platforms='any',
    entry_points={
        'console_scripts': ['logmonitor=logmonitor:main', ], },
    extras_require={
        'dev': ['pytest', 'log-generator', 'wheel'],
        'test': ['pytest', 'log-generator'],
    },
    project_urls={
          'Bug Reports': 'https://github.com/FConstantinos/logmonitor/issues',
          'Source': 'https://github.com/FConstantinos/logmonitor/',
    },
)

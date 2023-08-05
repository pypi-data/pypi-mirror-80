from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='mercado_bitcoin_api',
    version='0.0.6',
    description='API implementation for Mercado Bitcoin (BR)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pedrohml/mercado-bitcoin-api',
    author='Pedro Lira',
    author_email='pedrohml@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='finance, bitcoin, api',

    packages=find_packages(),

    python_requires='>=3.5, <4',

    install_requires=['requests==2.24.0', 'pandas==1.1.2', 'scipy==1.5.2'],

    extras_require={
        'dev': ['jupyterlab==2.2.8']
    },

    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # project_urls={
    #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #     'Funding': 'https://donate.pypi.org',
    #     'Say Thanks!': 'http://saythanks.io/to/example',
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)

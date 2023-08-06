# type: ignore

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='valkyrie_util',
    version='2.3.3',
    author='David Castner',
    author_email='davidjcastner@gmail.com',
    description='A python library of various math and performance tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/davidjcastner/valkyrie-util',
    packages=setuptools.find_packages(),
    package_data={'valkyrie_util': ['py.typed']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    python_requires='>=3.8',
)

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='colourise',
    version='0.0.4',
    author='Sander Huijsen',
    author_email='sander.huijsen@nmtafe.wa.edu.au',
    description='Package performing colour conversions',
    long_description=long_description,
    url='https://github.com/Sandyman/colourise',
    packages=setuptools.find_packages(exclude=['*.test', 'test']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

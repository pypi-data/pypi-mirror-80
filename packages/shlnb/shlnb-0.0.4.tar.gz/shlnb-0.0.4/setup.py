import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required_modules = list([ # update list with all modules used in package
        'numpy>=1.11.3',
        'setuptools',
        'arlpy',
        'soundfile'
        ])

setuptools.setup(
    name= 'shlnb',
    version="0.0.4", # update to latest release version
    author="Nicholas Butterly",
    author_email="butterlyn888@gmail.com",
    description="Beamforming and signal analysis of microphone ULA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/butterlyn/SHLNB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = required_modules,
    setup_requires = required_modules
)

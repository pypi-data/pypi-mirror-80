import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coverage-fixpaths",
    version="1.2.0",
    author="Teake Nutma",
    description="A small CLI tool that automatically fixes paths in Cobertura coverage reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omegacen/coverage-fixpaths",
    packages=setuptools.find_packages(),
    license_file='LICENSE',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['coverage-fixpaths=coveragefixpaths.coverage.__main__:main'],
    }
)

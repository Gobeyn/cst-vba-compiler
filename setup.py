from setuptools import find_packages, setup

setup(
    name="cst_vba_compiler",
    version="0.0.1",
    author="Aaron Gobeyn",
    author_email="aaron.gobeyn@tu-darmstadt.de",
    description="Python package for writing CST macros and compiling it to a VBA script readable by CST.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[],
)

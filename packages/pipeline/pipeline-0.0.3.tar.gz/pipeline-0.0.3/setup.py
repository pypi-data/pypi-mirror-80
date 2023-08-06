import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pipeline",
    version="0.0.3",
    author="Poor Yorick",
    author_email="org.pypi@pooryorick.com",
    description="Command pipelines for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pooryorick/pipeline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlops-local",
    version="1.0.0",
    author="Petter Hultin Gustafsson",
    author_email="petter@mlops.cloud",
    description="Package to test preprocessing and ML scripts locally before pushing to the MLOps platform",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["Click", "docker", "gitpython"],
    python_requires='>=3.6',
    entry_points={"console_scripts": ["mlops=main:cli"]},
)

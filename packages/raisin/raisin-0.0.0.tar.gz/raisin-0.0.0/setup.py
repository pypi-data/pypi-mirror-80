import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="raisin", # Replace with your own username
    version="0.0.0",
    author="Robin RICHARD (robinechuca)",
    author_email="raisin@ecomail.fr",
    description="Cluster Work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/robinechuca/raisin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.4",
)

import setuptools

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="UltraEval",
    version="0.1",
    author="UltraEval Team",
    author_email="",
    description="A framework for evaluating language models",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": ["black", "flake8", "pre-commit", "pytest", "pytest-cov"],
    },
)

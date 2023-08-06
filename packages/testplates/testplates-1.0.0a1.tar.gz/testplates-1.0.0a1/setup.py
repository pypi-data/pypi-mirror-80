import os
import codecs

from typing import Final
from setuptools import setup, find_packages

RESULTFUL: Final[str] = "resultful == 1.0.0a2"

BLACK: Final[str] = "black == 20.8b1"
FLAKE8: Final[str] = "flake8 ~= 3.8.0"
MYPY: Final[str] = "mypy ~= 0.782"

PYTEST: Final[str] = "pytest ~= 6.0.1"
PYTEST_COV: Final[str] = "pytest-cov ~= 2.8.0"
HYPOTHESIS: Final[str] = "hypothesis ~= 5.36.0"

SPHINX: Final[str] = "sphinx ~= 3.0.0"
SPHINX_RTD_THEME: Final[str] = "sphinx_rtd_theme ~= 0.4.3"
SPHINX_AUTODOC_TYPEHINTS: Final[str] = "sphinx_autodoc_typehints ~= 1.10.0"

WHEEL: Final[str] = "wheel"
TWINE: Final[str] = "twine"


def main():
    with codecs.open("README.rst", encoding="utf-8") as handle:
        long_description = handle.read()

    setup(
        name="testplates",
        author="Krzysztof Przybyła",
        url="https://github.com/kprzybyla/testplates",
        description="Testing Templates",
        long_description=long_description,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Testing",
            "Topic :: Software Development :: Libraries",
        ],
        python_requires="~= 3.8",
        install_requires=[RESULTFUL, MYPY],
        extras_require={
            "black": [BLACK],
            "lint": [FLAKE8],
            "mypy": [MYPY, PYTEST, HYPOTHESIS],
            "test": [PYTEST, PYTEST_COV, HYPOTHESIS],
            "docs": [SPHINX, SPHINX_RTD_THEME, SPHINX_AUTODOC_TYPEHINTS],
            "deploy": [WHEEL, TWINE],
        },
        use_scm_version={"write_to": os.path.join("src/testplates/__version__.py")},
        platforms=["linux"],
        setup_requires=["setuptools_scm"],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        package_data={"testplates": ["py.typed"]},
    )


if __name__ == "__main__":
    main()

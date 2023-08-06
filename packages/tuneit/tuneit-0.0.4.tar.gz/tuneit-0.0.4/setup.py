from lyncs_setuptools import setup

requirements = [
    "dill",
    "dataclasses",
    "python-varname",
    "tabulate",
    "numpy",
]

extras = {
    "graph": [
        "graphviz",
    ],
    "test": ["pytest", "pytest-cov"],
}

setup(
    "tuneit",
    install_requires=requirements,
    extras_require=extras,
)

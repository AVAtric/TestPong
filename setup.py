"""Setup script for TestPong."""

from setuptools import setup, find_packages

setup(
    name="pongclaw",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pongclaw=pongclaw.__main__:main",
        ],
    },
    python_requires=">=3.6",
)
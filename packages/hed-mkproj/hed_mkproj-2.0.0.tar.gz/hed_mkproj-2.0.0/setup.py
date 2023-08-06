from distutils.core import setup
from pathlib import Path

setup(
    name="hed_mkproj",
    version="2.0.0",
    description="Vanilla project skeleton generator.",
    long_description=Path(__file__).parent.joinpath("README.md").read_text(encoding="utf-8"),
    author="Hrisimir Dakov",
    author_email="hrisimir.dakov@gmail.com",
    url="https://www.github.com/Hrissimir/hed_mkproj",
    packages=[
        "mkproj",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mkproj = mkproj.cli:run",
        ]
    },
    license=Path(__file__).parent.joinpath("LICENSE.txt").read_text(encoding="utf-8"),
)

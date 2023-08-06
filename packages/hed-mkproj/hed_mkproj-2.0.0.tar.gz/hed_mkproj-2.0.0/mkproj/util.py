"""Simple project skeleton generator,"""
import logging
from pathlib import Path
from textwrap import dedent
from typing import Tuple

_log = logging.getLogger("mkproj")
_log.addHandler(logging.NullHandler())

SETUP_PY = dedent("""\
           from distutils.core import setup
           from pathlib import Path

           setup(
               name="{}",
               version="0.0.1",
               description="{}",
               long_description=Path(__file__).parent.joinpath("README.md").read_text(encoding="utf-8"),
               author="",
               author_email="",
               url="",
               packages=[
                   "{}", 
               ],
               include_package_data=True,
               license=Path(__file__).parent.joinpath("LICENSE.txt").read_text(encoding="utf-8"),
           )
           """)

MANIFEST_IN = dedent("""\
            include *.md
            include *.txt
            recursive-include Docs * 
            recursive-include tests *
            """)

BUILD_SH = dedent("""\
            #!/bin/bash
            rm -rf build
            rm -rf dist
            python setup.py clean
            python setup.py build
            python setup.py sdist
            """)


def _mkdirs(root: Path, name: str, package="") -> Tuple[Path, Path]:
    _log.info("creating directory structure for: '%s' in '%s' (package: '%s')", name, str(root), package)

    project_dir = root / name
    project_dir.mkdir(parents=True)
    _log.info("%s created!", str(project_dir))

    package_dir = project_dir / (package or name)
    package_dir.mkdir()
    _log.info("%s created!", str(package_dir))

    docs = project_dir / "Docs"
    docs.mkdir()
    _log.info("%s created!", str(docs))

    tests = project_dir / "tests"
    tests.mkdir()
    _log.info("%s created!", str(tests))

    return project_dir, package_dir


def _mkfiles(project_dir: Path, package_dir: Path, description: str):
    _log.info("creating project files...")

    setup = project_dir / "setup.py"
    setup.write_text(
        SETUP_PY.format(project_dir.name, description, package_dir.name),
        encoding="utf-8"
    )

    readme = project_dir / "README.md"
    readme.write_text(project_dir.name)
    _log.info("%s created", str(readme))

    license_ = project_dir / "LICENSE.txt"
    license_.write_text("license-goes-here", encoding="utf-8")
    _log.info("%s created!", str(license_))

    manifest = project_dir / "MANIFEST.in"
    manifest.write_text(MANIFEST_IN, encoding="utf-8")
    _log.info("%s created!", str(manifest))

    init = package_dir / "__init__.py"
    init.write_text("", encoding="utf-8")
    _log.info("%s created!", str(init))

    build = project_dir / "build.sh"
    build.write_text(BUILD_SH, encoding="utf-8")
    _log.info("%s created!", str(build))


def mkproj(root: Path, name: str, description: str, package=""):
    """Create project skeleton in target dir.

    Args:
        root:           project root dir
        name:           project name
        description:    project description
        package:        project package
    """

    if not name:
        raise ValueError()

    project_dir, package_dir = _mkdirs(root, name, package)
    _mkfiles(project_dir, package_dir, description)
    _log.info("all done!")

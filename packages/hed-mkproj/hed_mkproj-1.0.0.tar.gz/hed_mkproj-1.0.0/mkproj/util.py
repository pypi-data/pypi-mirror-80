"""Simple project skeleton generator,"""
import logging
from pathlib import Path
from textwrap import dedent
from typing import Tuple

_log = logging.getLogger("mkproj")
_log.addHandler(logging.NullHandler())

SETUP_PY = dedent("""\
           from distutils.core import setup

           setup(
               name="{}",
               version="0.0.1",
               author="",
               author_email="",
               url="",
               packages=[
                   "{}", 
               ],
               include_package_data=True,
           )
           """)

MANIFEST_IN = dedent("""\
            include *.md
            recursive-include Docs * 
            recursive-include tests *
            """)


def _mkdirs(root: Path, project: str, package="") -> Tuple[Path, Path]:
    project_dir = root / project
    project_dir.mkdir(parents=True)
    _log.info("created project dir: '%s'", str(project_dir))

    package_dir = project_dir / (package or project)
    package_dir.mkdir()
    _log.info("created package dir: '%s'", str(package_dir))

    docs = project_dir / "Docs"
    docs.mkdir()
    _log.info("%s created", str(docs))

    tests = project_dir / "tests"
    tests.mkdir()
    _log.info("%s created", str(tests))

    return project_dir, package_dir


def _mkfiles(project_dir: Path, package_dir: Path):
    init = package_dir / "__init__.py"
    init.write_text("", encoding="utf-8")
    _log.info("%s created", str(init))

    readme = project_dir / "README.md"
    readme.write_text(project_dir.name)
    _log.info("%s created", str(readme))

    setup = project_dir / "setup.py"
    setup.write_text(
        SETUP_PY.format(project_dir.name, package_dir.name),
        encoding="utf-8"
    )
    _log.info("%s created", str(setup))

    manifest = project_dir / "MANIFEST.in"
    manifest.write_text(MANIFEST_IN, encoding="utf-8")


def mkproj(root: Path, project: str, package=""):
    """Create project skeleton in cwd.

    Args:
        root:       project root dir.
        project:    project name.
        package:    project package name.
    """

    if not project:
        raise ValueError()

    _log.info("making directory structure for: '%s' in '%s' (package: '%s')", project, str(Path.cwd()), package)
    project_dir, package_dir = _mkdirs(root, project, package)

    _log.info("creating files...")
    _mkfiles(project_dir, package_dir)

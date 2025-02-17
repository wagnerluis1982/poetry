from typing import TYPE_CHECKING

import pytest

from cleo.io.null_io import NullIO

from poetry.core.packages.project_package import ProjectPackage
from poetry.puzzle.provider import Provider as BaseProvider
from poetry.repositories import Pool
from poetry.repositories import Repository


if TYPE_CHECKING:
    from tests.helpers import TestRepository


class Provider(BaseProvider):
    def set_package_python_versions(self, python_versions: str) -> None:
        self._package.python_versions = python_versions
        self._python_constraint = self._package.python_constraint


@pytest.fixture
def repo() -> Repository:
    return Repository()


@pytest.fixture
def pool(repo: "TestRepository") -> Pool:
    pool = Pool()
    pool.add_repository(repo)

    return pool


@pytest.fixture
def root() -> ProjectPackage:
    return ProjectPackage("myapp", "0.0.0")


@pytest.fixture
def provider(pool: Pool, root: ProjectPackage) -> Provider:
    return Provider(root, pool, NullIO())

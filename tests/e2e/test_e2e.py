from pathlib import Path
from typing import List

from cleo.testers.application_tester import ApplicationTester
from poetry.core.packages.package import Package
from poetry.core.pyproject.toml import PyProjectTOML
from pytest_mock import MockerFixture


def test_command(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_command_with_latest(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )

    path = project_path / "expected_pyproject_with_latest.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up --latest") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_command_with_dry_run(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )

    expected = PyProjectTOML(tmp_pyproject_path).file.read()

    assert app_tester.execute("up --dry-run") == 0
    # assert pyproject.toml file not modified
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_not_called()


def test_command_with_no_install(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up --no-install") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="lock", args="--no-update")
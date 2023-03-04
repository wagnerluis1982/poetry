from __future__ import annotations

from typing import TYPE_CHECKING

from cleo.helpers import argument

from poetry.console.commands.env_command import EnvCommand
from poetry.utils._compat import WINDOWS


if TYPE_CHECKING:
    from poetry.core.masonry.utils.module import Module


class RunCommand(EnvCommand):
    name = "run"
    description = "Runs a command in the appropriate environment."

    arguments = [
        argument("args", "The command and arguments/options to run.", multiple=True)
    ]

    def handle(self) -> int:
        args = self.argument("args")
        script = args[0]
        scripts = self.poetry.local_config.get("scripts")

        if scripts and script in scripts:
            self._ensure_installed_script(script, scripts[script])

        try:
            return self.env.execute(*args)
        except FileNotFoundError:
            self.line_error(f"<error>Command not found: <c1>{script}</c1></error>")
            return 1

    @property
    def _module(self) -> Module:
        from poetry.core.masonry.utils.module import Module

        poetry = self.poetry
        package = poetry.package
        path = poetry.file.parent
        module = Module(package.name, path.as_posix(), package.packages)

        return module

    def _ensure_installed_script(
        self, script: str, entry_point: str | dict[str, str]
    ) -> None:
        """Ensure an entry point is installed in order to be executable

        If an entry point script does not exist in the file system, then it is made an
        attempt to create the script before the execution.
        """
        for script_dir in self.env.script_dirs:
            script_path = script_dir / script
            if WINDOWS:
                script_path = script_path.with_suffix(".cmd")
            if script_path.exists():
                return

        # If reach this point, the script is not installed
        self.line(
            f"WARNING: '{script}' is an entry point defined in pyproject.toml, but it"
            " is not installed."
        )
        self.line("")
        question_text = (
            f"You need to install the project in order to make '{script}' available."
            " Proceed with installation?"
        )
        if self.confirm(question_text):
            self._install()

    def _install(self) -> None:
        from poetry.console.application import Application
        from poetry.console.commands.install import InstallCommand

        command = InstallCommand()
        command.set_application(self.application)
        command.set_poetry(self.poetry)
        command.set_env(self.env)
        Application.configure_installer_for_command(command, self.io)

        status = command.execute(self.io)

        if status != 0:
            raise RuntimeError("Error on install")

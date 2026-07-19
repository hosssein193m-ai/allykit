"""
Python Package Management and Python Execution Utility Module

This module provides comprehensive functionality for managing Python packages
using pip and executing Python scripts/commands. It extends the Cmd class
to provide pip-specific operations and Python runtime management.
"""

from allykit.Automobile_kit.Automobile import Cmd


class Pip(Cmd.cmd):
    """
    A comprehensive pip package management utility class.
    
    This class provides a complete interface for Python package management
    operations including installation, uninstallation, listing, updating,
    and dependency management. All methods inherit command execution
    capabilities from the Cmd class.
    
    Features:
        - Package installation (single, multiple, from requirements)
        - Package uninstallation (single, all)
        - Package listing and information
        - Dependency management (freeze, requirements)
        - Package updates (single, all outdated)
        - Cache management
        - Editable installations
        - Constraint file support
    
    Inheritance:
        - Cmd.cmd: Provides command execution capabilities
    """
    
    def pip(self, module: str) -> str:
        """
        Install a single Python package using pip.
        
        Args:
            module (str): The name of the package to install.
        
        Returns:
            str: The output from the pip installation command.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip("requests")
            >>> print(result)
            'Collecting requests\\n  Downloading requests-2.28.1-py3-none-any.whl...'
        """
        return self.cmd(f"pip install {module}")

    def pips(self, modules: list):
        """
        Install multiple Python packages sequentially using a generator.
        
        This method yields the output of each package installation as it
        completes, allowing for real-time progress monitoring.
        
        Args:
            modules (list): A list of package names to install.
        
        Yields:
            str: The output from each pip installation command.
        
        Example:
            >>> pip = Pip()
            >>> for result in pip.pips(["requests", "flask", "numpy"]):
            ...     print(f"Installation result: {result[:100]}...")
        """
        for module in modules:
            yield self.cmd(f"pip install {module}")        

    def data_pip(self) -> str:
        """
        Get installed packages and their versions as a dictionary.
        
        This method parses the output of 'pip freeze' and returns a
        structured dictionary mapping package names to their versions.
        
        Returns:
            dict: A dictionary where keys are package names and values are
                  their version strings. Returns empty dict if no packages
                  are installed or if parsing fails.
        
        Example:
            >>> pip = Pip()
            >>> packages = pip.data_pip()
            >>> print(packages.get("requests"))
            '2.28.1'
            >>> for name, version in packages.items():
            ...     print(f"{name}=={version}")
        """
        packages = {}
        result = self.cmd("pip freeze")
        for line in result.strip().split('\n'):
            if '==' in line:
                name, version = line.split('==')
                packages[name.strip()] = version.strip()
        return packages

    def show_pip(self, package: str) -> str:
        """
        Display detailed information about an installed package.
        
        Args:
            package (str): The name of the package to show information for.
        
        Returns:
            str: Detailed package information including version, location,
                 dependencies, and metadata.
        
        Example:
            >>> pip = Pip()
            >>> info = pip.show_pip("requests")
            >>> print(info)
            'Name: requests\\nVersion: 2.28.1\\nSummary: Python HTTP for Humans...'
        """
        return self.cmd(f"pip show {package}")

    def create_requirements(self, filename: str = "requirements.txt"):
        """
        Create a requirements.txt file with all installed packages.
        
        Args:
            filename (str, optional): The name of the requirements file.
                                     Defaults to "requirements.txt".
        
        Returns:
            str: The output from the pip freeze command, redirected to file.
        
        Example:
            >>> pip = Pip()
            >>> pip.create_requirements()
            >>> pip.create_requirements("dependencies.txt")
        """
        return self.cmd(f"pip freeze > {filename}")
    
    def pip_install_all(self, modules: list[str]) -> str:
        """
        Install multiple packages in a single pip command.
        
        Args:
            modules (list[str]): List of package names to install.
        
        Returns:
            str: The combined output from the pip installation.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_install_all(["pandas", "matplotlib", "scipy"])
        """
        return self.cmd(f"pip install {' '.join(modules)}")  

    def pip_upgrade(self, module: str) -> str:
        """
        Upgrade a specific package to the latest version.
        
        Args:
            module (str): The name of the package to upgrade.
        
        Returns:
            str: Output from the pip upgrade command.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_upgrade("django")
        """
        return self.cmd(f"pip install --upgrade {module}")

    def pip_upgrade_all(self) -> str:
        """
        Upgrade all outdated packages to their latest versions.
        
        This method finds all outdated packages and upgrades them one by one.
        Note: This command uses Linux-style commands (grep, cut, xargs) and
        may not work on Windows without additional tools.
        
        Returns:
            str: Output from the upgrade process.
        
        Note:
            - Uses shell pipeline commands
            - May require Linux environment or Windows Subsystem for Linux (WSL)
            - Consider using pip-review or pip-upgrade as alternatives
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_upgrade_all()
        """
        return self.cmd("pip list --outdated --format=freeze | grep -v '^-e' | cut -d = -f 1 | xargs -n1 pip install -U")

    def pip_uninstall(self, module: str) -> str:
        """
        Uninstall a specific package with automatic confirmation.
        
        Args:
            module (str): The name of the package to uninstall.
        
        Returns:
            str: Output from the pip uninstall command.
        
        Note:
            Uses -y flag for automatic confirmation without user prompts.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_uninstall("old-package")
        """
        return self.cmd(f"pip uninstall -y {module}")

    def pip_uninstalls(self, modules: list[str]) -> str:
        """
        Uninstall multiple Python packages sequentially.
        
        This method iterates through a list of package names and uninstalls
        each one using pip uninstall with automatic confirmation.
        
        Args:
            modules (list[str]): A list of package names to uninstall.
        
        Returns:
            str: A concatenated string containing the output from all
                uninstallation operations. Returns an empty string if
                the modules list is empty.
        
        Note:
            - Uses pip_uninstall() method which includes the -y flag
            for automatic confirmation
            - Uninstalls packages one by one sequentially
            - Continues even if one package fails to uninstall
            - Each uninstallation output is separated by a newline
            
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_uninstalls(["requests", "flask", "numpy"])
            >>> print(result)
            'Found existing installation: requests 2.28.1\\nUninstalling requests-2.28.1:\\n  Successfully uninstalled requests-2.28.1\\nFound existing installation: flask 2.2.2...'
        
        Example with error handling:
            >>> packages = ["package1", "package2", "nonexistent_package"]
            >>> result = pip.pip_uninstalls(packages)
            >>> if "ERROR" in result:
            ...     print("Some packages failed to uninstall")
            ... else:
            ...     print("All packages uninstalled successfully")
        
        Note:
            - This method does not stop on errors; it attempts to uninstall
            all packages in the list regardless of individual failures
            - Consider wrapping in try/except for comprehensive error handling
            - For uninstalling all packages at once, use pip_uninstall_all()
        """
        outputs = []
        for module in modules:
            outputs.append(self.pip_uninstall(module))
        return "\n".join(outputs)

    def pip_uninstall_all(self) -> str:
        """
        Uninstall all installed packages.
        
        Returns:
            str: Output from the pip uninstall command.
        
        Warning:
            This will remove ALL installed packages. Use with caution.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_uninstall_all()
            # Warning: This removes all packages!
        """
        return self.cmd("pip freeze | xargs pip uninstall -y")

    def pip_list(self) -> str:
        """
        List all installed packages.
        
        Returns:
            str: A list of all installed packages with their versions.
        
        Example:
            >>> pip = Pip()
            >>> packages = pip.pip_list()
            >>> print(packages)
            'Package    Version\\n---------- -------\\npip        22.0.4\\nsetuptools 58.1.0...'
        """
        return self.cmd("pip list")

    def pip_outdated(self) -> str:
        """
        List all packages that have newer versions available.
        
        Returns:
            str: A list of outdated packages with current and latest versions.
        
        Example:
            >>> pip = Pip()
            >>> outdated = pip.pip_outdated()
            >>> print(outdated)
            'Package    Version Latest Type\\n---------- ------- ------ ----\\nrequests   2.28.1  2.31.0 wheel\\nflask      2.2.2   2.3.2  wheel'
        """
        return self.cmd("pip list --outdated")

    def pip_info(self, module: str) -> str:
        """
        Get detailed information about a specific package.
        
        This is an alias for show_pip().
        
        Args:
            module (str): The name of the package to get information for.
        
        Returns:
            str: Detailed package information.
        
        Example:
            >>> pip = Pip()
            >>> info = pip.pip_info("numpy")
        """
        return self.cmd(f"pip show {module}")

    def pip_download(self, module: str, dest: str = ".") -> str:
        """
        Download a package distribution without installing it.
        
        Args:
            module (str): The name of the package to download.
            dest (str, optional): Destination directory for the download.
                                 Defaults to current directory (".").
        
        Returns:
            str: Output from the pip download command.
        
        Example:
            >>> pip = Pip()
            >>> pip.pip_download("requests", "./downloads/")
        """
        return self.cmd(f"pip download {module} -d {dest}")

    def pip_freeze_local(self) -> str:
        """
        List installed packages in a format suitable for requirements files.
        
        This method only shows packages installed locally (not from a VCS).
        
        Returns:
            str: Package list in freeze format (package==version).
        
        Example:
            >>> pip = Pip()
            >>> freeze = pip.pip_freeze_local()
            >>> print(freeze)
            'requests==2.28.1\\nflask==2.2.2\\nclick==8.1.3'
        """
        return self.cmd("pip freeze --local")

    def pip_install_editable(self, path: str) -> str:
        """
        Install a package in editable/development mode.
        
        This installs the package from a local directory in development mode,
        allowing changes to the source to be immediately reflected.
        
        Args:
            path (str): The path to the package directory.
        
        Returns:
            str: Output from the editable installation.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_install_editable("./my-package")
        """
        return self.cmd(f"pip install -e {path}")

    def pip_install_requirements(self, filename: str = "requirements.txt") -> str:
        """
        Install all packages from a requirements file.
        
        Args:
            filename (str, optional): The requirements file name.
                                     Defaults to "requirements.txt".
        
        Returns:
            str: Output from the pip installation.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_install_requirements()
            >>> result = pip.pip_install_requirements("dev-requirements.txt")
        """
        return self.cmd(f"pip install -r {filename}")

    def pip_install_constraints(self, filename: str = "constraints.txt") -> str:
        """
        Install packages using a constraints file.
        
        Constraints files are like requirements files but only impose
        version limits without actually installing the packages.
        
        Args:
            filename (str, optional): The constraints file name.
                                     Defaults to "constraints.txt".
        
        Returns:
            str: Output from the pip installation with constraints.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_install_constraints("constraints.txt")
        """
        return self.cmd(f"pip install -c {filename}")

    def pip_check(self) -> str:
        """
        Check for dependency conflicts in the installed packages.
        
        Returns:
            str: A report of any dependency conflicts or compatibility issues.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_check()
            >>> if "No broken requirements found" in result:
            ...     print("All dependencies are satisfied")
            ... else:
            ...     print("Dependency conflicts found!")
        """
        return self.cmd("pip check")

    def pip_cache_info(self) -> str:
        """
        Display information about the pip cache.
        
        Returns:
            str: Information about cache location, size, and usage.
        
        Example:
            >>> pip = Pip()
            >>> info = pip.pip_cache_info()
            >>> print(info)
            'Package index cache: /home/user/.cache/pip\\nSize: 256.3 MB...'
        """
        return self.cmd("pip cache info")

    def pip_cache_purge(self) -> str:
        """
        Clear the pip cache completely.
        
        This removes all cached package distributions and wheels.
        
        Returns:
            str: Output confirming the cache purge operation.
        
        Example:
            >>> pip = Pip()
            >>> result = pip.pip_cache_purge()
            >>> print(result)
            'Files removed: 153\\nDisk space freed: 1.2 GB'
        """
        return self.cmd("pip cache purge")


class Python(Pip):
    """
    A comprehensive Python runtime execution utility class.
    
    This class extends the Pip class to add Python script execution,
    virtual environment management, and Python module execution capabilities.
    
    Features:
        - Python script execution with arguments
        - Virtual environment creation and management
        - Module execution (python -m)
        - Interactive Python shell
        - Code execution from strings (-c flag)
        - Virtual environment integration
    
    Inheritance:
        - Pip: Inherits all pip package management functionality
    """
    
    def run_script(self, script_path: str) -> str:
        """
        Execute a Python script.
        
        Args:
            script_path (str): The path to the Python script to execute.
        
        Returns:
            str: The output from the script execution.
        
        Example:
            >>> py = Python()
            >>> result = py.run_script("./my_script.py")
            >>> print(result)
            'Hello World\\nScript execution complete'
        """
        return self.cmd(f"python {script_path}")
    
    def create_venv(self, name: str = "venv") -> str:
        """
        Create a new Python virtual environment.
        
        Args:
            name (str, optional): The name/directory for the virtual environment.
                                 Defaults to "venv".
        
        Returns:
            str: Output from the virtual environment creation command.
        
        Example:
            >>> py = Python()
            >>> result = py.create_venv()
            >>> result = py.create_venv("myenv")
        """
        return self.cmd(f"python -m venv {name}")  
    
    def run(self, script_path: str, args: str = "") -> str:
        """
        Execute a Python script with optional command-line arguments.
        
        Args:
            script_path (str): The path to the Python script.
            args (str, optional): Command-line arguments to pass to the script.
                                 Defaults to empty string.
        
        Returns:
            str: The output from the script execution.
        
        Example:
            >>> py = Python()
            >>> result = py.run("./script.py", "--verbose --output result.txt")
        """
        return self.cmd(f"python {script_path} {args}")

    def run_module(self, module: str) -> str:
        """
        Execute a Python module using the -m flag.
        
        Args:
            module (str): The module name to execute.
        
        Returns:
            str: The output from the module execution.
        
        Example:
            >>> py = Python()
            >>> # Run the http server module
            >>> result = py.run_module("http.server")
            >>> # Run a custom module
            >>> result = py.run_module("my_package.cli")
        """
        return self.cmd(f"python -m {module}")

    def run_interactive(self) -> str:
        """
        Start an interactive Python interpreter session.
        
        Returns:
            str: The output from starting the interactive Python shell.
        
        Example:
            >>> py = Python()
            >>> py.run_interactive()
            # Opens an interactive Python session
        """
        return self.cmd("python")

    def run_with_venv(self, script_path: str, venv_name: str = "venv") -> str:
        """
        Execute a Python script using a specific virtual environment's Python interpreter.
        
        Args:
            script_path (str): The path to the script to execute.
            venv_name (str, optional): The name of the virtual environment.
                                      Defaults to "venv".
        
        Returns:
            str: The output from the script execution using the venv's Python.
        
        Note:
            This method uses Windows-specific path syntax (\\Scripts\\python).
            For Linux/Mac, the path would be different.
        
        Example:
            >>> py = Python()
            >>> # Run script with default venv
            >>> result = py.run_with_venv("./my_script.py")
            >>> # Run script with custom venv
            >>> result = py.run_with_venv("./my_script.py", "myenv")
        """
        return self.cmd(f"{venv_name}\\Scripts\\python {script_path}")

    def run_code(self, code: str) -> str:
        """
        Execute Python code passed as a string using the -c flag.
        
        Args:
            code (str): The Python code to execute.
        
        Returns:
            str: The output from the code execution.
        
        Example:
            >>> py = Python()
            >>> result = py.run_code("print('Hello World')")
            >>> print(result)
            'Hello World'
            >>> result = py.run_code("import sys; print(sys.version)")
            >>> print(result)
            '3.10.0 (main, Oct 5 2021, 10:45:18)...'
        """
        return self.cmd(f"python -c {code}")
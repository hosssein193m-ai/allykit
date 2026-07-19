"""
Git Version Control Utility Module

This module provides a comprehensive interface for Git version control operations.
It wraps common Git commands into Python methods, making it easy to automate
Git workflows from Python scripts.
"""

from allykit.Automobile_kit.Automobile import Cmd
from time import sleep

class Git(Cmd.cmd):
    """
    A comprehensive Git version control utility class.
    
    This class provides a Pythonic interface to common Git operations including
    cloning, committing, pushing, pulling, branching, and repository management.
    All methods inherit command execution capabilities from the Cmd class.
    
    Features:
        - Repository operations (clone, init, status)
        - Staging and committing (add, commit, amend)
        - Remote operations (push, pull)
        - Branch management (branch, log)
        - File operations (restore, reset)
        - Configuration management (user name, email)
        - History viewing (log, oneline)
    
    Inheritance:
        - Cmd.cmd: Provides command execution capabilities
    """
    
    def clone(self, repo_url: str) -> str:
        """
        Clone a remote Git repository to the local machine.
        
        Args:
            repo_url (str): The URL of the remote repository to clone.
        
        Returns:
            str: Output from the git clone command.
        
        Example:
            >>> git = Git()
            >>> result = git.clone("https://github.com/user/repo.git")
            >>> print(result)
            'Cloning into "repo"...\\nremote: Enumerating objects: 100, done.'
        """
        return self.cmd(f"git clone {repo_url}")

    def status(self) -> str:
        """
        Display the current state of the working directory and staging area.
        
        Returns:
            str: Git status output showing:
                - Untracked files
                - Changes to be committed
                - Changes not staged for commit
                - Branch information
        
        Example:
            >>> git = Git()
            >>> status = git.status()
            >>> print(status)
            'On branch main\\nYour branch is up to date with "origin/main".\\n\\nChanges not staged for commit:\\n  modified:   file.py'
        """
        return self.cmd("git status")

    def commit(self, message: str) -> str:
        """
        Commit staged changes to the repository with a message.
        
        Args:
            message (str): The commit message describing the changes.
        
        Returns:
            str: Output from the git commit command.
        
        Example:
            >>> git = Git()
            >>> result = git.commit("Fix bug in user authentication")
            >>> print(result)
            '[main abcd123] Fix bug in user authentication\\n 1 file changed, 5 insertions(+)'
        """
        return self.cmd(f'git commit -m "{message}"')

    def push(self) -> str:
        """
        Push local commits to the remote repository.
        
        Returns:
            str: Output from the git push command.
        
        Example:
            >>> git = Git()
            >>> result = git.push()
            >>> print(result)
            'Enumerating objects: 5, done.\\nCounting objects: 100% (5/5), done.\\n...'
        """
        return self.cmd("git push")

    def pull(self) -> str:
        """
        Pull and merge changes from the remote repository.
        
        Returns:
            str: Output from the git pull command.
        
        Example:
            >>> git = Git()
            >>> result = git.pull()
            >>> print(result)
            'remote: Enumerating objects: 10, done.\\nUnpacking objects: 100% (10/10), done.\\n...'
        """
        return self.cmd("git pull")

    def branch(self) -> str:
        """
        List all local branches in the repository.
        
        Returns:
            str: A list of local branches with current branch highlighted.
        
        Example:
            >>> git = Git()
            >>> branches = git.branch()
            >>> print(branches)
            '* main\\n  develop\\n  feature-login'
        """
        return self.cmd("git branch")

    def log(self, count: int = 10) -> str:
        """
        Display the commit history with a specified number of entries.
        
        Args:
            count (int, optional): Number of commits to display.
                                  Defaults to 10.
        
        Returns:
            str: The commit history showing commit hashes, authors, dates, and messages.
        
        Example:
            >>> git = Git()
            >>> history = git.log(5)
            >>> print(history)
            'commit abc123 (HEAD -> main)\\nAuthor: John Doe <john@email.com>\\nDate: Mon Jan 1 12:00:00 2024\\n\\n    Initial commit'
        """
        return self.cmd(f"git log -n {count}")    

    def init(self) -> str:
        """
        Initialize a new Git repository in the current directory.
        
        Returns:
            str: Output from the git init command.
        
        Example:
            >>> git = Git()
            >>> result = git.init()
            >>> print(result)
            'Initialized empty Git repository in /path/to/repo/.git/'
        """
        return self.cmd("git init")

    def add(self, namefile: str) -> str:
        """
        Stage a specific file for commit.
        
        Args:
            namefile (str): The name or path of the file to stage.
        
        Returns:
            str: Output from the git add command.
        
        Example:
            >>> git = Git()
            >>> git.add("main.py")
            >>> git.add("src/utils/helper.py")
        """
        return self.cmd(f"git add {namefile}")

    def adds(self) -> str:
        """
        Stage all changes in the current directory for commit.
        
        Returns:
            str: Output from the git add . command.
        
        Example:
            >>> git = Git()
            >>> result = git.adds()
            >>> print(result)
            # Stages all modified and untracked files
        """
        return self.cmd("git add .")

    def restore(self, namefile: str) -> str:
        """
        Restore a file to its last committed state (discard uncommitted changes).
        
        Args:
            namefile (str): The file to restore.
        
        Returns:
            str: Output from the git restore command.
        
        Example:
            >>> git = Git()
            >>> git.restore("broken_file.py")
            # Discards all unstaged changes to broken_file.py
        """
        return self.cmd(f"git restore {namefile}")

    def restore2(self, namefile: str) -> str:
        """
        Unstage a file while keeping the changes in the working directory.
        
        Args:
            namefile (str): The file to unstage.
        
        Returns:
            str: Output from the git restore --staged command.
        
        Example:
            >>> git = Git()
            >>> git.restore2("accidentally_staged.py")
            # Removes from staging but keeps local changes
        """
        return self.cmd(f"git restore --staged {namefile}")

    def reset_hard(self, commit_hash: str) -> str:
        """
        Reset the repository to a specific commit (discard all changes after it).
        
        Args:
            commit_hash (str): The hash or reference of the commit to reset to.
        
        Returns:
            str: Output from the git reset --hard command.
        
        Warning:
            This is a destructive operation that will discard all uncommitted
            changes and commits after the specified hash.
        
        Example:
            >>> git = Git()
            >>> git.reset_hard("abc123")
            # Resets repository to commit abc123, discarding all later changes
        """
        return self.cmd(f"git reset --hard {commit_hash}")

    def reset_file(self, namefile: str) -> str:
        """
        Restore a file to its state in the latest commit (discard unstaged changes).
        
        This is an alias for `git checkout -- <file>`.
        
        Args:
            namefile (str): The file to reset.
        
        Returns:
            str: Output from the git checkout command.
        
        Example:
            >>> git = Git()
            >>> git.reset_file("file.py")
            # Discards all local changes to file.py
        """
        return self.cmd(f"git checkout -- {namefile}")
    
    def oneline(self) -> str:
        """
        Display a condensed one-line per commit commit history.
        
        Returns:
            str: Commit history with each commit on a single line showing
                 commit hash and message.
        
        Example:
            >>> git = Git()
            >>> history = git.oneline()
            >>> print(history)
            'abc123 (HEAD -> main) Initial commit\\ndef456 Add feature X\\nghi789 Fix bug Y'
        """
        return self.cmd("git log --oneline")

    def commit2(self, message: str) -> str:
        """
        Amend the last commit with a new message.
        
        This modifies the most recent commit, replacing its message.
        Use with caution if the commit has already been pushed.
        
        Args:
            message (str): The new commit message.
        
        Returns:
            str: Output from the git commit --amend command.
        
        Example:
            >>> git = Git()
            >>> git.commit2("Updated commit message with more detail")
            # Amends the last commit with a new message
        """
        return self.cmd(f'git commit --amend -m "{message}"')

    def user_name(self, Name: str) -> str:
        """
        Set the global Git user name for all repositories.
        
        Args:
            Name (str): The user name to configure globally.
        
        Returns:
            str: Output from the git config command.
        
        Example:
            >>> git = Git()
            >>> git.user_name("John Doe")
        """
        return self.cmd(f"git config --global user.name {Name}")

    def user_email(self, email: str) -> str:
        """
        Set the global Git user email for all repositories.
        
        Args:
            email (str): The email to configure globally.
        
        Returns:
            str: Output from the git config command.
        
        Example:
            >>> git = Git()
            >>> git.user_email("john.doe@example.com")
        """
        return self.cmd(f"git config --global user.email {email}")

    def user(self, name: str, email: str, time: int = 10) -> str:
        """
        Set both global Git user name and email with a delay between commands.
        
        This method sequentially sets the user name and email, with a
        configurable sleep time between the two operations.
        
        Args:
            name (str): The user name to configure globally.
            email (str): The email to configure globally.
            time (int, optional): Sleep time in seconds between setting
                                 name and email. Defaults to 10 seconds.
        
        Returns:
            str: The output from setting the email (last command executed).
        
        Note:
            - Uses self.user_name() and self.user_email() internally
            - The delay can be useful for systems that need time to process
              the first configuration before accepting the second
        
        Example:
            >>> git = Git()
            >>> git.user("John Doe", "john.doe@example.com", 5)
            # Sets name, waits 5 seconds, then sets email
        """
        self.user_name(name)
        sleep(time)
        self.user_email(email)
__author__ = "Juliana Guamá"
__version__ = "0.1.0"
__all__ = [
]

import typing as tp
import subprocess as sp

from take_blipscore.custom_exceptions import ShellError


def process_run(command: tp.List[str], error_message: str='') -> None:
    """Run shell command.
    
    :param command: Command list.
    :type command: ``list`` from ``str``
    :param error_message: The error message.
    :type: ``str``
    """
    status = sp.run(command, shell=True, capture_output=True)
    if status.returncode != 0:
        raise ShellError(f"Error {status.returncode}:\nerror_message")
    
    
def access_repository(user: str, password: str, repository: str, chdir: str, branch: str="master") -> None:
    """Access repository, change branch and set the work directory.
    
    :param user: User id for repository.
    :type user: ``str``
    :param password: User password for repository.
    :type password: ``str``
    :param repository: Url for http access on repository.
    :type repository: ``str``
    :param chdir: Project work directory on repository.
    :type chdir: ``str``
    :param branch: Repository branch name. Default value is "master".
    :type branch: ``str``
    """
    process_run(command=["git", "clone", repository.format(USER=user, PASS=password)],
                error_message="`git clone` failed.")
    
    process_run(command=["git", "checkout", branch],
                error_message="`git checkout`failed.")
    
    process_run(command=["chdir", chdir],
                error_message="`chdir`failed.")
    
    
    
    
    
    
    
    # 2- change branch
    # 3- change directory
    pass

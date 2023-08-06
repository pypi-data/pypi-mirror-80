"""Command-line interface."""
import functools
from typing import Any
from typing import Callable
from typing import cast
from typing import Tuple
from typing import TypeVar
from typing import Union

import click

import git_portfolio.config_manager as cm
import git_portfolio.github_manager as ghm
import git_portfolio.prompt as p
import git_portfolio.response_objects as res
import git_portfolio.use_cases.config_init_use_case as ci
import git_portfolio.use_cases.config_repos_use_case as cr
import git_portfolio.use_cases.gh_create_issue_use_case as ghci
import git_portfolio.use_cases.gh_create_pr_use_case as ghcp
import git_portfolio.use_cases.gh_delete_branch_use_case as ghdb
import git_portfolio.use_cases.gh_merge_pr_use_case as ghmp
import git_portfolio.use_cases.git_use_case as guc

F = TypeVar("F", bound=Callable[..., Any])
CONFIG_MANAGER = cm.ConfigManager()


def gitp_config_check(func: F) -> F:
    """Validate if there are selected repos and outputs success."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if CONFIG_MANAGER.config_is_empty():
            click.secho(
                "Error: no config found, please run `gitp config init`.",
                fg="red",
            )
        else:
            value = func(*args, **kwargs)
            _echo_outputs(value)
            return value

    return cast(F, wrapper)


@click.group("cli")
def main() -> None:
    """Git Portfolio."""
    pass


def _echo_outputs(response: Union[res.ResponseFailure, res.ResponseSuccess]) -> None:
    if bool(response):
        success = cast(res.ResponseSuccess, response)
        click.secho(success.value)
    else:
        click.secho(f"Error: {response.value['message']}", fg="red")


@main.command("add")
@click.argument("args", nargs=-1)
@gitp_config_check
def add(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git add` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "add", args
    )


@main.command("checkout", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
@gitp_config_check
def checkout(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git checkout` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "checkout", args
    )


@main.command("commit", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
@gitp_config_check
def commit(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git commit` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "commit", args
    )


@main.command("pull")
@click.argument("args", nargs=-1)
@gitp_config_check
def pull(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git pull` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "pull", args
    )


@main.command("push", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
@gitp_config_check
def push(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git push` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "push", args
    )


@main.command("reset", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
@gitp_config_check
def reset(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git reset` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "reset", args
    )


@main.command("status")
@click.argument("args", nargs=-1)
@gitp_config_check
def status(args: Tuple[str]) -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Batch `git status` command."""
    return guc.GitUseCase().execute(
        CONFIG_MANAGER.config.github_selected_repos, "status", args
    )


@click.group("config")
def configure() -> None:
    """Config command group."""
    pass


@click.group("create")
def create() -> None:
    """Create command group."""
    pass


@click.group("merge")
def merge() -> None:
    """Merge command group."""
    pass


# TODO
# @click.group("close")
# def close() -> None:
#     """Close command group."""
#     pass


@click.group("delete")
def delete() -> None:
    """Delete command group."""
    pass


@configure.command("init")
def config_init() -> None:
    """Initialize `gitp` config."""
    github_manager = ghm.GithubManager(CONFIG_MANAGER.config)
    response = ci.ConfigInitUseCase(CONFIG_MANAGER, github_manager).execute()
    _echo_outputs(response)


@configure.command("repos")
@gitp_config_check
def config_repos() -> Union[res.ResponseFailure, res.ResponseSuccess]:
    """Configure current working `gitp` repositories."""
    new_repos = p.new_repos(CONFIG_MANAGER.config.github_selected_repos)
    if not new_repos:
        return res.ResponseSuccess()
    github_manager = ghm.GithubManager(CONFIG_MANAGER.config)
    repo_names = github_manager.get_repo_names()
    selected_repos = p.select_repos(repo_names)
    return cr.ConfigReposUseCase(CONFIG_MANAGER).execute(selected_repos)


@create.command("issues")
def create_issues() -> None:
    """Batch creation of issues on GitHub."""
    manager = ghm.GithubManager(CONFIG_MANAGER.config)
    ghci.GhCreateIssueUseCase(manager).execute()


@create.command("prs")
def create_prs() -> None:
    """Batch creation of pull requests on GitHub."""
    manager = ghm.GithubManager(CONFIG_MANAGER.config)
    ghcp.GhCreatePrUseCase(manager).execute()


@merge.command("prs")
def merge_prs() -> None:
    """Batch merge of pull requests on GitHub."""
    manager = ghm.GithubManager(CONFIG_MANAGER.config)
    ghmp.GhMergePrUseCase(manager).execute()


@delete.command("branches")
def delete_branches() -> None:
    """Batch deletion of branches on GitHub."""
    manager = ghm.GithubManager(CONFIG_MANAGER.config)
    ghdb.GhDeleteBranchUseCase(manager).execute()


main.add_command(configure)
main.add_command(create)
# main.add_command(close)
main.add_command(merge)
main.add_command(delete)


if __name__ == "__main__":
    main(prog_name="gitp")  # pragma: no cover

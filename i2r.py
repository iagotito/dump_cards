#!/usr/bin/env python3
"""Github issues to redmine (issues2redmine)

Usage:
    i2r.py config
    i2r.py issues fetch
    i2r.py test

Options:
    -h --help  Show this screen.
    --version  Show version.
"""
import os

import dotenv
from InquirerPy import inquirer

from modules.docopt import docopt
from modules import github

I2R_DIR_PATH = os.getcwd()
DOTENV_PATH = f"{I2R_DIR_PATH}/.env"

dotenv.load_dotenv(DOTENV_PATH)
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)


def _abort(message):
    print(message)
    exit()


def config():
    try:
        github_access_token = inquirer.secret(
            message=f"Your GitHub access token{' (blank to use current GitHub token)' if GITHUB_ACCESS_TOKEN is not None else ''}: ",
            transformer=lambda _: "[hidden]",
            filter=lambda text: text.replace('\n', ''),
            validate=lambda text: text or GITHUB_ACCESS_TOKEN
        ).execute()
    except KeyboardInterrupt:
        _abort("Operation cancelled.")

    # save the GITHUB_ACCESS_TOKEN now so if there is an error when geting
    # the orgs and projects, you don't have to add the github token again
    if not github_access_token: github_access_token = GITHUB_ACCESS_TOKEN
    dotenv.set_key(dotenv_path=DOTENV_PATH, key_to_set="GITHUB_ACCESS_TOKEN", value_to_set=github_access_token)

    try:
        org_list = github.get_orgs(github_access_token)
    except AssertionError as e:
        _abort(str(e))

    if not org_list:
        print("User isn't a member of any orgs")
        exit()

    try:
        org_login = inquirer.select(
            message=f"Select your organization:",
            choices=org_list
        ).execute()
    except KeyboardInterrupt:
        _abort("Operation cancelled.")

    try:
        projects_dict = github.get_projects(org_login, github_access_token)
    except AssertionError as e:
        _abort(str(e))

    if not projects_dict:
        print("No projects found")
        exit()

    try:
        project_name = inquirer.select(
            message=f"Select your project:",
            choices=list(projects_dict.keys())
        ).execute()
    except KeyboardInterrupt:
        _abort("Operation cancelled.")

    project_id = projects_dict[project_name]

    dotenv.set_key(DOTENV_PATH, "GITHUB_ACCESS_TOKEN", github_access_token)
    dotenv.set_key(DOTENV_PATH, "ORGANIZATION_LOGIN", org_login)
    dotenv.set_key(DOTENV_PATH, "PROJECT_ID", project_id)


def main():
    arguments = docopt(__doc__, version="i2r 0.1")
    if not arguments:
        print(__doc__)

    if arguments.get("config"):
        config()

    if arguments.get("issues"):
        if arguments.get("fetch"):
            print(github.fetch_issues())

    if arguments.get("test"):
        github.test()

if __name__ == "__main__":
    main()

import os

import requests
import dotenv

from i2r import DOTENV_PATH

dotenv.load_dotenv(DOTENV_PATH)

GITHUB_REST_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def get_orgs(token: str) -> list[str]:
    """Get a list of orgs for the authenticated user (from token).

    Args:
        token (str): GitHub API Token

    Returns:
        list of the user's orgs
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(f"{GITHUB_REST_URL}/user/memberships/orgs", headers=headers)
    assert res.status_code == 200, f"Get user's organizations failed by returning status code {res.status_code}: {res.json().get('message')}"

    data = res.json()

    org_list = [org['organization']['login'] for org in data]

    return org_list


def get_projects(org_login:str, token: str) -> dict[str,str]:
    """Get list of all projects(beta) in an org.

    Args:
        org (str): GitHub Organization login
        token (str): GitHub API Token

    Returns:
        dictionary in format {<project_name>: <project_id>}
    """
    headers = {"Authorization": f"Bearer {token}"}
    query = f"""
        query{{
            organization(login: "{org_login}"){{
                projectsNext(first: 10){{
                    nodes{{
                        id
                        title
        }} }} }} }}
    """
    json = {"query": query}

    res = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json=json)
    assert res.status_code == 200, f"Get org's projects failed by returning status code {res.status_code}: {res.json().get('message')}"

    data = res.json()
    assert not "errors" in json.keys(), json.get("message")

    projects = data["data"]["organization"]["projectsNext"]["nodes"]

    projects_dict = {proj["title"]: proj["id"] for proj in projects}

    return projects_dict

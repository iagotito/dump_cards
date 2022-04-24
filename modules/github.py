import os

import requests
import dotenv

from i2r import DOTENV_PATH

dotenv.load_dotenv(DOTENV_PATH)

GITHUB_REST_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)
ORGANIZATION_LOGIN = os.environ.get("ORGANIZATION_LOGIN", None)
PROJECT_ID = os.environ.get("PROJECT_ID", None)
HEADERS = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}


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


def fetch_issues():
    query = f"""
        query{{
            node(id: "{PROJECT_ID}"){{
                ... on ProjectNext {{
                    fields(first: 20){{
                        nodes {{
                            id
                            name
                            settings
        }} }} }} }} }}
    """
    json = {"query": query}

    res = requests.post(GITHUB_GRAPHQL_URL, headers=HEADERS, json=json)
    assert res.status_code == 200, f"Get project's info failed by returning status code {res.status_code}: {res.json().get('message')}"

    data = res.json()
    assert not "errors" in json.keys(), json.get("message")

    results = data["data"]["node"]["fields"]["nodes"]
    for field in results:
        print(field.get("name"))
        print(field.get("settings"))
        print("----")
        print()


def test():
    # getPage = True
    cursor = ""
    # while getPage:
    query = f"""
        query{{
        node(id: "{PROJECT_ID}") {{
            ... on ProjectNext {{
                items(first: 100 {cursor}) {{
                    pageInfo{{
                        hasNextPage endCursor
                    }}
                    nodes{{
                        title
                        fieldValues(first: 100) {{
                            nodes {{
                                value
                            }}
                        }}
                    }}
        }} }} }} }}
    """
    json = {"query": query}
    res = requests.post(GITHUB_GRAPHQL_URL, headers=HEADERS, json=json)
    assert res.status_code == 200, f"Get project's columns cards failed by returning status code {res.status_code}: {res.json().get('message')}"

    data = res.json()
    assert not "errors" in data.keys(), data.get("errors")

    print(data)

                # ... on ProjectNext{{
                    # items(first: 100 {cursor}){{
                        # pageInfo{{
                            # hasNextPage endCursor
                        # }}
                        # nodes{{
                            # title
                            # fieldValues(first: 8){{
                                # nodes{{
                                    # value
                                # }}
                            # }}
                        # content{{
                            # ...on Issue{{
                                # number
                                # labels(first: 50){{
                                    # nodes{{
                                        # name
        # }} }} }} }} }} }} }} }} }}
        # """
        # json = {"query": query}
        # res = requests.post(GITHUB_GRAPHQL_URL, headers=HEADERS, json=json)
        # assert res.status_code == 200, f"Get project's columns cards failed by returning status code {res.status_code}: {res.json().get('message')}"

        # data = res.json()
        # assert not "errors" in data.keys(), data.get("errors")

        # cards = data
        # print(data)
        # getPage = False
        # getPage = json_cards["data"]["node"]["items"]["pageInfo"]["hasNextPage"]

    return 'a'

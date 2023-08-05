"""
    contributors
    ~~~~~~
    get a list of contributors

    :copyright: (c) 2020 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""
import sys

import crayons

import gease.utils as utils
import gease.constants as constants
import gease.exceptions as exceptions
from gease.rest import Api
from gease._version import __version__
from gease.uritemplate import UriTemplate

HELP = """%s. version %s

Usage: %s

Where:
   user/org is the your github username or orgnisation name
   repo is the repository name

Examples:

    contributors pyexcel pyexcel-io
""" % (
    crayons.yellow("contributors list the contributors of a repo"),
    crayons.magenta(__version__, bold=True),
    crayons.yellow("contributors user/org repo", bold=True),
)
REPO_URL = "https://api.github.com/repos{/owner}{/repo}/contributors"


class EndPoint(object):
    """
    Github authenticated user's repo endpoint
    """

    def __init__(self, owner, repo):
        self.__template = UriTemplate(REPO_URL)
        self.__template.owner = owner
        self.__template.repo = repo
        self.__client = Api.get_public_api()

    @property
    def url(self):
        return str(self.__template)

    def get_all_contributors(self):
        json_reply = self.__client.get(self.url)
        contributors = []
        for user in json_reply:
            user_details = self.__client.get(user["url"])
            user_name = user_details["name"]
            if user_name is None:
                user_details["name"] = user["login"]
            contributors.append(user_details)
        return contributors


def main():
    if len(sys.argv) < 3:
        if len(sys.argv) == 2:
            error(constants.NOT_ENOUGH_ARGS)
        print(HELP)
        sys.exit(-1)

    user = sys.argv[1]
    repo = sys.argv[2]
    try:
        repo = EndPoint(user, repo)
        message = repo.get_all_contributors()
        print(message)
    except exceptions.RepoNotFoundError:
        fatal("%s does not exist!" % repo)
    except exceptions.AbnormalGithubResponse as e:
        fatal(str(e))
    except exceptions.NoGeaseConfigFound as e:
        fatal(str(e))
    except KeyError as e:
        fatal("Key %s is not found" % str(e))


def get_default_user():
    return utils.get_info(constants.KEY_GEASE_USER)


def error(message):
    print("Error: %s" % crayons.red(message))


def fatal(message):
    error(message)
    sys.exit(-1)


if __name__ == "__main__":
    main()

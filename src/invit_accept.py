from github import Github
import os


def acceptInvitations():
    g = Github(os.getenv('GITHUB_TOKEN'))
    invits = g.get_user().get_invitations()
    for inv in invits:
        g.get_user().accept_invitation(inv.id)
        print("{} accepted !".format(inv.id))


if __name__ == "__main__":
    acceptInvitations()
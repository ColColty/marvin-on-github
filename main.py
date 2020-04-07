from src.alumns_usernames import getNewUsernames
from src.invit_accept import acceptInvitations
import time
import os


REQUIRED_ENV_VALUES = ['GITHUB_TOKEN', 'EMAIL_USERNAMES', 'EMAIL_USERNAMES_PASSWORD', 'EMAIL_USERNAMES_SMTP_PORT', 'EMAIL_USERNAMES_SMTP_SERVER', 'SUBJECT_EMAIL_USERNAMES', 'DB_USERNAME', 'DB_PASSWORD']


def main():
    for env_val in REQUIRED_ENV_VALUES:
        if not os.getenv(env_val):
            print("Some environment values are remaining...")
            print("The needed env values are:\n\t{}".format('\n\t'.join(REQUIRED_ENV_VALUES)))
            exit(1)
    while 1:
        getNewUsernames()
        acceptInvitations()
        time.sleep(3600)


if __name__ == "__main__":
    main()
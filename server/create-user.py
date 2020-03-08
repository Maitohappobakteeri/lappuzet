from db import session_scope
from services.user import UserService

import sys


def main():
    username = sys.argv[1]
    password = sys.argv[2]
    with session_scope() as session:
        userService = UserService(session)
        userService.createUser(username, password, False)


if __name__ == "__main__":
    main()

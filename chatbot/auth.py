users = {}


def signup(username, password):

    users[username] = password


def login(username, password):

    if username in users:

        if users[username] == password:
            return True

    return False
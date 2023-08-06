class Credentials:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    @classmethod
    def from_event(cls, event):
        credentials = event.get('credentials')
        return cls(credentials['username'], credentials['password'])

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def __eq__(self, other):
        return isinstance(other,
                          Credentials) and other.__username == self.__username and other.__password == self.__password

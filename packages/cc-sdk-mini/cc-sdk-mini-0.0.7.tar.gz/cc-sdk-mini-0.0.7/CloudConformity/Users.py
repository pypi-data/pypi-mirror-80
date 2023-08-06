
class Users:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def CurrentUser(self):
        return self._connection.get(url='/users/whoami')
    def describe(self, id):
        return self._connection.get(url='/users/{id}'.format(id))
    def list(self):
        return self._connection.get(url='/users')
    def invite(self, payload):
        return self._connection.post(url='/users', data=payload)
    def AddSSOUser(self, payload):
        return self._connection.post(url='/users/sso', data=payload)
    def update(self, id, payload):
        return self._connection.patch(url='/users/{id}'.format(id), data=payload)
    def revoke(self, id):
        return self._connection.delete(url='/users/{id}'.format(id))

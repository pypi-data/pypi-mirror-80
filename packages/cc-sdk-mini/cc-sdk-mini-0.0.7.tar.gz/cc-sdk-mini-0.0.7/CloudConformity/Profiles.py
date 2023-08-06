
class Profiles:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def list(self):
        return self._connection.get(url='/profiles')
    def describe(self, id):
        return self._connection.get(url='/profiles/{id}'.format(id=id))
    def create(self, payload):
        return self._connection.post(url='/profiles', data=payload)
    def update(self, id, payload):
        return self._connection.patch(url='/profiles/{id}'.format(id=id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/profiles/{id}'.format(id=id))
    def apply(self, id, payload):
        return self._connection.post(url='/profiles/{id}/apply'.format(id=id), data=payload)
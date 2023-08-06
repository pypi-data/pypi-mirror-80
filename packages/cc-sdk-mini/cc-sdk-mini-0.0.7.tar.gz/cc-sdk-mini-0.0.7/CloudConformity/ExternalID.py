
class ExternalID:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def get(self):
        return self._connection.get(url='/organisation/external-id')
    def create(self, data):
        return self._connection.post(url='/organisation/external-id', payload=None)
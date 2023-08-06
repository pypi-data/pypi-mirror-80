
class TemplateScanner:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def Scan(self, payload):
        return self._connection.post(url='/template-scanner/scan', data=payload)
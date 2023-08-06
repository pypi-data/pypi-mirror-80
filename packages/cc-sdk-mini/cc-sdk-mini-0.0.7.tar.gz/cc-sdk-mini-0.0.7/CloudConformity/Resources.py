
class Resources:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def ExcludedResources(self, excluded=True, accountIDs=None, pageSize=100, pageNumber=None ):
        params = {}
        if excluded:
            params['excluded'] = str(excluded)
        if accountIDs:
            params['accountIds'] = accountIDs
        if pageSize:
            params['page[size]'] = str(pageSize)
        if pageNumber:
            params['page[number]'] = str(pageNumber)
        return self._connection.get(url='/resources', params=params)
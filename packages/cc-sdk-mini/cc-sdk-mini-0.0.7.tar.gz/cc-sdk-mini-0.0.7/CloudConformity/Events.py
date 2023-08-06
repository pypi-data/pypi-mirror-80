
class Events:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def list(self, accountIDs=None,aws=None, cc=None,pageSize=100, pageNumber=None,regions=None, services=None,userIds=None, name=None, identities=None, since=None, until=None):
        params = {}
        if accountIDs:
            params['accountIds'] = accountIDs
        if aws:
            params['aws'] = aws
        if cc:
            params['cc'] = cc
        if pageSize:
            params['page[size]'] = str(pageSize)
        if pageNumber:
            params['page[number]'] = str(pageNumber)
        if regions:
            params['filter[regions]'] = regions
        if services:
            params['filter[services]'] = services
        if userIds:
            params['filter[userIds]'] = userIds
        if name:
            params['filter[name]'] = name
        if identities:
            params['filter[identities]'] = identities
        if since:
            params['filter[since]'] = str(since)
        if until:
            params['filter[until]'] = str(until)
        return self._connection.get(url='/events', params=params)


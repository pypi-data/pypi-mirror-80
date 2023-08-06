
class Checks:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection

    def create(self, payload):
        return self._connection.post(url='/checks', data=payload)

    def update(self, id, payload):
        return self._connection.patch(url='/checks/{id}'.format(id=id), data=payload)

    def list(self, accountIDs, pageSize=100, pageNumber=None, regions=None, services=None, categories=None,
             riskLevels=None, statuses=None, ruleIds=None, suppressedFilterMode=None, suppressed=None, createdDate=None,
             tags=None, compliances=None):
        params = {}
        if accountIDs:
            params['accountIds'] = accountIDs
        if pageSize:
            params['page[size]'] = str(pageSize)
        if pageNumber:
            params['page[number]'] = str(pageNumber)
        if regions:
            params['filter[regions]'] = regions
        if services:
            params['filter[services]'] = services
        if categories:
            params['filter[categories]'] = categories
        if riskLevels:
            params['filter[riskLevels]'] = riskLevels
        if statuses:
            params['filter[statuses]'] = statuses
        if ruleIds:
            params['filter[ruleIds]'] = ruleIds
        if suppressedFilterMode:
            params['filter[suppressedFilterMode]'] = suppressedFilterMode
        if suppressed:
            params['filter[suppressed]'] = suppressed
        if createdDate:
            params['filter[createdDate]'] = str(createdDate)
        if tags:
            params['filter[tags]'] = tags
        if compliances:
            params['filter[compliances]'] = compliances
        return self._connection.get(url='/checks', params=params)

    def describe(self, id):
        return self._connection.get(url='/checks/{id}'.format(id=id))
    def delete(self, id):
        return self._connection.delete(url='/checks/{id}'.format(id=id))

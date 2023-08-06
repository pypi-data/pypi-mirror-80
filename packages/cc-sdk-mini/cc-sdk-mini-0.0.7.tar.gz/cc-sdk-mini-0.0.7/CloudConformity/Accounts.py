
class Accounts:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    def create(self, payload):
        return self._connection.post(url='/accounts', data=payload)
    def list(self):
        return self._connection.get(url='/accounts')
    def detail(self, id):
        return self._connection.get(url='/accounts/{id}'.format(id=id))
    def access(self, id):
        return self._connection.get(url='/accounts/{id}/access'.format(id=id))
    def botSetting(self, id, payload):
        return self._connection.patch(url='/accounts/{id}/settings/bot'.format(id=id), data=payload)
    def scan(self, id, payload):
        return self._connection.post(url='/accounts/{id}/scan'.format(id=id), data=payload)
    def subscription(self, id, payload):
        return self._connection.patch(url='/accounts/{id}/subscription'.format(id=id), data=payload)
    def update(self, id, payload):
        return self._connection.patch(url='/accounts/{id}'.format(id=id), data=payload)
    def ruleSetting(self, id, ruleID, notes=None):
        params = {}
        if notes:
            params['notes'] = notes
        return self._connection.get(url='/accounts/{id}/settings/rules/{ruleID}'.format(id=id, ruleID=ruleID), params=params)
    def updateRuleSetting(self, id, ruleID, payload):
        return self._connection.patch(url='/accounts/{id}/settings/rules/{ruleID}'.format(id=id, ruleID=ruleID), data=payload)
    def ruleSettings(self, id, includeDefaults=None):
        params = {}
        if includeDefaults:
            params['includeDefaults'] = str(includeDefaults)
        return self._connection.get(url='/accounts/{id}/settings/rules'.format(id=id), params=params)
    def updateRuleSettings(self, id, payload):
        return self._connection.patch(url='/accounts/{id}/settings/rules'.format(id=id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/accounts/{id}'.format(id=id))
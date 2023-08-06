from cerberus.requests.BodyRQ import BodyRQ

class QueryRQ(BodyRQ):

    def __init__(self, fields=None, concats=None,conditions=None,unnest=None,limit=None):
        self.__fields = fields
        self.__concats = concats
        self.__conditions= conditions
        self.__unnest= unnest
        self.__limit=limit

    def getFields(self):
        return self.__fields

    def getConcats(self):
        return self.__concats

    def getConditions(self):
        return self.__conditions

    def getUnnest(self):
        return self.__unnest
    
    def getLimit(self):
        return self.__limit

class Datatype():
    def __init__(self, sqltype, tfunc, allow_null=True):
        self.__sqltype = sqltype
        self.__tfunc = tfunc
        self.__allow_null = allow_null

    def sqltype(self):
        if self.__allow_null:
            return self.__sqltype
        else:
            return self.__sqltype + " NOT NULL"

    def parse(self, val):
        return self.__tfunc(val)

    def copy(self, allow_null):
        return Datatype(self.__sqltype, self.__tfunc, allow_null)

    @property
    def allow_null(self):
        return self.__allow_null

from databricksbundle.dbutils.DbUtilsWrapper import DbUtilsWrapper
from databricksbundle.dbutils.IPythonDbUtilsResolver import resolveDbUtils

class NotebookDbUtilsFactory:

    def create(self) -> DbUtilsWrapper:
        return DbUtilsWrapper(resolveDbUtils)

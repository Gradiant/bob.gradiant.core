import os


class DatabasesPathChecker(object):

    def __init__(self):
        pass

    @staticmethod
    def check_if_environment_is_defined_for(database_path):
        environment_varible_is_defined = False
        if database_path in os.environ and os.path.isdir(os.environ[database_path]):
            environment_varible_is_defined = True
        return environment_varible_is_defined

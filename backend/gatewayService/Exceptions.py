class PackageNotFoundException(Exception):
    pass


class ConflictNotResolvedException(Exception):
    pass


class DependencySolvingTimedOutException(Exception):
    pass
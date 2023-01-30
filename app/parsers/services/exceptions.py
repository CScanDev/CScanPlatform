

class CantGetData(Exception):
    """Can't get data due to unknown error"""


class CantFindParser(CantGetData):
    """Parser with given name is not found"""


class CantGetPage(CantGetData):
    """Parser can't get HTML page"""

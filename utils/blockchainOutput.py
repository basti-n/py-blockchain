def printDependingOn(condition: bool, successMsg: str, errorMsg: str) -> None:
    if condition:
        print(successMsg)
    else:
        print(errorMsg)

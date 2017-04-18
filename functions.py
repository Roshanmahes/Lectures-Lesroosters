from csv import *
def read(path):
    """
    Reads csv file from path and returns a list, stripping the first row
    if it contains no digits (if it is a header).
    """
    with open(path, "r", encoding="utf-8") as f:
        result = list(reader(f))

    # strip the first row if it is a header
    if not any(cell.isdigit() for cell in result[0]):
        result = result[1:]

    return result

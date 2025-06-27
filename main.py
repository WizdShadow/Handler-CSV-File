import csv
import re
import argparse
from tabulate import tabulate


def agg(agr: str, spisoc: list, column: list) -> tuple[str, str]:
    if not spisoc:
        return None, "No data"
    v, op = agr.split("=")
    if v not in column:
        return None, "No column"
    spisoc = [o[v] for o in spisoc]
    if op == "max":
        return str(max(spisoc)), op
    elif op == "min":
        return str(min(spisoc)), op
    elif op == "avg":
        if spisoc[0].isdigit():
            return str(sum([int(o) for o in spisoc]) // len(spisoc)), op
        return str(sum([float(o) for o in spisoc]) / len(spisoc)), op
    else:
        return None, "No operator"


def where(args: argparse.Namespace) -> tuple[str, str]:
    if args.file is None:
        return None, "No file or incorrect file path"
    spisoc = []
    with open(args.file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            spisoc.append(row)
    if not spisoc:
        return None, "No data"
    column = [o for o in spisoc[0]]
    if args.where:
        operator = re.sub(r"[^<>=]", "", args.where)
        if operator != "=" and operator != ">" and operator != "<":
            return None, "No operator"
        fil, op = args.where.split(operator)
        if fil not in column:
            return None, "No column"
        for val in spisoc:
            if operator == "=":
                spisoc = [o for o in spisoc if o[fil] == op]
            elif operator == ">":
                spisoc = [o for o in spisoc if o[fil] > op]
            elif operator == "<":
                spisoc = [o for o in spisoc if o[fil] < op]
    if args.aggregate:
        val, colums = agg(args.aggregate, spisoc, column)
        table = [
            [colums],
            [val]
        ]
        return table, None
    else:
        table_data = [[item[key] for key in column] for item in spisoc]
        data = [column] + table_data
        return data, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--where")
    parser.add_argument("--aggregate")
    args = parser.parse_args()
    table, error = where(args)
    if error:
        print(error)
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))

import sys
import json

from .processor import process_file
from .printer import Printer
from .printer_json import JsonPrinter
 

def main(file, cols=1, remove_hyphens=False) -> None:
    output = ''
    # construct json Printer
    printer: Printer = JsonPrinter(remove_hyphens=remove_hyphens)

    def write_if_nonempty(s: str) -> None:
        pass

    write_if_nonempty(printer.begin())

    # iterate over files
    doc = process_file(
        file,
        columns_per_page=cols,
        emit_progress_to=None,
        laparams=None)

    for line in printer.print_file(file.name, doc):
        output += line

    write_if_nonempty(printer.end())
    return json.loads(output)
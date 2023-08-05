from sys import argv

from htmldump import (
    html_dump,
    html_json,
)


html_dump_usage = f'''Usage:
    html_dump {{path}} {{*args}}

    Dumps HTML file

    args:
         tags  : all tags, no data
         data  : data only
        [tags] : tags with data
'''
def do_html_dump():
    try:
        html_dump(*argv[1:])
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_dump_usage)


html_json_usage = f'''Usage:
    html_to_json {{path}}

    Convert HTML to JSON
'''
def do_html_to_json():
    try:
        path = argv[1]
        html_to_json(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_json_usage)


html_tags_usage = f'''Usage:
    html_tags {{path}}

    Dump HTML Tags to JSON
'''
def do_html_tags():
    try:
        path = argv[1]
        html_tags(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_tags_usage)


from json import dump
from pathlib import Path

from htmldump.html_parser import HTML


def html_dump(path, *args):
    cont = open(path).read()
    html = HTML(cont)
    if args:
        if args[0]=='tags':
            html.body.dump_tags()
        elif args[0]=='data':
            html.body.dump_data()
        else:
            tags = set(a.lower() for a in args)
            for node in html.body.walk():
                if node.tag in tags:
                    print(f'\n    [ {node.label} ]')
                    if node.tag=='a':
                        print(node.data or '', node.href)
                    elif node.data:
                        print(node.data)
    else:
        html.body.dump()


def html_json(path):
    path = Path(path)
    cont = open(path).read()
    html = HTML(cont)
    data = html.body.items
    dest = path.with_suffix('.json')
    with open(dest, 'w') as out:
        dump(data, out)


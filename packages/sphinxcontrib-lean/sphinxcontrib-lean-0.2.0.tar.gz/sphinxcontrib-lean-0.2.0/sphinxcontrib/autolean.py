from collections import defaultdict
from pathlib import Path
from textwrap import dedent, indent
import json
import os
import re
import subprocess
import sys


def doc_string(decl):
    return re.sub(
        r"(?ms)\n?```(?P<language>\w*)$(?P<contents>.*)```",
        to_code_block,
        decl["doc_string"],
    )


def to_code_block(markdown):
    return f"\n\n.. code-block:: {markdown['language']}\n" + indent(
        markdown["contents"],
        prefix="    ",
    )


def axiom(decl):
    pass


def constant(decl):
    return f".. constant:: {decl['name']}\n\n" + indent(
        doc_string(decl),
        prefix="    ",
    ) + "\n\n    Fields:\n\n" + indent(
        "\n\n".join(
            structure_field(each) for each in decl["structure_fields"]
        ),
        prefix="        ",
    ) + "\n"


def definition(decl):
    return f".. definition:: {decl['name']}\n\n" + indent(
        doc_string(decl),
        prefix="    ",
    ) + "\n"


def theorem(decl):
    return f".. theorem:: {decl['name']}\n\n" + indent(
        doc_string(decl),
        prefix="    ",
    ) + "\n"


def structure_field(field):
    name, type = field
    return f".. field:: {name}\n"


emitters = {
    "cnst": constant,
    "def": definition,
    "thm": theorem,
}


exported = os.environ.get("SPHINX_EXPORTED_LEAN")
if exported is not None:
    with open(exported) as file:
        contents = json.load(file)
else:
    ran = subprocess.run(
        ["lean", "--run", Path(__file__).parent / "lean" / "export_json.lean"],
        capture_output=True,
    )
    contents = json.loads(ran.stdout)


sys.stdout.write(
    dedent(
        """\
        =============
        API Reference
        =============
        """,
    ),
)

by_filename = defaultdict(list)
for decl in contents["decls"]:
    by_filename[decl["filename"]].append(decl)


# FIXME: I don't see anywhere on module_info (i.e. in export_json.lean)
#        a way to convert module *id to name*, rather than vice versa (i.e.
#        path to dotted name)
def _name_of(path):
    _, _, tail = path.rpartition("src/")
    name, _ = os.path.splitext(tail)
    return name.replace("/", ".")


by_name = sorted((_name_of(k), v) for k, v in by_filename.items())

for module, decls in by_name:
    sys.stdout.write("\n")
    sys.stdout.write("``")
    sys.stdout.write(module)
    sys.stdout.write("``\n")
    sys.stdout.write("-" * (len(module) + 4))
    sys.stdout.write("\n\n")

    sys.stdout.write(".. module:: ")
    sys.stdout.write(module)
    sys.stdout.write("\n\n")

    for each in sorted(decls, key=lambda decl: decl["name"]):
        sys.stdout.write("\n")
        sys.stdout.write(emitters[decl["kind"]](each))

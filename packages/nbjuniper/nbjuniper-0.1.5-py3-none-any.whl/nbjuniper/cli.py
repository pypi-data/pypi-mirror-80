"""Converts notebooks to interactive HTML pages.

Usage:
  nbjuniper NOTEBOOK (-f juniper_settings.yaml)
  nbinteract [options] NOTEBOOKS ...
  nbinteract (-h | --help)

`nbinteract NOTEBOOK ...` converts notebooks into HTML pages.

Arguments:
  NOTEBOOK   IPython notebook to convert.

Options:
  -h --help                  Show this screen.
  -f FILENAME                yaml file containing specific settings for the Juniper client.
                             See https://github.com/ines/juniper for all possibilities.
"""

import json
import yaml
import sys
from markdown import markdown

def main():

    juniper_settings = {
        "url": "https://mybinder.org",
        "repo": "ashtonmv/conda",
        "theme": "callysto",
        "msgLoading": " ",
        "useStorage": True,
        "isolateCells": False
    }

    notebook = None
    for i, arg in enumerate(sys.argv):
        if i == 1:
            with open(arg) as f:
                notebook = json.load(f)

        if arg == "-f":
            with open(sys.argv[i+1]) as f:
                juniper_settings.update(yaml.safe_load(f))

    if notebook is None:
        raise ValueError("Please specify a notebook to convert: nbjuniper example_notebook.ipynb")

    for k, v in juniper_settings.items():
        if type(v) != bool:
            juniper_settings[k] = f"'{v}'"
        else:
            juniper_settings[k] = str(v).lower()

    juniper_json = ", ".join([f"{key}: {value}" for key, value in juniper_settings.items()]) 

    language = notebook["metadata"]["kernelspec"]["language"]

    content = [
        "<script type='text/javascript' src='https://code.jquery.com/jquery-3.5.1.min.js'></script>",
        "<script type='text/javascript' src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/juniper.min.js'></script>",
        "<script type='text/javascript' src='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/events.js'></script>",
        "<script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>"
        "<link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/ashtonmv/nbjuniper/style.css'></link>",
        "<div class='juniper-notebook'>"
    ]

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            content.append("<pre data-executable>")
            content.append("".join(cell["source"]))
            content.append("</pre>")
        else:
            content.append(markdown("".join(cell["source"])))

    content.append("</div>")

    content.append(f"<script>new Juniper({{ {juniper_json} }});</script>")

    with open(sys.argv[1].replace("ipynb", "html"), "w") as o:
        o.write("\n".join(content))

if __name__ == "__main__":
    main()
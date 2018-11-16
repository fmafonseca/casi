"""
This script copies all notebooks from the book into the website directory, and
creates pages which wrap them and link together.

This version was adapted by @fmafonseca from the original version of @jakevdp
"""
import os
import nbformat
import shutil

def abspath_from_here(*args):
    here = os.path.dirname(__file__)
    path = os.path.join(here, *args)
    return os.path.abspath(path)

REPO_NAME = 'casi'
NB_NAME_DIR = 'notebooks'
FIG_NAME_DIR = 'figures'
OUT_NAME_DIR = 'output'

NB_SOURCE_DIR = abspath_from_here('..', NB_NAME_DIR)
FIG_SOURCE_DIR = abspath_from_here('..', NB_NAME_DIR, FIG_NAME_DIR)

NB_DEST_DIR = abspath_from_here(OUT_NAME_DIR)
FIG_DEST_DIR = abspath_from_here(OUT_NAME_DIR, FIG_NAME_DIR)

def convert_notebooks_to_html():
    nblist = sorted(nb for nb in os.listdir(NB_SOURCE_DIR)
                    if nb.endswith('.ipynb'))
    name_map = {nb: nb.rsplit('.', 1)[0].lower() + '.html'
                for nb in nblist}

    if os.path.exists(FIG_DEST_DIR):
        shutil.rmtree(FIG_DEST_DIR)
    shutil.copytree(FIG_SOURCE_DIR, FIG_DEST_DIR)

    figurelist = os.listdir(FIG_DEST_DIR)
    figure_map = {os.path.join(FIG_NAME_DIR, fig): os.path.join('/' + REPO_NAME + '/' + FIG_NAME_DIR, fig)
                  for fig in figurelist}

    for nb in nblist:
        base, ext = os.path.splitext(nb)
        print('-', nb)

        content = nbformat.read(os.path.join(NB_SOURCE_DIR, nb),
                                as_version=4)

        # Replace internal URLs and figure links in notebook
        for cell in content.cells:
            if cell.cell_type == 'markdown':
                for nbname, htmlname in name_map.items():
                    if nbname in cell.source:
                        cell.source = cell.source.replace(nbname, htmlname)
                for figname, newfigname in figure_map.items():
                    if figname in cell.source:
                        cell.source = cell.source.replace(figname, newfigname)

        newnbpath = os.path.join(NB_DEST_DIR, nb)
        nbformat.write(content, newnbpath)

        os.system('jupyter nbconvert "' + newnbpath + '"')
        os.system('del "' + newnbpath + '"')
        htmlfile = base.lower() + '.html'
        os.system('rename "' + NB_DEST_DIR + '\\' + base + '.html" ' + htmlfile)

if __name__ == '__main__':
    #os.system('del / q "' + NB_DEST_DIR + '\\*"')
    convert_notebooks_to_html()

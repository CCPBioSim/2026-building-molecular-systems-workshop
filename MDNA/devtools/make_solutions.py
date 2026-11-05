"""Build solutions/*_solutions.ipynb from the exercise notebooks and the answers in devtools/answers/.

    python devtools/make_solutions.py                  # all notebooks
    python devtools/make_solutions.py 2_build          # only solutions/2_build_solutions.ipynb
    python devtools/make_solutions.py --execute        # also run the solutions, so they show the output
    python devtools/make_solutions.py --list 2_build   # show the cell ids of 2_build.ipynb

devtools/answers/<notebook>.py holds the answers for <notebook>.ipynb, as cells. Each cell starts with a line

    # %% replace <cell id>     the cell replaces the exercise cell with that id
    # %% after <cell id>       the cell is added after that cell (several cells after one id keep their order)

Write `# %% [markdown] replace ...` or `# %% [markdown] after ...` for a markdown cell, and start each line of a
markdown cell with '# '. Text after the cell id is a reminder for the reader and is ignored.

So edit the exercise notebook as usual, put answers in devtools/answers/, and run this script. With --execute
the notebooks run in a temporary folder (with data/ and devtools/), so the files they write do not end
up in the repository.

The solutions notebooks are in their own folder, but data/ and devtools/ are in the main folder. So a
solutions notebook that uses mdna starts with a cell that moves to the main folder.
"""
import argparse
import hashlib
import re
import shutil
import tempfile
from pathlib import Path

import nbformat

ROOT = Path(__file__).parent.parent
ANSWERS = Path(__file__).parent / 'answers'
SOLUTIONS = ROOT / 'solutions'
TO_MAIN_FOLDER = """# The solutions are in the solutions/ folder: run them from the main folder, where data/ and devtools/ are
import os
if os.path.basename(os.getcwd()) == 'solutions':
    os.chdir('..')"""
HEADER = re.compile(r'# %%(?: \[(markdown)\])? (replace|after) (\S+)')


def read_answers(path):
    """List of (action, cell id, cell type, source) from an answers file."""
    answers = []
    for line in path.read_text().splitlines():
        header = HEADER.match(line)
        if header:
            cell_type = header.group(1) or 'code'
            answers.append([header.group(2), header.group(3), cell_type, []])
        elif answers:
            answers[-1][3].append(line)

    for answer in answers:
        lines = answer[3]
        while lines and not lines[-1].strip():
            lines.pop()
        if answer[2] == 'markdown':
            lines = [line[2:] if line.startswith('# ') else line.lstrip('#') for line in lines]
        answer[3] = '\n'.join(lines)
    return answers


def make_solutions(name):
    notebook = nbformat.read(ROOT / f'{name}.ipynb', as_version=4)
    cells = notebook.cells
    ids = {cell.id for cell in cells}
    last_added = {}  # cell id -> id of the last cell added after it

    for action, cell_id, cell_type, source in read_answers(ANSWERS / f'{name}.py'):
        position = [cell.id for cell in cells].index(cell_id) if cell_id in ids else None
        if position is None:
            raise SystemExit(f'devtools/answers/{name}.py: {name}.ipynb has no cell with id {cell_id}')

        new = nbformat.v4.new_markdown_cell(source) if cell_type == 'markdown' else nbformat.v4.new_code_cell(source)
        if action == 'replace':
            new.id = cell_id
            cells[position] = new
        else:
            anchor = last_added.get(cell_id, cell_id)
            # a fixed id for every added cell, so that rebuilding does not change the notebook
            new.id = hashlib.sha1(f'{name} {anchor}'.encode()).hexdigest()[:8]
            cells.insert([cell.id for cell in cells].index(anchor) + 1, new)
            last_added[cell_id] = new.id

    code = [cell for cell in cells if cell.cell_type == 'code']
    if any('import mdna' in cell.source for cell in code):
        to_main_folder = nbformat.v4.new_code_cell(TO_MAIN_FOLDER)
        to_main_folder.id = hashlib.sha1(f'{name} main folder'.encode()).hexdigest()[:8]
        cells.insert(cells.index(code[0]), to_main_folder)
    return notebook


def execute(notebook):
    from nbclient import NotebookClient

    with tempfile.TemporaryDirectory() as folder:
        (Path(folder) / 'data').symlink_to(ROOT / 'data', target_is_directory=True)
        shutil.copytree(ROOT / 'devtools', Path(folder) / 'devtools', ignore=shutil.ignore_patterns('answers', '__pycache__'))
        NotebookClient(notebook, timeout=None, resources={'metadata': {'path': folder}}).execute()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('notebooks', nargs='*', help='names without .ipynb, for example 2_build (default: all)')
    parser.add_argument('--execute', action='store_true', help='run the solutions notebooks')
    parser.add_argument('--list', action='store_true', help='print the cell ids of the exercise notebooks')
    args = parser.parse_args()
    names = args.notebooks or sorted(path.stem for path in ANSWERS.glob('*.py'))

    for name in names:
        if args.list:
            for cell in nbformat.read(ROOT / f'{name}.ipynb', as_version=4).cells:
                first_line = cell.source.strip().split('\n')[0]
                print(f'{cell.id}  {cell.cell_type:8}  {first_line[:70]}')
            continue
        notebook = make_solutions(name)
        if args.execute:
            print(f'running {name}_solutions.ipynb')
            execute(notebook)
        nbformat.write(notebook, SOLUTIONS / f'{name}_solutions.ipynb')
        print(f'wrote solutions/{name}_solutions.ipynb')


if __name__ == '__main__':
    main()

# Computational Physics 2026/27

Lecture notes and code examples for the CIS Computational Physics course at the
University of Hamburg.

## Repository layout

Course material is organized by chapter, using names such as `01_intro`.

- `code/templates/<chapter>/`: clean notebooks distributed through Git
- `code/workspace/<chapter>/`: personal working copies, ignored by Git
- `data/`: local datasets, ignored by Git
- `notes/`: local lecture-note sources and PDFs, ignored by Git

Lecture notes are distributed separately through the university platform.

## Setup

Using a standard Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
python -m pip install -r requirements.txt
```

Alternatively, using Conda:

```bash
conda env create -f environment.yml
conda activate physics_course
```

## Create your workspace

Run the synchronization script from anywhere:

```bash
python sync_workspace.py
```

It copies template notebooks into `code/workspace/` and adds `_RUN` to their
names. For example, `01_intro/plot_function.ipynb` becomes
`01_intro/plot_function_RUN.ipynb`. Existing `_RUN.ipynb` files are never
overwritten, so rerunning the command is safe. If the teacher's template
changes, the script creates `plot_function_UPDATE.ipynb` beside the working
copy. Students can compare the two files and merge the changes they need.

The `_UPDATE.ipynb` file is disposable: later template changes replace it.
Rename it before editing if you want to preserve that version.

Each notebook reports one of three statuses:

- `created`: first workspace copy
- `skipped`: the template has not changed
- `created update`: the disposable update was created
- `replaced update`: the disposable update was replaced with a newer template

Start Jupyter and open the notebook from `code/workspace/01_intro/`:

```bash
jupyter notebook
```

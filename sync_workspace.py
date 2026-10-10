"""Copy course notebooks into a student's protected workspace."""

from pathlib import Path
import shutil


REPOSITORY_ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = REPOSITORY_ROOT / "code" / "templates"
WORKSPACE_DIR = REPOSITORY_ROOT / "code" / "workspace"


def files_match(first: Path, second: Path) -> bool:
    """Compare two files efficiently."""
    if first.stat().st_size != second.stat().st_size:
        return False

    with first.open("rb") as first_file, second.open("rb") as second_file:
        while True:
            first_chunk = first_file.read(1024 * 1024)
            second_chunk = second_file.read(1024 * 1024)
            if first_chunk != second_chunk:
                return False
            if not first_chunk:
                return True


def replace_file(source: Path, destination: Path) -> None:
    """Replace a disposable update using an atomic rename."""
    temporary_file = destination.with_suffix(destination.suffix + ".tmp")
    shutil.copy2(source, temporary_file)
    temporary_file.replace(destination)


def sync_workspace() -> None:
    """Mirror template folders and copy new notebooks without overwriting work."""
    if not TEMPLATE_DIR.is_dir():
        raise FileNotFoundError(f"Template directory not found: {TEMPLATE_DIR}")

    for template_folder in sorted(
        path for path in TEMPLATE_DIR.rglob("*") if path.is_dir()
    ):
        relative_folder = template_folder.relative_to(TEMPLATE_DIR)
        (WORKSPACE_DIR / relative_folder).mkdir(parents=True, exist_ok=True)

    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    for source in sorted(TEMPLATE_DIR.rglob("*.ipynb")):
        relative_source = source.relative_to(TEMPLATE_DIR)
        run_notebook = (
            WORKSPACE_DIR
            / relative_source.parent
            / f"{source.stem}_RUN.ipynb"
        )
        update_notebook = (
            WORKSPACE_DIR
            / relative_source.parent
            / f"{source.stem}_UPDATE.ipynb"
        )
        run_notebook.parent.mkdir(parents=True, exist_ok=True)

        if not run_notebook.exists():
            shutil.copy2(source, run_notebook)
            print(f"{run_notebook.relative_to(WORKSPACE_DIR)}: created")
            continue

        if not update_notebook.exists():
            if files_match(source, run_notebook):
                print(f"{run_notebook.relative_to(WORKSPACE_DIR)}: skipped")
            else:
                shutil.copy2(source, update_notebook)
                print(
                    f"{update_notebook.relative_to(WORKSPACE_DIR)}: "
                    "created update"
                )
            continue

        if files_match(source, update_notebook):
            print(f"{update_notebook.relative_to(WORKSPACE_DIR)}: skipped")
            continue

        replace_file(source, update_notebook)
        print(
            f"{update_notebook.relative_to(WORKSPACE_DIR)}: replaced update"
        )


if __name__ == "__main__":
    sync_workspace()

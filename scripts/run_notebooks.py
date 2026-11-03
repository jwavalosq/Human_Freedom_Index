"""Execute every notebook in notebooks/ in place, with nbconvert.

Run from the project root:
    python3 scripts/run_notebooks.py

Or, with the virtual environment used for this build:
    ~/.venv_hfi/bin/python scripts/run_notebooks.py

The script stops on the first notebook that fails, and then
prints a check of every notebook for error outputs. A notebook
counts as clean only if it has no output with output_type
equal to "error" and no traceback in any cell.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def check_notebook(path):
    with open(path, encoding="utf-8") as handle:
        nb = json.load(handle)
    errors = []
    for index, cell in enumerate(nb.get("cells", [])):
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                errors.append((index, output.get("ename", "error")))
            text = ""
            if isinstance(output.get("text"), list):
                text = "".join(output["text"])
            elif isinstance(output.get("text"), str):
                text = output["text"]
            if "Traceback" in text:
                errors.append((index, "traceback in text output"))
    return errors


def main():
    notebooks = sorted(NB_DIR.glob("*.ipynb"))
    if not notebooks:
        print("No notebooks found in", NB_DIR)
        sys.exit(1)
    for path in notebooks:
        print(f"Executing {path.name} ...")
        result = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert",
             "--to", "notebook", "--execute", "--inplace",
             "--ExecutePreprocessor.timeout=600",
             str(path)],
            cwd=NB_DIR, capture_output=True, text=True)
        print(result.stdout[-2000:] if result.stdout else "")
        if result.returncode != 0:
            print(result.stderr[-4000:])
            print(f"FAILED: {path.name}")
            sys.exit(1)
        print(f"  done: {path.name}")
    print()
    print("Error check:")
    failed = False
    for path in notebooks:
        errors = check_notebook(path)
        if errors:
            failed = True
            print(f"  {path.name}: ERRORS {errors}")
        else:
            print(f"  {path.name}: clean, zero error outputs")
    if failed:
        sys.exit(1)
    print("All notebooks executed with zero cell errors.")


if __name__ == "__main__":
    main()

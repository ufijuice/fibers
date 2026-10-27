"""Build the current presentation without leaving LaTeX intermediates beside it."""

from pathlib import Path
import shutil
import subprocess
import sys

from preseed_budget import generate


ROOT = Path(__file__).resolve().parent
DOCUMENTS = ("photonic_npu_preseed", "photonic_npu_one_pager")


def main():
    generate()
    if "--budget-only" in sys.argv:
        return
    compiler = shutil.which("pdflatex")
    if not compiler:
        raise SystemExit("pdflatex is required; the budget has been generated.")
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    for name in DOCUMENTS:
        for _ in range(2):
            try:
                result = subprocess.run(
                    [compiler, "-interaction=nonstopmode", "-halt-on-error",
                     "-file-line-error", "-output-directory=build", name + ".tex"],
                    cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, timeout=120,
                )
            except subprocess.TimeoutExpired:
                raise SystemExit(
                    "pdflatex timed out. Check access to the TeX installation's "
                    "font/package caches and any pending package prompt."
                ) from None
            if result.returncode:
                print("\n".join(result.stdout.splitlines()[-60:]), file=sys.stderr)
                raise SystemExit(result.returncode)
        shutil.copy2(build / (name + ".pdf"), ROOT / (name + ".pdf"))
        print("Built " + str(ROOT / (name + ".pdf")))


if __name__ == "__main__":
    main()

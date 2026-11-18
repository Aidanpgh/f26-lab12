# Setup

You need Python, a virtual environment, and four tools from
`requirements-dev.txt`.

## 1. Python

Python 3.11 or newer. Check with:

```
python3 --version
```

If you are below 3.11, install a current release from python.org or through
your package manager.

## 2. Virtual environment

From this directory:

```
python3 -m venv .venv
source .venv/bin/activate
```

On Windows the activate line is `.venv\Scripts\activate` instead. The prompt
picks up a `(.venv)` prefix once it works. `.venv/` is gitignored.

Every command below assumes the environment is active. If a command reports
that `pytest` or `ruff` is missing, the environment is not active.

## 3. Install the tools

```
pip install -r requirements-dev.txt
```

That is pytest, ruff, mypy, and pip-audit at exact pinned versions, so your machine and
everyone else's run the same checks and get the same results.

The service itself needs no install. `pyproject.toml` sets
`pythonpath = ["."]`, so pytest imports `refunds` straight from this directory.

## 4. Run the tests

```
pytest
```

All 18 tests should pass. If they fail before you have touched
anything, the problem is your environment. Go back to step 2.

## 5. ruff, mypy, and pip-audit

`requirements-dev.txt` also installed ruff, mypy, and pip-audit. ruff and mypy
are configured in `pyproject.toml`. The lab handout tells you when to use all
three. You do not need
to run them to finish setup.

## 6. Editor

Any editor works. VS Code with the Python extension will pick up `.venv`
automatically once you open this folder as the project root. Point it at the
interpreter in `.venv/bin/python` if it does not. Whatever you use, run the
commands above in a terminal to check.

# flake8: noqa

template = {
    "__desc": "a new-style Python project",
    "README.md": """
# {{name}}

{{description}}

This project uses [poetry](https://python-poetry.org/). Install that, then run
the tests with:

```bash

  poetry install
  poetry run task checks

```
""",
    "pyproject.toml": """[tool.poetry]
name = "{{name}}"
version = "0.0.1"
description = ""
authors = [{{author}}]

[tool.poetry.dependencies]
python = "^3.6"
typing-extensions = "^3.7.4"

[tool.poetry.dev-dependencies]
black = "^19.10b0"
coverage = "^4.5.2"
flake8 = "^3.7.9"
flake8-bugbear = "^19.8.0"
mypy = "^0.761"
pytest = "^5.2"
taskipy = "^1.3.0"

[tool.black]
line-length = 80
target-version = ['py36', 'py37', 'py38']
include = '\.pyi?$'
exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.pytest]
testpaths = [ '{{snake_case_name}}', 'tests' ]

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"

[tool.taskipy.tasks]
black = "black {{snake_case_name}} tests"
flake8 = "flake8  --extend-ignore=E203,E501 {{snake_case_name}} tests"
mypy = "mypy {{snake_case_name}} tests"
tests = "PYTHONPATH=. pytest -vv"
checks = 'task black && task flake8 && task mypy && task tests'

[tool.poetry.scripts]
{{snake_case_name}} = "{{snake_case_name}}.cli:main"

""",
    "mypy.ini": """
[mypy]
python_version=3.6

check_untyped_defs=True
disallow_any_generics=True
disallow_untyped_calls=True
disallow_untyped_defs=True
follow_imports=normal
strict_optional=True
warn_no_return=True
warn_redundant_casts=True
warn_return_any=True
warn_unused_ignores=True
""",
    ".gitignore": """
.mypy_cache
.pytest_cache
__pycache__
dist/*
{{ name }}.egg-info/*
""",
    "{{snake_case_name}}/__init__.py": "",
    "{{snake_case_name}}/cli.py": """import argparse


def cli() -> None:
    parser = argparse.ArgumentParser(description="{{description_escape_quotes}}")
    parser.add_argument("words", type=str, help="words to echo back")
    args = parser.parse_args()

    print(args.words)

""",
    "tests/test_{{snake_case_name}}.py": """def test_example() -> None:
    assert 4 == 2 + 2

""",
}

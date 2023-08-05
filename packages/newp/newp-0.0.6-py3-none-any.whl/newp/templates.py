import typing as t

import jinja2
from . import naming
from .projects.cpp import template as cpp
from .projects.javascript import template as javascript
from .projects.python import template as python


ProjectTemplate = t.Dict[str, str]
Options = t.NamedTuple(
    "Options", [("type", str), ("name", str), ("description", str)],
)

projects = {"cpp": cpp, "javascript": javascript, "python": python}


def get_list() -> t.List[t.Tuple[str, str]]:
    return [(name, value["__desc"]) for name, value in projects.items()]


class MissingTemplate(BaseException):
    pass


def _load(name: str) -> ProjectTemplate:
    if name not in projects:
        raise MissingTemplate()
    return projects[name]


def _evaluate(options: Options, template: ProjectTemplate) -> t.Dict[str, str]:
    jinja_args = {
        "name": options.name,
        "description": options.description,
        "camel_case_name": naming.camel_case(options.name),
        "kebab_case_name": naming.kebab_case(options.name),
        "pascal_case_name": naming.pascal_case(options.name),
        "scream_case_name": naming.scream_case(options.name),
        "snake_case_name": naming.snake_case(options.name),
    }

    result: t.Dict[str, str] = {}

    for file_name, content in template.items():
        if file_name == "__desc":
            continue
        new_file_name = jinja2.Template(file_name).render(**jinja_args)
        new_content = jinja2.Template(content).render(**jinja_args)
        result[new_file_name] = new_content

    return result


def render(options: Options) -> t.Dict[str, str]:
    template = _load(options.type)
    files = _evaluate(options, template)
    return files

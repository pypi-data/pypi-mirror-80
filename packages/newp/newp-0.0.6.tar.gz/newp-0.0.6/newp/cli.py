import argparse
import pathlib
import sys

from newp import templates


def show_list() -> None:
    for name, desc in templates.get_list():
        print(name)
        print("\t" + desc)
        print()


def create(options: templates.Options, directory: pathlib.Path) -> None:
    abd = directory.absolute()
    if not abd.parent.exists():
        print(f"Could not find parent directory for {directory}.")
        sys.exit(1)

    try:
        files = templates.render(options)
    except templates.MissingTemplate:
        print(f'Error: No template found with name "{options.name}"')
        sys.exit(1)
    for file_name, content in files.items():
        full_path = abd / file_name
        parent = full_path.parent
        parent.mkdir(parents=True, exist_ok=True)
        with open(abd / file_name, "w") as f:
            f.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Creates a new project")
    subparsers = parser.add_subparsers(help="command")
    list_p = subparsers.add_parser("list", help="List project types")
    list_p.set_defaults(list="list")
    create_p = subparsers.add_parser("create", help="Create a new project")
    create_p.set_defaults(create=True)
    create_p.add_argument("template", type=str, help="type of project")
    create_p.add_argument("name", type=str, help="name of new project")
    create_p.add_argument(
        "--description", type=str, help="Description", required=True
    )
    create_p.add_argument(
        "--directory",
        type=str,
        help="directory (defaults to a new directory named after project)",
    )

    p_args = parser.parse_args()

    if hasattr(p_args, "list"):
        show_list()
    elif hasattr(p_args, "create"):
        create(
            templates.Options(
                p_args.template, p_args.name, p_args.description,
            ),
            pathlib.Path(p_args.directory or p_args.name),
        )
    else:
        print("Missing command argument.")
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

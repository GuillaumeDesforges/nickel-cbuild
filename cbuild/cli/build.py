import pathlib
import subprocess
import sys
import pydantic

import click

from cbuild.recipe import Recipe
from .cli import cli, echo


class RecipeJson(pydantic.BaseModel):
    name: str
    system: str
    executable: str
    args: list[str]


@cli.command()
@click.argument("field", type=str)
def build(field: str):
    cwd = pathlib.Path(".")
    cbuild_file = cwd / "cbuild.ncl"
    nickel_result = subprocess.run(
        [
            "nickel",
            "export",
            "--field",
            field,
            str(cbuild_file),
        ],
        capture_output=True,
    )
    if nickel_result.returncode != 0:
        echo("Nickel evaluation failed.")
        echo("Failed with error:\n")
        echo(nickel_result.stderr.decode())
        echo("Debug you Nickel expression with:")
        echo("")
        echo("    " + " ".join(nickel_result.args))
        echo("")
        sys.exit(1)
    echo("Recipe:")
    recipe_json = nickel_result.stdout.decode()
    echo(recipe_json)
    echo("Building recipe.")
    parsed_recipe_json = RecipeJson.model_validate_json(recipe_json)
    recipe = Recipe(
        name=parsed_recipe_json.name,
        system=parsed_recipe_json.system,
        executable=parsed_recipe_json.executable,
        args=parsed_recipe_json.args,
    )

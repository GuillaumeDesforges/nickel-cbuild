from cbuild.recipe import Recipe
import docker


def build(
    recipe: Recipe,
    docker_client: docker.DockerClient,
    builder_image: str,
    store: Store,
):
    """
    Build a recipe.
    """
    # run recipe's executable in a container
    container = docker_client.containers.run(
        builder_image,
        command=[recipe.executable] + recipe.args,
        mounts=[
            docker.types.Mount(
                target="/build",
                source=recipe.source_dir,
                type="bind",
            ),
    )

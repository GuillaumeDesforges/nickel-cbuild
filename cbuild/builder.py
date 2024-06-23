from cbuild.recipe import Recipe
import pwd
import grp
import os
import hashlib
import docker.types
import subprocess


class Store:
    def __init__(
        self,
        store_path="/cbuild/store",
        user="cbuild",
    ) -> None:
        self.store_path = store_path
        self.user = user
        self._create_store()

    def _create_user(self):
        try:
            grp.getgrnam(self.user)
        except KeyError:
            groupadd_result = subprocess.run(
                ["groupadd", ...]  # TODO: add group
            )

        try:
            pwd.getpwnam(self.user)
        except KeyError:
            useradd_result = subprocess.run(
                ["useradd", ...]  # TODO: add user
            )
            useradd_result.check_returncode()

    def _create_store(self):
        if not os.path.exists(self.store_path):
            mkdir_result = subprocess.run(
                ["sudo", "mkdir", "-p", self.store_path],
            )
            mkdir_result.check_returncode()
            chown_result = subprocess.run(
                ["sudo", "chown", f"{self.user}:{self.user}", self.store_path],
            )
            chown_result.check_returncode()

    def get_output_path(
        self,
        recipe: Recipe,
    ) -> str:
        recipe_hash = hashlib.sha256(repr(recipe).encode()).hexdigest()
        return f"{self.store_path}/{recipe_hash}-{recipe.name}"


def build_recipe(
    recipe: Recipe,
    docker_client: docker.DockerClient,
    builder_image: str,
    store: Store,
):
    """
    Build a recipe.
    """
    output_path = store.get_output_path(recipe)

    # run recipe's executable in a container
    container = docker_client.containers.create(
        builder_image,
        # command=[recipe.executable] + recipe.args,
        mounts=[],
        environment={
            "out": output_path,
        },
        tty=True,
        detach=True,
    )
    container.start()
    container.exec_run(cmd=[recipe.executable] + recipe.args)
    container.stop()

    # copy result to store
    with open(output_path, "w") as f:
        raw_stream_chunks, archive_stats = container.get_archive(output_path)
        for chunk in raw_stream_chunks:
            f.write(chunk)

    container.remove()

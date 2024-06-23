from cbuild.recipe import Recipe
import docker.types
import grp
import hashlib
import logging
import os
import pwd
import subprocess


class UnixUser:
    """
    Context manager to temporarily change the UID and GID of the current process.
    """

    def __init__(self, uid: int, gid: int | None = None):
        self.uid = uid
        self.gid = gid

    def __enter__(self):
        self.main_uid, self.main_gid = os.getuid(), os.getgid()
        if self.gid is not None:
            os.setgid(self.gid)
        os.setuid(self.uid)

    def __exit__(self, *_):
        os.setuid(self.main_uid)
        os.setgid(self.main_gid)


class Store:
    def __init__(
        self,
        store_path="/cbuild/store",
        user="cbuild",
    ) -> None:
        """
        A store to store outputs of built recipes.

        Args:
            store_path: Path to store outputs.
            user: User to own the store.
        """
        self.store_path = store_path
        self.user = user
        self._create_user()
        self._create_store()

    def _create_user(self):
        """
        Create the cbuild user and group if they don't exist.
        """
        # create group if it doesn't exist
        try:
            grp.getgrnam(self.user)
        except KeyError:
            logging.info(f"Creating group {self.user}")
            groupadd_result = subprocess.run(["sudo", "groupadd", self.user])
            groupadd_result.check_returncode()
        # create user if it doesn't exist
        try:
            pwd.getpwnam(self.user)
        except KeyError:
            logging.info(f"Creating group {self.user}")
            useradd_result = subprocess.run(["sudo", "useradd", self.user])
            useradd_result.check_returncode()

    def in_store_user(self):
        return UnixUser(
            pwd.getpwnam(self.user).pw_uid,
            grp.getgrnam(self.user).gr_gid,
        )

    def _create_store(self):
        """
        Create the store directory if it doesn't exist.
        """
        if os.path.exists(self.store_path):
            return

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
        """
        Get the output path for a recipe.

        The output path is in the form of `{store_path}/{recipe_hash}-{recipe_name}`.

        Args:
            recipe: Recipe to get the output path for.
        """
        recipe_hash = hashlib.sha256(repr(recipe).encode()).hexdigest()
        return f"{self.store_path}/{recipe_hash}-{recipe.name}"


def build_recipe(
    recipe: Recipe,
    docker_client: docker.DockerClient,
    builder_image: str,
    store: Store,
):
    """
    Build a recipe in a container and copy the result to the store.

    Args:
        recipe: Recipe to build.
        docker_client: Docker client to use.
        builder_image: Image to use for building.
        store: Store to copy the result to.
    """
    output_path = store.get_output_path(recipe)

    # run recipe's executable in a container
    container = docker_client.containers.create(
        builder_image,
        mounts=[],
        environment={
            "out": output_path,
        },
        tty=True,
        detach=True,
    )
    container.start()
    container.exec_run(cmd=["mkdir", output_path])
    container.exec_run(cmd=[recipe.executable] + recipe.args)
    container.stop()

    # copy result to store
    with store.in_store_user():
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            raw_stream_chunks, archive_stats = container.get_archive(output_path)
            for chunk in raw_stream_chunks:
                f.write(chunk)

    container.remove()

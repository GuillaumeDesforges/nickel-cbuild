import shutil
import pathlib
import httpx
import tarfile
from .cli import cli, echo

TARBALL_URL = (
    "https://api.github.com/repos/GuillaumeDesforges/nickel-cbuild/tarball/master"
)


@cli.command()
def init():
    echo("Initializing project.")
    cbuild_dir = pathlib.Path(".cbuild")
    cbuild_dir.mkdir(parents=True, exist_ok=True)
    cbuild_cache_dir = cbuild_dir / "cache"
    cbuild_cache_dir.mkdir(parents=True, exist_ok=True)
    echo("Copying Nickel lib.")
    # fetch from github to .cbuild
    cached_tarball = cbuild_cache_dir / "nickel-cbuild.tar.gz"
    if not cached_tarball.exists():
        echo(f"Downloading {TARBALL_URL} to {cached_tarball}.")
        tarball_request = httpx.get(TARBALL_URL, follow_redirects=True)
        cached_tarball.write_bytes(tarball_request.content)
    with tarfile.open(cached_tarball) as cbuild_tarball:
        cbuild_tarball_root = cbuild_tarball.getmembers()[0].path
        cbuild_tarball.extractall(
            path=cbuild_cache_dir,
            filter="data",
        )
    cbuild_nickel_dir = cbuild_dir / "nickel"
    echo(f"Copying Nickel code to {cbuild_nickel_dir}")
    shutil.copytree(
        src=cbuild_cache_dir / cbuild_tarball_root / "nickel",
        dst=cbuild_nickel_dir,
        dirs_exist_ok=True,
    )

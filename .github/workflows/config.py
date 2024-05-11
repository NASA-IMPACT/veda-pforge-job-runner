import argparse
import hashlib
import pathlib
import subprocess
import tempfile
import os

from contextlib import contextmanager
from venvception import venv
from pathlib import Path
from typing import Generator
from repo2docker import contentproviders
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def hash_requirements(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()


def zip_site_packages(env_root_path: pathlib.Path, requirements_hash_digest):
    user_site_dir = env_root_path / 'lib' / 'python3.10' / 'site-packages'
    user_site_dir = str(user_site_dir)
    logger.debug(f"User site-packages directory: {user_site_dir}")
    os.chdir(user_site_dir)
    result = subprocess.run(["ls", "-lah"], capture_output=True, text=True)
    logger.info(f"site-packages: stderr={result.stderr.strip()} stdout={result.stdout.strip()}")

    gh_actions_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    zip_path = os.path.join(gh_actions_folder, f"site-packages-{requirements_hash_digest}.zip")
    zip_command = ["zip", "-r", zip_path, "."]
    result = subprocess.run(zip_command, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("Successfully zipped the directory")
    else:
        logger.info(f"Failed to zip the directory: stderr={result.stderr.strip()} stdout={result.stdout.strip()}")


@contextmanager
def checkout(repo: str, ref:str) -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as checkout_dir:
        cp = contentproviders.Git()
        spec = cp.detect(repo, ref=ref)
        if spec is None:
            raise ValueError(
                f"Could not fetch {repo}, content provider detection failed"
            )

        logger.info(
            "Picked {cp} content "
            "provider.\n".format(cp=cp.__class__.__name__),
            extra={"status": "fetching"},
        )
        for log_line in cp.fetch(
            spec, checkout_dir, yield_output=True
        ):
            logger.info(log_line, extra=dict(status="fetching"))

        yield checkout_dir


def main(repo: str, ref: str, feedstock_subdir: str) -> None:
    with checkout(repo, ref) as checkout_dir:
        requirements_path = Path(checkout_dir) / feedstock_subdir / "requirements.txt"
        digest = hash_requirements(str(requirements_path))
        with venv(requirements_path) as env_path:
            # in the `venv` context manager, all dynamic recipe requirements should
            # be installed in an activated virtualenv.
            # Here, we check that all dependencies are available and
            # alert if deps in requirements.txt are missing things
            from importlib.metadata import distributions

            deps_set = {"pangeo-forge-recipes", "fsspec", "apache-beam"}
            dist_set = {d.metadata["Name"] for d in distributions()}
            missing_deps = deps_set - dist_set
            if missing_deps:
                raise ValueError(
                    f"The packages {missing_deps} must be listed in your recipe's requirements.txt"
                )
            zip_site_packages(env_path, digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some strings.")
    # NOTE: these are positional args
    parser.add_argument('repo', type=str,
                        help='The repository URL or path')
    parser.add_argument('ref', type=str,
                        help='The reference in the repository, such as a branch or tag')
    parser.add_argument('feedstock_subdir', type=str,
                        help='The subdirectory within the repository related to the feedstock')
    args = parser.parse_args()
    main(args.repo, args.ref, args.feedstock_subdir)

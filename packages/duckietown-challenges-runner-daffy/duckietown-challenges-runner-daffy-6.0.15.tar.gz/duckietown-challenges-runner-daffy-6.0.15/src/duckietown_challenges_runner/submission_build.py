# coding=utf-8
import subprocess

from duckietown_challenges import get_important_env_build_args

from . import logger


def build_image(client, path: str, tag: str, dockerfile: str, no_build: bool, no_cache: bool = False):
    if not no_build:
        cmd = ["docker", "build", "--pull", "-t", tag, "-f", dockerfile]
        if no_cache:
            cmd.append("--no-cache")
        with open(dockerfile) as _:
            df_contents = _.read()

        cmd.extend(get_important_env_build_args(df_contents))

        cmd.append(path)

        logger.info("running command", cmd=cmd)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            logger.error(f"Cannot run command", cmd=cmd, stderr=e.stderr)
            raise

    image = client.images.get(tag)
    return image

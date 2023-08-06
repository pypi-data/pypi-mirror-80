# coding=utf-8
import os
import subprocess
from . import logger


def build_image(client, path: str, tag: str, dockerfile: str, no_build: bool, no_cache: bool = False):
    if not no_build:
        cmd = ["docker", "build", "--pull", "-t", tag, "-f", dockerfile]
        if no_cache:
            cmd.append("--no-cache")
        with open(dockerfile) as _:
            contents = _.read()
        vnames = ["AIDO_REGISTRY", "PIP_INDEX_URL"]
        for vname in vnames:
            if vname in contents:
                value = os.environ.get(vname)
                cmd.extend(["--build-arg", f"{vname}={value}"])
        cmd.append(path)

        logger.info("running command", cmd=cmd)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            logger.error(f"Cannot run command", cmd=cmd, stderr=e.stderr)
            raise

    image = client.images.get(tag)
    return image

# coding=utf-8
__version__ = "6.0.1"

import sys

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)

enc = sys.getdefaultencoding()
from docker import __version__ as docker_version
from requests import __version__ as requests_version

vmsg = (
    f"dt-challenges-runner {__version__} - encoding {enc} docker_py {docker_version} requests "
    f"{requests_version}"
)
logger.info(vmsg)
from .runner import dt_challenges_evaluator

from .runner_local import runner_local_main

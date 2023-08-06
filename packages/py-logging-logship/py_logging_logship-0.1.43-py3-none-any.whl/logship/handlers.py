# -*- coding: utf-8 -*-

import logging
import warnings
import unpaddedbase64
import json

from logging.handlers import QueueHandler
from logging.handlers import QueueListener
from queue import Queue
from typing import Dict
from typing import Optional
from typing import Type

from logship import const
from logship import emitter

import logging
logging.getLogger("urllib3").setLevel(logging.INFO)

class LokiQueueHandler(QueueHandler):
    """This handler automatically creates listener and `Handler` to handle logs queue."""

    def __init__(self, queue: Queue, **kwargs):
        """Create new logger handler with the specified queue and kwargs for the `Handler`."""
        super().__init__(queue)
        self.handler = Handler(**kwargs)  # noqa: WPS110
        self.listener = QueueListener(self.queue, self.handler)
        self.listener.start()


class Handler(logging.Handler):
    """
    Log handler that sends log records to Loki.

    `Loki API <https://github.com/grafana/loki/blob/master/docs/api.md>`_
    """

    emitters: Dict[str, Type[emitter.LokiEmitter]] = {
        "0": emitter.LokiEmitterV0,
        "1": emitter.LokiEmitterV1,
    }

    def __init__(
        self,
        api_key: str,
        # url: str,
        # auth: Optional[emitter.BasicAuth] = None,
        tags: Optional[dict] = None,
        version: Optional[str] = None,
    ):
        """
        Create new Loki logging handler.

        Arguments:
            url: Endpoint used to send log entries to Loki (e.g. `https://my-loki-instance/loki/api/v1/push`).
            tags: Default tags added to every log record.
            auth: Optional tuple with username and password for basic HTTP authentication.
            version: Version of Loki emitter to use.

        """
        super().__init__()

        tenant = None
        json_key = json.loads(unpaddedbase64.decode_base64(api_key).decode("ascii"))
        if not json_key['internal']:
            url = f"https://{json_key['tenant']}.logship.io/loki/api/v1/push"
        else:
            url = f"http://distributor.ls-global/loki/api/v1/push"
            tenant = {json_key['tenant']}

        auth = ('logship', api_key)

        if version is None and const.emitter_ver == "0":
            msg = (
                "Loki /api/prom/push endpoint is in the depreciation process starting from version 0.4.0.",
                "Explicitly set the emitter version to '0' if you want to use the old endpoint.",
                "Or specify '1' if you have Loki version> = 0.4.0.",
                "When the old API is removed from Loki, the handler will use the new version by default.",
            )
            warnings.warn(" ".join(msg), DeprecationWarning)

        version = version or const.emitter_ver
        if version not in self.emitters:
            raise ValueError("Unknown emitter version: {0}".format(version))
        self.emitter = self.emitters[version](url, tags, auth, tenant=tenant)

    def handleError(self, record):  # noqa: N802
        """Close emitter and let default handler take actions on error."""
        self.emitter.close()
        super().handleError(record)

    def emit(self, record: logging.LogRecord):
        """Send log record to Loki."""
        # noinspection PyBroadException
        try:
            self.emitter(record, self.format(record))
        except Exception:
            self.handleError(record)

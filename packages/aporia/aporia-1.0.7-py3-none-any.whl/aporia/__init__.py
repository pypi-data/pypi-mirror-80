"""Aporia SDK.

Usage:
    >>> import aporia
    >>> aporia.init(
    >>>     token='12345',
    >>>     host='production.myorg.cloud.aporia.com',
    >>>     port=443,
    >>>     environment="production"
    >>> )
    >>> model = aporia.Model(model_name='my-model'], model_version='v1')
    >>> model.set_features(feature_names=['x1', 'x2', 'x3'], categorical=['x2'])
    >>> model.log_predict(x=[1.3, 0.7, 0.2], y=[0.09])
"""
import atexit
from contextlib import suppress
import logging
import sys
from typing import Optional

from aporia.consts import LOG_FORMAT, LOGGER_NAME
from aporia.errors import handle_error
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient
from aporia.model import Model

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


__all__ = ["init", "flush", "Model"]


class Context:
    """Global context."""

    def __init__(
        self,
        graphql_client: GraphQLClient,
        event_loop: EventLoop,
        environment: str,
        debug: bool,
        throw_errors: bool,
        timeout: int,
    ):
        """Initializes the context.

        Args:
            graphql_client (GraphQLClient): GraphQL client.
            event_loop (EventLoop): Event loop.
            environment (str): Environment aporia is running in.
            debug (bool): True if debug logs and stack traces should be displayed.
            throw_errors (bool): True if errors should be raised as exceptions.
            timeout (int): Timeout for blocking API calls.
        """
        self.graphql_client = graphql_client
        self.event_loop = event_loop
        self.environment = environment
        self.debug = debug
        self.throw_errors = throw_errors
        self.timeout = timeout


context: Optional[Context] = None
logger = logging.getLogger(LOGGER_NAME)


def init(
    token: str,
    host: str,
    environment: str,
    port: int = 443,
    debug: bool = False,
    throw_errors: bool = False,
    blocking_call_timeout: int = 3,
):
    """Initializes the Aporia SDK.

    Args:
        token (str): Authentication token.
        host (str): Controller host.
        environment (str): Environment in which aporia is initialized (e.g production, staging).
        port (int): Controller port. Defaults to 443.
        debug (bool): True to enable debug mode - this will cause additional logs
            and stack traces during exceptions. Defaults to False.
        throw_errors (bool): True to cause errors to be raised as exceptions. Defaults to False.
        blocking_call_timeout (int): Timout, in seconds, for blocking aporia API
            calls - Model(), set_features(), add_parameter(), add_metric().
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, style="{"))
    logger.addHandler(handler)

    logger.debug("Initializing Aporia SDK.")

    try:
        # Init graphql client and event loop
        event_loop = EventLoop()
        graphql_client = GraphQLClient(token=token, host=host, port=port)
        event_loop.run_coroutine(graphql_client.open())

        global context
        context = Context(
            graphql_client=graphql_client,
            event_loop=event_loop,
            environment=environment.strip().lower(),
            debug=debug,
            throw_errors=throw_errors,
            timeout=blocking_call_timeout,
        )

        atexit.register(shutdown)
        logger.debug("Aporia SDK initialized.")
    except Exception as err:
        handle_error(
            message=f"Initializing Aporia SDK failed, error: {str(err)}",
            add_trace=debug,
            raise_exception=throw_errors,
            original_exception=err,
        )


def flush():
    """Waits for all of the prediction logs to reach the controller."""
    if context is None:
        logger.error("Flush failed, Aporia SDK was not initialized.")
        return

    logger.debug("Flushing remaining data")
    context.event_loop.flush()


def shutdown():
    """Shuts down the Aporia SDK.

    Notes:
        * It is advised to call flush() before calling shutdown(), to ensure that
          all of the data that was sent reaches the controller.
    """
    with suppress(Exception):
        global context
        if context is not None:
            context.event_loop.run_coroutine(context.graphql_client.close())
            context = None

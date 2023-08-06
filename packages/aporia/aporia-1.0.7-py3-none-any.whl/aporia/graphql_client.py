import logging

import aiohttp
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError

logger = logging.getLogger(LOGGER_NAME)


QUERY_MAX_ATTEMPTS = 4
QUERY_TIMEOUT = 10
QUERY_RETRY_INITIAL_SLEEP = 2
DEFAULT_TIMEOUT_SEC = 300


class GraphQLClient:
    """Asynchronous graphql client."""

    def __init__(self, token: str, host: str, port: int):
        """Initialize a GraphQLClient instance.

        Args:
            token (str): Authorization token
            host (str): Controller address
            port (int): Controller port
        """
        logger.debug("Initializing GraphQL client.")
        if not host.startswith("http"):
            host = f"https://{host}"

        self.request_url = f"{host}:{port}/v1/controller/graphql"
        self.headers = {"Authorization": f"Bearer {token}"}
        self.session: aiohttp.ClientSession = None  # type: ignore

    async def open(self):
        """Opens the http session.

        Notes:
            * This must be executed in the event loop
        """
        logger.debug("Creating HTTP session with controller.")
        self.session = aiohttp.ClientSession(headers=self.headers)

    @retry(
        stop=stop_after_attempt(QUERY_MAX_ATTEMPTS),
        wait=wait_exponential(min=QUERY_RETRY_INITIAL_SLEEP),
        retry=retry_if_exception(lambda err: not isinstance(err, AporiaError)),
        reraise=True,
    )
    async def query_with_retries(
        self, query: str, variables: dict, timeout: int = DEFAULT_TIMEOUT_SEC
    ) -> dict:
        """Executes a GraphQL query with retries in case of failure.

        Args:
            query (str): GraphQL query string
            variables (dict): Variables for the query
            timeout (int): Timeout for the entire request, in seconds. Defaults to 5 minutes.

        Returns:
            dict: GraphQL query result
        """
        return await self.query(query, variables, timeout)

    async def query(self, query: str, variables: dict, timeout: int = DEFAULT_TIMEOUT_SEC) -> dict:
        """Executes a GraphQL query and returns the result.

        Args:
            query (str): GraphQL query string
            variables (dict): Variables for the query
            timeout (int): Timeout for the entire request, in seconds. Defaults to 5 minutes.

        Returns:
            dict: GraphQL query result
        """
        logger.debug(f"Sending GraphQL query: {query}, variables: {variables}")
        # Note: By default, aiohttp uses SSL and verifies the certificate in HTTPS requests
        async with self.session.post(
            url=self.request_url,
            json={"query": query, "variables": variables},
            timeout=aiohttp.ClientTimeout(total=timeout),
        ) as response:

            if response.status != 200:
                if response.status == 400:
                    errors = (await response.json())["errors"]  # type: ignore
                    raise AporiaError(f"Server Error: {errors[0]['message']}")

                elif response.status == 401:
                    raise AporiaError("Authentication failed, please check your token.")

                else:
                    raise AporiaError(f"Unexpected HTTP error {response.status}")

            return (await response.json())["data"]  # type: ignore

    async def close(self):
        """Closes the http session."""
        await self.session.close()

from datetime import datetime
import logging
from typing import Any, cast, Dict, List, Optional, Union

import aporia
from aporia.api.log_json import log_json
from aporia.api.log_predict import is_valid_predict_input, log_predict_batch
from aporia.api.model_setup import (
    add_extra_inputs,
    add_extra_outputs,
    check_model_exists,
    set_features,
)
from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError, handle_error
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient

logger = logging.getLogger(LOGGER_NAME)
FeatureValue = Union[float, int, bool, str]


class BaseModel:
    """Base class for Model objects."""

    def __init__(
        self,
        model_id: str,
        model_version: str,
        environment: Optional[str],
        graphql_client: Optional[GraphQLClient],
        event_loop: Optional[EventLoop],
        debug: bool,
        throw_errors: bool,
        timeout: Optional[int],
    ):
        """Initializes a BaseModel object.

        Args:
            model_id (str): Model identifier
            model_version (str): Model version
            environment (str): Environment's name
            graphql_client (Optional[GraphQLClient]): GraphQL client
            event_loop (Optional[EventLoop]): AsyncIO event loop
            debug (bool): True to enable debug mode
            throw_errors (bool): True to raise exceptions in object creation and set_features
            timeout (Optional[int]): Timeout, in seconds, for synchronous functions
        """
        logger.debug(f"Initializing model object for model {model_id} version {model_version}")
        self.model_id = model_id
        self.model_version = model_version
        self._environment = cast(str, environment)
        self._graphql_client = cast(GraphQLClient, graphql_client)
        self._event_loop = cast(EventLoop, event_loop)
        self._debug = debug
        self._throw_errors = throw_errors
        self._model_ready = False
        self._model_version_exists = False
        self._timeout = cast(int, timeout)

        # Check model existence
        if event_loop is not None and graphql_client is not None:
            self._check_model_existence()

        if not self._model_ready:
            logger.error("Model object initialization failed - model operations will not work.")

    def _check_model_existence(self):
        logger.debug(
            f"Checking if model {self.model_id} version {self.model_version} already exists."
        )
        try:
            model_exists, model_version_exists = self._event_loop.run_coroutine(
                check_model_exists(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    timeout=self._timeout,
                )
            )

            if not model_exists:
                raise AporiaError(f"Model {self.model_id} does not exist.")

            self._model_version_exists = model_version_exists
            self._model_ready = True

        except Exception as err:
            handle_error(
                message=f"Creating model object failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def set_features(
        self, feature_names: List[str], categorical: Optional[List[Union[int, str]]] = None,
    ):
        """Sets feature names and categorical features for the model.

        Args:
            feature_names (List[str]): List of feature names
            categorical (List[Union[int, str]], optional): A list indicating which of the
                features in the 'feature_names' argument are considered categorical.
        """
        if not self._model_ready:
            return

        logger.debug("Setting model features.")
        try:
            self._event_loop.run_coroutine(
                set_features(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    feature_names=feature_names,
                    categorical_features=categorical,
                    timeout=self._timeout,
                )
            )

            # If the query didn't fail, then the model version should now exist in the DB
            self._model_version_exists = True
        except Exception as err:
            handle_error(
                message=f"Setting features for {self.model_id} failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def add_extra_inputs(self, extra_inputs: Dict[str, str]):
        """Adds extra inputs to the model, which can then be reported in log_predict.

        Args:
            extra_inputs (Dict[str, str]): A mapping of input_name: input_type. type must
                be one of the following: 'numeric', 'categorical', 'boolean', 'string'.
        """
        if not self._model_ready:
            return

        logger.debug("Adding extra inputs")
        try:
            self._event_loop.run_coroutine(
                add_extra_inputs(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    extra_inputs=extra_inputs,
                    timeout=self._timeout,
                )
            )
        except Exception as err:
            handle_error(
                message=f"Adding extra inputs failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def add_extra_outputs(self, extra_outputs: Dict[str, str]):
        """Adds extra outputs to the model, which can then be reported in log_predict.

        Args:
            extra_outputs (Dict[str, str]): A mapping of output_name: output_type. type
                must be one of the following: 'numeric', 'categorical', 'boolean', 'string'.
        """
        if not self._model_ready:
            return

        logger.debug("Adding extra outputs")
        try:
            self._event_loop.run_coroutine(
                add_extra_outputs(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    extra_outputs=extra_outputs,
                    timeout=self._timeout,
                )
            )
        except Exception as err:
            handle_error(
                message=f"Adding extra outputs failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def log_predict(
        self,
        x: List[FeatureValue],
        y: List[float],
        confidence: Optional[List[float]] = None,
        occurred_at: Optional[datetime] = None,
        extra_inputs: Optional[Dict[str, FeatureValue]] = None,
        extra_outputs: Optional[Dict[str, FeatureValue]] = None,
    ):
        """Logs a single prediction.

        Args:
            x (List[FeatureValue]): X values for all of the features in the prediction
            y (List[float]): Prediction result
            confidence (List[float], optional): Prediction confidence. Defaults to None.
            occurred_at (datetime, optional): Prediction timestamp. Defaults to None.
            extra_inputs (Dict[str, FeatureValue], optional): Extra inputs, each input
                value must be a single bool, int, float or string. Defaults to None.
            extra_outputs (Dict[str, FeatureValue], optional): Extra outputs, each output
                value must be a single bool, int, float or string. Defaults to None.

        Notes:
            * The features reported in the x parameter must be set with the set_features
              method before logging predictions.
            * Extra inputs and outputs should be defined with add_extra_inputs or
              add_extra_outputsbefore they are passed to log_predict.
            * Many libraries provide a way to convert their objects to lists:
                * numpy array: Use data.tolist()
                * pandas dataframe: Use data.values.tolist()
                * scipy sparse matrix: Use data.toarray().tolist()
        """
        self.log_predict_batch(
            x=[x],
            y=[y],
            confidence=None if confidence is None else [confidence],
            occurred_at=occurred_at,
            extra_inputs=None if extra_inputs is None else [extra_inputs],
            extra_outputs=None if extra_outputs is None else [extra_outputs],
        )

    def log_predict_batch(
        self,
        x: List[List[FeatureValue]],
        y: List[List[float]],
        confidence: Optional[List[List[float]]] = None,
        occurred_at: Optional[datetime] = None,
        extra_inputs: Optional[List[Dict[str, FeatureValue]]] = None,
        extra_outputs: Optional[List[Dict[str, FeatureValue]]] = None,
    ):
        """Logs multiple predictions.

        Args:
            x (List[List[FeatureValue]]): X values for all of the features in each of the predictions
            y (List[List[float]]): Predictions results for each prediction
            confidence (List[List[float]], optional): Confidence for each prediction. Defaults to None.
            occurred_at (datetime, optional): Timestamp for each prediction. Defaults to datetime.now().
            extra_inputs (List[Dict[str, FeatureValue]], optional): Extra inputs for each prediction, each
                element in the list should a dict mapping the input name to its value, which
                can be bool, int, float or string. Defaults to None.
            extra_outputs (List[Dict[str, FeatureValue]], optional): Extra outputs for each prediction, each
                element in the list should a dict mapping the output name to its value, which
                can be bool, int, float or string. Defaults to None.

        Notes:
            * The features reported in the x parameter must be set with the set_features
              method before logging predictions.
            * Extra inputs and outputs should be defined with add_extra_inputs or
              add_extra_outputsbefore they are passed to log_predict_batch.
            * Many libraries provide a way to convert their objects to lists:
                * numpy array: Use data.tolist()
                * pandas dataframe: Use data.values.tolist()
                * scipy sparse matrix: Use data.toarray().tolist()
        """
        if not self._model_ready:
            return

        if not self._model_version_exists:
            logger.warning(
                "Logging prediction failed: features for this model version were not reported."
            )
            return

        logger.debug(f"Logging {len(y)} predictions")
        try:
            if not is_valid_predict_input(
                x=x,
                y=y,
                confidence=confidence,
                extra_inputs=extra_inputs,
                extra_outputs=extra_outputs,
            ):
                logger.warning("Logging prediction failed: Invalid input.")
                return

            self._event_loop.run_coroutine(
                coro=self._log_predict_batch(
                    x=x,
                    y=y,
                    confidence=confidence,
                    occurred_at=occurred_at,
                    extra_inputs=extra_inputs,
                    extra_outputs=extra_outputs,
                ),
                await_result=False,
            )
        except Exception as err:
            handle_error(
                message=f"Logging prediction batch failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO,
            )

    async def _log_predict_batch(
        self,
        x: List[List[FeatureValue]],
        y: List[List[float]],
        confidence: Optional[List[List[float]]] = None,
        occurred_at: Optional[datetime] = None,
        extra_inputs: Optional[List[Dict[str, FeatureValue]]] = None,
        extra_outputs: Optional[List[Dict[str, FeatureValue]]] = None,
    ):
        try:
            await log_predict_batch(
                graphql_client=self._graphql_client,
                model_id=self.model_id,
                model_version=self.model_version,
                environment=self._environment,
                x=x,
                y=y,
                confidence=confidence,
                occurred_at=occurred_at,
                extra_inputs=extra_inputs,
                extra_outputs=extra_outputs,
            )
        except Exception as err:
            handle_error(
                message=f"Logging prediction failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO,
            )

    def log_json(self, data: Any):
        """Logs arbitrary data.

        Args:
            data (Any): Data to log, must be JSON serializable
        """
        if not self._model_ready:
            return

        logger.debug(f"Logging arbitrary data.")
        try:
            self._event_loop.run_coroutine(
                coro=self._log_json(data=data), await_result=False,
            )
        except Exception as err:
            handle_error(
                message=f"Logging arbitrary data failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO,
            )

    async def _log_json(self, data: Any):
        try:
            await log_json(
                graphql_client=self._graphql_client,
                model_id=self.model_id,
                model_version=self.model_version,
                environment=self._environment,
                data=data,
            )
        except Exception as err:
            handle_error(
                message=f"Logging arbitrary data failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO,
            )


class Model(BaseModel):
    """Model object."""

    def __init__(self, model_id: str, model_version: str):
        """Initializes a Model object.

        Args:
            model_id (str): Model identifier, as received from the Aporia dashboard.
            model_version (str): Model version - this can be any string that represents the model
                version, such as "v1" or a git commit hash.
        """
        if aporia.context is None:
            logger.error("Aporia was not initialized.")
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=None,
                environment=None,
                event_loop=None,
                debug=False,
                throw_errors=False,
                timeout=None,
            )
        else:
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=aporia.context.graphql_client,
                event_loop=aporia.context.event_loop,
                environment=aporia.context.environment,
                debug=aporia.context.debug,
                throw_errors=aporia.context.throw_errors,
                timeout=aporia.context.timeout,
            )

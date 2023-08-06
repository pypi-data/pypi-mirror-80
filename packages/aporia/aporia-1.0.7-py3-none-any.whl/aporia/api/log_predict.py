from datetime import datetime
import logging
from typing import Dict, List, Optional, Union

from aporia.consts import LOGGER_NAME
from aporia.graphql_client import GraphQLClient

logger = logging.getLogger(LOGGER_NAME)


FeatureValue = Union[float, int, bool, str]


async def log_predict_batch(
    graphql_client: GraphQLClient,
    model_id: str,
    model_version: str,
    environment: str,
    x: List[List[FeatureValue]],
    y: List[List[float]],
    confidence: Optional[List[List[float]]] = None,
    occurred_at: Optional[datetime] = None,
    extra_inputs: Optional[List[Dict[str, FeatureValue]]] = None,
    extra_outputs: Optional[List[Dict[str, FeatureValue]]] = None,
):
    """Reports a batch of predictions.

    Args:
        graphql_client (GraphQLClient): GraphQL client
        model_id (str): Model ID
        model_version (str): Model version
        environment (str): Environment in which aporia is running.
        x (List[List[FeatureValue]]): Feature values
        y (List[List[float]]): Prediction result
        confidence (List[List[float]], optional): Prediction confidence. Defaults to None.
        occurred_at (datetime, optional): Prediction timestamp. Defaults to None.
        extra_inputs (List[Dict[str, FeatureValue]], optional): Extra inputs. Defaults to None.
        extra_outputs (List[Dict[str, FeatureValue]], optional): Extra outputs. Defaults to None.
    """
    query = """
        mutation LogPredict(
            $modelId: String!,
            $modelVersion: String!,
            $x: [[FeatureValue]]!,
            $yPred: [[Float]]!,
            $confidence: [[Float]],
            $occurredAt: String,
            $environment: String!,
            $extraInputs: [[ExtraInputValue]]
            $extraOutputs: [[ExtraOutputValue]]
        ) {
            logPredictions(
                modelId: $modelId,
                modelVersion: $modelVersion,
                x: $x,
                yPred: $yPred,
                confidence: $confidence,
                occurredAt: $occurredAt,
                environment: $environment,
                extraInputs: $extraInputs
                extraOutputs: $extraOutputs
            ) {
                warnings
            }
        }
    """

    variables = {
        "modelId": model_id,
        "modelVersion": model_version,
        "x": x,
        "yPred": y,
        "confidence": confidence,
        "occurredAt": None if occurred_at is None else occurred_at.isoformat(),
        "environment": environment,
        "extraInputs": _build_extra_io_values(extra_inputs),
        "extraOutputs": _build_extra_io_values(extra_outputs),
    }

    result = await graphql_client.query_with_retries(query, variables)
    for warning in result["logPredictions"]["warnings"]:
        logger.warning(warning)


def _build_extra_io_values(
    data: Optional[List[Dict[str, FeatureValue]]] = None
) -> Optional[List[List[dict]]]:
    if data is None:
        return None

    result = []
    for data_point in data:
        result.append([{"name": name, "value": value} for name, value in data_point.items()])

    return result


def is_valid_predict_input(
    x: List[List[FeatureValue]],
    y: List[List[float]],
    confidence: Optional[List[List[float]]] = None,
    extra_inputs: Optional[List[Dict[str, FeatureValue]]] = None,
    extra_outputs: Optional[List[Dict[str, FeatureValue]]] = None,
) -> bool:
    """Checks if log_predict_batch input is valid.

    Args:
        x (List[List[FeatureValue]]): Feature values
        y (List[List[float]]): Prediction result
        confidence (List[List[float]], optional): Prediction confidence. Defaults to None.
        extra_inputs (List[Dict[str, FeatureValue]], optional): Extra inputs. Defaults to None.
        extra_outputs (List[Dict[str, FeatureValue]], optional): Extra outputs. Defaults to None.

    Returns:
        bool: True if all of the parameters are valid. False otherwise
    """
    if not _is_valid_predict_param_list(x):
        logger.debug("Invalid input format for x parameter")
        return False

    if not _is_valid_predict_param_list(y):
        logger.debug("Invalid input format for y parameter")
        return False

    if len(x) != len(y):
        logger.debug("Invalid input: x and y should have identical length")
        return False

    if confidence is not None:
        if not _is_valid_predict_param_list(confidence):
            logger.debug("Invalid input format for confidence parameter")
            return False

        if len(y) != len(confidence):
            logger.debug("Invalid input: y and confidence should have identical length")
            return False

    if extra_inputs is not None:
        if not _is_valid_extra_io(data=extra_inputs, expected_length=len(x)):
            logger.debug(
                "Invalid input: extra_inputs must be a list of values equal in length to the "
                "number of predictions, such that each element in the list is a dict "
                "containing the extra inputs for a single prediction"
            )
            return False

    if extra_outputs is not None:
        if not _is_valid_extra_io(data=extra_outputs, expected_length=len(x)):
            logger.debug(
                "Invalid input: extra_outputs must be a list of values equal in length to the "
                "number of predictions, such that each element in the list is a dict "
                "containing the extra outputs for a single prediction"
            )
            return False

    return True


def _is_valid_extra_io(data: List[Dict[str, FeatureValue]], expected_length: int) -> bool:
    if not isinstance(data, list):
        return False

    if len(data) != expected_length:
        return False

    if not all(isinstance(data_point, dict) for data_point in data):
        return False

    return True


def _is_valid_predict_param_list(data: Union[List[List[float]], List[List[FeatureValue]]]) -> bool:
    if not isinstance(data, list):
        return False

    if len(data) == 0:
        return False

    if not all((isinstance(data_point, list) and len(data_point) > 0) for data_point in data):
        return False

    return True

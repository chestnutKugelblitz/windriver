"""
This file contains logic to work with endpoints from swagger
"""
import base64
from typing import TypedDict, Tuple


class JsonOutput(TypedDict):
    """
    Class to describe structure of JSON output for REST API
    """

    Input: str
    Output: str
    Status: str
    Message: str


def generate_output(
    return_input: str,
    return_output: str,
    return_status: str,
    return_message: str,
) -> JsonOutput:
    """
    Function to generate dict (to convert it later to json) with results of work endpoints
    :param return_input: what user set
    :param return_output: what we generate
    :param return_status: what is status of generation
    :param return_message: what is error message
    :param return_code: what is HTTP return code
    :return: return strict typed class JsonOutput
    """
    rest: JsonOutput = {
        "Input": return_input,
        "Output": return_output,
        "Status": return_status,
        "Message": return_message,
    }
    return rest


def encrypt_str(input_json: dict) -> Tuple[JsonOutput, int]:
    """
    Endpoint-related function to encrypt input, posted using
    :param inputJson: comes from POST request
    :return: tuple with dict and HTTP return code
    """
    try:
        return_output = base64.b64encode(
            input_json["Input"].encode(encoding="ascii")
        ).decode("utf-8")
        return_code = 200
        return_status = "success"
        return_message = ""
    #Catch wide class of extansitions due can be a lot of different types of Exceptions
    except Exception as parsing_exception:
        return_output = ""
        return_code = 415
        return_status = "error"
        return_message = str(parsing_exception)

    return (
        generate_output(
            input_json["Input"], return_output, return_status, return_message
        ),
        return_code,
    )


def decrypt_str(input_json: dict) -> Tuple[JsonOutput, int]:
    """
    Endpoint-related function to decrypt from base64 to ascii string line.
    :param inputJson: comes from POST request
    :return: tuple with dict and HTTP return code
    """
    try:
        return_output = base64.b64decode(
            input_json["Input"].encode(encoding="ascii")
        ).decode("utf-8")
        return_code = 200
        return_status = "success"
        return_message = ""
    #Catch wide class of extansitions due can be a lot of different types of Exceptions
    except Exception as parsing_exception:
        return_output = ""
        return_code = 415
        return_status = "error"
        return_message = str(parsing_exception)

    return (
        generate_output(
            input_json["Input"], return_output, return_status, return_message
        ),
        return_code,
    )


def welcome_endpoint() -> Tuple[str, int]:
    """
    health check for kubernetes
    :return: Nothing(empty string). Sets custom http request: 204 (no content)
    """
    return "", 204

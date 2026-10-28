
import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID",
    "amazon.nova-lite-v1:0"
)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "ALLOWED_ORIGINS", "*"
    ).split(",")
    if origin.strip()
]

bedrock = boto3.client("bedrock-runtime")


def make_response(status_code, body, origin=""):
    if "*" in ALLOWED_ORIGINS:
        allowed_origin = "*"
    elif origin in ALLOWED_ORIGINS:
        allowed_origin = origin
    else:
        allowed_origin = "null"

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowed_origin,
            "Vary": "Origin",
            "X-Content-Type-Options": "nosniff"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    headers = event.get("headers") or {}
    origin = headers.get("origin", "")

    if (
        ALLOWED_ORIGINS != ["*"]
        and origin not in ALLOWED_ORIGINS
    ):
        return make_response(
            403,
            {"error": "Origin not allowed"},
            origin
        )

    try:
        body = event.get("body") or "{}"

        if event.get("isBase64Encoded"):
            return make_response(
                400,
                {"error": "Encoded requests are not supported"},
                origin
            )

        payload = json.loads(body)
        question = payload.get("question", "")

        if not isinstance(question, str):
            return make_response(
                400,
                {"error": "Question must be text"},
                origin
            )

        question = question.strip()

        if not question:
            return make_response(
                400,
                {"error": "Please enter a question"},
                origin
            )

        if len(question) > 2000:
            return make_response(
                400,
                {"error": "Question must be 2000 characters or fewer"},
                origin
            )

        result = bedrock.converse(
            modelId=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"text": question}
                    ]
                }
            ],
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.4
            }
        )

        answer = result["output"]["message"]["content"][0]["text"]

        return make_response(
            200,
            {"answer": answer},
            origin
        )

    except json.JSONDecodeError:
        return make_response(
            400,
            {"error": "Invalid JSON request"},
            origin
        )

    except (ClientError, BotoCoreError) as error:
        print(
            f"Bedrock error: {type(error).__name__}: {error}"
        )

        return make_response(
            502,
            {
                "error": (
                    "AI service request failed. "
                    "Check Bedrock model access and Lambda logs."
                )
            },
            origin
        )

    except Exception as error:
        print(
            f"Unexpected error: {type(error).__name__}: {error}"
        )

        return make_response(
            500,
            {"error": "Internal server error"},
            origin
        )

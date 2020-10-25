import asyncio
import os
import ssl

current_path = os.getenv('PWD')

loop = asyncio.get_event_loop()

# Default timeout for HTTP requests
timeout = 3

# Default headers for HTTP requests
headers = {
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "close",
    "User-Agent": "Ubook HTTP Client"
}

# Ciphers list for HTTPS connections
ssl_ciphers = ":".join([
    "ECDHE+AESGCM",
    "ECDHE+CHACHA20",
    "DHE+AESGCM",
    "DHE+CHACHA20",
    "ECDH+AESGCM",
    "DH+AESGCM",
    "ECDH+AES",
    "DH+AES",
    "RSA+AESGCM",
    "RSA+AES",
    "!aNULL",
    "!eNULL",
    "!MD5",
    "!DSS"
])

# Default options for SSL contexts
ssl_options = (
	ssl.OP_ALL \
	| ssl.OP_NO_SSLv2 \
	| ssl.OP_NO_SSLv3 \
    | ssl.OP_NO_TLSv1 \
	| ssl.OP_NO_TLSv1_1 \
	| ssl.OP_NO_TICKET \
	| ssl.OP_NO_COMPRESSION \
	| ssl.OP_NO_RENEGOTIATION \
	| ssl.OP_SINGLE_DH_USE \
	| ssl.OP_SINGLE_ECDH_USE
)

# Default verify flags for SSL contexts
ssl_verify_flags = (
	ssl.VERIFY_X509_STRICT \
	| ssl.VERIFY_X509_TRUSTED_FIRST \
	| ssl.VERIFY_DEFAULT
)

# CA bundle for server certificate validation
cafile = f"{current_path}/package_data/ca-bundle.crt"

# CA certs path for server certificate validation
capath = os.path.dirname(cafile)

# Login endpoint
endpoint = "https://www.ubook.com/backend/login"

# DNS cache
dns_cache = {"www.ubook.com": "104.26.15.2"}
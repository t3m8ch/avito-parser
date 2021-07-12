import ssl
from typing import Optional

from .config import config


def get_ssl_context() -> Optional[ssl.SSLContext]:
    if config.ssl_is_set:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(
            config.ssl_certificate_path,
            config.ssl_private_key_path
        )
    else:
        ssl_context = None

    return ssl_context


def get_ssl_certificate_bytes() -> Optional[bytes]:
    if config.ssl_is_set:
        with open(config.ssl_certificate_path, 'rb') as file:
            ssl_certificate = file.read()
    else:
        ssl_certificate = None

    return ssl_certificate

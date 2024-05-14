import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

if __name__ == "__main__":
    ssl_cert_path = os.getenv('SSL_CERT_PATH', '/default/path/to/certificate.crt')
    ssl_key_path = os.getenv('SSL_KEY_PATH', '/default/path/to/private.key')

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        ssl_certfile=ssl_cert_path,
        ssl_keyfile=ssl_key_path
    )

import os
from pathlib import Path

import trustme
import uvicorn

#  Uvicorn server settings
if __name__ == '__main__':

    # This mocks ssl certificate
    with trustme.CA().issue_server_cert(
            'localhost',
            '127.0.0.1',
            '::1',
            '0.0.0.0',
    ).private_key_and_cert_chain_pem.tempfile() as ssl_certfile:

        uvicorn.run(
            'entropy.asgi:application',
            host='localhost',
            port=8000,
            log_level='info',
            reload=True,
            reload_dirs=[
                Path('..'),
                Path(__file__).parent.parent.absolute(),
            ],
            workers=os.cpu_count(),
            #env_file=Path(r'.env').absolute(),
            use_colors=True,
            # ssl_keyfile=Path(r'rootCA-key.pem'),
            # ssl_certfile=Path(r'rootCA.pem'),
            #ssl_certfile=ssl_certfile,  Раскоментить только эту строку
        )
    print(Path(__file__).parent.absolute(),)
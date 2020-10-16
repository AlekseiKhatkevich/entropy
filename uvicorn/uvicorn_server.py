import uvicorn
import os
from pathlib import Path

#  Uvicorn server settings
if __name__ == '__main__':
    uvicorn.run(
        'entropy.asgi:application',
        host='localhost',
        port=8000,
        log_level='info',
        reload=True,
        workers=os.cpu_count(),
        env_file=Path(r'entropy\.env'),
        use_colors=True,
        #ssl_keyfile=Path(r'ssl\rootCA-key.pem'),
        #ssl_certfile=Path(r'ssl\rootCA.pem'),
    )
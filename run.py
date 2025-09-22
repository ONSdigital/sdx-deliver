from pathlib import Path

from sdx_base.run import run

from app.routes import router
from app.settings import Settings

if __name__ == '__main__':
    proj_root = Path(__file__).parent  # sdx-deliver dir
    run(Settings, routers=[router], proj_root=proj_root)

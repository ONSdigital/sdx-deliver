from pathlib import Path

from sdx_base.run import run
from sdx_base.server.server import RouterConfig

from app.routes import router
from app.settings import Settings

if __name__ == '__main__':
    proj_root = Path(__file__).parent  # sdx-deliver dir
    router_config = RouterConfig(router)
    run(Settings, routers=[router_config], proj_root=proj_root)

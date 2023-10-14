from fastapi import FastAPI

from ...core.settings import settings
from .router import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cashu Wallet REST API",
        description="REST API for Cashu Nutshell",
        version=settings.version,
        license_info={
            "name": "MIT License",
            "url": "https://raw.githubusercontent.com/cashubtc/cashu/main/LICENSE",
        },
    )
    return app


app = create_app()

app.include_router(router=router)

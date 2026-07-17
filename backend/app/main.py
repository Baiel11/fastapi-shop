from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .middleware.security import SecurityHeadersMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .core.database.session import engine
from .core.config import settings
from .routes.customer import products_router, categories_router, cart_router, auth_router
from .routes.admin import (
    dashboard_router,
    admin_products_router,
    admin_categories_router,
    admin_users_router,
)

from .core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .core.limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    lifespan=lifespan,
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(SecurityHeadersMiddleware)

app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Customer routes
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(categories_router)
app.include_router(products_router)

# Admin routes
app.include_router(dashboard_router)
app.include_router(admin_products_router)
app.include_router(admin_categories_router)
app.include_router(admin_users_router)

@app.get('/')
def root():
    return {
        'message': 'Welcome to Baya FastAPI Shop',
        'docs': 'api/docs'
    }

@app.get('/health')
def health_check():
    return {'status': 'healthy'}
import logging

import stripe
from fastapi import FastAPI

from app.bootstrap import cors, exceptions
from app.environ import STRIPE_PRIVATE_KEY
from app.routes.authentication import auth_router
from app.routes.cart import cart_router
from app.routes.category import category_router
from app.routes.order import order_router
from app.routes.product import product_router
from app.routes.search import search_router
from app.routes.user import user_router
from app.routes.webhook import webhook_router
from app.stripe_config import StripeShippingRateError, load_shipping_rates

stripe.api_key = STRIPE_PRIVATE_KEY

app = FastAPI(
    servers=[
        {
            "url": "https://produce-goose-frontend.herokuapp.com",
            "description": "Production environment",
        },
        {
            "url": "https://produce-goose-frontend-stg.herokuapp.com",
            "description": "Staging environment",
        },
        {
            "url": "http://localhost:8080",
            "description": "Dev environment",
        },
    ],
    root_path="/api",
)

app.include_router(order_router, prefix="/order", tags=["order"])
app.include_router(webhook_router, prefix="/webhook", tags=["webhook"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(product_router, prefix="/product", tags=["product"])

cors.setup_cors(app)
exceptions.setup_exception_handlers(app)


@app.on_event("startup")
def on_startup(): # pragma: no cover
    try:
        load_shipping_rates()
    except StripeShippingRateError:
        logger = logging.getLogger("uvicorn.error")
        logger.warning("Not all shipping options are available. Make sure "
                       + "to follow the README and restart the container after running "
                       + "`docker compose exec backend python manage stripe setup` to setup "
                       + "the shipping options in Stripe.")

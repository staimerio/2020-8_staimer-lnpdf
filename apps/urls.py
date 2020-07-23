# Retic
from retic import App as app

"""Define all other apps"""
BACKEND_LNPDF = {
    u"base_url": app.config.get('APP_BACKEND_LNPDF'),
    u"posts": "/posts",
}

APP_BACKEND = {
    u"lnpdf": BACKEND_LNPDF
}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")

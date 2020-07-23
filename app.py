"""Main app"""

# Retic
from retic import App as app

# Settings
import settings

# Apps
from apps.urls import APP_BACKEND

# Routes
from routes.routes import router

# Agregar las rutas a la aplicación
app.use(router)

# Crear un servidor web
app.listen(
    # use_reloader=True,
    # use_debugger=True,
    hostname=app.env('APP_HOSTNAME', "localhost"),
    port=app.env.int('APP_PORT', 1801),
)

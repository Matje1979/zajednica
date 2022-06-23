import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# from django.core.asgi import get_asgi_application
from channels.http import AsgiHandler

import home.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_manager.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": AsgiHandler(),
        "websocket": AuthMiddlewareStack(URLRouter(home.routing.websocket_urlpatterns)),
        # Just HTTP for now. (We can add other protocols later.)
    }
)

# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault(
#     "DJANGO_SETTINGS_MODULE", "channels_celery_heroku_project.settings"
# )
# django.setup()

# from channels.auth import AuthMiddleware, AuthMiddlewareStack
# from notifications_app.routing import websocket_urlpatterns

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
#     }
# )

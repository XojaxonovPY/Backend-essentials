from apps.urls.tasks import urlpatterns as tasks
from apps.urls.delivery_videos import urlpatterns as delivery
from apps.urls.login import urlpatterns as login

urlpatterns = [
    *tasks,
    *delivery,
    *login
]

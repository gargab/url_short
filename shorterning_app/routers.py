from rest_framework import routers
from views import urlMapView as urlView




router = routers.SimpleRouter()

router.register('',urlView)

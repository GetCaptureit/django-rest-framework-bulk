from rest_framework_bulk import generics
from . import models, serializers


class SimpleBulkUpdateAPIView (generics.BulkUpdateAPIView):
    queryset = models.SimpleModel.objects.all()
    serializer_class = serializers.SimpleModelSerializer

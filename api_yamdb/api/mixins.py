from rest_framework import mixins, viewsets


class CreateOrListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet, mixins.DestroyModelMixin):
    pass

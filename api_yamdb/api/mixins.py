from rest_framework import mixins, viewsets


class CDLViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 mixins.ListModelMixin, viewsets.GenericViewSet):
    """Базовый viewset class.
    Поддерживаемые методы: Create, Destroy, List.
    """
    pass

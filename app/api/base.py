from rest_framework.viewsets import ViewSet


class BaseViewSet(ViewSet):
    serializer_class = None

    def get_serializer(
            self, *args, serializer_class=None, request=None, **kwargs
    ):
        """
        Return instance of serializer with a request in context.
        """
        serializer_class = serializer_class or self.serializer_class
        if "context" not in kwargs:
            request = request or getattr(self, "request", None)
            assert request, "self.request is not set and is not passed in kwargs"
            kwargs["context"] = {"request": request}
        return serializer_class(**kwargs)

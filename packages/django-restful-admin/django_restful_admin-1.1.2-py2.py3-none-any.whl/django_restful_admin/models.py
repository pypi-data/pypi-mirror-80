from django.contrib.auth import get_permission_codename
from django.db.models.base import ModelBase
from django.utils.functional import cached_property
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import ModelSerializer


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class AuthPermissionViewSetMixin:
    NOT_FOUND_PERMISSION_DEFAULT = False
    permission_map = dict()

    def get_permission_map(self):
        permission_map = {
            'list': self._make_permission_key('view'),
            'retrieve': self._make_permission_key('view'),
            'create': self._make_permission_key('add'),
            'update': self._make_permission_key('update'),
            'delete': self._make_permission_key('delete'),
        }
        permission_map.update(self.permission_map)
        return permission_map

    @cached_property
    def _options(self):
        return self.get_queryset().model._meta

    def _make_permission_key(self, action):
        code_name = get_permission_codename(action, self._options)
        return "{0}.{1}".format(self._options.app_label, code_name)

    def _has_perm_action(self, action, request, obj=None):
        perm_map = self.get_permission_map()
        if action not in perm_map:
            return self.NOT_FOUND_PERMISSION_DEFAULT

        perm_code = perm_map[action]
        if callable(perm_code):
            return perm_code(self, action, request, obj)

        return request.user.has_perm(
            perm_code
        )


class IsStaffAccess(BasePermission):
    """
    Allows access only to authenticated Trainee users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return self.has_permission(request, view)


class HasPermissionAccess(BasePermission):
    """
    Allows access only to authenticated Trainee users.
    """

    def has_permission(self, request, view):
        assert hasattr(view, 'get_permission_map'), """
        Must be inherit from RestFulModelAdmin to use this permission
        """
        print(view.action)
        return view._has_perm_action(view.action, request)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return view._has_perm_action(view.action, request, obj)


class RestFulModelAdmin(AuthPermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = None
    single_serializer_class = None
    permission_classes = (IsStaffAccess, HasPermissionAccess)

    @staticmethod
    def get_doc():
        return 'asd'

    def get_single_serializer_class(self):
        return self.single_serializer_class if self.single_serializer_class else self.get_serializer_class()

    def get_single_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_single_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        """list all of objects"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        """Create new object"""
        serializer = self.get_single_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None, **kwargs):
        """Get object Details"""
        instance = self.get_object()
        serializer = self.get_single_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        """Update object"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_single_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, pk=None, **kwargs):
        """Partial Update"""
        return super().partial_update(request, pk=pk, **kwargs)

    def destroy(self, request, pk=None, **kwargs):
        """Delete object"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseModelSerializer(ModelSerializer):
    class Meta:
        pass


class RestFulAdminSite:
    def __init__(self):
        self._registry = {}
        self._url_patterns = []

    def register_decorator(self, *model_or_iterable, **options):
        def wrapper(view_class):
            return self.register(model_or_iterable, view_class, **options)

        return wrapper

    def register(self, model_or_iterable, view_class=None, **options):
        if not view_class:
            view_class = RestFulModelAdmin

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered with admin.' % model.__name__
                )

            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            options.update({
                "__doc__": self.generate_docs(model)
            })
            view_class = type("%sAdmin" % model.__name__, (view_class,), options)
            print(view_class.pagination_class)
            # self.set_docs(view_class, model)
            # Instantiate the admin class to save in the registry
            self._registry[model] = view_class

    def register_url_pattern(self, url_pattern):
        self._url_patterns.append(url_pattern)

    @classmethod
    def generate_docs(cls, model):
        return """
    ### The APIs include:


    > `GET`  {app}/{model} ===> list all `{verbose_name_plural}` page by page;

    > `POST`  {app}/{model} ===> create a new `{verbose_name}`

    > `GET` {app}/{model}/123 ===> return the details of the `{verbose_name}` 123

    > `PATCH` {app}/{model}/123 and `PUT` {app}/{model}/123 ==> update the `{verbose_name}` 123

    > `DELETE` {app}/{model}/123 ===> delete the `{verbose_name}` 123

    > `OPTIONS` {app}/{model} ===> show the supported verbs regarding endpoint `{app}/{model}`

    > `OPTIONS` {app}/{model}/123 ===> show the supported verbs regarding endpoint `{app}/{model}/123`

            """.format(
            app=model._meta.app_label,
            model=model._meta.model_name,
            verbose_name=model._meta.verbose_name,
            verbose_name_plural=model._meta.verbose_name_plural
        )

    def unregister(self, model_or_iterable):
        """
        Unregister the given model(s).

        If a model isn't already registered, raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]

    def is_registered(self, model):
        """
        Check if a model class is registered with this `AdminSite`.
        """
        return model in self._registry

    def get_urls(self):
        router = DefaultRouter()
        view_sets = []
        for model, view_set in self._registry.items():
            if view_set.queryset is None:
                view_set.queryset = model.objects.all()
            if view_set.serializer_class is None:
                serializer_class = type("%sModelSerializer" % model.__name__, (ModelSerializer,), {
                    "Meta": type("Meta", (object,), {
                        "model": model,
                        "fields": "__all__"
                    }),
                })
                view_set.serializer_class = serializer_class

            view_sets.append(view_set)
            router.register('%s/%s' % (model._meta.app_label, model._meta.model_name), view_set)

        return router.urls + self._url_patterns

    @property
    def urls(self):
        return self.get_urls(), 'django_restful_admin', 'django_restful_admin'


site = RestFulAdminSite()

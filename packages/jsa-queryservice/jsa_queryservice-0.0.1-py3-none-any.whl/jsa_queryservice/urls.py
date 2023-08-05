from django.urls import path

from .views import ReadEntityAction, IntrospectEntityAction, DeleteEntityAction

urlpatterns = [
    path("introspect/", IntrospectEntityAction.as_view()),
    path("read/", ReadEntityAction.as_view()),
    path("delete/", DeleteEntityAction.as_view()),
]

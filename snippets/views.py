from rest_framework import permissions, renderers, viewsets, generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse


from snippets.models import BannedUser, Snippet, SavedSnippet, SnippetSave
from snippets.serializers import (
    BannedUserSerializer,
    SnippetSerializer,
    UserSerializer,
    SavedSnippetSerializer,
    SnippetSaveSerializer,
)
from snippets.permissions import IsOwnerOrReadOnly, IsNotBanned
from django.contrib.auth.models import User


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


class SnippetViewSet(viewsets.ModelViewSet):
    """Model Viewset
    Combines CRUD and list view actions

    Snippet can also be highlighted
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
        IsNotBanned,
    ]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """RO Viewset = retrieve and list all"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class BannedUserViewSet(viewsets.ModelViewSet):
    """Model Viewset
    Combines CRUD and list view actions

    Snippet can also be highlighted
    """

    queryset = BannedUser.objects.all()
    serializer_class = BannedUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# TODO: finish this and the snippetsave view
# class SavedSnippetList(generics.GenericAPIView):
#     """ Saved Snippets List
#     User generated lists containing collections of snippets for future reference.
#     This model links to SnippetSave for the id of the snippet.

#     The user can create lists, delete lists, rename lists from this endpoint
#     SnippetSave will deal with the adding new snippets to the list
#     """
#     queryset = SavedSnippet
#     serializer_class = SavedSnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsNotBanned]

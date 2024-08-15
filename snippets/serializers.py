from rest_framework import serializers
from snippets.models import Snippet, BannedUser, SavedSnippet, SnippetSave
from django.contrib.auth.models import User


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )

    class Meta:
        model = Snippet
        fields = [
            "url",
            "id",
            "highlight",
            "title",
            "code",
            "linenos",
            "language",
            "style",
            "owner",
        ]


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedIdentityField(
        many=True, view_name="snippet-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]


class BannedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedUser
        fields = ["user_id", "status"]


class SavedSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSnippet
        fields = ["id", "user_id", "name"]


class SnippetSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnippetSave
        fields = ["id", "list_id", "snippet_id"]

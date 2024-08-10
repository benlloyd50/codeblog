from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
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


# BoilerPlate
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, data: Snippet):
#         """ Creates a Snippet with *valid* data"""
#         return Snippet.objects.create(**data)

#     def update(self, instance: Snippet, data: Snippet):
#         """ Updates an instance of Snippet with *valid* data"""
#         instance.title = data.get('title', instance.title)
#         instance.code = data.get('code', instance.code)
#         instance.linenos = data.get('linenos', instance.linenos)
#         instance.language = data.get('language', instance.language)
#         instance.style = data.get('style', instance.style)
#         instance.save()
#         return instance

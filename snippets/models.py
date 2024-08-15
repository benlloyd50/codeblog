from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
BANNED_STATUS = [(item, item) for item in ["BANNED", "SQUASHED"]]


class Snippet(models.Model):
    owner = models.ForeignKey(
        "auth.User", related_name="snippets", on_delete=models.CASCADE
    )
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)

    class Meta:
        ordering = ["created"]

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)


class BannedUser(models.Model):
    user_id = models.OneToOneField(
        "auth.User",
        related_name="banned_users",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    status = models.CharField(choices=BANNED_STATUS, default="BANNED", max_length=100)

    def is_banned(self):
        """Checks the status is equal to `BANNED`"""
        return self.status == "BANNED"


# create a list of saved snippets.
# user can have multiple lists, starting with 1
# lists can have multiple snippets


# user creates these as the owner of the list
class SavedSnippet(models.Model):
    """The lists of snippets created from the user"""

    user_id = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, default="Saved Snippets")


class SnippetSave(models.Model):
    """The snippets saved for each list"""

    list_id = models.ForeignKey(SavedSnippet, on_delete=models.CASCADE)
    snippet_id = models.ForeignKey(Snippet, on_delete=models.CASCADE)

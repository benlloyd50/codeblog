from django.contrib import admin

from snippets.models import Snippet, BannedUser

# Register your models here.
admin.site.register(Snippet)
admin.site.register(BannedUser)

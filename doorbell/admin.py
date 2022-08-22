from django.contrib import admin

from doorbell.models import (
  Visit,
  Friend,
  Category,
  ClientToken,
)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
  pass


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
  pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  pass


@admin.register(ClientToken)
class ClientTokenAdmin(admin.ModelAdmin):
  pass
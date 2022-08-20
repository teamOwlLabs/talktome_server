from django.db import models
from django.utils.translation import gettext_lazy as _

class Friend(models.Model):
  name = models.CharField(_("Friend"), max_length=128)
  relation = models.CharField(_("Relation"), max_length=32)
  image = models.ImageField(_("Image"), upload_to="friend/image/")
  created_at = models.DateTimeField(_("Created At"), auto_now_add=True)


class Category(models.Model):
  type = models.CharField(_("Type"), max_length=32)


class Visit(models.Model):
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="category_visits", null=True)
  friend = models.ForeignKey(Friend, on_delete=models.SET_NULL, related_name="friend_vist", null=True, blank=True)
  visit_reason = models.TextField(_("Visti Reason"))
  created_at = models.DateTimeField(_("Created At"), auto_now=True)

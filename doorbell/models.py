from django.db import models
from django.utils.translation import gettext_lazy as _

class Friend(models.Model):
  name = models.CharField(_("Friend"), max_length=128)
  relation = models.CharField(_("Relation"), max_length=32)
  image = models.ImageField(_("Image"), upload_to="friend/image/")
  created_at = models.DateTimeField(_("Created At"), auto_now_add=True)


class Category(models.Model):
  type = models.CharField(_("Type"), max_length=32)
  rgb_color = models.CharField(_("RGB Color"), max_length=8, null=True)
  vibration_pattern = models.CharField(_("Vibration Pattern"), max_length=10, null=True)


class Visit(models.Model):
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="category_visits", null=True)
  friend = models.ForeignKey(Friend, on_delete=models.SET_NULL, related_name="friend_vist", null=True, blank=True)
  visit_reason = models.TextField(_("Visti Reason"), blank=True)
  num_of_confirmation = models.PositiveIntegerField(_("Number Of Confirmation"), default=0)
  created_at = models.DateTimeField(_("Created At"), auto_now=True)


# ClientToken을 어드민 페이지에서 손 쉽게 변혀하기 위해서 만든 테이블 나중에는 방식이 변경되어야 합니다.
class ClientToken(models.Model):
  fcm_token = models.TextField(_("FCM Token"), null=True, blank=True)

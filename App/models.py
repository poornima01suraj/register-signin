from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Additional fields
    
    username = models.TextField(_('username'), max_length=150, unique=True, blank=True, null=True)
    password = models.CharField(_('password'), max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]' or use the raw value."),)
    web_terms = models.BooleanField(default=False)
    dataprocessing = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def web_terms_display(self):
        return "1" if self.web_terms else "0"

    @property
    def dataprocessing_display(self):
        return "1" if self.dataprocessing else "0"

    @property
    def subscription_display(self):
        return "1" if self.subscription else "0"

    def __str__(self):
        return self.username
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users_groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users_permissions'
    )

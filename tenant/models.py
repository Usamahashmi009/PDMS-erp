from django.db import models
from django.contrib.auth.models import User 
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog_name = models.CharField(max_length=100)
    blog_image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    featured = models.BooleanField(default=False)
    updated_at = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True
    auto_drop_schema = True

class Domain(DomainMixin):
    pass
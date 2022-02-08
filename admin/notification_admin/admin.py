from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, Roles, UserRole, Templates, Others


class RoleInlineAdmin(admin.TabularInline):
    model = UserRole
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'confirmed', 'mail_subscribe', 'get_role')
    list_filter = ('confirmed', 'mail_subscribe')
    search_fields = ('login', 'email',)
    fields = (
        'login',
        'email',
        'confirmed',
        'mail_subscribe',
        'password',
    )
    inlines = (RoleInlineAdmin,)
    list_prefetch_related = ('roles',)

    def get_role(self, obj):
        return ''.join([role.name for role in obj.roles.all()])

    get_role.short_description = _('Role')


@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = (
        'name',
    )


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = (
        'name',
        'template',
    )


@admin.register(Others)
class OthersAdmin(admin.ModelAdmin):
    list_display = ('title', 'template')
    search_fields = ('title',)
    fields = (
        'title',
        'description',
        'template',
    )

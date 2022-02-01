from django.contrib import admin

from .models import User, Role, UserRole, Templates, Discounts, UpdatingContent


class RoleInlineAdmin(admin.TabularInline):
    model = UserRole
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'confirmed',)
    list_filter = ('confirmed',)
    search_fields = ('login', 'email',)
    fields = (
        'login',
        'email',
        'confirmed',
        'password',
    )
    inlines = (RoleInlineAdmin,)


@admin.register(Role)
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


@admin.register(Discounts)
class DiscountsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = (
        'title',
        'description',
        'template',
    )


@admin.register(UpdatingContent)
class UpdatingContentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = (
        'title',
        'description',
        'template',
    )

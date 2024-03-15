from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import *

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('email',)

class MyUserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class MovieAdmin(admin.ModelAdmin):

    list_display = ['title', 'date_time']
    search_fields = ['title', 'description']
    readonly_fields = ['booked_tickets', 'reserved_seats']



class SeatAdmin(admin.ModelAdmin):

    list_display = ['name']
    search_fields = ['name']

class CommentAdmin(admin.ModelAdmin):

    list_display = ['username']



admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Comment, CommentAdmin)
from django import forms
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from users.models import User


class UserForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        instance = super(UserForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = User
        fields = '__all__'


# noinspection PyClassHasNoInit
# pylint: disable=bad-continuation
class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    form = UserForm

    list_display = [
        'id', 'email', 'full_name', 'is_superuser', 'is_active'
    ]

    list_filter = ['is_superuser']

    fieldsets = (
        (None, {'fields': (
            'email', 'password',
        )}),
        ('Personal info', {'fields': (
            'first_name', 'last_name'
        )}),
        ('Permissions', {'fields': (
             'is_superuser', 'is_staff'
        )}),
        ('Important dates', {'fields': (
            'updated_at', 'last_login',
        )}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'full_name', 'id')
    ordering = ['-id']
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
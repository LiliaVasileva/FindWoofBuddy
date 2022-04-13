from django.contrib import admin
from django.contrib.auth.models import Group

from find_buddy.dog.admin import DogInlineAdmin
from find_buddy.home.forms import GroupAdminForm
from find_buddy.home.models import Profile, FindBuddyUser


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'picture', 'birth_date', 'user')


@admin.register(FindBuddyUser)
class FindBuddyUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInlineAdmin, DogInlineAdmin)
    list_display = ('email', 'is_staff', 'date_joined', 'is_active')


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']

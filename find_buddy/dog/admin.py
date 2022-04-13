from django.contrib import admin

from find_buddy.dog.models import Dog, DogMissingReport


class DogInlineAdmin(admin.StackedInline):
    model = Dog

class DogMissingReportInlineAdmin(admin.StackedInline):
    model =DogMissingReport

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    inlines = (DogMissingReportInlineAdmin,)
    list_display = ('name', 'address', 'description', 'if_lost', 'user')

@admin.register(DogMissingReport)
class DogMissingReportAdmin(admin.ModelAdmin):
    list_display = ('reported_address', 'subject', 'message')
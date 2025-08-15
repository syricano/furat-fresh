# profiles/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    can_delete = False
    extra = 0
    fields = (
        "default_first_name", "default_last_name", "default_email",
        "default_phone_number",
        "default_street_address1", "default_street_address2",
        "default_town_or_city", "default_county",
        "default_postcode", "default_country",
    )

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username", "email", "first_name", "last_name", "is_staff",
        "profile_phone", "profile_city", "profile_country",
    )
    search_fields = (
        "username", "email", "first_name", "last_name",
        "userprofile__default_phone_number",
        "userprofile__default_town_or_city",
    )

    @admin.display(description="Phone")
    def profile_phone(self, obj):
        return getattr(obj.userprofile, "default_phone_number", "")

    @admin.display(description="City")
    def profile_city(self, obj):
        return getattr(obj.userprofile, "default_town_or_city", "")

    @admin.display(description="Country")
    def profile_country(self, obj):
        return getattr(obj.userprofile, "default_country", "")

# Replace default User admin with one that includes the inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", "default_first_name", "default_last_name",
        "default_phone_number", "default_town_or_city", "default_country",
    )
    list_select_related = ("user",)
    search_fields = (
        "user__username", "user__email",
        "default_first_name", "default_last_name",
        "default_phone_number", "default_town_or_city",
    )
    list_filter = ("default_country",)
    fieldsets = (
        (None, {"fields": ("user",)}),
        ("Defaults", {"fields": (
            "default_first_name", "default_last_name",
            "default_email", "default_phone_number",
        )}),
        ("Address", {"fields": (
            "default_street_address1", "default_street_address2",
            "default_town_or_city", "default_county",
            "default_postcode", "default_country",
        )}),
    )

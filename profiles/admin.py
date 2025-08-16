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
        "first_name", "last_name", "email", "phone_number",
        "street_address1", "street_address2",
        "town_or_city", "county",
        "postcode", "country",
    )


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username", "email", "first_name", "last_name", "is_staff",
        "profile_phone", "profile_city", "profile_country",
    )
    search_fields = (
        "username", "email", "first_name", "last_name",
        "userprofile__phone_number",
        "userprofile__town_or_city",
    )

    @admin.display(description="Phone")
    def profile_phone(self, obj):
        up = getattr(obj, "userprofile", None)
        return up.phone_number if up and up.phone_number else ""

    @admin.display(description="City")
    def profile_city(self, obj):
        up = getattr(obj, "userprofile", None)
        return up.town_or_city if up and up.town_or_city else ""

    @admin.display(description="Country")
    def profile_country(self, obj):
        up = getattr(obj, "userprofile", None)
        if not up or not up.country:
            return ""
        return getattr(up.country, "name", str(up.country))


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", "first_name", "last_name",
        "phone_number", "town_or_city", "country",
    )
    list_select_related = ("user",)
    search_fields = (
        "user__username", "user__email",
        "first_name", "last_name",
        "phone_number", "town_or_city",
    )
    list_filter = ("country",)
    fieldsets = (
        (None, {"fields": ("user",)}),
        ("Contact", {"fields": (
            "first_name", "last_name",
            "email", "phone_number",
        )}),
        ("Address", {"fields": (
            "street_address1", "street_address2",
            "town_or_city", "county",
            "postcode", "country",
        )}),
    )

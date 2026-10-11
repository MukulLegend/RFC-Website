from django.contrib import admin

from .models import Announcement, Contact, Match, Player, Register

admin.site.site_header = "Ramos Football Club - Admin"
admin.site.site_title = "RFC Admin"
admin.site.index_title = "Manage your club"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact_no", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ("user", "contact_no")
    search_fields = ("user__username", "user__email")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "jersey_number", "is_captain", "is_active")
    list_filter = ("position", "is_active")
    search_fields = ("name",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("date", "opponent", "competition", "is_home", "our_score", "opponent_score")
    list_filter = ("competition", "is_home")
    date_hierarchy = "date"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "body")

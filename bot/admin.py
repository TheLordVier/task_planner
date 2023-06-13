from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ["chat_id"]
    readonly_fields = ["verification_code"]
    search_fields = ["chat_id"]

# @admin.register(TgUser)
# class TgUserAdmin(admin.ModelAdmin):
#     list_display = ("chat_id", "db_user")
#     readonly_fields = ("verification_code", "updated")
#
#     def db_user(self, obj: TgUser) -> str | None:
#         if obj.user:
#             return obj.user.username
#         else:
#             return None

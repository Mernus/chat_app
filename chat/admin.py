from django.contrib import admin
from chat.models import Room, Message, RoomMember


admin.site.register((Room, Message, RoomMember))

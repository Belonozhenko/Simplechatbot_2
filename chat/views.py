

from django.utils.safestring import mark_safe
from .models import Chat
from django.shortcuts import render, get_object_or_404
import json

def index(request):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps('lobby'))
    })





def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def get_last_100_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:100]


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)

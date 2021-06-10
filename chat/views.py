from rest_framework.views import APIView
from rest_framework.response import Response

from notifications.utils import notify
from notifications import default_settings as notifs_settings

from chat.models import Message, Room


class ChatSessionView(APIView):
    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        user = request.session.get('user_id')

        chat_session = Room.objects.create()
        chat_session.members.create(user_id=user, room=chat_session)

        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })

    def patch(self, request, *args, **kwargs):
        uri = kwargs['uri']
        username = request.session['username']
        user_id = request.session['user_id']

        chat_session = Room.objects.get(uri=uri)
        chat_session.members.get_or_create(user_id=user_id, room=chat_session)

        members = [
            {'id': chat_session.user_id, 'username': chat_session.username}
            for chat_session in chat_session.members.all()
        ]

        return Response({
            'status': 'SUCCESS', 'members': members,
            'message': '%s joined the chat' % username,
            'user':  {'id': user_id, 'username': username}
        })


class ChatSessionMessageView(APIView):
    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = Room.objects.get(uri=uri)
        messages = [chat_session_message.to_json()
                    for chat_session_message in chat_session.messages.all()]

        return Response({
            'id': chat_session.id, 'uri': chat_session.uri, 'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']

        user_id = request.session.get('user_id')
        username = request.session.get('username')
        chat_session = Room.objects.get(uri=uri)

        chat_session_message = Message.objects.create(
            author_id=user_id, room=chat_session, content=message
        )

        notif_args = {
            'source': user_id,
            'source_display_name': username,
            'category': 'chat', 'action': 'Sent',
            'obj': chat_session_message.id,
            'short_description': 'You a new message', 'silent': True,
            'extra_data': {
                notifs_settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM:
                    chat_session.uri,
                'message': chat_session_message.to_json()
            }
        }
        notify(**notif_args, channels=['websocket'])

        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': message, 'user': {'id': user_id, 'username': username}
        })

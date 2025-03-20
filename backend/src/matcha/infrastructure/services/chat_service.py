from typing import Dict, List, Set, Any, Optional
import uuid
from datetime import datetime


class ChatService:
    """
    Service de gestion des conversations et messages entre utilisateurs.
    """

    def __init__(self, notifications_service):
        # Structure: conversation_id -> liste de messages
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        # Structure: user_id -> set de conversation_ids
        self.user_conversations: Dict[str, Set[str]] = {}
        # Structure: conversation_id -> set des user_ids participants
        self.conversation_participants: Dict[str, Set[str]] = {}
        # Service de notifications pour envoyer des alertes de nouveaux messages
        self.notifications_service = notifications_service

    async def create_conversation(self, participants: List[str],
                                 name: Optional[str] = None) -> str:
        """
        Crée une nouvelle conversation entre participants.
        """
        conversation_id = str(uuid.uuid4())

        # Initialiser la conversation
        self.conversations[conversation_id] = []
        self.conversation_participants[conversation_id] = set(participants)

        # Associer chaque utilisateur à cette conversation
        for user_id in participants:
            if user_id not in self.user_conversations:
                self.user_conversations[user_id] = set()
            self.user_conversations[user_id].add(conversation_id)

        # Notifier les participants de la création de la conversation
        conversation_data = {
            "conversation_id": conversation_id,
            "participants": participants,
            "name": name or ", ".join(participants[:2]) + (
                f" and {len(participants) - 2} others" if len(participants) > 2 else ""
            ),
            "created_at": datetime.now().isoformat(),
            "last_message": None
        }

        for user_id in participants:
            await self.notifications_service.send_notification(
                user_id,
                "conversation_created",
                conversation_data
            )

        return conversation_id

    async def send_message(self, conversation_id: str, sender_id: str,
                          content: str, message_type: str = "text") -> Dict[str, Any]:
        """
        Envoie un message dans une conversation.
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} does not exist")

        if sender_id not in self.conversation_participants[conversation_id]:
            raise ValueError(f"User {sender_id} is not part of conversation {conversation_id}")

        message = {
            "id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "content": content,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "read_by": [sender_id]
        }

        # Ajouter le message à la conversation
        self.conversations[conversation_id].append(message)

        # Notifier les autres participants
        for user_id in self.conversation_participants[conversation_id]:
            if user_id != sender_id:
                await self.notifications_service.send_notification(
                    user_id,
                    "new_message",
                    {
                        "conversation_id": conversation_id,
                        "message": message
                    },
                    source_user_id=sender_id
                )

        return message

    async def get_conversation_messages(self, conversation_id: str,
                                      limit: int = 50,
                                      before_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les messages d'une conversation avec pagination.
        """
        if conversation_id not in self.conversations:
            return []

        messages = self.conversations[conversation_id]

        # Appliquer la pagination si before_id est fourni
        if before_id:
            for i, msg in enumerate(messages):
                if msg["id"] == before_id:
                    messages = messages[:i]
                    break

        # Appliquer la limite et renvoyer les messages les plus récents
        return messages[-limit:] if limit > 0 else messages

    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les conversations d'un utilisateur.
        """
        if user_id not in self.user_conversations:
            return []

        result = []
        for conversation_id in self.user_conversations[user_id]:
            messages = self.conversations.get(conversation_id, [])
            last_message = messages[-1] if messages else None

            result.append({
                "id": conversation_id,
                "participants": list(self.conversation_participants[conversation_id]),
                "last_message": last_message,
                "unread_count": self._count_unread_messages(conversation_id, user_id)
            })

        # Trier par date du dernier message (le plus récent en premier)
        result.sort(key=lambda x: (
            x["last_message"]["timestamp"]
            if x["last_message"] else "0000-00-00T00:00:00"
        ), reverse=True)

        return result

    async def mark_messages_as_read(self, conversation_id: str, user_id: str) -> int:
        """
        Marque tous les messages non lus d'une conversation comme lus.
        Retourne le nombre de messages marqués comme lus.
        """
        if (conversation_id not in self.conversations or
            user_id not in self.conversation_participants[conversation_id]):
            return 0

        count = 0
        for message in self.conversations[conversation_id]:
            if user_id not in message["read_by"]:
                message["read_by"].append(user_id)
                count += 1

        return count

    def _count_unread_messages(self, conversation_id: str, user_id: str) -> int:
        """
        Compte le nombre de messages non lus dans une conversation.
        """
        if conversation_id not in self.conversations:
            return 0

        return sum(1 for msg in self.conversations[conversation_id]
                  if user_id not in msg["read_by"])

    async def add_participants(self, conversation_id: str, user_ids: List[str]) -> bool:
        """
        Ajoute des participants à une conversation existante.
        """
        if conversation_id not in self.conversations:
            return False

        # Ajouter les nouveaux participants
        for user_id in user_ids:
            self.conversation_participants[conversation_id].add(user_id)

            if user_id not in self.user_conversations:
                self.user_conversations[user_id] = set()
            self.user_conversations[user_id].add(conversation_id)

            # Notifier le nouveau participant
            await self.notifications_service.send_notification(
                user_id,
                "added_to_conversation",
                {
                    "conversation_id": conversation_id,
                    "participants": list(self.conversation_participants[conversation_id])
                }
            )

        # Notifier les participants existants
        for user_id in self.conversation_participants[conversation_id]:
            if user_id not in user_ids:
                await self.notifications_service.send_notification(
                    user_id,
                    "participants_added",
                    {
                        "conversation_id": conversation_id,
                        "new_participants": user_ids
                    }
                )

        return True

    async def leave_conversation(self, conversation_id: str, user_id: str) -> bool:
        """
        Permet à un utilisateur de quitter une conversation.
        """
        if (conversation_id not in self.conversations or
            user_id not in self.conversation_participants[conversation_id]):
            return False

        # Retirer l'utilisateur de la conversation
        self.conversation_participants[conversation_id].remove(user_id)
        self.user_conversations[user_id].remove(conversation_id)

        # Notifier les autres participants
        for remaining_user_id in self.conversation_participants[conversation_id]:
            await self.notifications_service.send_notification(
                remaining_user_id,
                "user_left_conversation",
                {
                    "conversation_id": conversation_id,
                    "user_id": user_id
                }
            )

        # Supprimer la conversation si plus personne
        if not self.conversation_participants[conversation_id]:
            del self.conversations[conversation_id]
            del self.conversation_participants[conversation_id]

        return True

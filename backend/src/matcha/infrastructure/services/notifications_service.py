import json
import asyncio
from datetime import datetime
from typing import Dict, List, Set, Any, Optional


class NotificationsService:
    """
    Service de notifications en temps réel.
    Permet d'envoyer des notifications aux utilisateurs connectés.
    """

    def __init__(self):
        # Mapping user_id -> liste des connexions actives
        self.active_connections: Dict[str, List[Any]] = {}
        # Notifications non lues par utilisateur
        self.unread_notifications: Dict[str, List[Dict[str, Any]]] = {}
        # Files d'attente de notification par utilisateur
        self.notification_queues: Dict[str, asyncio.Queue] = {}

    async def register_connection(self, user_id: str, connection: Any):
        """
        Enregistre une nouvelle connexion WebSocket pour un utilisateur.
        """
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(connection)

        # Créer une file d'attente si nécessaire
        if user_id not in self.notification_queues:
            self.notification_queues[user_id] = asyncio.Queue()

    async def unregister_connection(self, user_id: str, connection: Any):
        """
        Supprime une connexion WebSocket pour un utilisateur.
        """
        if user_id in self.active_connections:
            if connection in self.active_connections[user_id]:
                self.active_connections[user_id].remove(connection)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_notification(self, user_id: str, notification_type: str,
                               data: Dict[str, Any], source_user_id: Optional[str] = None):
        """
        Envoie une notification à un utilisateur spécifique.
        """
        notification = {
            "id": f"{notification_type}_{datetime.now().timestamp()}",
            "type": notification_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "read": False
        }

        if source_user_id:
            notification["source_user_id"] = source_user_id

        # Stocker la notification comme non lue
        if user_id not in self.unread_notifications:
            self.unread_notifications[user_id] = []

        self.unread_notifications[user_id].append(notification)

        # Envoyer la notification aux connexions actives
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(notification))
                except Exception:
                    # Gérer les erreurs de connexion
                    pass

        # Ajouter à la file d'attente pour les connexions futures
        if user_id in self.notification_queues:
            await self.notification_queues[user_id].put(notification)

    async def broadcast_notification(self, notification_type: str, data: Dict[str, Any],
                                   exclude_users: Optional[Set[str]] = None):
        """
        Envoie une notification à tous les utilisateurs connectés, sauf ceux exclus.
        """
        exclude_users = exclude_users or set()

        for user_id in self.active_connections:
            if user_id not in exclude_users:
                await self.send_notification(user_id, notification_type, data)

    async def mark_notification_as_read(self, user_id: str, notification_id: str):
        """
        Marque une notification comme lue.
        """
        if user_id in self.unread_notifications:
            for notification in self.unread_notifications[user_id]:
                if notification["id"] == notification_id:
                    notification["read"] = True
                    break

    async def get_unread_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les notifications non lues pour un utilisateur.
        """
        if user_id in self.unread_notifications:
            return [n for n in self.unread_notifications[user_id] if not n["read"]]
        return []

    async def consume_notifications(self, user_id: str, callback):
        """
        Consomme la file de notifications pour un utilisateur.
        Utilisé pour traiter les notifications en temps réel.
        """
        if user_id not in self.notification_queues:
            self.notification_queues[user_id] = asyncio.Queue()

        queue = self.notification_queues[user_id]

        while True:
            notification = await queue.get()
            try:
                await callback(notification)
            except Exception:
                # Gérer les erreurs de callback
                pass
            queue.task_done()

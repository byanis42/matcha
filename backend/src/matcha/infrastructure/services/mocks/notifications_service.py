from datetime import datetime
from typing import Dict, List, Set, Any, Optional


class MockNotificationsService:
    """
    Version simulée du service de notifications pour les tests.
    """

    def __init__(self):
        # Mapping user_id -> liste des notifications
        self.notifications: Dict[str, List[Dict[str, Any]]] = {}
        # Pour vérifier facilement les notifications envoyées
        self.sent_notifications: List[Dict[str, Any]] = []

    async def register_connection(self, user_id: str, connection: Any):
        """
        Simule l'enregistrement d'une connexion (non utilisé dans les tests).
        """
        pass

    async def unregister_connection(self, user_id: str, connection: Any):
        """
        Simule la déconnexion (non utilisé dans les tests).
        """
        pass

    async def send_notification(self, user_id: str, notification_type: str,
                               data: Dict[str, Any], source_user_id: Optional[str] = None):
        """
        Simule l'envoi d'une notification à un utilisateur.
        """
        notification = {
            "id": f"{notification_type}_{datetime.now().timestamp()}",
            "type": notification_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "read": False,
            "user_id": user_id
        }

        if source_user_id:
            notification["source_user_id"] = source_user_id

        # Stocker la notification
        if user_id not in self.notifications:
            self.notifications[user_id] = []

        self.notifications[user_id].append(notification)
        self.sent_notifications.append(notification)

        return notification

    async def broadcast_notification(self, notification_type: str, data: Dict[str, Any],
                                   exclude_users: Optional[Set[str]] = None):
        """
        Simule l'envoi d'une notification à tous les utilisateurs.
        """
        exclude_users = exclude_users or set()

        # Créer une liste d'utilisateurs fictifs si aucun n'existe
        all_users = set(self.notifications.keys())
        if not all_users:
            all_users = {"user1", "user2", "user3"}

        for user_id in all_users:
            if user_id not in exclude_users:
                await self.send_notification(user_id, notification_type, data)

    async def mark_notification_as_read(self, user_id: str, notification_id: str):
        """
        Marque une notification comme lue.
        """
        if user_id in self.notifications:
            for notification in self.notifications[user_id]:
                if notification["id"] == notification_id:
                    notification["read"] = True
                    break

    async def get_unread_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les notifications non lues pour un utilisateur.
        """
        if user_id in self.notifications:
            return [n for n in self.notifications[user_id] if not n["read"]]
        return []

    def clear_notifications(self):
        """
        Efface toutes les notifications simulées.
        """
        self.notifications.clear()
        self.sent_notifications.clear()

    def get_notifications_by_type(self, notification_type: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les notifications d'un type spécifique.
        """
        return [n for n in self.sent_notifications if n["type"] == notification_type]

    def get_user_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les notifications pour un utilisateur.
        """
        return self.notifications.get(user_id, [])

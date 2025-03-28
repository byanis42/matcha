from datetime import datetime
import json
import uuid
from typing import Union, Any, Dict

from pydantic import BaseModel, Field, ConfigDict
from pydantic.json import pydantic_encoder


class DomainObject(BaseModel):
    """Base class for all domain objects"""

    model_config = ConfigDict(
        use_enum_values=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
    )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"<DomainObject({self.__class__.__name__}) | {self.model_dump()}>"

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire pour la persistence"""
        return self.model_dump()


class ValueObject(DomainObject):
    """
    Objet immuable sans identité, défini uniquement par ses attributs.
    Deux value objects avec les mêmes attributs sont considérés comme égaux.
    """

    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:
        return f"<ValueObject({self.__class__.__name__}) | {self.model_dump()}>"


class Entity(DomainObject):
    """
    Entité avec une identité et un cycle de vie.
    Deux entités avec les mêmes attributs mais des IDs différents sont distinctes.
    """

    id: str = Field(frozen=True, default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(frozen=True, default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())

    def __str__(self) -> str:
        return f"<Entity({self.__class__.__name__}) | id={self.id}>"

    def update(self, **kwargs) -> None:
        """Met à jour l'entité avec les attributs fournis et actualise updated_at"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)

        # Mettre à jour le timestamp
        object.__setattr__(self, 'updated_at', datetime.utcnow())


class Aggregate(Entity):
    """
    Agrégat racine qui garantit la cohérence d'un groupe d'entités liées.
    Point d'entrée pour les modifications d'un groupe d'objets liés.
    """

    def __str__(self) -> str:
        return f"<Aggregate({self.__class__.__name__}) | id={self.id}>"


class Event(DomainObject):
    """
    Événement du domaine représentant un fait qui s'est produit dans le système.
    Utilisé pour propager les changements et la communication asynchrone.
    """

    occurred_at: datetime = Field(default_factory=lambda: datetime.utcnow())

    def __str__(self) -> str:
        return f"<Event({self.__class__.__name__}) | {self.model_dump()}>"

    def to_message(self) -> bytes:
        """Sérialise l'événement pour le bus de messages"""
        data = self.model_dump()
        data["__type__"] = self.__class__.__name__
        return json.dumps(data, default=pydantic_encoder).encode("utf-8")


class Command(DomainObject):
    """
    Commande représentant une intention de changer l'état du système.
    Utilisée dans le pattern CQRS pour encapsuler une demande de changement.
    """

    issued_at: datetime = Field(default_factory=lambda: datetime.utcnow())

    def __str__(self) -> str:
        return f"<Command({self.__class__.__name__}) | {self.model_dump()}>"

    def to_message(self) -> bytes:
        """Sérialise la commande pour le bus de messages"""
        data = self.model_dump()
        data["__type__"] = self.__class__.__name__
        return json.dumps(data, default=pydantic_encoder).encode("utf-8")


# Type pour représenter un message qui peut être soit un événement soit une commande
Message = Union[Event, Command]

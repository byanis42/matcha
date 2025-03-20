import os
import shutil
import uuid
from typing import Optional, BinaryIO, List, Dict, Any


class StorageService:
    """
    Service de stockage de fichiers (images, etc.)
    Gère le stockage, la récupération et la suppression de fichiers.
    """

    def __init__(self):
        self.storage_path = os.environ.get("STORAGE_PATH", "./storage")
        self.max_file_size = 5 * 1024 * 1024  # 5 MB par défaut

        # Créer le dossier de stockage s'il n'existe pas
        os.makedirs(self.storage_path, exist_ok=True)

    async def save_file(self, file_content: BinaryIO, file_name: Optional[str] = None,
                        directory: Optional[str] = None) -> str:
        """
        Sauvegarde un fichier et retourne son identifiant unique.
        """
        # Générer un identifiant unique si aucun nom de fichier n'est fourni
        if file_name is None:
            file_extension = ".jpg"  # Extension par défaut
            file_name = f"{uuid.uuid4()}{file_extension}"

        # Déterminer le chemin complet du fichier
        target_dir = os.path.join(self.storage_path, directory or "")
        os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(target_dir, file_name)

        # Écrire le contenu du fichier
        with open(file_path, "wb") as target_file:
            # Copier le contenu en morceaux pour éviter de charger tout en mémoire
            shutil.copyfileobj(file_content, target_file)

        # Retourner le chemin relatif pour pouvoir le référencer plus tard
        relative_path = os.path.join(directory or "", file_name)
        return relative_path

    async def get_file_path(self, file_id: str) -> str:
        """
        Retourne le chemin complet d'un fichier à partir de son identifiant.
        """
        return os.path.join(self.storage_path, file_id)

    async def delete_file(self, file_id: str) -> bool:
        """
        Supprime un fichier et retourne True si réussi, False sinon.
        """
        file_path = await self.get_file_path(file_id)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    async def list_files(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Liste tous les fichiers dans un répertoire donné.
        """
        target_dir = os.path.join(self.storage_path, directory or "")

        if not os.path.exists(target_dir):
            return []

        files = []
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            if os.path.isfile(file_path):
                file_stats = os.stat(file_path)
                files.append({
                    "name": file_name,
                    "path": os.path.join(directory or "", file_name),
                    "size": file_stats.st_size,
                    "created_at": file_stats.st_ctime,
                    "modified_at": file_stats.st_mtime,
                })

        return files

from typing import Optional, BinaryIO, List, Dict, Any
import uuid


class MockStorageService:
    """
    Version simulée du service de stockage pour les tests.
    Stocke les fichiers en mémoire plutôt que sur disque.
    """

    def __init__(self):
        self.files: Dict[str, bytes] = {}  # Stockage en mémoire des fichiers
        self.file_metadata: Dict[str, Dict[str, Any]] = {}  # Métadonnées des fichiers

    async def save_file(self, file_content: BinaryIO, file_name: Optional[str] = None,
                        directory: Optional[str] = None) -> str:
        """
        Simule la sauvegarde d'un fichier en le stockant en mémoire.
        """
        # Générer un identifiant unique si aucun nom de fichier n'est fourni
        if file_name is None:
            file_extension = ".jpg"  # Extension par défaut
            file_name = f"{uuid.uuid4()}{file_extension}"

        # Créer un chemin virtuel pour le fichier
        file_path = f"{directory or ''}/{file_name}"

        # Lire et stocker le contenu du fichier
        content = file_content.read()
        if isinstance(content, str):
            content = content.encode('utf-8')

        self.files[file_path] = content

        # Stocker les métadonnées
        self.file_metadata[file_path] = {
            "name": file_name,
            "directory": directory or "",
            "size": len(content),
            "created_at": 1234567890,  # Timestamp fictif
            "modified_at": 1234567890,  # Timestamp fictif
        }

        return file_path

    async def get_file_path(self, file_id: str) -> str:
        """
        Retourne le chemin virtuel d'un fichier.
        """
        return file_id if file_id in self.files else None

    async def delete_file(self, file_id: str) -> bool:
        """
        Simule la suppression d'un fichier.
        """
        if file_id in self.files:
            del self.files[file_id]
            if file_id in self.file_metadata:
                del self.file_metadata[file_id]
            return True
        return False

    async def list_files(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Liste tous les fichiers simulés dans un répertoire donné.
        """
        files = []
        dir_prefix = f"{directory or ''}/"

        for file_path, metadata in self.file_metadata.items():
            if directory is None or file_path.startswith(dir_prefix):
                files.append({
                    "name": metadata["name"],
                    "path": file_path,
                    "size": metadata["size"],
                    "created_at": metadata["created_at"],
                    "modified_at": metadata["modified_at"],
                })

        return files

    def clear_storage(self):
        """
        Efface tous les fichiers simulés.
        """
        self.files.clear()
        self.file_metadata.clear()

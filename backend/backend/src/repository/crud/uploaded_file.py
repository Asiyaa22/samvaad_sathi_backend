from typing import Optional
from src.models.db.uploaded_file import UploadedFile
from src.repository.crud.base import BaseCRUDRepository

class UploadedFileCRUDRepository(BaseCRUDRepository):
    async def create_uploaded_file(
        self,
        original_file_name: str,
        stored_file_name: str,
        file_type: str,
        file_size: int,
        file_path: str,
        purpose: Optional[str] = None
    ) -> UploadedFile:
        new_file = UploadedFile(
            original_file_name=original_file_name,
            stored_file_name=stored_file_name,
            file_type=file_type,
            file_size=file_size,
            file_path=file_path,
            purpose=purpose
        )
        self.async_session.add(new_file)
        await self.async_session.flush()
        return new_file

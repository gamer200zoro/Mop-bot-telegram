class SupabaseStorage:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key

    async def upload_file(self, bucket: str, path: str, file_data: bytes) -> str:
        return "File upload not yet implemented."

    async def download_file(self, bucket: str, path: str) -> bytes:
        return b"File download not yet implemented."

from fastapi import FastAPI

class CustomFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.qdrant_handler = None
        self.document_service = None
        self.qa_service = None
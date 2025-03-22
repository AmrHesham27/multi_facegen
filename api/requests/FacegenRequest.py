from pydantic import BaseModel

class FacegenRequest(BaseModel):
    key: str
    prompt: str
    negative_prompt: str = None
    face_image: str
    width: str = None
    height: str = None
    #samples: int = None
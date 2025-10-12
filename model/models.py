from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union

class MetaData(BaseModel):
    Summary: List[str]= Field(default_factory=list, description="Summary of the document")
    Title: str
    Author: str
    DataCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    Pagecount: Union[int, str]
    SentimentTone: str
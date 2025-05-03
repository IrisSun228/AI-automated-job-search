from typing import List, Optional

from pydantic import BaseModel


class Job(BaseModel):
    id: Optional[str] = None
    location: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    jobProvider: Optional[str] = None
    url: Optional[str] = None
    rating: Optional[int] = None
    rating_description: Optional[str] = None
    # company_rating: Optional[int] 
    # company_rating_description: Optional[str]  

    
class JobResults(BaseModel): 
    jobs: Optional[List[Job]]

from pydantic import BaseModel, Field
from typing import List, Optional

class JobDetails(BaseModel):
    company_name: str = Field(description="The name of the company.")
    title: str = Field(description="Job title.")
    company_website: Optional[str] = Field(description="The website of the company.")
    mails: List[str] = Field(description="Mails of people working in the company that can be contacted for a job.")
    company_summary: str = Field(description="A brief 2-liner summary of what the company does and how my job is connected to it.")
    company_location: List[str] = Field(description="The location of the company. This can be a list if there are multiple locations with the first one being the HQ.")
    company_domain: str = Field(description="The specific industry or domain the company operates in (e.g., FinTech, SaaS, Healthcare).")
    recent_feature: str = Field(description="A recent product or feature the company has launched or is working on that is exciting.")
    metadata: Optional[dict] = Field(description="Extra details about the company that you deem relevant.")
    summary: str = Field(description="A 3-liner summary of the job and company that will eventually be used in my cover letter.")

class JobList(BaseModel):
    jobs: List[JobDetails]
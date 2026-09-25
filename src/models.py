from dataclasses import dataclass

@dataclass
class JobPosting:
    company: str
    job_id: str
    title: str
    location: str
    apply_url: str
    posted_date: str
    
    @property
    def unique_id(self) -> str:
        """Restituisce un identificativo globale univoco per evitare collisioni tra aziende diverse"""
        return f"{self.company.lower()}:{self.job_id}"
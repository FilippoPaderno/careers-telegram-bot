from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import httpx
from src.models import JobPosting

class MicrosoftCareersClient:
    """Client per estrarre le offerte di lavoro dal portale Microsoft Careers."""
    
    BASE_URL= "https://apply.careers.microsoft.com"
    SEARCH_ENDPOINT = "https://apply.careers.microsoft.com/api/pcsx/search"
    
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9,it;q=0.8",
    }
    
    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout
    
    def fetch_jobs(self, query: str = "", location: str = "Italy", seniority: Optional[str] = "Intern",) -> List[JobPosting]:
        """Interroga l'API di Microsoft e restituisce una lista di oggetti JobPosting universali."""
        #utilizziamo un client di sessione
        with httpx.Client(
            headers=self.DEFAULT_HEADERS,
            timeout=self.timeout,
            follow_redirects=True
        ) as client:
            
            #handshake iniziale per ottenere i cookie e il token
            init_res = client.get(f"{self.BASE_URL}/careers")
            init_res.raise_for_status()
            csrf_token = init_res.headers.get("x-csrf-token", "")
            
            search_headers = {
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.BASE_URL}/careers",
            }
            if csrf_token:
                search_headers["x-csrf-token"] = csrf_token
                
            params: Dict[str, Any] = {
                "domain": "microsoft.com",
                "start": 0,
                "num": 50,
            }
            
            if query:
                params["query"] = query
            if location:
                params["location"] = location
            if seniority:
                params["filter_seniority"] = seniority
            
            response = client.get(
                self.SEARCH_ENDPOINT,
                params=params,
                headers=search_headers
            )
            response.raise_for_status()
            data = response.json()
            
        positions_raw = data.get("data", {}).get("positions", [])
        job_postings: List[JobPosting] = []
        
        for pos in positions_raw:
            job_id = str(pos.get("id") or pos.get("displayJobId") or "").strip()
            title = pos.get("name", "Titolo non disponibile").strip()
            locations_list = pos.get("locations") or []
            job_loc = locations_list[0] if locations_list else "Sede non specificata"
            
            posted_ts = pos.get("postedTs")
            if posted_ts:
                posted_date = datetime.fromtimestamp(posted_ts, tz=timezone.utc).strftime("%Y-%m-%d")
            else:
                posted_date = "Data recente"
                
            pos_path = pos.get("positionUrl") or f"/careers/job/{job_id}"
            apply_url = f"{self.BASE_URL}{pos_path}"
            
            posting = JobPosting(
                company="Microsoft",
                job_id=job_id,
                title=title,
                location=job_loc,
                apply_url=apply_url,
                posted_date=posted_date,
            )
            job_postings.append(posting)
            
        return job_postings
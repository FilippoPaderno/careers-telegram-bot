import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    telegram_bot_token: str
    telegram_chat_id: str
    search_location: str
    search_seniority: str
    search_query: str
    
    @classmethod
    def load(cls) -> "Config":
        """Legge le variabili d'ambiente e crea l'oggetto Config."""
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
        location = os.getenv("SEARCH_LOCATION", "Italy").strip()
        seniority = os.getenv("SEARCH_SENIORITY", "Intern").strip()
        query = os.getenv("SEARCH_QUERY", "").strip()
        
        #controlliamo che non siano vuote
        if not token:
            raise ValueError("Bot token non impostato nel .env")
        if not chat_id:
            raise ValueError("Chat id non impostato nel .env")
    
        return cls(
            telegram_bot_token = token,
            telegram_chat_id = chat_id,
            search_location = location,
            search_seniority = seniority,
            search_query = query,
        )
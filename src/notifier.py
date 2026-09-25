import html
import httpx
from src.models import JobPosting

class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str, timeout: float = 15.0):
         self.bot_token = bot_token
         self.chat_id = chat_id
         self.timeout = timeout
         #indirizzo web a cui fare la richiesta
         self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
         
    def send_message(self, text: str) -> bool:
        """Invia un messaggio formattato in HTML alla chat Telegram."""
        #pacchetto dati per telegram
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False #Mostra l'anteprima del link se disponibile
        }
        
        try:
            #creiamo un client HTTP temporaneo con timeout di sicurezza
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(self.api_url, json=payload)
                #verifica che telegram abbia risposto in modo positivo
                response.raise_for_status()
                return True
        except Exception as exc:
            print(f"[ERRORE TELEGRAM] Impossibile inviare il messaggio: {exc}")
            return False
    
    def notify_job(self, job: JobPosting) -> bool:
        """Formatta un annuncio di lavoro in HTML e lo invia su Telegram."""
        safe_title = html.escape(job.title)
        safe_company = html.escape(job.company)
        safe_location = html.escape(job.location)
        safe_date = html.escape(job.posted_date)
        
        message = (
            f"🎯 <b>Nuova Posizione: {safe_company}!</b>\n\n"
            f"💼 <b>Ruolo:</b> {safe_title}\n"
            f"📍 <b>Sede:</b> {safe_location}\n"
            f"📅 <b>Data:</b> {safe_date}\n\n"
            f"👉 <a href=\"{job.apply_url}\"><b>Clicca qui per candidarti</b></a>"
        )
        
        return self.send_message(message)
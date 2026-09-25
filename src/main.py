import time
from pathlib import Path
from src.config import Config
from src.client import MicrosoftCareersClient
from src.notifier import TelegramNotifier
from src.storage import LocalStorage

def main() -> None:
    print("=" * 50)
    print("🚀 Avvio controllo Microsoft Careers...")
    print("=" * 50)
    
    #carichiamo configurazione .env
    config = Config.load()
    
    #inizializziamo i moduli
    storage = LocalStorage(Path("data/seen_jobs.json"))
    client = MicrosoftCareersClient()
    notifier = TelegramNotifier(
        bot_token= config.telegram_bot_token,
        chat_id=config.telegram_chat_id
    )
    
    print(f"Filtri attivi: Location='{config.search_location}', Seniority='{config.search_seniority}'")
    
    #prendiamo gli annunci da Microsoft
    current_jobs = client.fetch_jobs(
        query=config.search_query,
        location=config.search_location,
        seniority=config.search_seniority
    )
    print(f"Annunci trovati sul portale: {len(current_jobs)}")
    
    if storage.is_first_run():
        print("[PRIMO AVVIO] Inizializzazione della memoria del bot")
        
        initial_ids = [job.unique_id for job in current_jobs]
        if initial_ids:
            storage.add_seen(initial_ids)
        
        storage.mark_as_initialized()
        
        #invio messaggio di benvenuto
        welcome_message = (
            f"🤖 <b>Microsoft Careers Bot Attivato!</b>\n\n"
            f"• <b>Sede monitorata:</b> {config.search_location}\n"
            f"• <b>Livello:</b> {config.search_seniority}\n"
            f"• <b>Posizioni attualmente online:</b> {len(current_jobs)}\n\n"
            f"🟢 <i>Da questo momento riceverai una notifica non appena Microsoft pubblicherà un nuovo annuncio!</i>"
        )
        notifier.send_message(welcome_message)
        print("✅ Inizializzazione completata e notifica di benvenuto inviata!")
        return

    #prendiamo i job il cui unique_id non è presente nello storage
    new_jobs = [job for job in current_jobs if not storage.is_seen(job.unique_id)]
        
    if new_jobs:
        print(f"🎉 Trovate {len(new_jobs)} NUOVE offerte! Invio notifiche...")
        for job in new_jobs:
            success = notifier.notify_job(job)
            if success:
                storage.add_seen([job.unique_id])
                print(f" -> Notificato: {job.title}")
                    
            time.sleep(1.0)
    else:
        print("💤 Nessuna nuova posizione pubblicata rispetto all'ultimo controllo.")
    
    print("Controllo completato con successo.")

if __name__ == "__main__":
    main()
# Microsoft Careers Internship Monitor

Un bot in Python che monitora il portale Microsoft Careers e invia una notifica su Telegram quando viene pubblicata una nuova posizione di tirocinio (Internship).


## 📌 Perché questo progetto?

Volevo tenere d'occhio eventuali posizioni di stage/internship in Microsoft (in particolare in Italia) senza dover controllare manualmente il sito ogni settimana. 

Ho quindi creato questo script per automatizzare il controllo: il bot interroga periodicamente il portale e mi invia un messaggio su Telegram non appena viene pubblicata una nuova opportunità.


## ⚙️ Come funziona

1. **Ricerca**: interroga le API del portale Microsoft Careers (`apply.careers.microsoft.com`).
2. **Filtro**: cerca le offerte con livello di esperienza `Intern` per la sede desiderata (es. `Italy`).
3. **Memoria anti-duplicati**: confronta i risultati con il file `data/seen_jobs.json` per evitare di inviare più volte lo stesso annuncio.
4. **Notifica**: se trova un annuncio nuovo, invia un messaggio su Telegram con titolo, sede e link diretto alla candidatura.
5. **Esecuzione in cloud**: tramite GitHub Actions, lo script può girare automaticamente ogni 30 minuti senza dover tenere acceso il computer.


## 📁 Struttura del codice

* `src/models.py`: definizione della classe `JobPosting` con ID univoco.
* `src/storage.py`: gestione della lettura e del salvataggio dei dati su `data/seen_jobs.json`.
* `src/config.py`: lettura delle variabili d'ambiente e dei filtri di ricerca.
* `src/client.py`: chiamate HTTP all'API di Microsoft Careers.
* `src/notifier.py`: invio dei messaggi formattati a Telegram.
* `src/main.py`: orchestratore che collega tutti i moduli.
* `.github/workflows/monitor.yml`: automazione per l'esecuzione periodica su GitHub Actions.


## 🚀 Configurazione e Avvio

### 1. Requisiti Telegram
* Crea un bot con `@BotFather` su Telegram e copia il tuo `TELEGRAM_BOT_TOKEN`.
* Ottieni il tuo ID utente con `@userinfobot` per il `TELEGRAM_CHAT_ID`.
* Avvia la chat con il bot appena creato premendo su **Start**.

### 2. Esecuzione in locale
Installa le dipendenze:
```bash
pip install -r requirements.txt
```

Crea il file `.env` nella cartella principale con i tuoi parametri:
```env
TELEGRAM_BOT_TOKEN=il_tuo_token_qui
TELEGRAM_CHAT_ID=il_tuo_chat_id_qui
SEARCH_LOCATION=Italy
SEARCH_SENIORITY=Intern
SEARCH_QUERY=
```

Avvia il monitor:
```bash
python -m src.main
```

### 3. Esecuzione in cloud con GitHub Actions
1. Carica il repository su GitHub.
2. Vai in **Settings** > **Secrets and variables** > **Actions** e aggiungi:
   * `TELEGRAM_BOT_TOKEN`
   * `TELEGRAM_CHAT_ID`
3. In **Settings** > **Actions** > **General** > **Workflow permissions**, seleziona **Read and write permissions** per consentire al bot di salvare lo storico degli annunci visti.

Il workflow si attiverà automaticamente ogni 30 minuti.

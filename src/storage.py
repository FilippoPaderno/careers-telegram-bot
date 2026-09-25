import json
from pathlib import Path
from typing import Set, List

class LocalStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.seen_job_ids: Set[str] = set()
        self.is_initialized: bool = False
        self.load()
    
    def load(self) -> None:
        """Legge il file JSON. Se il file non esiste ancora, lo crea vuoto."""
        #se il file non esiste
        if not self.file_path.exists():
            self.save() #crea il file vuoto
            return

        #se esiste, lo aprimo in lettura
        #with open garantisce che il file venga chiuso automaticamente alla fine della lettura
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.seen_job_ids = set(data.get("seen_job_ids", [])) #prende la chiave seen_job_ids, se non ce da una lista vuota
            self.is_initialized = data.get("is_initialized", False)
            
    def save(self) -> None:
        """Salva lo stato corrente nel file JSON."""
        #si assicura che la cartella data/ esista
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        #Trasformiamo il set in una lista
        data = {
            "seen_job_ids": sorted(list(self.seen_job_ids)),
            "total_seen_count": len(self.seen_job_ids),
            "is_initialized": self.is_initialized
        }
        
        #apriamo in scrittura e salviamo
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def is_seen(self, unique_id: str) -> bool:
        """Restituisce True se l'annuncio è già presente nel set, False altrimenti."""
        return unique_id in self.seen_job_ids
    
    def add_seen(self, unique_ids: List[str]) -> None:
        """Aggiunge una lista di nuovi ID al set e salva subito su disco."""
        for uid in unique_ids:
            self.seen_job_ids.add(uid)
        self.save()
    
    def is_first_run(self) -> bool:
        """Restituisce True se la memoria è completamente vuota (primo avvio)."""
        return not self.is_initialized
    
    def mark_as_initialized(self) -> bool:
        self.is_initialized = True
        self.save()
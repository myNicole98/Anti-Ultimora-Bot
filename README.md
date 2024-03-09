# Anti Ultimora Bot
<img src="assets/logo.jpg"/></br>

#
Anti Ultimora Bot è un bot Telegram progettato per eliminare i messaggi inoltrati da canali di notizie di ultim'ora. Repository ufficiale di https://t.me/antiultimorabot

## Funzionalità

- **Rilevamento degli inoltri da ultim'ora:** Il bot monitora i messaggi inoltrati nelle chat in cui è attivo e identifica quelli provenienti da canali di ultim'ora.
  
- **Cancellazione automatica:** I messaggi inoltrati riconosciuti come provenienti da ultim'ora vengono cancellati automaticamente per mantenere pulita la chat.

- **Utilizzo di cosine similarity:** Oltre al rilevamento diretto, il bot utilizza il calcolo del cosine similarity per identificare i messaggi simili a quelli di ultim'ora anche se non inoltrati direttamente.

## Requisiti

- Python 3.11
- pip

## Installazione

- Clona la repository
> git clone https://gitea.nikko.eu.org/nikko/Anti-Ultimora-Bot

- Entra nella directory clonata
> cd Anti-Ultimora-Bot

- Installa i requisiti
> pip install -r requirements.txt


## Utilizzo

1. Aggiungi il bot al gruppo di Telegram in cui desideri eliminare i messaggi e promuovilo ad admin
   
2. Avvia il bot
> python main.py

## Contributi

Sono benvenuti contributi e suggerimenti per migliorare le funzionalità del bot.

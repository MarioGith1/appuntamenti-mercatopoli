# 📅 Appuntamenti Mercatopoli

Sistema completo di prenotazioni appuntamenti per Mercatopoli Lucca.

## 🚀 Avvio Rapido

### 1. Avvio Automatico
```bash
# Doppio clic su
AVVIO_APP.bat
```

### 2. Avvio Manuale
```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia app
streamlit run app.py
```

## 🔐 Accesso

### URL: http://localhost:8501

### Utente Test:
- **Email:** marioddamonte@gmail.com
- **Password:** password123

## 📋 Funzionalità

### ✅ Utenti
- Registrazione nuovi utenti
- Login sicuro con password hash
- Gestione profilo

### ✅ Appuntamenti
- Prenotazione appuntamenti
- Visualizzazione appuntamenti personali
- Gestione orari e categorie

### ✅ Lista Attesa
- Iscrizione lista attesa
- Visualizzazione lista attesa
- Gestione per categoria

### ✅ Database
- Google Sheets integration
- Dati persistenti
- Backup automatico

## 🏗️ Architettura

### 📱 Frontend
- **Streamlit** - Interfaccia utente
- **Responsive** - Funziona su tutti i dispositivi
- **Session state** - Gestione sessioni utente

### 🖥️ Backend
- **Python** - Logica business
- **Google Sheets API** - Database
- **OAuth2** - Autenticazione sicura

### 📊 Database
- **Google Sheets** - Storage principale
- **Clienti** - Gestione utenti
- **Appuntamenti** - Calendario prenotazioni
- **ListaAttesa** - Coda attesa
- **PasswordResets** - Reset password

## 🔧 Configurazione

### Google Sheets Setup
1. Crea progetto Google Cloud
2. Abilita Google Sheets API
3. Crea service account
4. Scarica credentials.json
5. Condividi Google Sheet con service account

### Struttura Google Sheet
```
Appuntamenti_Mercatopoli
├── Clienti (Email, Password, Nome, Cellulare, ...)
├── Appuntamenti (Email, Data, Ora, Categoria, ...)
├── ListaAttesa (Email, Categoria, DataAggiunta)
└── PasswordResets (Email, Token, DataScadenza)
```

## 🛠️ Sviluppo

### Dipendenze
```
streamlit==1.28.1
gspread==5.7.2
oauth2client==4.1.3
pandas==1.5.3
google-api-python-client==2.108.0
google-auth-httplib2==0.1.1
google-auth-oauthlib==1.1.0
requests==2.31.0
```

### Struttura File
```
App_puntamenti/
├── app.py              # Applicazione principale
├── requirements.txt    # Dipendenze Python
├── credentials.json    # Credenziali Google Cloud
├── AVVIO_APP.bat      # Batch avvio automatico
└── README.md          # Documentazione
```

## 🚀 Deploy

### Streamlit Cloud
1. Push su GitHub
2. Connetti Streamlit Cloud
3. Configura secrets

### VPS/Server
1. Installa Python e pip
2. Clona repository
3. Installa dipendenze
4. Avvia con systemd/supervisor

## 🔒 Sicurezza

### Password Hash
- PBKDF2 con salt
- 100.000 iterazioni
- SHA-256 algorithm

### OAuth2
- Service account authentication
- Token-based access
- Secure credential storage

## 📞 Supporto

Per assistenza tecnica:
- Controlla log errori
- Verifica connessione Google Sheets
- Controlla configurazione credentials.json

## 🔄 Aggiornamenti

### Versione 1.0
- Sistema base di prenotazioni
- Google Sheets integration
- Gestione utenti e appuntamenti

### Prossime versioni
- Notifiche email
- Calendario sincronizzato
- Dashboard admin
- Mobile app

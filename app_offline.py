# 🏥 APPUNTAMENTI MERCATOPOLI - VERSIONE OFFLINE

import streamlit as st
import json
from datetime import datetime, timedelta
import hashlib
import secrets
import pandas as pd

# --- DATABASE FAKE ---
USERS_DB = {
    "marioddamonte@gmail.com": {
        "password": "password123",
        "nome": "Mario Rossi",
        "cellulare": "3331234567",
        "livello": "1"
    }
}

APPOINTMENTS_DB = []
WAITING_LIST_DB = []

# --- DATABASE MANAGER ---
class DatabaseManager:
    def __init__(self):
        pass
    
    def hash_password(self, password: str) -> str:
        """Hash password con salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${password_hash.hex()}"
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica password hash"""
        try:
            salt, stored_hash = hashed_password.split('$')
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash.hex() == stored_hash
        except:
            return False
    
    def get_user(self, email: str):
        """Ottieni utente da email"""
        return USERS_DB.get(email)
    
    def create_user(self, email: str, password: str, nome: str, cellulare: str):
        """Crea nuovo utente"""
        USERS_DB[email] = {
            "password": password,
            "nome": nome,
            "cellulare": cellulare,
            "livello": "1"
        }
        return True
    
    def verify_login(self, email: str, password: str):
        """Verifica login"""
        user = self.get_user(email)
        if user and user["password"] == password:
            return user
        return None
    
    def get_appuntamenti_giorno(self, data: str):
        """Ottieni appuntamenti per giorno"""
        return [a for a in APPOINTMENTS_DB if a.get('data') == data]
    
    def create_appuntamento(self, email: str, data: str, ora: str, categoria: str):
        """Crea appuntamento"""
        APPOINTMENTS_DB.append({
            "email": email,
            "data": data,
            "ora": ora,
            "categoria": categoria,
            "stato": "Prenotato",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return True
    
    def get_lista_attesa(self, categoria: str = None):
        """Ottieni lista attesa"""
        if categoria:
            return [w for w in WAITING_LIST_DB if w.get('categoria') == categoria]
        return WAITING_LIST_DB
    
    def aggiungi_lista_attesa(self, email: str, categoria: str):
        """Aggiungi alla lista attesa"""
        WAITING_LIST_DB.append({
            "email": email,
            "categoria": categoria,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return True

# --- INTERFACCIA UTENTE ---
def show_login():
    """Pagina login"""
    st.title("🔐 Login - Appuntamenti Mercatopoli")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Inserisci la tua email")
        password = st.text_input("🔑 Password", type="password", placeholder="Inserisci la tua password")
        
        if st.form_submit_button("🚀 Accedi"):
            if email and password:
                db = DatabaseManager()
                user = db.verify_login(email, password)
                
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(f"✅ Bentornato {user.get('nome', '')}!")
                    st.rerun()
                else:
                    st.error("❌ Email o password non validi")
            else:
                st.error("❌ Compila tutti i campi")

def show_registration():
    """Pagina registrazione"""
    st.title("📝 Registrazione - Nuovo Utente")
    
    with st.form("register_form"):
        email = st.text_input("📧 Email", placeholder="Inserisci la tua email")
        password = st.text_input("🔑 Password", type="password", placeholder="Crea una password")
        confirm_password = st.text_input("🔑 Conferma Password", type="password", placeholder="Conferma la password")
        nome = st.text_input("👤 Nome Completo", placeholder="Inserisci il tuo nome")
        cellulare = st.text_input("📱 Cellulare", placeholder="Inserisci il tuo numero")
        
        if st.form_submit_button("📝 Registrati"):
            if email and password and confirm_password and nome and cellulare:
                if password != confirm_password:
                    st.error("❌ Le password non coincidono")
                elif len(password) < 8:
                    st.error("❌ La password deve avere almeno 8 caratteri")
                else:
                    db = DatabaseManager()
                    if db.get_user(email):
                        st.error("❌ Email già registrata")
                    else:
                        if db.create_user(email, password, nome, cellulare):
                            st.success("✅ Registrazione completata! Ora puoi fare il login")
                            st.session_state.show_login = True
                            st.rerun()
                        else:
                            st.error("❌ Errore durante la registrazione")
            else:
                st.error("❌ Compila tutti i campi")

def show_dashboard():
    """Dashboard principale"""
    user = st.session_state.user
    st.title(f"📅 Appuntamenti - Benvenuto {user.get('nome', '')}")
    
    # Sidebar
    st.sidebar.success(f"👋 Ciao {user.get('nome', '')}")
    st.sidebar.write(f"📧 {st.session_state.user_email}")
    st.sidebar.write(f"📱 {user.get('cellulare', '')}")
    
    # Menu
    scelta = st.selectbox("📋 Cosa vuoi fare?", [
        "📅 Prenota Appuntamento",
        "⏳ Lista d'Attesa",
        "📊 I Miei Appuntamenti",
        "🚪 Esci"
    ])
    
    if scelta == "📅 Prenota Appuntamento":
        show_prenota_appuntamento()
    elif scelta == "⏳ Lista d'Attesa":
        show_lista_attesa()
    elif scelta == "📊 I Miei Appuntamenti":
        show_miei_appuntamenti()
    elif scelta == "🚪 Esci":
        st.session_state.clear()
        st.rerun()

def show_prenota_appuntamento():
    """Prenota appuntamento"""
    st.subheader("📅 Prenota Nuovo Appuntamento")
    
    with st.form("prenota_form"):
        data = st.date_input("📅 Data", min_value=datetime.today())
        ora = st.selectbox("⏰ Orario", ["09:00", "10:00", "11:00", "12:00", "15:00", "16:00", "17:00"])
        categoria = st.selectbox("📦 Categoria", ["Abbigliamento", "Oggettistica"])
        
        if st.form_submit_button("📅 Prenota"):
            db = DatabaseManager()
            data_str = data.strftime('%Y-%m-%d')
            
            if db.create_appuntamento(st.session_state.user_email, data_str, ora, categoria):
                st.success("✅ Appuntamento prenotato con successo!")
            else:
                st.error("❌ Errore durante la prenotazione")

def show_lista_attesa():
    """Lista attesa"""
    st.subheader("⏳ Lista d'Attesa")
    
    db = DatabaseManager()
    lista = db.get_lista_attesa()
    
    if lista:
        df = pd.DataFrame(lista)
        st.dataframe(df)
    else:
        st.info("📭 Nessuno in lista d'attesa")
    
    with st.form("aggiungi_lista_form"):
        categoria = st.selectbox("📦 Categoria", ["Abbigliamento", "Oggettistica"])
        
        if st.form_submit_button("⏳ Aggiungi alla Lista"):
            db = DatabaseManager()
            if db.aggiungi_lista_attesa(st.session_state.user_email, categoria):
                st.success("✅ Aggiunto alla lista d'attesa!")
            else:
                st.error("❌ Errore durante l'aggiunta")

def show_miei_appuntamenti():
    """Mostra appuntamenti utente"""
    st.subheader("📊 I Miei Appuntamenti")
    
    db = DatabaseManager()
    oggi = datetime.now().strftime('%Y-%m-%d')
    appuntamenti = db.get_appuntamenti_giorno(oggi)
    
    # Filtra per utente corrente
    miei_appuntamenti = [a for a in appuntamenti if a.get('email') == st.session_state.user_email]
    
    if miei_appuntamenti:
        df = pd.DataFrame(miei_appuntamenti)
        st.dataframe(df)
    else:
        st.info("📭 Nessun appuntamento per oggi")

# --- MAIN ---
def main():
    st.set_page_config(
        page_title="Appuntamenti Mercatopoli",
        page_icon="📅",
        layout="wide"
    )
    
    # Session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""
    
    # Routing
    if not st.session_state.logged_in:
        if st.session_state.show_login:
            show_login()
        else:
            show_registration()
        
        # Link tra pagine
        if st.session_state.show_login:
            st.markdown("---")
            if st.button("📝 Non hai un account? Registrati"):
                st.session_state.show_login = False
                st.rerun()
        else:
            st.markdown("---")
            if st.button("🔐 Hai già un account? Accedi"):
                st.session_state.show_login = True
                st.rerun()
    else:
        # Salva email utente
        if st.session_state.user and not st.session_state.user_email:
            st.session_state.user_email = st.session_state.user.get('email', '')
        show_dashboard()

if __name__ == "__main__":
    main()

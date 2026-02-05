# 🏥 APPUNTAMENTI MERCATOPOLI - VERSIONE MIGLIORATA

import streamlit as st
import json
import os
from datetime import datetime, timedelta
import hashlib
import secrets
import pandas as pd

# --- DATABASE PERSISTENTE SU FILE ---
class FileDatabase:
    def __init__(self):
        self.users_file = "users.json"
        self.appointments_file = "appointments.json"
        self.waiting_list_file = "waiting_list.json"
        self.init_files()
    
    def init_files(self):
        """Inizializza file JSON se non esistono"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.appointments_file):
            with open(self.appointments_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.waiting_list_file):
            with open(self.waiting_list_file, 'w') as f:
                json.dump([], f)
    
    def load_users(self):
        """Carica utenti da file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users):
        """Salva utenti su file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_appointments(self):
        """Carica appuntamenti da file"""
        try:
            with open(self.appointments_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_appointments(self, appointments):
        """Salva appuntamenti su file"""
        with open(self.appointments_file, 'w') as f:
            json.dump(appointments, f, indent=2)
    
    def load_waiting_list(self):
        """Carica lista attesa da file"""
        try:
            with open(self.waiting_list_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_waiting_list(self, waiting_list):
        """Salva lista attesa su file"""
        with open(self.waiting_list_file, 'w') as f:
            json.dump(waiting_list, f, indent=2)

# --- DATABASE MANAGER MIGLIORATO ---
class DatabaseManager:
    def __init__(self):
        self.file_db = FileDatabase()
        self.init_default_user()
    
    def init_default_user(self):
        """Inizializza utente di default se non esiste"""
        users = self.file_db.load_users()
        if "marioddamonte@gmail.com" not in users:
            users["marioddamonte@gmail.com"] = {
                "password": "password123",
                "nome": "Mario Rossi",
                "cellulare": "3331234567",
                "livello": "1",
                "created_at": datetime.now().isoformat()
            }
            self.file_db.save_users(users)
    
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
        users = self.file_db.load_users()
        return users.get(email)
    
    def create_user(self, email: str, password: str, nome: str, cellulare: str):
        """Crea nuovo utente"""
        users = self.file_db.load_users()
        if email in users:
            return False
        
        users[email] = {
            "password": password,  # In produzione usare hash
            "nome": nome,
            "cellulare": cellulare,
            "livello": "1",
            "created_at": datetime.now().isoformat()
        }
        self.file_db.save_users(users)
        return True
    
    def verify_login(self, email: str, password: str):
        """Verifica login"""
        user = self.get_user(email)
        if user and user["password"] == password:
            return user
        return None
    
    def get_appuntamenti_giorno(self, data: str):
        """Ottieni appuntamenti per giorno"""
        appointments = self.file_db.load_appointments()
        return [a for a in appointments if a.get('data') == data]
    
    def create_appuntamento(self, email: str, data: str, ora: str, categoria: str):
        """Crea appuntamento"""
        appointments = self.file_db.load_appointments()
        
        # Controlla se esiste già appuntamento stesso orario
        for a in appointments:
            if a.get('data') == data and a.get('ora') == ora:
                return False
        
        new_appointment = {
            "email": email,
            "data": data,
            "ora": ora,
            "categoria": categoria,
            "stato": "Prenotato",
            "created_at": datetime.now().isoformat()
        }
        
        appointments.append(new_appointment)
        self.file_db.save_appointments(appointments)
        return True
    
    def get_lista_attesa(self, categoria: str = None):
        """Ottieni lista attesa"""
        waiting_list = self.file_db.load_waiting_list()
        if categoria:
            return [w for w in waiting_list if w.get('categoria') == categoria]
        return waiting_list
    
    def aggiungi_lista_attesa(self, email: str, categoria: str):
        """Aggiungi alla lista attesa"""
        waiting_list = self.file_db.load_waiting_list()
        
        # Controlla se utente è già in lista per questa categoria
        for w in waiting_list:
            if w.get('email') == email and w.get('categoria') == categoria:
                return False
        
        new_entry = {
            "email": email,
            "categoria": categoria,
            "created_at": datetime.now().isoformat()
        }
        
        waiting_list.append(new_entry)
        self.file_db.save_waiting_list(waiting_list)
        return True
    
    def get_user_appointments(self, email: str):
        """Ottieni appuntamenti utente"""
        appointments = self.file_db.load_appointments()
        return [a for a in appointments if a.get('email') == email]
    
    def delete_appointment(self, email: str, data: str, ora: str):
        """Elimina appuntamento"""
        appointments = self.file_db.load_appointments()
        appointments = [a for a in appointments if not (
            a.get('email') == email and 
            a.get('data') == data and 
            a.get('ora') == ora
        )]
        self.file_db.save_appointments(appointments)
        return True

# --- INTERFACCIA UTENTE MIGLIORATA ---
def show_login():
    """Pagina login migliorata"""
    st.title("🔐 Login - Appuntamenti Mercatopoli")
    
    # Check if database exists
    if not os.path.exists("users.json"):
        st.info("🔄 Inizializzazione database in corso...")
        db = DatabaseManager()
        st.success("✅ Database pronto!")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Inserisci la tua email")
        password = st.text_input("🔑 Password", type="password", placeholder="Inserisci la tua password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("🚀 Accedi"):
                if email and password:
                    db = DatabaseManager()
                    user = db.verify_login(email, password)
                    
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.user_email = email
                        st.success(f"✅ Bentornato {user.get('nome', '')}!")
                        st.rerun()
                    else:
                        st.error("❌ Email o password non validi")
                else:
                    st.error("❌ Compila tutti i campi")
        
        with col2:
            if st.form_submit_button("📝 Registrati"):
                if email and password:
                    db = DatabaseManager()
                    if db.create_user(email, password, email.split('@')[0], "0000000000"):
                        st.success("✅ Registrazione automatica completata!")
                        st.rerun()
                    else:
                        st.error("❌ Email già registrata")
                else:
                    st.error("❌ Compila tutti i campi")
    
    # Credenziali di test
    st.markdown("---")
    st.info("🧪 **Credenziali di Test:**")
    st.code("📧 Email: marioddamonte@gmail.com\n🔑 Password: password123")

def show_dashboard():
    """Dashboard principale migliorata"""
    user = st.session_state.user
    st.title(f"📅 Appuntamenti - Benvenuto {user.get('nome', '')}")
    
    # Sidebar migliorata
    with st.sidebar:
        st.success(f"👋 Ciao {user.get('nome', '')}")
        st.write(f"📧 {st.session_state.user_email}")
        st.write(f"📱 {user.get('cellulare', '')}")
        st.write(f"🎯 Livello: {user.get('livello', '1')}")
        
        st.markdown("---")
        
        # Statistiche utente
        db = DatabaseManager()
        user_appointments = db.get_user_appointments(st.session_state.user_email)
        user_waiting = db.get_lista_attesa()
        user_waiting_count = len([w for w in user_waiting if w.get('email') == st.session_state.user_email])
        
        st.metric("📅 Appuntamenti", len(user_appointments))
        st.metric("⏳ In Attesa", user_waiting_count)
    
    # Menu principale
    st.markdown("---")
    scelta = st.selectbox("📋 Cosa vuoi fare?", [
        "📅 Prenota Appuntamento",
        "📊 I Miei Appuntamenti", 
        "⏳ Lista d'Attesa",
        "🚪 Esci"
    ])
    
    if scelta == "📅 Prenota Appuntamento":
        show_prenota_appuntamento()
    elif scelta == "📊 I Miei Appuntamenti":
        show_miei_appuntamenti()
    elif scelta == "⏳ Lista d'Attesa":
        show_lista_attesa()
    elif scelta == "🚪 Esci":
        st.session_state.clear()
        st.rerun()

def show_prenota_appuntamento():
    """Prenota appuntamento migliorata"""
    st.subheader("📅 Prenota Nuovo Appuntamento")
    
    db = DatabaseManager()
    
    # Mostra appuntamenti esistenti per oggi
    oggi = datetime.now().strftime('%Y-%m-%d')
    appuntamenti_oggi = db.get_appuntamenti_giorno(oggi)
    
    if appuntamenti_oggi:
        st.info(f"📅 Ci sono già {len(appuntamenti_oggi)} appuntamenti oggi:")
        for a in appuntamenti_oggi:
            st.write(f"• {a.get('ora')} - {a.get('categoria')} ({a.get('email')})")
    
    with st.form("prenota_form"):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("📅 Data", min_value=datetime.today())
        with col2:
            ora = st.selectbox("⏰ Orario", ["09:00", "10:00", "11:00", "12:00", "15:00", "16:00", "17:00"])
        
        categoria = st.selectbox("📦 Categoria", ["Abbigliamento", "Oggettistica"])
        
        if st.form_submit_button("📅 Prenota"):
            data_str = data.strftime('%Y-%m-%d')
            
            if db.create_appuntamento(st.session_state.user_email, data_str, ora, categoria):
                st.success("✅ Appuntamento prenotato con successo!")
                st.balloons()
            else:
                st.error("❌ Orario già occupato o errore durante la prenotazione")

def show_miei_appuntamenti():
    """Mostra appuntamenti utente migliorata"""
    st.subheader("📊 I Miei Appuntamenti")
    
    db = DatabaseManager()
    appointments = db.get_user_appointments(st.session_state.user_email)
    
    if appointments:
        # Filtra solo futuri
        oggi = datetime.now().strftime('%Y-%m-%d')
        futuri = [a for a in appointments if a.get('data') >= oggi]
        
        if futuri:
            df = pd.DataFrame(futuri)
            df['Data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
            df = df[['Data', 'ora', 'categoria', 'stato']]
            df.columns = ['Data', 'Orario', 'Categoria', 'Stato']
            
            st.dataframe(df, use_container_width=True)
            
            # Opzione cancellazione
            st.markdown("---")
            st.warning("⚠️ Per cancellare un appuntamento, contatta l'amministrazione")
        else:
            st.info("📭 Nessun appuntamento futuro")
    else:
        st.info("📭 Nessun appuntamento trovato")

def show_lista_attesa():
    """Lista attesa migliorata"""
    st.subheader("⏳ Lista d'Attesa")
    
    db = DatabaseManager()
    
    # Mostra tutta la lista
    lista = db.get_lista_attesa()
    
    if lista:
        df = pd.DataFrame(lista)
        df['Data Aggiunta'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
        df = df[['email', 'categoria', 'Data Aggiunta']]
        df.columns = ['Email', 'Categoria', 'Data Aggiunta']
        
        st.dataframe(df, use_container_width=True)
        
        # Controlla se utente è già in lista
        user_in_list = [w for w in lista if w.get('email') == st.session_state.user_email]
        
        if user_in_list:
            st.warning(f"⚠️ Sei già in lista attesa per: {', '.join([w.get('categoria') for w in user_in_list])}")
        else:
            with st.form("aggiungi_lista_form"):
                categoria = st.selectbox("📦 Categoria", ["Abbigliamento", "Oggettistica"])
                
                if st.form_submit_button("⏳ Aggiungi alla Lista"):
                    if db.aggiungi_lista_attesa(st.session_state.user_email, categoria):
                        st.success("✅ Aggiunto alla lista d'attesa!")
                        st.rerun()
                    else:
                        st.error("❌ Sei già in lista per questa categoria")
    else:
        st.info("📭 Nessuno in lista d'attesa")
        
        with st.form("aggiungi_lista_form"):
            categoria = st.selectbox("📦 Categoria", ["Abbigliamento", "Oggettistica"])
            
            if st.form_submit_button("⏳ Aggiungi alla Lista"):
                db = DatabaseManager()
                if db.aggiungi_lista_attesa(st.session_state.user_email, categoria):
                    st.success("✅ Aggiunto alla lista d'attesa!")
                    st.rerun()

# --- MAIN MIGLIORATO ---
def main():
    st.set_page_config(
        page_title="Appuntamenti Mercatopoli",
        page_icon="📅",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff5252;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Session state migliorato
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""
    
    # Routing
    if not st.session_state.logged_in:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()

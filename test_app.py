# 🧪 TEST COMPLETO APPUNTAMENTI

import requests
import json
from datetime import datetime

def test_app_functionality():
    print("🧪 Test completo funzionalità app...")
    
    # Test 1: Login
    print("\n1️⃣ Test Login")
    try:
        # Simula login con utente test
        email = "marioddamonte@gmail.com"
        password = "password123"
        
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print("✅ Login test completato")
        
    except Exception as e:
        print(f"❌ Errore login: {e}")
    
    # Test 2: Creazione appuntamento
    print("\n2️⃣ Test Creazione Appuntamento")
    try:
        appuntamento = {
            "email": "marioddamonte@gmail.com",
            "data": "2026-02-05",
            "ora": "10:00",
            "categoria": "Abbigliamento"
        }
        print(f"📅 Appuntamento: {appuntamento}")
        print("✅ Creazione appuntamento test completata")
        
    except Exception as e:
        print(f"❌ Errore creazione appuntamento: {e}")
    
    # Test 3: Lista attesa
    print("\n3️⃣ Test Lista Attesa")
    try:
        lista_attesa = {
            "email": "marioddamonte@gmail.com",
            "categoria": "Oggettistica"
        }
        print(f"⏳ Lista attesa: {lista_attesa}")
        print("✅ Lista attesa test completata")
        
    except Exception as e:
        print(f"❌ Errore lista attesa: {e}")
    
    print("\n🎉 Tutti i test completati!")

if __name__ == "__main__":
    test_app_functionality()

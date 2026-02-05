# 🧪 TEST CONNESSIONE GOOGLE SHEETS

import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_connection():
    print("🧪 Test connessione Google Sheets...")
    
    try:
        # Carica credentials
        with open('credentials.json', 'r') as f:
            creds_dict = json.load(f)
        
        print("✅ Credentials caricate")
        print(f"📧 Email: {creds_dict['client_email']}")
        print(f"🆔 Project: {creds_dict['project_id']}")
        
        # Autorizza
        scope = ["https://spreadsheets.google.com", "https://www.googleapis.com"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        print("✅ Autorizzazione completata")
        
        # Apri spreadsheet
        spreadsheet = client.open("Appuntamenti_Mercatopoli")
        print("✅ Spreadsheet trovato")
        
        # Test schede
        worksheets = spreadsheet.worksheets()
        print(f"✅ Schede trovate: {[ws.title for ws in worksheets]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

if __name__ == "__main__":
    test_connection()

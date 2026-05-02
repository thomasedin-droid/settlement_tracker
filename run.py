# run.py - Enkel startscript
from app import app

if __name__ == '__main__':
    print("""
    ═══════════════════════════════════════════════════════════
                    SETTLEMENT TRACKER
    ═══════════════════════════════════════════════════════════
    
    Servern startar på: http://localhost:5000
    
    API Endpoints:
    • /api/settlements - Lista alla settlements
    • /api/settlement/<id> - Hämta specifikt settlement
    • /api/settlement/<id>/npcs - Hämta NPCs för settlement
    
    ═══════════════════════════════════════════════════════════
    """)
    app.run(debug=True, port=5000, host='0.0.0.0')
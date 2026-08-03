# README.md

# Settlement Tracker - Web Application

Ett komplett system för att tracka settlements, NPCs, och dynamiska kaskadeffekter i apokalyptiska rollspelsvärldar.

## Installation

### 1. Installera Python 3.8+
Se till att du har Python 3.8 eller senare installerat.

### 2. Installera dependencies
```bash
pip install -r requirements.txt
```

### 3. Initiera databasen
```bash
python init_db.py
```

Detta skapar databasen och lägger till exempel-data:
- 3 settlements (Järngrinden, Skogsholm, Bergfästet)
- 7 NPCs
- Settlement-relationer

### 4. Starta applikationen
```bash
python run.py
```

Öppna sedan din webbläsare och gå till: **http://localhost:5000**

## Funktioner

### Settlement Management
- **Skapa settlements** med 7 parametrar (0-100 skala)
- **Spåra veckor** - avancera tid och applicera automatiska kaskader
- **Parameter-trösklar** - automatiska triggers baserat på värden
- **Kaskadsystem** - händelser utlöser följdeffekter över tid
- **Momentum** - accelererande förändringar vid upprepade trender

### NPC System
- **Skapa NPCs** med stats (Strength, Intelligence, Charisma, Combat, Survival)
- **Settlement-påverkan** - NPCs modifieras automatiskt av settlement-parametrar
- **Loyalty-tracking** - spåra NPC-lojalitet till settlements
- **Traits & Motivationer** - dynamiska egenskaper baserat på settlement-tillstånd

### Kaskad-mekanik
Systemet kontrollerar automatiskt tröskelvärden och aktiverar kaskader:

**Resursläge <30:**
- Aggression: +2/vecka
- Moralisk flexibilitet: +1/vecka
- Tillit: -1/vecka

**Aggression >70:**
- Grannars aggression: +10
- Resursläge: -2/vecka (kriget tär)

**Tillit <15:**
- Överlevnadsstrategi: -5/månad (stänger sig)

**Moralisk flexibilitet >80:**
- Samhällsstruktur: -3/vecka (kaos)

### Händelsesystem
- **Fördefinierade händelser** från händelsebanken (6 st idag, enkelt att utöka i `predefined_events`-listan i `app.py`)
- **Anpassade händelser** - skapa egna med parameter-ändringar
- **Automatisk kaskad-trigger** - händelser aktiverar nya kaskader
- **Event-historik** - se alla händelser per settlement

### Regional Översikt
- **Jämför settlements** - se alla parametrar i tabell
- **Regional stabilitet** - beräknas från alla settlements
- **Aktiva hot** - varningar för kritiska tillstånd
- **Möjligheter** - identifiera handelsmöjligheter och allianser

## API Integration

### REST API Endpoints
```python
# Hämta alla settlements
GET /api/settlements

# Hämta specifikt settlement
GET /api/settlement/<id>

# Hämta NPCs för settlement
GET /api/settlement/<id>/npcs

# Avancera till nästa vecka
POST /settlement/<id>/advance_week
```

### Integration med NPC-systemet

Systemet kan integreras med det befintliga NPC-systemet via API:
```javascript
// Exempel: Hämta settlement-data för NPC-påverkan
async function getSettlementData(settlementId) {
    const response = await fetch(`/api/settlement/${settlementId}`);
    const settlement = await response.json();
    
    // Använd settlement-data för att modifiera NPC
    if (settlement.aggression > 60) {
        npc.combat += 2;
        npc.charisma -= 2;
    }
}
```

## Databas-schema

### Settlement
- Parametrar (0-100): survival_strategy, resource_level, social_structure, aggression, tech_level, trust, moral_flexibility
- Metadata: population, location, terrain, current_week

### NPC
- Stats: strength, intelligence, charisma, combat, survival
- Settlement-relation: settlement_id, loyalty
- Dynamiskt: traits, motivations (JSON)

### Event
- Kopplas till settlement
- Parameter-ändringar (JSON)
- Vecka-timestamp

### Cascade
- Aktiv/inaktiv status
- Automatiska förändringar per vecka
- Kopplas till tröskel-triggers

### SettlementRelation
- Relationer mellan settlements (-100 till +100)
- Distans, handelsavtal

## Användning

### Skapa ett nytt settlement
1. Gå till "Nytt settlement"
2. Fyll i grundinformation
3. Justera parametrar med sliders
4. Eller använd fördefinierade mallar (Järngrinden, Skogsholm, Bergfästet)

### Lägga till händelse
1. Gå till settlement-sidan
2. Klicka "Ny händelse"
3. Välj fördefinierad händelse ELLER skapa egen
4. Ange parameter-ändringar
5. Systemet kontrollerar automatiskt trösklar och aktiverar kaskader

### Avancera tid
1. På settlement-sidan, klicka "Nästa vecka"
2. Alla aktiva kaskader appliceras automatiskt
3. Momentum kontrolleras
4. Nya kaskader kan aktiveras

### Skapa NPC
1. Gå till settlement
2. Klicka "Ny NPC"
3. Fyll i stats och information
4. Systemet applicerar automatiskt settlement-modifieringar

## Exempel-scenario

### Vecka 0: Misslyckad skörd i Järngrinden
```
Resursläge: 60 → 35 (-25)
Moralisk flexibilitet: 40 → 50 (+10)

KASKAD AKTIVERAD: Resursläge <30
  → Aggression: +2/vecka
  → Moralisk flexibilitet: +1/vecka
  → Tillit: -1/vecka
```

### Vecka 1-3: Kaskaden tickar
```
Vecka 1: Aggression 60→62, Mor.flex 50→51, Tillit 20→19
Vecka 2: Aggression 62→64, Mor.flex 51→52, Tillit 19→18
Vecka 3: MOMENTUM AKTIVERAD (3 veckor samma riktning)
  → Nästa Aggression-ökning: +3 (50% bonus)
```

### Vecka 4: Järnkäften beslutar raid
```
NPC Järnkäften trigger: Resursläge <40 = Desperat
  → Quest aktiverad: "Järnhanden"
  → Settlement planerar raid mot Skogsholm

NPC Erik trigger: Aggression >60 = Exalterad
  → "ÄNTLIGEN! Låt mig leda raiden!"
```

## Teknisk information

**Framework:** Flask 3.0.0  
**Databas:** SQLite (SQLAlchemy ORM)  
**Frontend:** Bootstrap 5, vanilla JavaScript  
**API:** RESTful JSON endpoints  

## Framtida förbättringar

- [ ] Kartvisualisering med Canvas/SVG
- [ ] Export/Import av settlements (JSON)
- [ ] Multiplayer-stöd (WebSocket för realtidsuppdateringar)
- [ ] AI-driven event-generering
- [ ] Avancerad statistik och grafer
- [ ] Mobile app (React Native)

## Support

För frågor eller bugrapporter, skapa ett issue på GitHub.

## Licens

MIT License - Fri att använda och modifiera
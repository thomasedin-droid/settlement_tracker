# init_db.py - Separat script för att initiera databasen
from app import app, db, Settlement, NPC, SettlementRelation
import json

def init_database():
    """Initiera databasen med exempel-data"""
    with app.app_context():
        # Skapa tabeller
        db.create_all()
        print("✓ Databastabeller skapade")
        
        # Kolla om det redan finns data
        if Settlement.query.first():
            print("! Data finns redan i databasen")
            return
        
        # Skapa Järngrinden
        jarngrinden = Settlement(
            name='Järngrinden',
            settlement_type='Befäst handelsnod',
            population=180,
            location='Centralt vid gamla E6',
            terrain='Slätt',
            survival_strategy=35,
            resource_level=25,
            social_structure=70,
            aggression=60,
            tech_level=45,
            trust=20,
            moral_flexibility=60,
            current_week=0
        )
        db.session.add(jarngrinden)
        db.session.flush()
        print(f"✓ Settlement '{jarngrinden.name}' skapad")
        
        # Skapa NPC: Järnkäften
        jarnkaften = NPC(
            name='Marcus "Järnkäften" Ståhlberg',
            age=52,
            gender='Man',
            role='Diktator',
            strength=12,
            intelligence=13,
            charisma=15,
            combat=14,
            survival=16,
            settlement_id=jarngrinden.id,
            loyalty=95,
            traits=json.dumps(['Tactical Genius', 'Paranoid', 'Desperate Leader', 'Brutal']),
            motivations=json.dumps(['Behålla makt', 'Få mat till folket', 'Eliminera förrädare']),
            notes='F.d. polis, nu diktator. Förlorade sin fru för 2 år sedan.'
        )
        db.session.add(jarnkaften)
        print(f"✓ NPC '{jarnkaften.name}' skapad")
        
        # Skapa NPC: Erik Stålhand
        erik = NPC(
            name='Erik "Stålhand" Bergström',
            age=34,
            gender='Man',
            role='Milischef',
            strength=16,
            intelligence=10,
            charisma=8,
            combat=18,
            survival=13,
            settlement_id=jarngrinden.id,
            loyalty=30,
            traits=json.dumps(['Battle-Scarred', 'Ambitious', 'Bloodthirsty', 'Distrustful']),
            motivations=json.dumps(['Ta över Järngrinden', 'Vinna fler strider', 'Döda alla från Skogsholm']),
            notes='Förlorade sin bror i raid mot Skogsholm. Vill genomföra kupp.'
        )
        db.session.add(erik)
        print(f"✓ NPC '{erik.name}' skapad")
        
        # Skapa NPC: Signe Mjukhänt
        signe = NPC(
            name='Signe Mjukhänt',
            age=29,
            gender='Kvinna',
            role='Läkare',
            strength=7,
            intelligence=15,
            charisma=12,
            combat=5,
            survival=9,
            settlement_id=jarngrinden.id,
            loyalty=20,
            traits=json.dumps(['Compassionate', 'Skilled Medic', 'Traumatized', 'Pacifist']),
            motivations=json.dumps(['FLY Järngrinden', 'Sluta tvingas behandla raiders', 'Bevara sin mänsklighet']),
            notes='Vill despererat fly. Har kusin i Skogsholm. Tappar sin själ dagligen.'
        )
        db.session.add(signe)
        print(f"✓ NPC '{signe.name}' skapad")
        
        # Skapa Skogsholm
        skogsholm = Settlement(
            name='Skogsholm',
            settlement_type='Skogssamhälle',
            population=95,
            location='20km NÖ från Järngrinden',
            terrain='Skog',
            survival_strategy=65,
            resource_level=40,
            social_structure=35,
            aggression=25,
            tech_level=30,
            trust=55,
            moral_flexibility=25,
            current_week=0
        )
        db.session.add(skogsholm)
        db.session.flush()
        print(f"✓ Settlement '{skogsholm.name}' skapad")
        
        # Skapa NPC: Björn Järnbrynja
        bjorn = NPC(
            name='Björn Järnbrynja',
            age=42,
            gender='Man',
            role='Jägare & Rådsledamot',
            strength=11,
            intelligence=12,
            charisma=13,
            combat=12,
            survival=16,
            settlement_id=skogsholm.id,
            loyalty=85,
            traits=json.dumps(['Master Hunter', 'Pacifist', 'Principled', 'Protective']),
            motivations=json.dumps(['Skydda Skogsholm', 'Kontakta syster Anna i Järngrinden', 'Hitta fredlig lösning']),
            notes='Syster Anna bor i Järngrinden. Har ej sett henne på 1 år.'
        )
        db.session.add(bjorn)
        print(f"✓ NPC '{bjorn.name}' skapad")
        
        # Skapa NPC: Freja Ljusbärare
        freja = NPC(
            name='Freja Ljusbärare',
            age=45,
            gender='Kvinna',
            role='Rådsledare & Andlig guide',
            strength=8,
            intelligence=15,
            charisma=17,
            combat=6,
            survival=11,
            settlement_id=skogsholm.id,
            loyalty=95,
            traits=json.dumps(['Inspiring Leader', 'Pacifist', 'Healer', 'Naive', 'Moral Anchor']),
            motivations=json.dumps(['Bevara Skogsholms mänsklighet', 'Hitta fred med Järngrinden', 'Skydda de svaga']),
            notes='F.d. präst. Förlorade sin make år 1. Detta driver hennes pacifism.'
        )
        db.session.add(freja)
        print(f"✓ NPC '{freja.name}' skapad")
        
        # Skapa Bergfästet
        bergfastet = Settlement(
            name='Bergfästet',
            settlement_type='Bergsfästning',
            population=45,
            location='35km V från Järngrinden',
            terrain='Berg',
            survival_strategy=50,
            resource_level=70,
            social_structure=80,
            aggression=20,
            tech_level=55,
            trust=40,
            moral_flexibility=35,
            current_week=0
        )
        db.session.add(bergfastet)
        db.session.flush()
        print(f"✓ Settlement '{bergfastet.name}' skapad")
        
        # Skapa NPC: Ragnhild "Bergets Mor"
        ragnhild = NPC(
            name='Ragnhild "Bergets Mor" Svensdotter',
            age=68,
            gender='Kvinna',
            role='Matriark',
            strength=10,
            intelligence=16,
            charisma=18,
            combat=8,
            survival=15,
            settlement_id=bergfastet.id,
            loyalty=100,
            traits=json.dumps(['Wise Leader', 'Strategic Mind', 'Mother Figure', 'Neutral Arbitrator']),
            motivations=json.dumps(['Skydda Bergfästet', 'Bevara gruvsamhällets värderingar', 'Hitta efterträdare']),
            notes='Byggt Bergfästet från grunden. Förlorade make och son år 1. Orolig för succession.'
        )
        db.session.add(ragnhild)
        print(f"✓ NPC '{ragnhild.name}' skapad")
        
        # Skapa relationer
        rel1 = SettlementRelation(
            settlement_id=jarngrinden.id,
            target_settlement_id=skogsholm.id,
            relation_value=-60,
            distance_km=20,
            trade_agreement=False
        )
        db.session.add(rel1)
        
        rel2 = SettlementRelation(
            settlement_id=skogsholm.id,
            target_settlement_id=jarngrinden.id,
            relation_value=-60,
            distance_km=20,
            trade_agreement=False
        )
        db.session.add(rel2)
        
        rel3 = SettlementRelation(
            settlement_id=jarngrinden.id,
            target_settlement_id=bergfastet.id,
            relation_value=10,
            distance_km=35,
            trade_agreement=True
        )
        db.session.add(rel3)
        
        rel4 = SettlementRelation(
            settlement_id=skogsholm.id,
            target_settlement_id=bergfastet.id,
            relation_value=30,
            distance_km=40,
            trade_agreement=True
        )
        db.session.add(rel4)
        
        print("✓ Settlement-relationer skapade")
        
        db.session.commit()
        print("\n✓✓✓ Databas initierad med exempel-data! ✓✓✓")
        print("\nStarta applikationen med: python app.py")
        print("Öppna sedan: http://localhost:5000")

if __name__ == '__main__':
    init_database()
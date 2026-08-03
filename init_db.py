# init_db.py - Separat script för att initiera databasen med exempel-data
#
# Kampanjsättning: Frankrike efter kollapsen. Rollpersonerna anländer till
# Cherbourg-en-Cotentin efter flykten från England och drar vidare söderut
# genom Loiredalen mot Amboise, där Hells Angels från Bourges just nu
# förbereder en erövring.
from app import app, db, Settlement, NPC, SettlementRelation, Cascade
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

        settlements = {}

        # --------------------------------------------------------------
        # CHERBOURG-EN-COTENTIN - rollpersonernas ankomstplats efter
        # flykten från England. Styrs av ett medborgarråd i spänd balans
        # mellan flera lokala faktioner.
        # --------------------------------------------------------------
        settlements['cherbourg'] = Settlement(
            name='Cherbourg-en-Cotentin',
            settlement_type='Rådsstyrd hamnstad',
            population=620,
            location='Cotentin-halvön, nordvästra Frankrike',
            terrain='Kust',
            survival_strategy=55,
            resource_level=45,
            social_structure=70,
            aggression=25,
            tech_level=40,
            trust=45,
            moral_flexibility=30,
            current_week=0
        )
        db.session.add(settlements['cherbourg'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['cherbourg'].name}' skapad")

        adrienne = NPC(
            name='Adrienne Rousseau',
            age=51, gender='Kvinna', role='Rådsordförande',
            strength=8, intelligence=16, charisma=17, combat=6, survival=12,
            settlement_id=settlements['cherbourg'].id,
            loyalty=80,
            traits=json.dumps(['Diplomat', 'Pragmatisk', 'Utmattad', 'Kompromissvillig']),
            motivations=json.dumps(['Hålla faktionerna i schack', 'Ge flyktingar en fristad', 'Undvika inbördeskrig']),
            notes='Vald ordförande i medborgarrådet efter den gamle borgmästarens död. Balanserar dagligen mellan fiskargillet, den gamla militären och nyanlända flyktinggrupper - däribland rollpersonerna.'
        )
        db.session.add(adrienne)
        print(f"✓ NPC '{adrienne.name}' skapad")

        julien = NPC(
            name='Julien "Kajen" Marchetti',
            age=44, gender='Man', role='Fiskargillets talesman',
            strength=13, intelligence=11, charisma=13, combat=10, survival=15,
            settlement_id=settlements['cherbourg'].id,
            loyalty=55,
            traits=json.dumps(['Misstänksam mot utomstående', 'Stolt', 'Praktisk']),
            motivations=json.dumps(['Skydda fiskeflottan och hamninkomsterna', 'Begränsa rådets makt', 'Hålla nyanlända under kontroll']),
            notes='Anser att rådet ger för mycket resurser till flyktingar på fiskargildets bekostnad. Ligger i ständig tyst maktkamp med Rousseau.'
        )
        db.session.add(julien)
        print(f"✓ NPC '{julien.name}' skapad")

        # --------------------------------------------------------------
        # LE HAVRE - kontrolleras helt av Hells Angels.
        # --------------------------------------------------------------
        settlements['le_havre'] = Settlement(
            name='Le Havre',
            settlement_type='Gängstyrd hamnstad',
            population=480,
            location='Normandiets kust, vid Seines mynning',
            terrain='Kust',
            survival_strategy=40,
            resource_level=55,
            social_structure=55,
            aggression=80,
            tech_level=35,
            trust=15,
            moral_flexibility=75,
            current_week=0
        )
        db.session.add(settlements['le_havre'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['le_havre'].name}' skapad")

        reaper = NPC(
            name='"Reaper" Dubois',
            age=47, gender='Man', role='Hells Angels - Chapter President',
            strength=15, intelligence=12, charisma=16, combat=17, survival=14,
            settlement_id=settlements['le_havre'].id,
            loyalty=90,
            traits=json.dumps(['Brutal', 'Karismatisk', 'Strategisk', 'Respekterad av sina egna']),
            motivations=json.dumps(['Kontrollera all handel genom hamnen', 'Expandera klubbens territorium', 'Aldrig visa svaghet']),
            notes='Har styrt Le Havre i över tio år. Ser hamnen som sin personliga skattkammare och tillåter ingen konkurrens.'
        )
        db.session.add(reaper)
        print(f"✓ NPC '{reaper.name}' skapad")

        # --------------------------------------------------------------
        # LE MANS - försöker framstå som neutralt, men driver slavhandel
        # bakom kulisserna.
        # --------------------------------------------------------------
        settlements['le_mans'] = Settlement(
            name='Le Mans',
            settlement_type='"Neutral" handelsstad',
            population=390,
            location='Pays de la Loire',
            terrain='Slätt',
            survival_strategy=50,
            resource_level=50,
            social_structure=60,
            aggression=30,
            tech_level=45,
            trust=35,
            moral_flexibility=70,
            current_week=0
        )
        db.session.add(settlements['le_mans'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['le_mans'].name}' skapad")

        eveline = NPC(
            name='Éveline Cortot',
            age=58, gender='Kvinna', role='Stadsäldste',
            strength=6, intelligence=17, charisma=18, combat=4, survival=10,
            settlement_id=settlements['le_mans'].id,
            loyalty=60,
            traits=json.dumps(['Charmig', 'Dubbelspelare', 'Kall kalkylator']),
            motivations=json.dumps(['Bevara skenet av neutralitet', 'Skydda sina egna affärer', 'Hålla slavhandeln dold för utomstående']),
            notes='Officiellt en fredsmäklare mellan grupper som passerar Le Mans. Inofficiellt drar hon nytta av en diskret slavhandel som förser andra bosättningar med arbetskraft.'
        )
        db.session.add(eveline)
        print(f"✓ NPC '{eveline.name}' skapad")

        # --------------------------------------------------------------
        # ORLÉANS - delad mellan Hells Angels och ryska soldater, med en
        # växande motståndsrörelse.
        # --------------------------------------------------------------
        settlements['orleans'] = Settlement(
            name='Orléans',
            settlement_type='Ockuperad stad',
            population=510,
            location='Loiredalen',
            terrain='Flodstad',
            survival_strategy=30,
            resource_level=35,
            social_structure=20,
            aggression=75,
            tech_level=40,
            trust=10,
            moral_flexibility=65,
            current_week=0
        )
        db.session.add(settlements['orleans'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['orleans'].name}' skapad")

        volkov = NPC(
            name='Kapten Igor Volkov',
            age=39, gender='Man', role='Rysk militär befälhavare',
            strength=14, intelligence=14, charisma=10, combat=16, survival=13,
            settlement_id=settlements['orleans'].id,
            loyalty=70,
            traits=json.dumps(['Disciplinerad', 'Hänsynslös', 'Lojal mot sin egen enhet']),
            motivations=json.dumps(['Behålla kontrollen över Loire-bron', 'Undvika öppen konflikt med Hells Angels', 'Krossa motståndsrörelsen']),
            notes='Leder en isolerad rysk enhet som hamnade i Orléans efter kollapsen. Delar staden i en spänd maktbalans med Hells Angels.'
        )
        db.session.add(volkov)
        print(f"✓ NPC '{volkov.name}' skapad")

        camille = NPC(
            name='Camille Fabre',
            age=27, gender='Kvinna', role='Motståndsledare',
            strength=10, intelligence=13, charisma=14, combat=12, survival=15,
            settlement_id=settlements['orleans'].id,
            loyalty=95,
            traits=json.dumps(['Modig', 'Idealistisk', 'Hemlighetsfull', 'Villig att offra sig']),
            motivations=json.dumps(['Befria Orléans', 'Sprida sabotage mot ockupanterna', 'Hitta allierade utanför staden']),
            notes='Leder en liten men växande motståndscell mot både ryssarna och Hells Angels. Söker desperat efter externa allierade - kanske rollpersonerna?'
        )
        db.session.add(camille)
        print(f"✓ NPC '{camille.name}' skapad")

        # --------------------------------------------------------------
        # BOURGES - Hells Angels-kontrollerad, planerar erövringen av
        # Amboise.
        # --------------------------------------------------------------
        settlements['bourges'] = Settlement(
            name='Bourges',
            settlement_type='Gängstyrd stad',
            population=340,
            location='Centralfrankrike, Berry',
            terrain='Slätt',
            survival_strategy=35,
            resource_level=30,
            social_structure=50,
            aggression=85,
            tech_level=35,
            trust=15,
            moral_flexibility=80,
            current_week=0
        )
        db.session.add(settlements['bourges'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['bourges'].name}' skapad")

        lefevre = NPC(
            name='"Slaktaren" Lefèvre',
            age=41, gender='Man', role='Hells Angels - Krigsherre',
            strength=17, intelligence=11, charisma=13, combat=19, survival=12,
            settlement_id=settlements['bourges'].id,
            loyalty=85,
            traits=json.dumps(['Blodtörstig', 'Ambitiös', 'Respekterad genom rädsla']),
            motivations=json.dumps(['Erövra Amboise och dess matproduktion', 'Bli regionens mäktigaste HA-ledare', 'Krossa allt motstånd']),
            notes='Driver planeringen av invasionen av Amboise. Ser stadens jordbruk och sjukhus som nästa erövring.'
        )
        db.session.add(lefevre)
        print(f"✓ NPC '{lefevre.name}' skapad")

        # --------------------------------------------------------------
        # TOURS - handelsstad, allierad och handelspartner med Amboise.
        # --------------------------------------------------------------
        settlements['tours'] = Settlement(
            name='Tours',
            settlement_type='Handelsstad',
            population=430,
            location='Loiredalen, väster om Amboise',
            terrain='Flodstad',
            survival_strategy=60,
            resource_level=55,
            social_structure=65,
            aggression=20,
            tech_level=45,
            trust=60,
            moral_flexibility=25,
            current_week=0
        )
        db.session.add(settlements['tours'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['tours'].name}' skapad")

        marguerite = NPC(
            name='Marguerite Dubreuil',
            age=49, gender='Kvinna', role='Handelsledare',
            strength=9, intelligence=15, charisma=15, combat=7, survival=11,
            settlement_id=settlements['tours'].id,
            loyalty=75,
            traits=json.dumps(['Affärsmässig', 'Pålitlig', 'Nätverkare']),
            motivations=json.dumps(['Skydda handelsvägen till Amboise', 'Hålla Tours neutralt gentemot Hells Angels', 'Bygga en regional handelsallians']),
            notes='Drivkraften bakom Tours nära band till Amboise. Förhandlar just nu om att skicka förstärkning inför den väntade attacken från Bourges.'
        )
        db.session.add(marguerite)
        print(f"✓ NPC '{marguerite.name}' skapad")

        # --------------------------------------------------------------
        # AMBOISE - styrs från det gamla slottet av borgmästaren. Har
        # matproduktion och ett litet sjukhus. Milisen försvarar staden
        # mot Hells Angels (från Bourges) och ryska räder.
        # --------------------------------------------------------------
        settlements['amboise'] = Settlement(
            name='Amboise',
            settlement_type='Slottsstad & jordbrukssamhälle',
            population=260,
            location='Loiredalen, öster om Tours',
            terrain='Flodstad',
            survival_strategy=55,
            resource_level=60,
            social_structure=75,
            aggression=45,
            tech_level=30,
            trust=50,
            moral_flexibility=20,
            current_week=0
        )
        db.session.add(settlements['amboise'])
        db.session.flush()
        print(f"✓ Settlement '{settlements['amboise'].name}' skapad")

        henri = NPC(
            name='Borgmästare Henri Lavigne',
            age=63, gender='Man', role='Borgmästare',
            strength=8, intelligence=15, charisma=14, combat=6, survival=12,
            settlement_id=settlements['amboise'].id,
            loyalty=90,
            traits=json.dumps(['Envis', 'Traditionsbunden', 'Beskyddande', 'Orolig']),
            motivations=json.dumps(['Försvara Amboise till varje pris', 'Säkra mat till sjukhuset', 'Få Tours att skicka förstärkning i tid']),
            notes='Styr Amboise från det gamla slottet, precis som hans familj gjort i generationer. Vet att staden inte klarar en fullskalig belägring utan hjälp utifrån.'
        )
        db.session.add(henri)
        print(f"✓ NPC '{henri.name}' skapad")

        odette = NPC(
            name='Milischef Odette Berthier',
            age=36, gender='Kvinna', role='Milischef',
            strength=14, intelligence=12, charisma=11, combat=16, survival=14,
            settlement_id=settlements['amboise'].id,
            loyalty=88,
            traits=json.dumps(['Taktisk', 'Orädd', 'Överarbetad']),
            motivations=json.dumps(['Hålla ut mot Hells Angels och ryska raider', 'Träna upp fler milissoldater', 'Skydda sjukhuset och matförråden']),
            notes='Ansvarar för Amboises försvar med en kraftigt underbemannad milis. Har redan avvärjt två mindre razzior från Bourges styrkor.'
        )
        db.session.add(odette)
        print(f"✓ NPC '{odette.name}' skapad")

        db.session.flush()

        # --------------------------------------------------------------
        # RELATIONER mellan bosättningarna
        # --------------------------------------------------------------
        def add_relation(a, b, value, distance, trade=False):
            db.session.add(SettlementRelation(
                settlement_id=settlements[a].id,
                target_settlement_id=settlements[b].id,
                relation_value=value,
                distance_km=distance,
                trade_agreement=trade
            ))

        # Bourges vill erövra Amboise - Amboise ser det som en existentiell fara
        add_relation('bourges', 'amboise', -40, 110, trade=False)
        add_relation('amboise', 'bourges', -90, 110, trade=False)

        # Tours och Amboise är handelsvänner och allierade
        add_relation('tours', 'amboise', 70, 25, trade=True)
        add_relation('amboise', 'tours', 70, 25, trade=True)

        # Le Havre och Bourges är båda Hells Angels-territorium
        add_relation('le_havre', 'bourges', 40, 300, trade=True)
        add_relation('bourges', 'le_havre', 40, 300, trade=True)

        # Orléans samarbetar löst med Hells Angels-nätverket
        add_relation('orleans', 'bourges', 30, 65, trade=False)
        add_relation('bourges', 'orleans', 30, 65, trade=False)
        add_relation('orleans', 'le_havre', 15, 280, trade=False)

        # Le Mans håller vaksam distans till gängen omkring sig
        add_relation('le_mans', 'bourges', -15, 130, trade=False)
        add_relation('le_mans', 'le_havre', -5, 180, trade=False)
        add_relation('le_mans', 'tours', 20, 80, trade=True)

        # Cherbourg oroar sig för Hells Angels expansion från kusten
        add_relation('cherbourg', 'le_havre', -30, 120, trade=False)
        add_relation('le_havre', 'cherbourg', -10, 120, trade=False)

        print("✓ Settlement-relationer skapade")

        # --------------------------------------------------------------
        # PÅGÅENDE KRISER (kaskader) redan aktiva från vecka 0
        # --------------------------------------------------------------
        db.session.add(Cascade(
            settlement_id=settlements['amboise'].id,
            cascade_type='belägring',
            parameter='resource_level',
            change_per_week=-3,
            active=True,
            started_week=0,
            description='Hells Angels-styrkor från Bourges skär av handelsvägar och slår mot skördarna runt Amboise.'
        ))
        db.session.add(Cascade(
            settlement_id=settlements['orleans'].id,
            cascade_type='ockupation',
            parameter='trust',
            change_per_week=-2,
            active=True,
            started_week=0,
            description='Motståndsrörelsens sabotage och den delade ockupationsmakten undergräver invånarnas förtroende vecka för vecka.'
        ))
        print("✓ Pågående kriser (kaskader) skapade")

        db.session.commit()
        print("\n✓✓✓ Databas initierad med exempel-data (Frankrike-kampanj)! ✓✓✓")
        print("\nStarta applikationen med: python app.py")
        print("Öppna sedan: http://localhost:5000")

if __name__ == '__main__':
    init_database()

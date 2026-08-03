# app.py - Huvudapplikation
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

from template_filters import init_template_filters

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///settlements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY läses från miljövariabel om satt, annars en dev-nyckel.
# Sätt en riktig hemlighet via: set SECRET_KEY=... (Windows) innan produktion/delning.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
db = SQLAlchemy(app)
init_template_filters(app)


def utcnow():
    """Tidszonsmedveten UTC-tidsstämpel (ersätter deprecated datetime.utcnow())."""
    return datetime.now(timezone.utc)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Settlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    settlement_type = db.Column(db.String(50))  # by, stad, fort
    population = db.Column(db.Integer)
    founded_date = db.Column(db.String(50))
    location = db.Column(db.String(200))
    terrain = db.Column(db.String(50))
    
    # Parametrar (0-100)
    survival_strategy = db.Column(db.Integer, default=50)
    resource_level = db.Column(db.Integer, default=50)
    social_structure = db.Column(db.Integer, default=50)
    aggression = db.Column(db.Integer, default=50)
    tech_level = db.Column(db.Integer, default=50)
    trust = db.Column(db.Integer, default=50)
    moral_flexibility = db.Column(db.Integer, default=50)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=utcnow)
    last_updated = db.Column(db.DateTime, default=utcnow)
    current_week = db.Column(db.Integer, default=0)
    
    # Relationer
    npcs = db.relationship('NPC', backref='settlement', lazy=True, cascade='all, delete-orphan')
    events = db.relationship('Event', backref='settlement', lazy=True, cascade='all, delete-orphan')
    cascades = db.relationship('Cascade', backref='settlement', lazy=True, cascade='all, delete-orphan')
    relations = db.relationship('SettlementRelation', 
                               foreign_keys='SettlementRelation.settlement_id',
                               backref='settlement_from', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'settlement_type': self.settlement_type,
            'population': self.population,
            'survival_strategy': self.survival_strategy,
            'resource_level': self.resource_level,
            'social_structure': self.social_structure,
            'aggression': self.aggression,
            'tech_level': self.tech_level,
            'trust': self.trust,
            'moral_flexibility': self.moral_flexibility,
            'current_week': self.current_week
        }

class NPC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    role = db.Column(db.String(100))
    
    # Stats
    strength = db.Column(db.Integer, default=10)
    intelligence = db.Column(db.Integer, default=10)
    charisma = db.Column(db.Integer, default=10)
    combat = db.Column(db.Integer, default=10)
    survival = db.Column(db.Integer, default=10)
    
    # Settlement relation
    settlement_id = db.Column(db.Integer, db.ForeignKey('settlement.id'), nullable=False)
    loyalty = db.Column(db.Integer, default=50)
    
    # Traits & Motivations (JSON)
    traits = db.Column(db.Text)  # JSON array
    motivations = db.Column(db.Text)  # JSON array
    
    # Notes
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'role': self.role,
            'strength': self.strength,
            'intelligence': self.intelligence,
            'charisma': self.charisma,
            'combat': self.combat,
            'loyalty': self.loyalty,
            'settlement_id': self.settlement_id,
            'traits': json.loads(self.traits) if self.traits else [],
            'motivations': json.loads(self.motivations) if self.motivations else []
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settlement_id = db.Column(db.Integer, db.ForeignKey('settlement.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(50))  # resource, military, social, tech
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Parameter changes (JSON format)
    parameter_changes = db.Column(db.Text)  # {"resource_level": -25, "moral_flexibility": 10}
    
    created_at = db.Column(db.DateTime, default=utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'week': self.week,
            'event_type': self.event_type,
            'name': self.name,
            'description': self.description,
            'parameter_changes': json.loads(self.parameter_changes) if self.parameter_changes else {}
        }

class Cascade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settlement_id = db.Column(db.Integer, db.ForeignKey('settlement.id'), nullable=False)
    cascade_type = db.Column(db.String(50), nullable=False)  # kris, momentum, etc
    parameter = db.Column(db.String(50), nullable=False)
    change_per_week = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    started_week = db.Column(db.Integer, nullable=False)
    
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cascade_type': self.cascade_type,
            'parameter': self.parameter,
            'change_per_week': self.change_per_week,
            'active': self.active,
            'started_week': self.started_week,
            'description': self.description
        }

class SettlementRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settlement_id = db.Column(db.Integer, db.ForeignKey('settlement.id'), nullable=False)
    target_settlement_id = db.Column(db.Integer, nullable=False)
    relation_value = db.Column(db.Integer, default=0)  # -100 to 100
    distance_km = db.Column(db.Integer)
    trade_agreement = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        target = db.session.get(Settlement, self.target_settlement_id)
        return {
            'id': self.id,
            'target_name': target.name if target else 'Unknown',
            'target_id': self.target_settlement_id,
            'relation_value': self.relation_value,
            'distance_km': self.distance_km,
            'trade_agreement': self.trade_agreement
        }

class Momentum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settlement_id = db.Column(db.Integer, db.ForeignKey('settlement.id'), nullable=False)
    parameter = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(10))  # up, down
    weeks_in_direction = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=False)
    multiplier = db.Column(db.Float, default=1.0)

# ============================================================================
# KASKAD-LOGIK
# ============================================================================

class CascadeEngine:
    """Hanterar alla kaskad-beräkningar"""
    
    THRESHOLD_RULES = {
        'resource_level': [
            {'threshold': 30, 'cascade_type': 'kris', 'effects': {'aggression': 2, 'moral_flexibility': 1, 'trust': -1}},
            {'threshold': 20, 'cascade_type': 'critical_kris', 'effects': {'aggression': 3, 'moral_flexibility': 2, 'trust': -2}},
            {'threshold': 10, 'cascade_type': 'collapse_imminent', 'effects': {}}
        ],
        'aggression': [
            {'threshold': 70, 'cascade_type': 'war_economy', 'effects': {'resource_level': -2, 'moral_flexibility': 1}},
            {'threshold': 90, 'cascade_type': 'suicidal_war', 'effects': {'resource_level': -5}}
        ],
        'trust': [
            {'threshold': 15, 'cascade_type': 'paranoia', 'effects': {'survival_strategy': -5}},
            {'threshold': 5, 'cascade_type': 'internal_fragmentation', 'effects': {'social_structure': -10}}
        ],
        'moral_flexibility': [
            {'threshold': 80, 'cascade_type': 'moral_decay', 'effects': {'social_structure': -3, 'trust': -2}},
            {'threshold': 95, 'cascade_type': 'societal_disintegration', 'effects': {}}
        ]
    }
    
    @staticmethod
    def check_and_activate_cascades(settlement):
        """Kontrollera tröskelvärden och aktivera nya kaskader"""
        new_cascades = []
        
        for param, rules in CascadeEngine.THRESHOLD_RULES.items():
            param_value = getattr(settlement, param)
            
            for rule in rules:
                threshold = rule['threshold']
                cascade_type = rule['cascade_type']
                
                # Kolla om tröskeln är nådd
                if param_value < threshold:
                    # Kolla om kaskaden redan är aktiv
                    existing = Cascade.query.filter_by(
                        settlement_id=settlement.id,
                        cascade_type=cascade_type,
                        active=True
                    ).first()
                    
                    if not existing:
                        # Skapa ny kaskad
                        for effect_param, change in rule['effects'].items():
                            cascade = Cascade(
                                settlement_id=settlement.id,
                                cascade_type=cascade_type,
                                parameter=effect_param,
                                change_per_week=change,
                                active=True,
                                started_week=settlement.current_week,
                                description=f"{cascade_type.replace('_', ' ').title()} kaskad aktiverad ({param} < {threshold})"
                            )
                            db.session.add(cascade)
                            new_cascades.append(cascade)
        
        db.session.commit()
        return new_cascades
    
    @staticmethod
    def apply_cascades(settlement):
        """Applicera alla aktiva kaskader för en vecka"""
        cascades = Cascade.query.filter_by(settlement_id=settlement.id, active=True).all()
        changes = {}
        
        for cascade in cascades:
            param = cascade.parameter
            base_change = cascade.change_per_week

            # Applicera momentum-multiplier om aktivt momentum finns för denna parameter
            momentum = Momentum.query.filter_by(
                settlement_id=settlement.id, parameter=param, active=True
            ).first()
            multiplier = momentum.multiplier if momentum else 1.0
            change = round(base_change * multiplier)

            # Applicera förändring
            current_value = getattr(settlement, param)
            new_value = max(0, min(100, current_value + change))
            setattr(settlement, param, new_value)
            
            changes[param] = changes.get(param, 0) + change
            
            # Deaktivera kaskad om parameter inte längre når tröskeln
            CascadeEngine._check_cascade_deactivation(settlement, cascade)
        
        db.session.commit()
        return changes
    
    @staticmethod
    def _check_cascade_deactivation(settlement, cascade):
        """Kolla om en kaskad ska deaktiveras"""
        # Hitta ursprunglig tröskel för denna kaskad
        for param, rules in CascadeEngine.THRESHOLD_RULES.items():
            for rule in rules:
                if rule['cascade_type'] == cascade.cascade_type:
                    threshold = rule['threshold']
                    param_value = getattr(settlement, param)
                    
                    # Om vi är över tröskeln igen, deaktivera
                    if param_value >= threshold:
                        cascade.active = False
                        return True
        return False
    
    @staticmethod
    def check_momentum(settlement):
        """Kontrollera och uppdatera momentum för alla parametrar"""
        params = ['survival_strategy', 'resource_level', 'social_structure', 
                  'aggression', 'tech_level', 'trust', 'moral_flexibility']
        
        for param in params:
            # Hämta senaste events för denna parameter
            recent_events = Event.query.filter_by(settlement_id=settlement.id)\
                .order_by(Event.week.desc()).limit(3).all()
            
            if len(recent_events) < 3:
                continue
            
            # Kolla om alla 3 senaste förändringarna var åt samma håll
            changes = []
            for event in recent_events:
                param_changes = json.loads(event.parameter_changes) if event.parameter_changes else {}
                if param in param_changes:
                    changes.append(param_changes[param])
            
            if len(changes) == 3:
                # Alla positiva eller alla negativa?
                all_positive = all(c > 0 for c in changes)
                all_negative = all(c < 0 for c in changes)
                
                if all_positive or all_negative:
                    # Aktivera momentum
                    momentum = Momentum.query.filter_by(
                        settlement_id=settlement.id,
                        parameter=param
                    ).first()
                    
                    if not momentum:
                        momentum = Momentum(
                            settlement_id=settlement.id,
                            parameter=param,
                            direction='up' if all_positive else 'down',
                            weeks_in_direction=3,
                            active=True,
                            multiplier=1.5
                        )
                        db.session.add(momentum)
                    else:
                        new_direction = 'up' if all_positive else 'down'
                        if momentum.direction == new_direction:
                            momentum.weeks_in_direction += 1
                        else:
                            # Trenden har vänt - börja om
                            momentum.weeks_in_direction = 3
                            momentum.direction = new_direction
                        momentum.active = True
                        momentum.multiplier = 1.5
                else:
                    # Trenden är inte längre entydig - deaktivera ev. befintligt momentum
                    momentum = Momentum.query.filter_by(
                        settlement_id=settlement.id,
                        parameter=param,
                        active=True
                    ).first()
                    if momentum:
                        momentum.active = False
        
        db.session.commit()

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    settlements = Settlement.query.all()
    return render_template('index.html', settlements=settlements)

@app.route('/settlement/<int:settlement_id>')
def settlement_detail(settlement_id):
    settlement = Settlement.query.get_or_404(settlement_id)
    npcs = NPC.query.filter_by(settlement_id=settlement_id).all()
    events = Event.query.filter_by(settlement_id=settlement_id)\
        .order_by(Event.week.desc()).limit(20).all()
    cascades = Cascade.query.filter_by(settlement_id=settlement_id, active=True).all()
    relations = SettlementRelation.query.filter_by(settlement_id=settlement_id).all()
    
    # Kolla kritiska trösklar
    warnings = []
    if settlement.resource_level < 30:
        warnings.append({'type': 'danger', 'message': f'KRIS: Resursläge kritiskt ({settlement.resource_level})'})
    if settlement.aggression > 70:
        warnings.append({'type': 'warning', 'message': f'Hög aggression ({settlement.aggression}) - Grannreaktioner troliga'})
    if settlement.trust < 15:
        warnings.append({'type': 'warning', 'message': f'Låg tillit ({settlement.trust}) - Paranoia ökar'})
    
    return render_template('settlement_detail.html', 
                         settlement=settlement, 
                         npcs=npcs, 
                         events=events, 
                         cascades=cascades,
                         relations=relations,
                         warnings=warnings)

@app.route('/settlement/new', methods=['GET', 'POST'])
def new_settlement():
    if request.method == 'POST':
        try:
            settlement = Settlement(
                name=request.form['name'],
                settlement_type=request.form['settlement_type'],
                population=int(request.form['population']),
                location=request.form['location'],
                terrain=request.form['terrain'],
                survival_strategy=int(request.form['survival_strategy']),
                resource_level=int(request.form['resource_level']),
                social_structure=int(request.form['social_structure']),
                aggression=int(request.form['aggression']),
                tech_level=int(request.form['tech_level']),
                trust=int(request.form['trust']),
                moral_flexibility=int(request.form['moral_flexibility'])
            )
        except (KeyError, ValueError):
            flash('Fyll i alla obligatoriska fält med giltiga värden.', 'danger')
            return render_template('new_settlement.html'), 400

        db.session.add(settlement)
        db.session.commit()
        
        return redirect(url_for('settlement_detail', settlement_id=settlement.id))
    
    return render_template('new_settlement.html')

@app.route('/settlement/<int:settlement_id>/edit', methods=['GET', 'POST'])
def edit_settlement(settlement_id):
    settlement = Settlement.query.get_or_404(settlement_id)
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            population = int(request.form['population'])
            survival_strategy = int(request.form['survival_strategy'])
            resource_level = int(request.form['resource_level'])
            social_structure = int(request.form['social_structure'])
            aggression = int(request.form['aggression'])
            tech_level = int(request.form['tech_level'])
            trust = int(request.form['trust'])
            moral_flexibility = int(request.form['moral_flexibility'])
        except (KeyError, ValueError):
            flash('Fyll i alla obligatoriska fält med giltiga värden.', 'danger')
            return render_template('edit_settlement.html', settlement=settlement), 400

        settlement.name = name
        settlement.population = population
        settlement.survival_strategy = survival_strategy
        settlement.resource_level = resource_level
        settlement.social_structure = social_structure
        settlement.aggression = aggression
        settlement.tech_level = tech_level
        settlement.trust = trust
        settlement.moral_flexibility = moral_flexibility
        settlement.last_updated = utcnow()
        
        db.session.commit()
        return redirect(url_for('settlement_detail', settlement_id=settlement.id))
    
    return render_template('edit_settlement.html', settlement=settlement)

@app.route('/settlement/<int:settlement_id>/advance_week', methods=['POST'])
def advance_week(settlement_id):
    settlement = Settlement.query.get_or_404(settlement_id)
    
    # Öka vecka
    settlement.current_week += 1
    
    # Applicera alla aktiva kaskader
    changes = CascadeEngine.apply_cascades(settlement)
    
    # Kontrollera nya kaskader
    new_cascades = CascadeEngine.check_and_activate_cascades(settlement)
    
    # Kontrollera momentum
    CascadeEngine.check_momentum(settlement)
    
    # Skapa event för veckan
    if changes:
        event = Event(
            settlement_id=settlement.id,
            week=settlement.current_week,
            event_type='cascade',
            name=f'Vecka {settlement.current_week} - Kaskadeffekter',
            description=f'Automatiska kaskadförändringar applicerade',
            parameter_changes=json.dumps(changes)
        )
        db.session.add(event)
    
    settlement.last_updated = utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'week': settlement.current_week,
        'changes': changes,
        'new_cascades': len(new_cascades)
    })

@app.route('/settlement/<int:settlement_id>/event/new', methods=['GET', 'POST'])
def new_event(settlement_id):
    settlement = Settlement.query.get_or_404(settlement_id)

    # Fördefinierade events från händelsebanken (behövs i både GET och felfallet av POST)
    predefined_events = [
        {'name': 'Misslyckad skörd', 'type': 'resource', 'changes': {'resource_level': -25, 'moral_flexibility': 10}},
        {'name': 'Sjukdomsutbrott', 'type': 'resource', 'changes': {'resource_level': -15, 'tech_level': -10}},
        {'name': 'Grannby anfaller', 'type': 'military', 'changes': {'aggression': 25, 'social_structure': 15}},
        {'name': 'Lyckad raid', 'type': 'military', 'changes': {'resource_level': 15, 'aggression': 10}},
        {'name': 'Ledare dödad', 'type': 'social', 'changes': {'social_structure': -35, 'aggression': 15}},
        {'name': 'Förkrigs-bunker hittad', 'type': 'tech', 'changes': {'tech_level': 25, 'resource_level': 20}},
    ]

    if request.method == 'POST':
        # Parse parameter changes
        try:
            param_changes = {}
            for param in ['survival_strategy', 'resource_level', 'social_structure', 
                         'aggression', 'tech_level', 'trust', 'moral_flexibility']:
                change_value = request.form.get(f'change_{param}')
                if change_value and int(change_value) != 0:
                    param_changes[param] = int(change_value)
                    
                    # Applicera förändring direkt
                    current = getattr(settlement, param)
                    new_value = max(0, min(100, current + int(change_value)))
                    setattr(settlement, param, new_value)
            event_type = request.form['event_type']
            event_name = request.form['name']
        except (KeyError, ValueError):
            flash('Fyll i händelsenamn och typ, och ange endast heltal för parameterändringar.', 'danger')
            return render_template('new_event.html', settlement=settlement, predefined_events=predefined_events), 400

        # Skapa event
        event = Event(
            settlement_id=settlement.id,
            week=settlement.current_week,
            event_type=event_type,
            name=event_name,
            description=request.form.get('description', ''),
            parameter_changes=json.dumps(param_changes)
        )
        db.session.add(event)
        
        # Kontrollera nya kaskader
        CascadeEngine.check_and_activate_cascades(settlement)
        
        # Kontrollera momentum
        CascadeEngine.check_momentum(settlement)
        
        settlement.last_updated = utcnow()
        db.session.commit()
        
        return redirect(url_for('settlement_detail', settlement_id=settlement.id))

    return render_template('new_event.html', settlement=settlement, predefined_events=predefined_events)

@app.route('/npc/<int:settlement_id>/new', methods=['GET', 'POST'])
def new_npc(settlement_id):
    settlement = Settlement.query.get_or_404(settlement_id)
    
    if request.method == 'POST':
        try:
            npc = NPC(
                name=request.form['name'],
                age=int(request.form['age']),
                gender=request.form['gender'],
                role=request.form['role'],
                strength=int(request.form['strength']),
                intelligence=int(request.form['intelligence']),
                charisma=int(request.form['charisma']),
                combat=int(request.form['combat']),
                survival=int(request.form['survival']),
                settlement_id=settlement_id,
                loyalty=int(request.form['loyalty']),
                traits=json.dumps([t.strip() for t in request.form.get('traits', '').split(',') if t.strip()]),
                motivations=json.dumps([m.strip() for m in request.form.get('motivations', '').split(',') if m.strip()]),
                notes=request.form.get('notes', '')
            )
        except (KeyError, ValueError):
            flash('Fyll i namn, ålder, roll och alla stats med giltiga värden.', 'danger')
            return render_template('new_npc.html', settlement=settlement), 400
        
        # Settlement-påverkan på NPC stats
        if settlement.aggression > 60:
            npc.combat += 2
            npc.charisma -= 2
        
        if settlement.resource_level < 30:
            npc.loyalty -= 10
        
        if settlement.trust < 25:
            # Lägg till "Distrustful" trait
            traits = json.loads(npc.traits) if npc.traits else []
            traits.append('Distrustful')
            npc.traits = json.dumps(traits)
        
        db.session.add(npc)
        db.session.commit()
        
        return redirect(url_for('settlement_detail', settlement_id=settlement_id))
    
    return render_template('new_npc.html', settlement=settlement)

@app.route('/npc/<int:npc_id>')
def npc_detail(npc_id):
    npc = NPC.query.get_or_404(npc_id)
    settlement = db.session.get(Settlement, npc.settlement_id)
    
    # Beräkna settlement-påverkan
    settlement_effects = []
    if settlement.aggression > 60:
        settlement_effects.append('Brutaliserad av krigföring (+2 Combat, -2 Charisma)')
    if settlement.resource_level < 30:
        settlement_effects.append(f'Desperat (-10 Loyalty, nu {npc.loyalty})')
    if settlement.trust < 25:
        settlement_effects.append('Misstänksam mot främlingar')
    
    return render_template('npc_detail.html', npc=npc, settlement=settlement, settlement_effects=settlement_effects)

@app.route('/api/settlements')
def api_settlements():
    settlements = Settlement.query.all()
    return jsonify([s.to_dict() for s in settlements])

@app.route('/api/settlement/<int:settlement_id>')
def api_settlement(settlement_id):
    settlement = Settlement.query.get_or_404(settlement_id)
    return jsonify(settlement.to_dict())

@app.route('/api/settlement/<int:settlement_id>/npcs')
def api_settlement_npcs(settlement_id):
    npcs = NPC.query.filter_by(settlement_id=settlement_id).all()
    return jsonify([npc.to_dict() for npc in npcs])

# Regional översikt
@app.route('/regional_overview')
def regional_overview():
    settlements = Settlement.query.all()
    
    # Beräkna regional stabilitet
    if settlements:
        avg_structure = sum(s.social_structure for s in settlements) / len(settlements)
        avg_resource = sum(s.resource_level for s in settlements) / len(settlements)
        regional_stability = (avg_structure + avg_resource) / 2
    else:
        regional_stability = 0
    
    # Status kategorisering
    if regional_stability < 30:
        stability_status = 'KAOSREGION'
        stability_class = 'danger'
    elif regional_stability < 50:
        stability_status = 'INSTABIL'
        stability_class = 'warning'
    elif regional_stability < 70:
        stability_status = 'STABIL'
        stability_class = 'info'
    else:
        stability_status = 'BLOMSTRANDE'
        stability_class = 'success'
    
    return render_template('regional_overview.html', 
                         settlements=settlements,
                         regional_stability=regional_stability,
                         stability_status=stability_status,
                         stability_class=stability_class)

# ============================================================================
# INITIALIZE DATABASE
# ============================================================================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")

# OBS: Exempeldata seedas via `python init_db.py` (se den filen) - inte via
# ett separat `flask seed_db`-kommando, för att undvika två datauppsättningar
# som kan glida isär.

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# template_filters.py - Lägg till i app.py
from flask import Flask
import json

def init_template_filters(app):
    """Registrera custom Jinja2 filters"""
    
    @app.template_filter('from_json')
    def from_json_filter(value):
        """Convert JSON string to Python object"""
        if not value:
            return {}
        try:
            return json.loads(value)
        except:
            return {}
    
    return app
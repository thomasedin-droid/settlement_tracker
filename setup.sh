#!/bin/bash
# setup.sh - Installation script för Settlement Tracker

echo "═══════════════════════════════════════════════════════════"
echo "         SETTLEMENT TRACKER - INSTALLATION"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "Kontrollerar Python-version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 hittades inte. Installera Python 3.8+ först."
    exit 1
fi

echo "✓ Python hittades"
echo ""

# Create virtual environment
echo "Skapar virtuell miljö..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Kunde inte skapa virtuell miljö"
    exit 1
fi

echo "✓ Virtuell miljö skapad"
echo ""

# Activate virtual environment
echo "Aktiverar virtuell miljö..."
source venv/bin/activate

# Install dependencies
echo "Installerar dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Kunde inte installera dependencies"
    exit 1
fi

echo "✓ Dependencies installerade"
echo ""

# Initialize database
echo "Initierar databas..."
python init_db.py

if [ $? -ne 0 ]; then
    echo "❌ Kunde inte initiera databas"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "         ✓✓✓ INSTALLATION KLAR! ✓✓✓"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "För att starta applikationen:"
echo "  1. Aktivera virtuell miljö: source venv/bin/activate"
echo "  2. Starta server: python run.py"
echo "  3. Öppna webbläsare: http://localhost:5000"
echo ""
echo "═══════════════════════════════════════════════════════════"
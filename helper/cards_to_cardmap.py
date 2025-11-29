import json
import re

INPUT_FILE = "cards.json"
OUTPUT_FILE = "cardmap.json"

def normalize_key(s: str) -> str:
    """Sonderzeichen entfernen, alles klein und zusammen."""
    s = s.lower()
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

# Lade das JSON-Array
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    cards = json.load(f)

# Sortiere die Karten nach normalisiertem Key alphabetisch
cards.sort(key=lambda c: normalize_key(c["key"]))

card_map = {}
counter = 1

# Berechne maximale Key-Länge für Ausrichtung
max_key_len = 0
for card in cards:
    keys = [card["key"], card["name"], card.get("sc_key", "")]
    for k in keys:
        if k:
            nk = normalize_key(k)
            max_key_len = max(max_key_len, len(nk))

# Erstelle Mapping ohne doppelte Keys
lines = []
for card in cards:
    keys = [card["key"], card["name"], card.get("sc_key", "")]
    keys = [normalize_key(k) for k in keys if k]  # normalize und leere Keys ignorieren
    for k in keys:
        if k not in card_map:
            card_map[k] = counter
            line = f'"{k}": {" " * (max_key_len - len(k) + 4)}{counter},'
            lines.append(line)
    lines.append("")  # leere Zeile zwischen Karten
    counter += 1

# Schreibe die Datei
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("{\n")
    f.write("\n".join(lines))
    f.write("\n}")

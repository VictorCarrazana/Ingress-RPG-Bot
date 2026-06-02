HEADERS = [
    "Time Span",
    "Agent Name",
    "Agent Faction",
    "Date (yyyy-mm-dd)",
    "Time (hh:mm:ss)",
    "Level",
    "Lifetime AP",
    "Current AP",
    "Unique Portals Visited",
    "Unique Portals Drone Visited",
    "Furthest Drone Distance",
    "Seer Points",
    "XM Collected",
    "OPR Agreements",
    "Portal Scans Uploaded",
    "Uniques Scout Controlled",
    "Resonators Deployed",
    "Links Created",
    "Control Fields Created",
    "Mind Units Captured",
    "Longest Link Ever Created",
    "Largest Control Field",
    "XM Recharged",
    "Portals Captured",
    "Unique Portals Captured",
    "Mods Deployed",
    "Hacks",
    "Drone Hacks",
    "Glyph Hack Points",
    "Overclock Hack Points",
    "Completed Hackstreaks",
    "Longest Sojourner Streak",
    "Resonators Destroyed",
    "Portals Neutralized",
    "Enemy Links Destroyed",
    "Enemy Fields Destroyed",
    "Battle Beacon Combatant",
    "Drones Returned",
    "Machina Links Destroyed",
    "Machina Resonators Destroyed",
    "Machina Portals Neutralized",
    "Machina Portals Reclaimed",
    "Max Time Portal Held",
    "Max Time Link Maintained",
    "Max Link Length x Days",
    "Max Time Field Held",
    "Largest Field MUs x Days",
    "Forced Drone Recalls",
    "Distance Walked",
    "Kinetic Capsules Completed",
    "Unique Missions Completed",
    "Research Bounties Completed",
    "Research Days Completed",
    "Mission Day(s) Attended",
    "NL-1331 Meetup(s) Attended",
    "First Saturday Events",
    "Second Sunday Events",
    "Orion Tokens",
    "Orion Link And Field Points",
    "Recursions",
    "Months Subscribed"
]

def parse_stats(text):
    text = text.strip()

    # =========================================
    # PASO 1: separar headers de valores
    # Buscamos el primer header ("Time Span") y el último ("Months Subscribed")
    # Todo lo que venga DESPUÉS de los headers son los valores
    # =========================================
    
    last_header = "Months Subscribed"
    idx = text.find(last_header)
    
    if idx == -1:
        raise Exception("No se encontraron los headers en el texto.")
    
    values_text = text[idx + len(last_header):].strip()
    
    # =========================================
    # PASO 2: detectar dinámicamente qué headers están presentes
    # Tomamos todo el texto ANTES de los valores y extraemos los headers
    # =========================================
    
    headers_text = text[:idx + len(last_header)]
    
    # Buscamos qué headers conocidos están presentes Y en qué orden
    found_headers = []
    search_from = 0
    for header in HEADERS:
        pos = headers_text.find(header, search_from)
        if pos != -1:
            found_headers.append(header)
            search_from = pos + len(header)  # avanzamos para mantener el orden
    
    # =========================================
    # PASO 3: tokenizar los valores
    # =========================================
    
    tokens = values_text.split()
    
    # =========================================
    # PASO 4: emparejar dinámicamente
    # Los primeros campos son especiales (no numéricos)
    # =========================================
    
    player_data = {}
    pos = 0  # cursor en tokens
    
    for header in found_headers:
        if pos >= len(tokens):
            player_data[header] = None  # no hay más valores
            continue
        
        if header == "Time Span":
            if tokens[pos].upper() == "ALL":
                player_data[header] = "ALL TIME"
                pos += 2
            else:
                # formato "2026-01-01 to 2026-05-19"
                player_data[header] = f"{tokens[pos]} {tokens[pos+1]} {tokens[pos+2]}"
                pos += 3
        
        elif header in ("Agent Name", "Agent Faction", "Date (yyyy-mm-dd)", "Time (hh:mm:ss)"):
            player_data[header] = tokens[pos]
            pos += 1
        
        else:
            # campo numérico
            try:
                player_data[header] = int(tokens[pos])
            except ValueError:
                player_data[header] = tokens[pos]  # lo guarda como string si no es número
            pos += 1
    
    # =========================================
    # PASO 5: si el texto tiene headers nuevos que no conocemos,
    # los ignoramos — el bot sigue funcionando igual
    # =========================================
    
    return player_data

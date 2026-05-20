import re

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
    "Anomaly Unique Hacks",
    "Orion Tokens",
    "Orion Link And Field Points",
    "Recursions",
    "Months Subscribed"
]


def parse_value(v):
    if v is None:
        return 0

    v = v.strip()

    # limpiar separadores raros
    v = v.replace(",", "")
    
    try:
        return int(v)
    except:
        try:
            return float(v)
        except:
            return v


def extract_field(text, field):
    """
    Busca "FieldName: value" o "FieldName value"
    tolerante a saltos, emojis y Telegram
    """

    pattern = rf"{re.escape(field)}\s*[:\-]?\s*([^\n]+)"
    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return None

    value = match.group(1)

    # cortar si aparece otro header después (evita contaminación)
    for h in HEADERS:
        if h != field and h in value:
            value = value.split(h)[0]

    return value.strip()


def parse_stats(text):
    data = {}

    for header in HEADERS:
        raw_value = extract_field(text, header)
        data[header] = parse_value(raw_value)

    return data
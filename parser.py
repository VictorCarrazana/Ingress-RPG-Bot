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


def parse_stats(text):

    # convertir todo a una sola línea
    clean_text = text.replace("\n", " ")

    # separar palabras
    tokens = clean_text.split()

    # buscar ALL TIME
    try:
        start_index = tokens.index("ALL")
    except:
        raise Exception(
            "No se encontró inicio de stats."
        )

    # reconstruir Time Span
    tokens[start_index] = "ALL TIME"

    # eliminar TIME sobrante
    del tokens[start_index + 1]

    values = tokens[start_index:]

    if len(values) < len(HEADERS):
        raise Exception(
            "Stats incompletas."
        )

    data = {}

    for i, header in enumerate(HEADERS):

        value = values[i]

        try:
            data[header] = int(value)

        except:
            try:
                data[header] = float(value)

            except:
                data[header] = value

    return data
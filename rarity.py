def calculate_rarity(results):

    scores = list(results.values())

    max_score = max(scores)

    count_85 = sum(
        1 for s in scores if s >= 85
    )

    # =====================================
    # ASCENDIDO
    # =====================================

    if count_85 >= 3:
        return {
            "name": "Ascendido",
            "description": "Domina múltiples estilos de juego."
        }

    # =====================================
    # HIBRIDO
    # =====================================

    if count_85 == 2:
        return {
            "name": "Híbrido",
            "description": "Especialista en dos perfiles."
        }

    # =====================================
    # LEGENDARIO
    # =====================================

    if max_score >= 90:
        return {
            "name": "Legendario",
            "description": "Nivel de especialización extremadamente raro."
        }

    # =====================================
    # ELITE
    # =====================================

    if max_score >= 85:
        return {
            "name": "Elite",
            "description": "Perfil altamente dominante."
        }

    # =====================================
    # NORMAL
    # =====================================

    return {
        "name": "Comun",
        "description": "Agente equilibrado."
    }
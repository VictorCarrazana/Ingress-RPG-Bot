from profiles import PROFILES

def calculate_profiles(player_data):

    results = {}

    for profile_name, profile_data in PROFILES.items():

        score = 0

        for stat_name, values in profile_data["stats"].items():

            reference, weight = values

            player_value = player_data.get(stat_name, 0)

            partial = (player_value / reference) * weight

            if partial > weight:
                partial = weight

            score += partial

        results[profile_name] = round(score)

    return results
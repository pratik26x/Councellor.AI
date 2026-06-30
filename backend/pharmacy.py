import pandas as pd

def generate_preferred_college_list(student_percentile, student_category, student_branch, data, preferred_cities):
    preferred_colleges = []

    category_column_mapping = {
        "OPEN": "OPEN Percentile",
        "SC":   "SC Percentile",
        "ST":   "ST Percentile",
        "NT1":  "NT1 Percentile",
        "OBC":  "OBC Percentile",
        "EWS":  "EWS Percentile",
        "TWFS": "TWFS Percentile"
    }

    if student_category not in category_column_mapping:
        return []

    category_percentile_column = category_column_mapping[student_category]

    # Normalise preferred cities to lowercase for case-insensitive matching
    preferred_cities_lower = [c.lower().strip() for c in preferred_cities] if preferred_cities else []

    for _, row in data.iterrows():
        college_name      = row['College Name']
        branch_name       = row['Branch Name']
        cutoff_rank       = row['Cutoff Rank']
        city              = str(row['City']).strip()
        cutoff_percentile = row[category_percentile_column]

        # City filter — case-insensitive partial match
        # e.g. "Mumbai" matches "Mumbai", "Navi Mumbai", "Mumbai Suburban"
        if preferred_cities_lower:
            city_lower = city.lower()
            if not any(pref in city_lower or city_lower in pref for pref in preferred_cities_lower):
                continue

        # Percentile filter
        if pd.isnull(cutoff_percentile) or student_percentile < float(cutoff_percentile):
            continue

        # Branch filter — case-insensitive partial match
        if student_branch is not None:
            if student_branch.lower().strip() not in branch_name.lower():
                continue

        preferred_colleges.append({
            "college_name":       college_name,
            "branch_name":        branch_name,
            "city":               city,
            "cutoff_rank":        cutoff_rank,
            "cutoff_percentile":  cutoff_percentile,
            "category":           student_category,
            # Keep legacy string format for backward compat
            "display": f"{college_name} ({branch_name}) - {city}, Cutoff Rank: {cutoff_rank}, {student_category} Cutoff Percentile: {cutoff_percentile}"
        })

    return preferred_colleges

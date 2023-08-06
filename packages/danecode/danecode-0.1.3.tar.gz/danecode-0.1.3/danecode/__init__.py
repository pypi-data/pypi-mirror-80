import jellyfish

from .country_data import departments


def get_data(department, municipality):

    department = department.lower()
    municipality=municipality.lower()

    department, department_distance = get_less_distant_item(
        department, departments.keys())

    municipalities = departments[department]['municipalities']
    municipality, municipality_distance = get_less_distant_item(
        municipality, municipalities.keys())


    dane_code =  departments[department]['municipalities']\
        [municipality]['dane_code']

    place_data = {
        "department":department,
        "department_code": departments[department]['dane_code'],
        "department_levenshtein_distance": department_distance,
        "municipality":municipality,
        "municipality_code": dane_code,
        "minicipality_levenshtein_distance": municipality_distance,
    }

    return place_data


def get_less_distant_item(to_compare, options):
    last_distance = None

    for option in options:
        distance = jellyfish.levenshtein_distance(to_compare, option)

        if last_distance == None:
            last_distance = distance
        elif distance > last_distance:
            continue

        last_distance = distance
        best_value = option

    return best_value, last_distance

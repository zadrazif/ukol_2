import json

def open_geojson(nazev_souboru):
    try:
        with open(nazev_souboru, encoding = 'utf-8') as f:
            containers_input = json.load(f)
            features = containers_input['features']
    except ValueError:
        print(f"Soubor {nazev_souboru} je chybný.")
        exit()
    except FileNotFoundError:
        print(f"Soubor {nazev_souboru} nebyl nalezen.")
        exit()
    except PermissionError:
        print(f"Soubor {nazev_souboru} je nepřístupný.")
    return features

features = open_geojson("zkouska.pptx")
print(features)
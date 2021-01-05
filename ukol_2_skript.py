import json, pyproj, math, statistics
from pyproj import Transformer
from math import hypot 

#Funkce, která otevírá geojson soubory kontejnerů a ošetřuje nekorektní vstupy 
def containers_file_open(container_file):
    try:
        with open(container_file, encoding = 'utf-8') as f:
            containers_input = json.load(f)
            features = containers_input['features']
    except ValueError:
        print(f"Soubor {container_file} je chybný.")
        exit()
    except FileNotFoundError:
        print(f"Soubor {container_file} nebyl nalezen.")
        exit()
    except PermissionError:
        print(f"Soubor {container_file} je nepřístupný.")
        exit()
    
    return features

#Funkce, která vyfiltruje jen ty kontejnery, které jsou volně přístupné 
def container_access_filter(features):
    containers_coords_sjtsk = []
    for feature in features:
        if feature['properties']['PRISTUP'] == 'volně':
            souradnice = feature['geometry']['coordinates']
            containers_coords_sjtsk.append(souradnice)
    return containers_coords_sjtsk

#Funkce, která otevírá geojson soubory adres a ošetřuje nekorektní vstupy 
"""def address_file_open(address_file):
    try:
        with open(address_file, encoding = 'utf-8') as f:
            address_input = json.load(f)
            addresses = address_input['features']
    except ValueError:
        print(f"Soubor {address_file} je chybný.")
        exit()
    except FileNotFoundError:
        print(f"Soubor {address_file} nebyl nalezen.")
        exit()
    except PermissionError:
        print(f"Soubor {address_file} je nepřístupný.")
        exit()
    
    return addresses"""

#Funkce, která převede souřadnice adres z WGS84 do S-JTSK a vrátí list slovníků obsahujících adresu a souřadnice adresního bodu
def address_points(addresses):
    positions = []
    transformer = Transformer.from_crs(4326, 5514, always_xy=True)
    for adresa in addresses:
        records = {}
        records['adresa'] = adresa['properties']['addr:street'] + ' ' + adresa['properties']['addr:housenumber']
        records['souradnice'] = transformer.transform(adresa['geometry']['coordinates'][0], adresa['geometry']['coordinates'][1])
        positions.append(records)
    return positions

#Funkce, která vypočítá nejkratší vzdálenosti ke kontejneru pro každý adresního bod
#Zároveň funkce vybere největší hodnotu z nejkratších vzdáleností a vrátí ji společně s adresou, pro níž nejvyšší hodnota platí 
def address_point_container_distance(positions, containers_coords_sjtsk):
    farthest_distance_address = 'Šalingrad'
    distances = []
    farthest_value = 0
    for adresa in positions:
        shortest_distance = 10000
        for kontejner in containers_coords_sjtsk:
            diff_lon = adresa['souradnice'][0] - kontejner[0]
            diff_lat = adresa['souradnice'][1] - kontejner[1]
            distance = math.hypot(diff_lon, diff_lat)
            if distance <= shortest_distance:
                shortest_distance = distance
        distances.append(shortest_distance)
        if shortest_distance > farthest_value:
            farthest_value = shortest_distance
            farthest_distance_address = adresa['adresa']
    return farthest_value, farthest_distance_address, distances

#Spuštění výše vypsaných funkcí
features = containers_file_open("soubor_kontejnery.geojson")
addresses = address_file_open("soubor_adresy.geojson")  
containers_coords_sjtsk = container_access_filter(features) 
positions = address_points(addresses) 
farthest_value, farthest_distance_address, distances = address_point_container_distance(positions, containers_coords_sjtsk)

#Výpočet průměru a mediánu nejkratších vzdáleností ke kontejnerům  
mean = statistics.mean(distances)
median = statistics.median(distances)

#Výstup programu
print("Celkem načteno", len(positions), "adresních bodů")
print("Celkem načteno", len(containers_coords_sjtsk), "kontejnerů na tříděný odpad")
print("Průměrná vzdálenost z adresního bodu ke kontejneru je:", f"{mean:.0f}", "m")
print("Medián vzdáleností z adresního bodu ke kontejneru je:", f"{median:.0f}", "m")
print("Největší vzdálenost ke kontejneru je", f"{farthest_value:.0f}", "m a to z adresy", farthest_distance_address)

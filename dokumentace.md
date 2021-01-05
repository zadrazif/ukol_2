# Dokumentace k 2. domácímu úkolu

### Úvod
Tento program dokáže po načtení vstupních souborů zjistit, jaká je minimální vzdálenost z adresních bodů ke kontejneru na tříděný odpad. Lze ho tedy využít například jako užitečnou pomůcku při analýze dostupnosti kontejnerů pro obyvatelstvo.

### Vstupní soubory
Vstupy do programu existují hned dva, oba ve formátu `.geojson`. Prvním z nich je `soubor_adresy.geojson`, který obsahuje adresní body v Praze na Starém Městě. Byl stažen ze stránky [Overpass Turbo](http://overpass-turbo.eu/). Ten obsahuje pro náš program důležité klíče `addr:street`, `addr:housenumber` a `coordinates`. Druhým vstupem je `soubor_kontejnery.geojson`, který byl získán ze stránek [pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB). Zde pracujeme s klíči `coordinates` a `PRISTUP`. Druhý zmiňovaný klíč nám slouží ve funkci `container_access_filter` k tomu, abychom odstranili ze seznamu kontejnery, které jsou přístupné pouze obyvatelům daného domu a dále pracovali jen s volně přístupnými. Ve funkci `load_json`, která načítá vstupy zároveň nalezneme užitečné ošetření proti načtení nevalidního souboru pomocí příkazů `try` a `except`. 

### Převod souřadnic
Vzhledem k tomu, že souřadnice adresních bodů jsou v souřadnicovém systému WGS84, byli jsme nuceni ve funkci `address_points` zajistit převod těchto souřadnic do S-JTSK. V téže funkci jsme vytvořili seznam `positions`, který obsahoval slovníky obsahující ulici, číslo popisné a již zmíněné převedené souřadnice pro každý adresní bod. 

### Výpočet nejkratších vzdáleností
Stěžejní funkcí programu je `address_point_container_distance`. Ta vrací hned několik důležitých informací. Tou snad úplně hlavní je schopnost zjistit nejkratší vzdálenost ke kontejneru pro každý adresní bod. Dokáže však také zjistit, pro jaký adresní bod je ona vypočítaná nejkratší vzdálenost největší. Pro takový adresní bod navíc vrátí i jeho přesnou adresu (ulice + číslo popisné).

### Výstupy
Další nezbytnou součástí programu je spuštění výše popsaných funkcí. Následuje výpočet průměru a mediánu pro nejkratší vzdálenosti ke kontejnerům a k uložení těchto hodnot do proměnných `mean` a `median`. Poslední část programu tvoří samotný výstup. Ten slouží jako sumář hodnot zjištěných v programu. Mimo jiné zde najdeme i celkový počet adresních bodů a kontejnerů. Všechny tři uvedené hodnoty pro vzdálenost zde byly zaokrouhleny ve formátovacím řetězci.

Příklad výstupu pro lokalitu Praha, Staré Město:
```
Celkem načteno 1891 adresních bodů
Celkem načteno 3449 kontejnerů na tříděný odpad
Průměrná vzdálenost z adresního bodu ke kontejneru je: 136 m
Medián vzdáleností z adresního bodu ke kontejneru je: 128 m
Největší vzdálenost ke kontejneru je 330 m a to z adresy Křižovnické náměstí 191/3
```

Filip Zadražil
3. BGEKA

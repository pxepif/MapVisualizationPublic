import folium
import numpy as np
import pandas as pd
import geopandas as gpd

def pullActualCoords(round, geoJson):
    row = geoJson[geoJson["name"] == round]
    lon = row.geometry.x.values[0]
    lat = row.geometry.y.values[0]
    return lat, lon

def createMap(otherRoundsSpreadSheet, geoJson, username):
    map = folium.Map(location=[0, 0], zoom_start=2)
    winnerCoords = otherRoundsSpreadSheet.loc[otherRoundsSpreadSheet['winner'] == username, ['lat', 'lng', 'round']]
    print(winnerCoords)
    if not winnerCoords.empty:
        for lat, lon, roundName in winnerCoords.values:
            folium.Marker(location = [lat, lon], popup="Winner Location", icon=folium.Icon(color='red')).add_to(map)
            actualLocation = pullActualCoords(roundName, geoJson)
            folium.Marker(location = actualLocation, popup="Actual Location", icon=folium.Icon(color='black', icon='info-sign')).add_to(map)
            folium.PolyLine(locations=[(lat, lon), actualLocation], color='red', weight=2.5, opacity=1).add_to(map)
    else:
        winnerCoords = None
    silverCoords = otherRoundsSpreadSheet.loc[otherRoundsSpreadSheet['silver'] == username, ['silver_lat','silver_lng', 'round']]
    print(silverCoords)
    if not silverCoords.empty:
        for lat, lon, roundName in silverCoords.values:
            folium.Marker(location = [lat, lon], popup="Silver Location", icon=folium.Icon(color='green')).add_to(map)
            actualLocation = pullActualCoords(roundName, geoJson)
            folium.Marker(location = actualLocation, popup="Actual Location", icon=folium.Icon(color='black', icon='info-sign')).add_to(map)
            folium.PolyLine(locations=[(lat, lon), actualLocation], color='green', weight=2.5, opacity=1).add_to(map)
    else:
        silverCoords = None
    bronzeCoords = otherRoundsSpreadSheet.loc[otherRoundsSpreadSheet['bronze'] == username, ['bronze_lat','bronze_lng', 'round']]
    print(bronzeCoords)
    if not bronzeCoords.empty:
        for lat, lon, roundName in bronzeCoords.values:
            folium.Marker(location = [lat, lon], popup="Bronze Location", icon=folium.Icon(color='blue')).add_to(map)
            actualLocation = pullActualCoords(roundName, geoJson)
            folium.Marker(location = actualLocation, popup="Actual Location", icon=folium.Icon(color='black', icon='info-sign')).add_to(map)
            folium.PolyLine(locations=[(lat, lon), actualLocation], color='blue', weight=2.5, opacity=1).add_to(map)
    else:   
        bronzeCoords = None
    #make map
    legend_html = '''<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 150px; height: 110px; 
    background-color: white; 
    border:2px solid grey; z-index:9999; 
    font-size:14px;
    padding: 10px;
">
<b>Legend</b><br>
<i class="fa fa-map-marker" style="color:red"></i>&nbsp;Winner<br>
<i class="fa fa-map-marker" style="color:green"></i>&nbsp;Silver<br>
<i class="fa fa-map-marker" style="color:blue"></i>&nbsp;Bronze<br>
<i class="fa fa-map-marker" style="color:black"></i>&nbsp;Actual Location
</div>'''
    map.get_root().html.add_child(folium.Element(legend_html))
    map.save("testMap.html")

def main():
    otherRoundsSpreadSheet = pd.read_csv("insert_path\\country cities sim with others rounds.csv") #REPLACE insert_path WITH ACTUAL FILE PATH
    geoJson = gpd.read_file("insert_path\\Cities from cities500 (one per graticule).geojson") #REPLACE insert_path WITH ACTUAL FILE PATH
    print("Type in your username")
    username = input()
    if (username not in otherRoundsSpreadSheet['winner'].values and 
    username not in otherRoundsSpreadSheet['silver'].values and 
    username not in otherRoundsSpreadSheet['bronze'].values):
        print("Username not found! Exiting program.")
        exit()
    createMap(otherRoundsSpreadSheet, geoJson, username)
    
if __name__ == "__main__":
    main()
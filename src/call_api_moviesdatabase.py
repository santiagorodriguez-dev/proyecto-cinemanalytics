import sys
import os
import http.client
import json
import pandas as pd # type: ignore
import asyncio

import sys
sys.path.append("../")
from src import soporte as sop

async def get_datos_movies(genre, titleType, page,key ):

    result = []
    #try:
    url = http.client.HTTPSConnection("moviesdatabase.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "moviesdatabase.p.rapidapi.com"
    }

    url_data = f"/titles?genre={genre}&startYear=1990&titleType={titleType}&sort=year.incr&page={page}"

    url.request(f"GET", url_data, headers=headers)

    res = url.getresponse()
    data = res.read()
    dicc_datos = json.loads(data.decode("utf-8"))

    result = dicc_datos['results']

    for r in result:
        print(r)
        thisdict = {
            "id": r['id'],
            "titleText": r['titleText'],
            # "releaseYear":  r['releaseYear']
            }
        result.append(thisdict)
    #except:
        #print(f"Error al hacer peticion api, en get_datos_movies: {url}")
    return result

async def alamacenar_datos_in_csv(key):

    df_final = pd.DataFrame()

    # genre = ["Drama", "Comedy", "Action", "Fantasy", "Horror", "Mystery", "Romance", "Thriller"]
    # titleType = ["movie","short"]

    genre = ["Drama"]
    titleType = ["movie"]
     
    for p in range(1,2):
        print(p)
        for g in genre:
            for t in titleType:
                diccionario = await get_datos_movies(g, t, p, key)
                df_temp = pd.DataFrame(diccionario)

            df_final = pd.concat([df_temp, df_final], ignore_index=True)
            df_final.to_csv(f"../data/data_movies.csv")



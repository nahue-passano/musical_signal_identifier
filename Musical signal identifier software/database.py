# -*- coding: utf-8 -*-
"""
Generación de la base de datos
"""

from fingerprint import fingerprint
import pickle

def database_function():
    """
    database_function():
        La función genera la base de datos cuando se la ejecuta, conteniendo
        los nombres de las canciones, como su path para reproducción y su res-
        -pectiva fingerprint. Toda esta información se aloja en la variable
        database, la cual es guardada con la librería pickle.

    """
    database_fp = [0]*6
    database_song = [0]*6
    database_path = [0]*6
    
    database_path[0] = 'audios_base_de_datos/bensound-dubstep.wav'    
    database_path[1] = 'audios_base_de_datos/bensound-funkyelement.wav'
    database_path[2] = 'audios_base_de_datos/bensound-happyrock.wav'
    database_path[3] = 'audios_base_de_datos/bensound-jazzyfrenchy.wav'
    database_path[4] = 'audios_base_de_datos/bensound-popdance.wav'
    database_path[5] = 'audios_base_de_datos/bensound-ukulele.wav'  
    
    database_fp[0] = fingerprint(database_path[0],0)
    database_fp[1] = fingerprint(database_path[1],0)
    database_fp[2] = fingerprint(database_path[2],0)
    database_fp[3] = fingerprint(database_path[3],0)
    database_fp[4] = fingerprint(database_path[4],0)
    database_fp[5] = fingerprint(database_path[5],0)
    
    database_song[0] = 'Dubstep - Bensound' 
    database_song[1] = 'Funky element - Bensound'
    database_song[2] = 'Happy rock - Bensound'
    database_song[3] = 'Jazzy frenchy - Bensound'
    database_song[4] = 'Popdance - Bensound'
    database_song[5] = 'Ukulele - Bensound' 
    
    database = [database_song , database_fp, database_path]
        
    with open('database.pickle','wb') as f:
            pickle.dump([database],f)
            
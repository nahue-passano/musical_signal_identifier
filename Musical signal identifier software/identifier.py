# -*- coding: utf-8 -*-
"""
Identificación de la canción
"""
def identifier(wav_file,it_recorded):
    """
    Parameters
    ----------
    wav_file : ndarray of 1D
        Archivo en formato .wav que se desea comparar
    it_recorded : int
        Selecciona y diferencia entre un audio que se esta grabando o un audio ya en formato .wav

    Returns
    -------
    song : str
        Nombre de la canción si es que hay coincidencia
    song_path : str
        Path de la canción si es que hay coincidencia

    """
    
    import numpy as np
    from fingerprint import fingerprint
    import scipy.signal as signal
    from database import database_function
    import pickle
    import copy
    
    try:
        with open('database.pickle', 'rb') as f:
            database = pickle.load(f)
    except:
        database_function()
        with open('database.pickle', 'rb') as f:
            database = pickle.load(f)
        
    audio_test = fingerprint(wav_file,it_recorded)
        
    max_correlations = np.empty(6)
    
    ## Correlación entre la señal a analizar y cada una de las canciones de la base de datos
    for i in np.arange(6):
        audio_base_i = database[0][1][i]
        max_correlations [i] = np.max(signal.correlate2d(audio_base_i, audio_test, mode='valid'))
    
    first_max_corr = np.max(max_correlations)
    index_first_max_corr = np.argmax(max_correlations)
    
    ## Cálculo del segundo máximo de correlación
    aux_max_correlations = copy.deepcopy(max_correlations)
    aux_max_correlations[index_first_max_corr] = 0
    second_max_corr = np.max(aux_max_correlations)
    
    ## Criterio de decisión 
    if first_max_corr >= 2.5*second_max_corr or first_max_corr >= 20:
        song = database[0][0][index_first_max_corr]
        song_path = database[0][2][index_first_max_corr]      
    else:
        song ='no_match'
        song_path = 0
     
    return song, song_path
    
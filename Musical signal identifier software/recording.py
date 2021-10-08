# -*- coding: utf-8 -*-
"""
Grabación del audio a analizar
"""

def recording(time):
    """
    Parameters
    ----------
    time : int
        Tiempo de grabación

    Returns
    -------
    audio_muestra : ndarray of 1D
        Vector con la información de la grabación.

    """
    
    import sounddevice as sd
    import numpy as np
    
    sd.default.device = 1
    sd.default.channels = 1,12
    
    fs = 8000  # Frecuencia de muestreo
    
    print('Grabando...')
    
    audio_muestra = sd.rec(int(time * fs), samplerate=fs, channels=1,dtype='float32')
    sd.wait()  # Espera hasta que la grabación finalice.
    audio_muestra = np.array(audio_muestra)
    audio_muestra = audio_muestra.flatten()
    print('Grabación finalizada.')
    
    return audio_muestra

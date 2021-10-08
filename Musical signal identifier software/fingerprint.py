# -*- coding: utf-8 -*-
"""
Extracción de información: fingerprint
"""

def fingerprint(wav_file, it_recorded):
    """
    Parameters
    ----------
    wav_file : ndarray of 1D
        Audio en formato .wav a realizar la fingerprint
    it_recorded : int
        Selecciona y diferencia entre un audio que se esta grabando o un audio ya en formato .wav

    Returns
    -------
    z_fingerprint : matrix
        Fingerprint de la señal de audio ingresada

    """

    import scipy.signal as signal
    import librosa    
    import numpy as np
    from scipy.ndimage.filters import maximum_filter
    from scipy.ndimage import (generate_binary_structure,iterate_structure)
    
    if it_recorded == 1:
        wav = np.transpose(wav_file)
        fs = 8000
    else:
        wav, fs = librosa.load(wav_file, sr=8000, mono=True) # Downsample 44.1kHz to 8kHz
    
    y_f,x_t,z_stft = signal.stft(wav,fs=fs,window='boxcar',nperseg=1000)
    z_stft_abs = np.abs(z_stft)/np.max(np.abs(z_stft))
    
    # Filtrado de máximos locales de cada partición:
        # Se genera una nueva matriz (z_local_max) donde almacena el máximo de cada partición
        # generada por struct y size_partición. Dicho máximo de cada partición lo repite para
        # todos los indices de dicha partición.
         
    size_particion = 5  
    struct = generate_binary_structure(2, 2) #Genera una matriz booleana de 3x3 con todo True
    particion = iterate_structure(struct, size_particion) #Que da de 21x21
    z_local_max = maximum_filter(z_stft_abs,footprint=particion) 
    
    
    # Se comparan los máximos locales con la función para detectar precisamente en que
    # indices se encuentran dichos máximos
    z_fingerprint = (z_stft_abs == z_local_max)
    z_fingerprint = np.array(z_fingerprint,dtype=int)


    return z_fingerprint
    
"""
This module is aimed at signal analysis and beamforming of data (.wav format) from microphones in a ULA configuration.

This package contains the following functions :
    find_extrema(wavform_data, maxima_or_minima) : 
        Finds the values of the maximas or the minimas (and their index locations) of a given sinusoidal waveform passed as a 1D numpy array.
    
And the following classes :
    Nil
"""

import numpy as np
from arlpy.bf import steering_plane_wave

def find_extrema(waveform_data : '1D ndarray', maxima_or_minima: 'str' = 'maxima'):
    """
    Finds the values of the maximas or the minimas (and their index locations) of a given sinusoidal waveform passed as a 1D ndarray.

    Parameters
    ----------
    waveform_data : 1D ndarray
        Sinusoidal waveform to be analysed.
    maxima_or_minima : {'maxima', 'minima'}
        Specify (as a string) whether to find the maximas or minimas of the sinusoidal waveform. (default: 'maxima').

    Returns
    -------
    extrema : 2D ndarray
        Numpy array of extrema index locations and corresponding values.

    Examples
    --------
    >>> waveform = np.sin(np.linspace(0,10*np.pi,1000))
    >>> extrema = find_extrema(waveform, 'minima')
    >>> plt.plot(waveform, '-D', markevery = extrema[0])
    """
    # Check if sample is greater than or equal to 2 samples to the left and two samples to the right. Store in bool array
    
    if maxima_or_minima == 'maxima':
        extrema_map = np.r_[waveform_data[2:] <= waveform_data[:-2],False,False] &\
                    np.r_[waveform_data[1:] <= waveform_data[:-1],False] &\
                    np.r_[False,waveform_data[:-1] <= waveform_data[1:]] &\
                    np.r_[False,False,waveform_data[:-2] <= waveform_data[2:]]
    elif maxima_or_minima == 'minima':
        extrema_map = np.r_[waveform_data[2:] >= waveform_data[:-2],False,False] &\
            np.r_[waveform_data[1:] >= waveform_data[:-1],False] &\
            np.r_[False,waveform_data[:-1] >= waveform_data[1:]] &\
            np.r_[False,False,waveform_data[:-2] >= waveform_data[2:]]
    else:
        raise ValueError("maxima_or_minima arument must be the string 'maxima' or 'minima'")

    # When a local maxima occurs twice consecutively, only count the first one
    extrema_map = extrema_map & np.diff(np.r_[False,extrema_map])

    # Identify when an extrema has been counted twice and remove duplicates
    extrema_index = np.where(extrema_map)[0]
    extrema_spacing = np.diff(extrema_index) # Find the spacing between extremas
    outliers_map = np.r_[True ,abs(extrema_spacing - np.mean(extrema_spacing)) < 8 * np.std(extrema_spacing)] # filter out outliers outside eight standard deviations
    extrema_index = extrema_index[outliers_map] # Remove outliers

    # Find values of extrema
    extrema_values = waveform_data[extrema_index]
    
    # Store results in a 2D ndarray
    extrema = np.array([extrema_index, extrema_values])
    return extrema

def find_amplitudes(waveform_data):
    """
    Finds the amplitudes of a given array of sinusoidal waveforms passed as a 2D ndarray.

    Parameters
    ----------
    waveform_data : 2D ndarray
        Sinusoidal waveforms to be analysed.

    Returns
    -------
    amplitudes : 1D ndarray
        Amplitudes of each sinusoidal waveform.

    Examples
    --------
    >>> waveform1 = np.sin(np.linspace(0,10*np.pi,1000))
    >>> waveform2 = 1.2*waveform1
    >>> waveform_data = np.array([waveform1, waveform2]).transpose()
    >>> amplitudes = find_amplitudes(waveform_data)
    """
    # Find all the extrema for all microphone waveforms
    num_microphones = waveform_data.shape[1]
    maxima = []
    minima = []
    for i in range(num_microphones):
        maxima.append(find_extrema(waveform_data[:,i], maxima_or_minima = 'maxima'))
        minima.append(find_extrema(waveform_data[:,i], maxima_or_minima = 'minima'))
    maxima = np.array(maxima)
    minima = np.array(minima)
    
    # Calculate the average amplitudes of each signal
    amplitudes = []
    for i in range(num_microphones):
        amplitudes.append(np.average(maxima[i][1]) - np.average(minima[i][1]))
    amplitudes = np.array(amplitudes)

    return amplitudes

def find_delays(waveform_data):
    """
    Finds the average time delay (in samples) between sinusoidal signals, using the first sinusoidal signal as a reference.

    Parameters
    ----------
    waveform_data : 2D ndarray
        Sinusoidal waveforms to be analysed.

    Returns
    -------
    average_delay : 1D ndarray
        average time delay (in samples) of each waveform.

    Examples
    --------
    >>> waveform1 = np.sin(np.linspace(0,10*np.pi,1000))
    >>> waveform2 = np.sin(np.linspace(0.1,10*np.pi+0.1,1000))
    >>> waveform_data = np.array([waveform1, waveform2]).transpose()
    >>> delays = find_delays(waveform_data)
    """
    # Find all the extrema for all microphone waveforms
    num_microphones = waveform_data.shape[1]
    maxima = []
    minima = []
    for i in range(num_microphones):
        maxima.append(find_extrema(waveform_data[:,i], maxima_or_minima = 'maxima'))
        minima.append(find_extrema(waveform_data[:,i], maxima_or_minima = 'minima'))
    maxima = np.array(maxima)
    minima = np.array(minima)
    
    # Calculate the average delay (unit: samples) of microphone signal compared to the first microphone in waveform_data
    temp = []
    average_delay = np.zeros(num_microphones)
    for j in range(num_microphones):
        for i in range(maxima.shape[2]-1):
            temp.append(maxima[0,0,i]-maxima[j,0,i])
        average_delay[j] = np.average(temp)
        temp = []
    
    return average_delay

if __name__ == '__main__':
    pass

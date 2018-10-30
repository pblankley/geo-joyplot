import json
import requests
import pandas as pd
import numpy as np

def _make_ranges(top_left, bot_right, n_vert=15, n_horiz=30):
    v_range = np.linspace(top_left[0], bot_right[0], n_vert)
    h_range = np.linspace(top_left[1], bot_right[1], n_horiz)
    return v_range, h_range

def _get_locs(lat, lngs):
    locs = ''
    for lng in lngs:
        if locs=='':
            locs+=str(lat)+','+str(lng)
        else:
            locs+='|'+str(lat)+','+str(lng)
    return locs

def _ping_elev_api(locs, api_key):
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={locs}&key={api_key}'
    response = requests.get(url)
    res_json = json.loads(response.text)
    return res_json

def _parse_elev_json(response):
    return np.array([r['elevation'] for r in response['results']])

def _sample_elev(lngs, elev, min_e):
    arr = np.array([])
    for lng,ele in zip(lngs,elev):
        arr = np.append(arr, np.array([lng]*(int(ele)-int(min_e)+1)))
    return arr

def get_plot_df(top_left, bot_right, api_key=None, n_vert=15, n_horiz=30):
    """ Function to get the dataframe to plot the joyplot of the geography
    ---------
    Args:
        top_left (tuple): tuple of (lat,lng), both floats, that is the top left of the area you want to query
        bot_right (tuple): tuple of (lat,lng), both floats, that is the bottom right of the area you want to query
        api_key (str): the api key you will use to query the Google Elevation API, link below - 
                        https://developers.google.com/maps/documentation/elevation/start
        n_vert (int): the number of points to query vertically (higher shows greater resolution, but is more api calls / slower)
        n_horiz (int): the number of points to query horizontally (higher shows greater resolution, but is more api calls / slower)
    ---------
    Returns:
        (pandas dataframe): has columns 'lat','lng', and 'lat_o'. The 'lat_o' column is used in plotting to make the vertical bands
    ---------
    Raises:
        ValueError if api_key is left at None
    """
    if api_key is None:
        raise ValueError('remember to enter a api key for the Google Elevation API') 
    v_range, h_range = _make_ranges(top_left, bot_right, n_vert=n_vert, n_horiz=n_horiz)

    elev_list = []
    for lat in v_range:
        q = _get_locs(lat, h_range)
        res = _ping_elev_api(q, api_key)
        elev = _parse_elev_json(res)
        elev_list.append(elev)

    min_e = np.min(elev_list)
    list_of_df = []
    for lat,ele in zip(v_range, elev_list):
        samps = _sample_elev(h_range, ele, min_e)
        edf = pd.DataFrame({'lat': np.array([lat]*len(samps)), 'lng': samps})
        list_of_df.append(edf)

    out_df = pd.concat(list_of_df).reset_index(drop=True)
    out_df['lat_o'] = [list(v_range).index(lt) for lt in out_df.lat]
    return out_df

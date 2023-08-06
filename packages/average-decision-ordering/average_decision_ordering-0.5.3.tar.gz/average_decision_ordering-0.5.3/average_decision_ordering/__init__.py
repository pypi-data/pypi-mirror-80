#! /usr/bin/env python

import numpy as np
import pandas as pd
import random

def heaviside(x):
    return 0.5 * (np.sign(x) + 1)

def norm(x):
    return (x-min(x))/(max(x)-min(x))

def random_pairs(x, y, l):
    random.shuffle(x)
    random.shuffle(y)
    min_size = min(len(x), len(y))
    x = x[:min_size]
    y = y[:min_size]
    rp = np.vstack((x,y)).T
    loop_count = 0
    while len(rp) < l:
        random.shuffle(x)
        random.shuffle(y)
        app_rp = np.vstack((x,y)).T
        rp = np.concatenate((rp, app_rp), axis=0)
        loop_count += 1
        if loop_count > 100:
            break
    df = pd.DataFrame({"x":rp[:,0], "y":rp[:,1]})
    df.drop_duplicates(inplace=True, keep='first')
    return df.to_numpy()

def calc_do(fx0, fx1, gx0, gx1):
    def heaviside(x):
        return 0.5 * (np.sign(x) + 1)

    dfx = fx0 - fx1
    dgx = gx0 - gx1
    dos = heaviside(np.multiply(dfx, dgx))
    return dos

def calc_ado(fx, gx, target, n_pairs):
    if n_pairs > len(fx)*len(gx):
        print("Requested pairs exceeds maximum sig/bkg combinations available")
        print("Please choose a value for n_pairs < len(fx)*len(gx)")
        return
    # normalize input data
    fx = norm(fx)
    gx = norm(gx)
        
    # Combine the data into a single dataframe
    dfy = pd.DataFrame({"fx": fx, "gx": gx, "y": target})

    # Separate data into signal and background
    dfy_sb = dfy.groupby("y")
    
    # Set signal/background dataframes
    df0 = dfy_sb.get_group(0)
    df1 = dfy_sb.get_group(1)

    # get the separate sig/bkg indices
    idx0 = df0.index.values.tolist()
    idx1 = df1.index.values.tolist()

    # generate random index pairs
    idx_pairs = random_pairs(idx0, idx1, n_pairs)
    idxp0 = idx_pairs[:, 0]
    idxp1 = idx_pairs[:, 1]

    # grab the fx and gx values for those sig/bkg pairs
    dfy0 = dfy.iloc[idxp0]
    dfy1 = dfy.iloc[idxp1]
    fx0 = dfy0["fx"].values
    fx1 = dfy1["fx"].values
    gx0 = dfy0["gx"].values
    gx1 = dfy1["gx"].values

    # find differently ordered pairs
    dos = calc_do(fx0=fx0, fx1=fx1, gx0=gx0, gx1=gx1)
    ado_val = np.mean(dos)
    if ado_val < 0.5:
        ado_val = 1.0 - ado_val

    return ado_val
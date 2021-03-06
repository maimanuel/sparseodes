# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_meas_to_rec.ipynb (unless otherwise specified).

__all__ = ['rand_par', 'traj_solve']

# Cell
from time import time
import numpy as np
import copy as cp
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy.random import permutation,rand,randn

from sklearn.decomposition import MiniBatchDictionaryLearning
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.feature_extraction.image import reconstruct_from_patches_2d
from sklearn import linear_model
from sklearn.feature_extraction.image import PatchExtractor as PE

from functools import partial,reduce


# Cell
def rand_par(par,cvar):
    '''This function adds gaussian noise to parameters (means) stored in a dictionary.
    Input
        par: dictionary of ODE parameters which constitute the means
        cvar: coeficient of variation of the distributon that each parameter will be sampled from (1 = 100% of the not noisy value).
    return
        dictionary with parameters sampled from gaussian around parameter means (inputs) or zero, if sampled value is negative
        '''
    temp = par.copy()
    for key in temp.keys():
        temp[key]=par[key]*(1+cvar*randn())
        if temp[key] < 0:
            temp[key] = 0
    return temp

# Cell
def traj_solve(N,dt,model_der,mod_par,cvar):
    '''Solve N trajectories with time delta dt for model given in model_der with parameters mod_par
    and coefficient of variation cvar'''
    t0 = 0
    tend = 100
    Nt = round((tend-t0)/float(dt))
    time = np.linspace(t0,tend,Nt)

    traj = np.full((N,len(time),2),-3.)
    for i in range(N):
        # add noise to the paramters
        rlvpar = rand_par(mod_par,cvar)
        yinit = rand(2)*np.array([3,0])
        traj[i,:,:] = odeint(model_der,yinit,time,args = (rlvpar,))
    return traj,time
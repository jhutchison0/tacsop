# -*- coding: utf-8 -*-
"""
Generate Values Based on Number of number
Created on Sun Aug  9 17:07:29 2020

@author: jhutchison
"""

import numpy as np
import pandas as pd
import seaborn as sns


###############################################################################
#### Methods
## 1 SMARTER

## 2 Rank Reciprical

## 3 Rank Sum Method

###############################################################################

def generateweights(data):
    """
    Develop weights for a number of items assuming ranks are 1 to n.  If there
    is a tie, then submit ranks. Number, n, must equal length of ranks.  Ranks
    will supercede number (if n is wrong, functions assumes ranks is correct)
    

    Parameters
    ----------
    data : Either a number (N), list of ranks (repeats are optional), or 
    dictionary of named attributes. Attributes must be unique.
    
    Example: N = 4, list = [1, 2, 2, 4], dict or series = {a:1, b:2, c:2, d:4}

    Returns
    -------
    Table of weights in three methods.

    """
    ## Build Data
    if type(data) == dict:
        data = pd.Series(data)
    if type(data) == pd.Series:
        number = len(data)
        Data = pd.DataFrame(data)
        Data.columns = ['Ranks']
    if (type(data) == int) | (type(data) == float) | (type(data) == list):
        if (type(data) == int) | (type(data) == float):
            number = data
            ranks = range(1,number+1)
            Data = pd.DataFrame(data = ranks, 
                                index = ranks, 
                                columns = ['Ranks'])
        else:    #(type(data) == list)
            number = len(data)
            ranks = data
            Data = pd.DataFrame(data = ranks, 
                                index = range(1,number+1), 
                                columns = ['Ranks'])
    Data.index.name = 'Attributes'
    original_order = Data.index.copy()
    Data = Data.sort_values(by = 'Ranks', axis = 0, ascending = True)
    
    ## Smarter
    Data['1-n'] = range(1, 1+number)
    Data['1/n'] = np.reciprocal(Data['1-n'].astype(float))
    Data['partial_sum'] = Data['1/n'].sort_values(ascending = True).values.cumsum()
    Data['partial_sum'] = Data['partial_sum'].sort_values(ascending = False).values
    
    ## Rank Reciprical
    Data['1/R'] = np.reciprocal(Data['Ranks'].astype('float'))

    ## Rank Sum 
    # find repeats
    Data['rank_adj'] = Data['Ranks'].copy(deep = True)
    repeats = Data['Ranks'].value_counts()
    repeats = repeats[repeats > 1]
    for repeat in repeats.index:
        match_index = Data[Data['Ranks'] == repeat].index
        Data.loc[match_index,'rank_adj'] += (len(match_index)-1)/len(match_index)
        Data.loc[match_index,'partial_sum'] = Data.loc[match_index,'partial_sum'].max()
    Data['rank_adj_rev'] = number - Data['rank_adj'].values + 1
    
    Data['SMARTER'] = Data['partial_sum'] / number
    Data['SMARTER'] = Data['SMARTER'] / Data['SMARTER'].sum()
    Data['Rank_Reciprocal'] = Data['1/R'] / Data['1/R'].sum()
    Data['Rank_Sum'] = Data['rank_adj_rev'] / Data['rank_adj_rev'].sum()
    Results = pd.DataFrame(data = Data[['Ranks',
                                        'SMARTER',
                                        'Rank_Reciprocal',
                                        'Rank_Sum']])
    Results.columns = ['Ranks', 'SMARTER', 'Rank Reciprocal', 'Rank Sum']
    Results = Results.reindex(original_order)
    
    Results = Results.style.format({col: "{:.2%}" for col in list(Results.columns)[1:]})
    cm = sns.light_palette("green", as_cmap=True)
    Results = Results.background_gradient(subset = ['SMARTER','Rank Reciprocal','Rank Sum'],
                                          low = 0, high = 1, axis = None, cmap = cm)
    #Results = Results.bar(subset=list(Results.columns)[1:], color='lightblue',
    #                      vmin = 0, vmax = 1)
    Results = Results.set_properties(**{'max-width': '80px'})
    return(Results)


data = [1,2,2,4]
generateweights(10).data
generateweights([1,2,2,4]).data
data = {'a':1,'b':3,'c':3,'d':2}
generateweights(data).data
data = pd.Series(data)
generateweights(data).data

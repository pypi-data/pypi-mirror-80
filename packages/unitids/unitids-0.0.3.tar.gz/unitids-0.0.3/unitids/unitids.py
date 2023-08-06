import re
import math
import numpy as np
from itertools import chain
from collections import Counter
import nltk
from nltk.util import ngrams # This is the ngram magic.
from textblob import TextBlob
import pandas as pd

NGRAM = 2

re_sent_ends_naive = re.compile(r'[.\n]')
re_stripper_alpha = re.compile('[^a-zA-Z]+')
re_stripper_naive = re.compile('[^a-zA-Z\.\n]')

splitter_naive = lambda x: re_sent_ends_naive.split(re_stripper_naive.sub(' ', x))

#sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def get_tuples_nosentences(txt):
    """Get tuples that ignores all punctuation (including sentences)."""
    if not txt: return None
    ng = ngrams(re_stripper_alpha.sub(' ', txt).split(), NGRAM)
    return list(ng)

def cosine_similarity_ngrams(a, b):
    a = get_tuples_nosentences(a)
    b = get_tuples_nosentences(b)
    vec1 = Counter(a)
    vec2 = Counter(b)
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

def get_unitids(dataframe):
    dta = dataframe
    master = pd.read_csv('master.csv')
    #dta = dta[dta['institution'] == 'Wheaton College']
    master.columns = ['unitid', 'institution_ipeds', 'state', 'nan']
    master = master.drop(columns = ["state", "nan"])

    user_list = list(dta.institution)
    ipeds_list = list(master.institution_ipeds)

    new = pd.DataFrame()
    new.append(dta)

    for x in range(0, len(user_list)):
        new[x] = user_list[x]

    new['institution'] = ipeds_list
    user_list.append('institution')
    new.columns = user_list

    user_list = user_list[:-1]

    max_cosine = []
    i = 0
    for x in user_list:
        cosine_list = []
        user_inst = x
        for z in ipeds_list:
            ipeds_inst = z
            cosine_list.append(cosine_similarity_ngrams(user_inst, ipeds_inst))
        new[user_inst] = cosine_list
        max_cosine.append(max(cosine_list))
        i = i + 1

    ipeds_names = []
    for x in user_list:
        if np.argmax(new[x]) < len(ipeds_list):
            ipeds_names.append(ipeds_list[np.argmax(new[x])])
        else:
            ipeds_names.append("No Match")

    dta['institution_ipeds'] = ipeds_names
    dta['Similarity'] = np.where(dta['institution_ipeds'] != "No Match", max_cosine, 0.0)

    dta = dta.merge(master, on = 'institution_ipeds', how = "left")

    no_match = dta[round(dta['Similarity'],2) != 1]
    matches = pd.DataFrame()

    for x in no_match.institution:
        cosine_list = []
        user_inst = x
        for z in ipeds_list:
            ipeds_inst = z
            cosine_list.append(cosine_similarity_ngrams(user_inst, ipeds_inst))
        new[user_inst] = cosine_list
        i = i + 1
        no_match_df = pd.DataFrame()
        no_match_df['institution'] = no_match.institution
        i = 1
        top_five = np.argpartition(cosine_list, -5)[-5:]
        inst_list = []
        cos_list = []
        unitid_list = []
        another = []

        for x in top_five:
            inst = ipeds_list[x]
            cos = cosine_list[x]
            unitid = list(master[master['institution_ipeds'] == inst].unitid)[0]
            another.append([inst, cos, unitid])
            i = i + 1

        inst_df = pd.DataFrame(another).sort_values(by = [1], ascending = False)
        inst_df['Institution'] = user_inst
        inst_df['match'] = inst_df[1].rank(ascending = False, method = "dense")
        inst_df.columns = ['Top 5', 'similarity', 'unitid', 'institution', 'match']

        matches = matches.append(inst_df)

    if matches.shape[0] != 0:
        matches = matches.groupby(['institution', "match", "Top 5"]).mean()  
    else:
        matches = pd.DataFrame()
        
    dta['match'] = round(dta['Similarity'] * 100, 4)
    dta = dta.drop(columns = 'Similarity')

    return dta, matches

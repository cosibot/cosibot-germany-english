#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:17:53 2020

@author: jennifer
"""

import pandas as pd
from collections import defaultdict
import yaml
from yaml.representer import Representer

#so we can print yaml with defaultdict settings
yaml.add_representer(defaultdict, Representer.represent_dict)

df = pd.read_excel('../data/Cosibot Answers DE-EN.xlsx')

def get_response_type(response):
    if response.startswith('<speak>'):
        rtype = 'ssml'
    elif response.startswith('<p>'):
        rtype = 'html'
    else:
        rtype = 'text'
    
    return rtype

domain_dict = defaultdict(list)
for index, row in df.iterrows(): 
    intent = str(row["ParentTitle"]).lower()
    answer = str(row["Answer"])    
    domain_dict[intent].append(answer) 

intents_dict = defaultdict(list)
domain_responses = defaultdict(list)

for intent, responses in domain_dict.items():
    intents_dict['intents'].append(intent)

    domain_responses['utter_' + intent] = [{
        'custom': {
            'answers': [{'type': get_response_type(response), 
                         'text':  response} for response in responses]
        }
    }]

final_dict = {'responses': domain_responses}

file = '../bot/domain.yml'
with open(file, 'w') as wfile:
    intents = yaml.dump(intents_dict, wfile)
    documents = yaml.dump(final_dict, wfile)
    
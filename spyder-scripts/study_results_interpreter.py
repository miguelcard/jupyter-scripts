# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 17:54:24 2020

@author: Migue
"""

import pandas as pd
import numpy as np
import re
import logging
import sys
from datetime import datetime

class Strategy:
    def __init__(self, df, combination):
        self.winning = combination.winning
        self.occasions = combination.occasions
        self.news = combination.news
        self.lists_of_ranges = []
        
        params = combination.parameters
        for i in range(len(params)) :
            parameter_list = [params[i]]
            self.lists_of_ranges.append(parameter_list)
    
    def update_properties(self, combi):
        new_params = combi.parameters
        new_news = combi.news
        
        for i in range(len(new_params)):    
            if new_params[i] not in self.lists_of_ranges[i]:
                self.lists_of_ranges[i].append(new_params[i])
        
        self.news = list(np.unique(self.news + new_news))    
        
    
    
class Combination:
    #static attribute, defined in class level
    count = 0
    
    def __init__(self, data):
        self.set_winning_occasions(data)
        self.set_parameters(data)
        
        #self.pm_spk_drp = self.Parameter("pm spk drp", data)
        Combination.count += 1
    
    def set_winning_occasions(self, data):
        first_line = data.splitlines()[0]
        numbers = list(map(float,re.findall('\d+', first_line)))
        self.winning = numbers[0] 
        self.occasions = numbers[1] 
    
    def set_parameters(self, data):
        parameters = []
        second_line = data.splitlines()[1]
        params = second_line.split(",")
        news = []
        for param in params:
            name_and_values = param.split(":")
            if len(name_and_values) < 2 or name_and_values[0].strip() == "n" :
                news.append(int(re.findall('\d+', param)[0]))
            else:
                name = name_and_values[len(name_and_values)-2].strip()
                values = name_and_values[len(name_and_values)-1]
                value_numbers = list(map(float,re.findall('\d+', values)))
                min_range = value_numbers[0]
                max_range = value_numbers[1]
                parameter = self.Parameter(name, min_range, max_range)
                parameters.append(parameter)
        self.news = news
        self.parameters = parameters
        
    class Parameter:
        def __init__(self, name, min_range, max_range):
            self.name = name
            self.min_range = min_range
            self.max_range = max_range
            
        def __eq__(self, other):
            if self.__dict__ == other.__dict__:
                return True
            return False

def get_unique_id(df, combination):
    
    parameters_names = ['PM Spike Drop (%)','Open Price','Float (M)','PM Volume (M)', 'PM Float Rotations','MC (M)','PM Change %','H(M) %']
    #filter_string = ""
    filtered_d = df
    if len(parameters_names) == len(combination.parameters):
        for i in range(len(combination.parameters)):
            #filter_string += "("+ str(combination.parameters[i].min_range)+"<= df['"+parameters_names[i]+"']) & (df['"+parameters_names[i]+"'] <= "+str(combination.parameters[i].max_range)+")"
            #if i != len(combination.parameters)-1:
               # filter_string += " & "
            filtered_d = filtered_d[(combination.parameters[i].min_range <= filtered_d[parameters_names[i]]) & (filtered_d[parameters_names[i]] <= combination.parameters[i].max_range)]
    
        if(len(combination.news) == 2):
            news_filter = (filtered_d['News'] == combination.news[0] ) | (filtered_d['News'] == combination.news[1])
        elif(len(combination.news) == 3):
            news_filter = (filtered_d['News'] == combination.news[0] ) | (filtered_d['News'] == combination.news[1]) | (filtered_d['News'] == combination.news[2])
        
        filtered_d = filtered_d[news_filter]
        
    else:
        print("Error: names sizes different from parameters sizes")
    
    s = str(int(combination.winning)) + str(int(combination.occasions))
    s += ''.join(map(str, filtered_d.index.values))
    unique_id = int(s)
    return unique_id
       
def get_data_frame(csv_file):
    data = pd.read_csv(r'C:\Users\migue\Trading\My Statistics\\'+csv_file, delimiter=';')
    # Formatting Million/Thousands Columns for better handling
    data['MC (M)'] = data['MC (M)']/1000000
    data['Float (M)'] = data['Float (M)']/1000000
    data['PM Volume (M)'] = data['PM Volume (M)']/1000000
    data['Av Vol (90) (k)'] = data['Av Vol (90) (k)']/1000  
    return data

def bubblesort(h_list, distinguisher):
    
    for iter_num in range(len(h_list)-1,0,-1):
        for idx in range(iter_num):
            if distinguisher == "w":
                e1 = int(str( h_list[idx])[0:2])
                e2 = int(str( h_list[idx+1])[0:2])
            elif distinguisher == "o":
                e1 = int(str( h_list[idx])[2:4])
                e2 = int(str( h_list[idx+1])[2:4])
            elif distinguisher == "w*o":
                e1 = int(str( h_list[idx])[0:2])*int(str( h_list[idx])[2:4])
                e2 = int(str( h_list[idx+1])[0:2])*int(str( h_list[idx+1])[2:4])
            
            if e1 < e2: 
                temp = h_list[idx]
                h_list[idx] = h_list[idx+1]
                h_list[idx+1] = temp
                
    return h_list

def get_top_highest(param_to_sort, highest_list, list_length, unique_id, distinguisher): 
    
    if len(highest_list) > 0:
        strategy = strategy_dict.get(highest_list[-1])
        if distinguisher == "w":
            last_on_list = strategy.winning
        elif distinguisher == "o":
            last_on_list = strategy.occasions
        elif distinguisher == "w*o":
            last_on_list = strategy.winning*strategy.occasions
        
    if len(highest_list) >= list_length and param_to_sort > last_on_list:
        highest_list.append(unique_id)
        highest_list = bubblesort(highest_list, distinguisher)
        
        #highest_list.sort(reverse=True) #This is just sorting the IDs!not the parameter you watn to sort
        highest_list.pop()
    elif len(highest_list) < list_length:
        highest_list.append(unique_id)
        highest_list = bubblesort(highest_list, distinguisher)
    
    return highest_list

def print_filter(strategy_list):
    #Write filt and wins_filt(Is just the ones that didnt overspyked))
    
    parameters_data_names = ['PM Spike Drop (%)','Open Price','Float (M)','PM Volume (M)', 'PM Float Rotations','MC (M)','PM Change %','H(M) %']      
    for u_id in strategy_list:   #print index of list too! use enum  
        
        strategy = strategy_dict.get(u_id)
        print("# W:",strategy.winning," O:",strategy.occasions, " W*O:", strategy.winning*strategy.occasions)
        #Printing morning push:
        print("m_push_min = ",strategy.lists_of_ranges[-1][0].min_range) 
        print()
        print("filt = ",end=" ")
        #Parameters: 
        for i, param_range in enumerate(strategy.lists_of_ranges):
            #skipping to print Push
            if i == len(strategy.lists_of_ranges)-1:
                continue
            
            for j in range(len(param_range)):
                print("(data['"+str(parameters_data_names[i])+"'] >=",int(param_range[j].min_range),") & (data['"+str(parameters_data_names[i])+"'] <=",int(param_range[j].max_range),")", end="")
                #print("(",int(param_range[j].min_range), int(param_range[j].max_range),")" ,end=" ")
          
                if j == len(param_range)-1:
                    print(" & \\")
                else:
                    print(" & ", end="")
        
        #News Filter: 
        n_filt = "("
        for i in range(len(strategy.news)):
            n_filt += "(data['News'] == "+str(strategy.news[i])+")"
            if i != len(strategy.news)-1:
                n_filt += " | "
        n_filt += ")"
        
        print(n_filt)
        print()   
    
    
# main 
now = datetime.now()
#Reading Data from file
results_file = "iterative_study_results2020-12-04-1750_first.csv.log"
sys.stdout = open("strategy_results"+str(now.date())+"-"+str(now.hour)+results_file+".txt", "w")
path = r"C:\Users\migue\.spyder-py3\\"+results_file

csv_file = '50_first.csv'

print("Program started... ")
df = get_data_frame(csv_file)
combinations = []
strategy_dict = dict()

#Relevant Results: 
highest_winning_percentages = []
highest_occasions = []
highest_multiplication = []


with open(path, "r") as file:
    lines = file.readlines()
    for i in range(len(lines)):
        same_r = False
        if lines[i].startswith("INFO:root:Winning"):
            lines_data = lines[i]
            for k in range(i+1, len(lines)):
                if lines[k].startswith("INFO:root:Winning"):
                    break
                
                if not lines[k].startswith("INFO:root:same"): # same... only appears by 66% 12 Times (Maybe not that relevant)
                    lines_data += lines[k] 
                    
                else:
                    same_r = True
            
            if(not same_r): # Excluding same result data for now... 66% 12 Times
                
                combination = Combination(lines_data)
                winning = combination.winning
                occasions = combination.occasions
              
                if winning * occasions > 780: #Filters other specific "high values" 1050 4 100 results 
                    unique_id = get_unique_id(df, combination)
                    
                    #Idea: Maybe just add to diccionary if its relevant enough 
                    #Only if memory issues (Make lists here, and continue repeating Ids in method)
                    
                    if unique_id in strategy_dict.keys():
                        #update strategy instance
                        strategy = strategy_dict.get(unique_id)
                        strategy.update_properties(combination)
                        strategy_dict[unique_id] = strategy   
                    else:
                        strategy = Strategy(df, combination)
                        strategy_dict[unique_id] = strategy
                        
                        results=20
                        highest_winning_percentages = get_top_highest(winning, highest_winning_percentages, results, unique_id, "w")
                        highest_occasions = get_top_highest(occasions, highest_occasions, results, unique_id, "o")
                        highest_multiplication = get_top_highest(winning*occasions, highest_multiplication, results, unique_id, "w*o")

                   
#Evaluate Most relevant Results:  
print("TOP ",results)
print("Highest Winning Percentages:")
print_filter(highest_winning_percentages)  
print("Highest Occasions:")
print_filter(highest_occasions)  
print("Highest Multiplier:")
print_filter(highest_multiplication)
    

"""parameters_data_names = ['PM Spike Drop (%)','Open Price','Float (M)','PM Volume (M)', 'PM Float Rotations','MC (M)','PM Change %','H(M) %']      
for u_id in highest_winning_percentages:     
    
    strategy = strategy_dict.get(u_id)
    print("W:",strategy.winning," O:",strategy.occasions, " W*O:", strategy.winning*strategy.occasions)
    #Parameters: 
    for i, param_range in enumerate(strategy.lists_of_ranges):
        for j in range(len(param_range)):
            if j == 0:
                print(parameters_data_names[i],": ", end=" ")
                
            print("(",int(param_range[j].min_range), int(param_range[j].max_range),")" ,end=" ")
        print() 
    print("News: ",strategy.news)
    print() """  
 
           
print("Length: ",len(strategy_dict.keys()))
print("count: ",combination.count)      

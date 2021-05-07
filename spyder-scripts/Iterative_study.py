# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import seaborn as sns
import matplotlib.gridspec as gridspec
import time
import logging
from datetime import datetime

file = '50_first.csv'
data = pd.read_csv(r'C:\Users\migue\Trading\My                                                                                                                                                              \\'+file, delimiter=';')
# logging  
now = datetime.now()
LOG = "iterative_study_results"+str(now.date())+"-"+str(now.hour)+file+".log"                                                 
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)  

# console handler  
console = logging.StreamHandler()  
console.setLevel(logging.ERROR)  
logging.getLogger("").addHandler(console)

# Formatting Million/Thousands Columns for better handling
data['MC (M)'] = data['MC (M)']/1000000
data['Float (M)'] = data['Float (M)']/1000000
data['PM Volume (M)'] = data['PM Volume (M)']/1000000
data['Av Vol (90) (k)'] = data['Av Vol (90) (k)']/1000

#Method checking if the index being passed is valid... a Class with this methods could be developed
def valid_index(array, i, r):
    if i < len(array)-r:
        return True
    else:
        return False
#Method to get filter of the reséctive range
def get_filter(array, header, i, j, r):
    filter = (data[header] >= array[i]) & (data[header] <= array[j+r])  
    return filter

def get_news_filt(array, header):
    if(len(array) == 2):
        filter = (data[header] == array[0] ) | (data[header] == array[1])
        return filter
    elif(len(array) == 3):
        filter = (data[header] == array[0] ) | (data[header] == array[1]) | (data[header] == array[2])
        return filter
    
# A more extensive research on the above findings
#Main Things to consider: Various Pushing Ranges, All possible ranges for each variable & its Change (Delta)
#Only trust resultes with over 10 occurences

hm_percentages_range = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 100] #create again with np/or not
pm_spike_drop_range = [0, 30, 50, 100] 
open_price_range = [0, 2, 10, 200] 
#NOT EXPLORED YET:
float_range =  [0, 3, 5, 10, 50, 500] 
pm_vol_range =  [0, 1, 5, 10, 100]
#_____________
float_rotation_range = [0, 3, 10, 100]
market_cap_range = [0, 50, 100, 500, 1500]
pm_change_range = [65, 100, 200, 1000] 
news_range = [[0,0],[1,1],[2,2],[0,1],[0,2], [1,2], [0,1,2]]   

#NOT EXPLORED YET:
#resisitance_vol_range = [0, 1, 5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100, 200]   #Add after
#resistance_distance_range = [-50 ,-30 , -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200] #Add after

min_to_show = 12
min_percentage = 67
max_percentage = 0
max_occurences = 0
df_last = pd.DataFrame() 
df_last['Ticker'] =""
winners = pd.DataFrame() 
last_w_percentage = 0  
start = time.time()
logging.info("Start on {} Min percentage: {} Min to Show {} ".format(now, min_percentage, min_to_show))
#Start of all nested loops

#To compute percentage:     
loop_len1 = len(pm_spike_drop_range)
loop_len2 = len(open_price_range)
loop_len3 = len(float_range)
loop_len4 = len(pm_vol_range)
#loop_len5 = len(float_rotation_range)

for j in range(len(pm_spike_drop_range)-1):
    if valid_index(pm_spike_drop_range, j, 1):
        for b in range(len(pm_spike_drop_range)-1):
            f2 = get_filter(pm_spike_drop_range, 'PM Spike Drop (%)', j, b, 1)    
            if(len(data[f2]) < min_to_show ):
                continue
            if(df_last.equals(winners)):
                logging.info("same result, parameter changed : pm spk drp {}-{}".format(pm_spike_drop_range[j], pm_spike_drop_range[b+1]))
                continue
            
            for k in range(len(open_price_range)-1):
                if valid_index(open_price_range, k, 1):
                    for c in range(len(open_price_range)-1):
                        f3 = get_filter(open_price_range, 'Open Price', k, c, 1)
                        if(len(data[f2&f3]) < min_to_show ):
                            continue
                        if(df_last.equals(winners)):
                            logging.info("same result, parameter changed : price {}-{}".format(open_price_range[k], open_price_range[c+1]))
                            continue
                                    
                        
                        for l in range(len(float_range)-1):
                            if valid_index(float_range, l, 1):
                                for d in range(len(float_range)-1):
                                    f4 = get_filter(float_range, 'Float (M)', l, d, 1)
                                    if(len(data[f2&f3&f4]) < min_to_show ):
                                        continue
                                    if(df_last.equals(winners)):
                                        logging.info("same result, parameter changed : float {}-{}".format(float_range[l], float_range[d+1]))
                                        continue

                                    for m in range(len(pm_vol_range)-1):
                                        if valid_index(pm_vol_range, m, 1):
                                            for e in range(len(pm_vol_range)-1):
                                                f5 = get_filter(pm_vol_range, 'PM Volume (M)', m, e, 1)
                                                if(len(data[f2&f3&f4&f5]) < min_to_show ):
                                                    continue
                                                if(df_last.equals(winners)):
                                                    logging.info("same result, parameter changed : pm vol {}-{}".format(pm_vol_range[m], pm_vol_range[e+1]))
                                                    continue
                                                
                                                for n in range(len(float_rotation_range)-1):
                                                    if valid_index(float_rotation_range, n, 1):
                                                        for f in range(len(float_rotation_range)-1):
                                                            f6 = get_filter(float_rotation_range, 'PM Float Rotations', n, f, 1)
                                                            if(len(data[f2&f3&f4&f5&f6]) < min_to_show ):   #f4&f5 excluded
                                                                continue
                                                            if(df_last.equals(winners)):
                                                                logging.info("same result, parameter changed : float rot {}-{}".format(float_rotation_range[n], float_rotation_range[f+1]))
                                                                continue
                                                                        
                                                            for o in range(len(market_cap_range)):         
                                                                if valid_index(market_cap_range, o, 1):   #Until here working but quite slow!
                                                                    for g in range(len(market_cap_range)-1):
                                                                        f7 = get_filter(market_cap_range, 'MC (M)', o, g, 1)
                                                                        if(len(data[f2&f3&f4&f5&f6&f7]) < min_to_show ):   #f4&f5 excluded
                                                                            continue
                                                                        if(df_last.equals(winners)):
                                                                            logging.info("same result, parameter changed : mc {}-{}".format( market_cap_range[o], market_cap_range[g+1]))
                                                                            continue
                                                                                    
                                                                        for p in range(len(pm_change_range)):
                                                                            if valid_index(pm_change_range, p, 2): #Here working, takes about 10 mins (See clock symbol in tab)
                                                                                for h in range(len(pm_change_range)-2):    
                                                                                    f8 = get_filter(pm_change_range, 'PM Change %', p, h, 2)
                                                                                    if(len(data[f2&f3&f4&f5&f6&f7&f8]) < min_to_show ):   #f4&f5 excluded
                                                                                        continue
                                                                                    if(df_last.equals(winners)):
                                                                                        logging.info("same result, parameter changed : pm ch {}-{}".format(pm_change_range[p], pm_change_range[h+2]))
                                                                                        continue
                            
                                                                                    for q in range(len(news_range)):
                                                                                        #if valid_index(news_range, q, 0): #Inner loop not necessary here
                                                                                        f9 = get_news_filt(news_range[q], 'News')
                                                                                        if(len(data[f2&f3&f4&f5&f6&f7&f8&f9]) < min_to_show ):   #f4&f5 excluded
                                                                                            continue
                                                                                        if(df_last.equals(winners)):
                                                                                            logging.info("same result, parameter changed : N {}".format(news_range[q]))
                                                                                            continue
                                                                                                        
                                                                                        """                                
                                                                                        for r in range(len(resisitance_vol_range)):
                                                                                            if valid_index(resisitance_vol_range, r, 1): # We are here! 
                                                                                                for i in range(len(resisitance_vol_range)-1):
                                                                                                    f10 = get_filter(resisitance_vol_range, 'Resistance Volume (M)', r, i, 1)
                                                                                                    if(len(data[f2&f3&f4&f5&f6&f7&f8&f9&f10]) < min_to_show ):   
                                                                                                        continue
                                                                                                    
                                                                                                    #Till here, create last continue and check logic!
                                                                                                    
                                                                                                    for s in range(len(resistance_distance_range)):
                                                                                                        if valid_index(resistance_distance_range, s, 1):
                                                                                                            for j in range(len(resistance_distance_range)-1):
                                                                                                                f11 = get_filter(resistance_distance_range, 'Res/Conso Dist (%)', s, j, 1)
                                                                                                                if(len(data[f2&f3&f4&f5&f6&f7&f8&f9&f10&f11]) < min_to_show ):
                                                                                                                    continue
                                                                                     """
                                                                                                                
                                                                                        for i in range(len(hm_percentages_range)-2):
                                                                                            if valid_index(hm_percentages_range, i, 2):
                                                                                                
                                                                                                #for a in range(len(hm_percentages_range)-2):
                                                                                                    #f1 = get_filter(hm_percentages_range, 'H(M) %', i, a, 2)   this makes no sense for this field
                                                                                               
                                                                                                if(len(data[f2&f3&f4&f5&f6&f7&f8&f9]) < min_to_show): #&f10&f11 excluded #f4&f5 
                                                                                                    continue
                                                                                                
                                                                                                filtered_data = data[f2&f3&f4&f5&f6&f7&f8&f9] #&f10&f11 excluded 
                                                                                                #Also Do HIGH Day > HIGH Mrn = Loser trade
                                                                                                push_filter = (filtered_data['H(M) %'] >= hm_percentages_range[i])
                                                                                                pushers = filtered_data[push_filter]
                                                                                                total_trades = len(pushers)
                                                                                                
                                                                                                if(total_trades < min_to_show):
                                                                                                    continue
                                                                                                
                                                                                                wins_filt = (pushers['H(M) %'] <= hm_percentages_range[i+2])
                                                                                                winners = pushers[wins_filt]
                                                                                                
                                                                                                total_wins =  len(winners)
                                                                                                
                                                                                                winning_percentage = (total_wins/total_trades)*100
                                                                                                if(winning_percentage >= min_percentage):
                                                                                                    if(df_last['Ticker'].equals(winners['Ticker']) and winning_percentage == last_w_percentage): 
                                                                                                        #print("Same result with a param change")
                                                                                                        logging.info("same result...")
                                                                                                        logging.info("pm spk drp: {}-{}, price: {}-{}," \
                                                                                                        " float: {}-{}, pm vol: {}-{},"\
                                                                                                        " float rot: {}-{}, mc: {}-{}, pm-ch: {}-{}, n: {}, m push: {}-{}" \
                                                                                                        .format(pm_spike_drop_range[j], pm_spike_drop_range[b+1], open_price_range[k],\
                                                                                                        open_price_range[c+1],\
                                                                                                        float_range[l], float_range[d+1], pm_vol_range[m], pm_vol_range[e+1],
                                                                                                        float_rotation_range[n], float_rotation_range[f+1], market_cap_range[o], market_cap_range[g+1],\
                                                                                                        pm_change_range[p], pm_change_range[h+2], news_range[q], \
                                                                                                        hm_percentages_range[i], hm_percentages_range[i+2])) 
                                                                                                        #float_range[l], float_range[d+1], pm_vol_range[m], pm_vol_range[e+1],\
                                                                                                    
                                                                                                        # just log the parameters and continue...
                                                                                                        # V2 improvement:
                                                                                                        #Create a method that show parametersd that changed: 
                                                                                                        # For these you need to know and store the last parameters you had... 
                                                                                                        continue
                                                                                                    
                                                                                                    if winning_percentage > max_percentage :
                                                                                                        max_percentage = winning_percentage
                                                                                                    if total_trades > max_occurences:
                                                                                                        max_occurences = total_trades
                                                                                                        
                                                                                                    df_last['Ticker'] = winners['Ticker']
                                                                                                    last_w_percentage = winning_percentage
                                                                                                    #print(winning_percentage,"% wins in ", total_trades," occasions")
                                                                                                    logging.info("Winning : %d  Occasions: %d", winning_percentage, total_trades)  #Use %% to show percentage symbol 
                                                                                                    logging.info("pm spk drp: {}-{}, price: {}-{}," \
                                                                                                    " float: {}-{}, pm vol: {}-{},"\
                                                                                                    " float rot: {}-{}, mc: {}-{}, pm-ch: {}-{}, n: {}, m push: {}-{}" \
                                                                                                    .format(pm_spike_drop_range[j], pm_spike_drop_range[b+1], open_price_range[k],\
                                                                                                    open_price_range[c+1], \
                                                                                                    float_range[l], float_range[d+1], pm_vol_range[m], pm_vol_range[e+1],
                                                                                                    float_rotation_range[n], float_rotation_range[f+1], market_cap_range[o], market_cap_range[g+1],\
                                                                                                    pm_change_range[p], pm_change_range[h+2], news_range[q], \
                                                                                                    hm_percentages_range[i], hm_percentages_range[i+2])) 
                                                                                                    
                                                                                                     # float_range[l], float_range[d+1], pm_vol_range[m], pm_vol_range[e+1],
                                                                                                
                                                                                                
                                                                                                """
                                                                                                filt = (data['H(M) %'] >= 30) & (data['PM Spike Drop (%)'] <= 30) & \
                                                                                                (data['Open Price'] >= 1) & (data['Float (M)'] >= 2 ) & (data['PM Volume (M)'] <= 5) & \
                                                                                                (data['PM Float Rotations'] < 2) & (data['MC (M)'] >= 2 ) & (data['PM Change %'] >= 2 ) & \
                                                                                                (data['News'] >= 2 ) & (data['Resistance Volume (M)'] >= 2) & (data['Res/Conso Dist (%)'] >= 2)
                            
                                                                                                ## AND HERE IS WHERE YOU DO YOUR CALCULATIONS! EASY *KISS*
                                                                                                print("H(M) % push ranges",hm_percentages_range[i],hm_percentages_range[i+2])
                                                                                                
                                                                                                """
logging.info("Max Winning Percentage: {} , Max Occurences: {}".format(max_percentage, max_occurences))
end = time.time()
logging.info("Runtime of the program is {}".format( end - start))
print(f"Runtime of the program is {end - start}")

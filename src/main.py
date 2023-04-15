import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx
import itertools

from preprocess import Preprocessing
from communities import Community
from winners import Winners
from ch_league_process import ChampionsDataProcess
    
    

"""
    Datasets
    0   ../dataset/primera-division.csv 
    1   ../dataset/1-bundesliga.csv 
    2   ../dataset/serie-a.csv 
    3   ../dataset/premier-league.csv
    4   ../dataset/ligue-1.csv
    5   ../dataset/all.csv
"""

champ_league_winners = ['Olympique Marseille','Marseille', 'AC Milan', 'Ajax', 'Juventus', 'Bor. Dortmund', 'Real Madrid',
                        'Manchester United', 'Real Madrid', 'Bayern Munich', 'Real Madrid', 'AC Milan',
                        'FC Porto', 'Liverpool FC', 'FC Barcelona', 'AC Milan', 'Man Utd', 'Barcelona',
                        'Inter', 'Barcelona', 'Chelsea', 'Bayern Munich', 'Real Madrid','Barcelona',
                        'Real Madrid', 'Real Madrid', 'Real Madrid', 'Liverpool', 'Bayern Munich',
                        'Chelsea FC', 'Real Madrid', 'Borussia Dortmund', 'Inter Milan']


europa_league_winners = ['Juventus', 'Inter Milan', 'Inter', 'Parma', 'Bayern Munich', 'Parma FC', 'Schalke 04',
                         'FC Schalke 04', 'Galatasaray', 'Liverpool FC', 'Liverpool', 'Feyenoord', 'FC Porto', 
                         'Valencia', 'Valencia CF', 'CSKA Moscow', 'Sevilla FC', 'Zenit S-Pb', 'Shakhtar D.', 
                         'Atlético Madrid', 'Atlético de Madrid', 'Chelsea', 'Chelsea FC', 'Manchester United',
                         'Man Utd', 'Villarreal', 'Villarreal CF', 'E. Frankfurt', 'Eintracht Frankfurt']

def data_community(ordered):
    print(len(ordered))
    for i in range(len(ordered)):
        print(ordered[i]) # Prints lists of communities
    

def main():
    
    # Preprocess the data 
    prep = Preprocessing()
    
    # Returns dictionary (seller, buyer) : (player, fee, year) for index (0 - 4) indicated
    soccer = prep.create_dict(0)
    # print(soccer)
    
    
    # Communities
    comm = Community()
    #order_comm, trimmed_graph = comm.process_community_graph(soccer, False, 0)
    #print("The ordered communities: ", ordered)
    #data_community(ordered)
    
    
    # Winners correlation
    # index 5 uses all leagues mixed dataset
    win = Winners()
    soccer_champ = prep.create_dict(5)
    
    # soccer_champ -> Dictionary ((seller, buyer), (player, fee_cleaned, year))
    # CHAMPIONS LEAGUE
    #champs_money_spent = prep.sub_champions_spent_community(soccer_champ, champ_league_winners, 0)
    #champs_money_received = prep.sub_champions_received_community(soccer_champ, champ_league_winners, 0)
    
    # EUROPA LEAGUE
    champs_money_spent_eur = prep.sub_champions_spent_community(soccer_champ, europa_league_winners, 1)
    champs_money_received_eur = prep.sub_champions_received_community(soccer_champ, europa_league_winners, 1)
    
    # ONLY CHAMPIONS COMMUNITIES
    ch_process = ChampionsDataProcess()
    
    """ Calculates the Pearson Correlation Coefficient """
    #ch_process.calculating_pearson_corr(champs_money_spent, 0, True)
    #ch_process.calculating_pearson_corr(champs_money_received, 0, False)
    
    ch_process.calculating_pearson_corr(champs_money_spent_eur, 1, True)
    ch_process.calculating_pearson_corr(champs_money_received_eur, 1, False)
    
    """     Given arguments for 'process_data' function:
                #   0 -> Champions League
                #   1 -> Europa League
                #   True -> Money Spent
                #   False -> Money Received
        'champ_league' function: Returns winners dict (seller, buyer) : (fee, player)
    """
    ch_winners = win.champ_league(soccer_champ, champ_league_winners)
    #ch_process.process_data(ch_winners, 0, True)
  
    eur_winners = win.europa_league(soccer_champ, europa_league_winners)
    #ch_process.process_data(eur_winners, 1, False)

main()

"""
    TODO:
    1. Create a Dictionary {team : (total_fee_spent, total_fee_received)}
        - Divide teams by clusters with threshold of total fee spent
        - Now, map them to their major trophy wins (We should see that more money = more trophies)
        - Number of relegations, which teams are getting relegated more? More or less money spent?
        
    2. Create A Dictionary by year {team : {list of position of players transferred into team} }
        - Compare to following season records.
        - Are teams getting more cbs, strikers, gks... doing better or worse?

    3. Create a dataset of teams performance (Avg position in the last decade, and compare it to how they do
        in the transfer market):
        
"""


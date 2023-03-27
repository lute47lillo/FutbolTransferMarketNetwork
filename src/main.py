import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx
import itertools

from preprocess import Preprocessing
from communities import Community
from winners import Winners

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
                        'Chelsea FC', 'Real Madrid', 'Borussia Dortmund']

europa_league_winners = []

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
    
    
    
    # Execute functions
    # Communities
    comm = Community()
    order_comm, trimmed_graph = comm.process_community_graph(soccer, False, 0)
    #print("The ordered communities: ", ordered)
    #data_community(ordered)
    
    
    # Winners correlation
    # index 5 uses all leagues mixed dataset
    win = Winners()
    soccer_champ = prep.create_dict(5)
    
    # Returns winners dict (seller, buyer) : (fee, player)
    winners = win.champ_league(soccer_champ, champ_league_winners)


main()

#fee_edge_labels = nx.get_edge_attributes(trim_graph, 'fee')

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


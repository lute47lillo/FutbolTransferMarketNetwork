import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx
import itertools

from preprocess import Preprocessing
from communities import Community
from winners import Winners
from ch_league_process import ChampionsDataProcess
from stats_comm import StatsAndCommunities
    
    

"""
    Datasets
    0   ../dataset/primera-division.csv 
    1   ../dataset/1-bundesliga.csv 
    2   ../dataset/serie-a.csv 
    3   ../dataset/premier-league.csv
    4   ../dataset/ligue-1.csv
    5   ../dataset/all.csv
"""

champ_league_winners = ['Olympique Marseille','Marseille', 'AC Milan', 'Ajax', 'Juventus FC', 'Bor. Dortmund', 'Real Madrid',
                        'Manchester United', 'Real Madrid', 'Bayern Munich', 'Real Madrid', 'AC Milan',
                        'FC Porto', 'Liverpool FC', 'FC Barcelona', 'AC Milan', 'Man Utd', 'Barcelona',
                        'Inter', 'Barcelona', 'Chelsea', 'Bayern Munich', 'Real Madrid','Barcelona',
                        'Real Madrid', 'Real Madrid', 'Real Madrid', 'Liverpool', 'Bayern Munich',
                        'Chelsea FC', 'Real Madrid', 'Borussia Dortmund', 'Inter Milan']


europa_league_winners = ['Juventus FC', 'Inter Milan', 'Inter', 'Parma', 'Bayern Munich', 'Parma FC', 'Schalke 04',
                         'FC Schalke 04', 'Galatasaray', 'Liverpool FC', 'Liverpool', 'Feyenoord', 'FC Porto', 
                         'Valencia', 'Valencia CF', 'CSKA Moscow', 'Sevilla FC', 'Zenit S-Pb', 'Shakhtar D.', 
                         'Atlético Madrid', 'Atlético de Madrid', 'Chelsea', 'Chelsea FC', 'Manchester United',
                         'Man Utd', 'Villarreal', 'Villarreal CF', 'E. Frankfurt', 'Eintracht Frankfurt']

''' Helper function that returns a dictionary with the ordered communities'''
def data_community(ordered, stats, do):
    ord = {}
    if do: # Trim the community
        for idx, teams in ordered.items():
            trim_teams = []
            n = len(teams)
            for t in range(n):
                if teams[t] in stats:
                    trim_teams.append(teams[t])
                    ord.update({idx+1:trim_teams})
        #print(ord)
        
    else:
        print(len(ordered))
        for i in range(len(ordered)):
            # print(ordered[i]) # Prints lists of communities
            ord.update({i+1:ordered[i]})
    return ord

def main():
    
    # Preprocess the data 
    prep = Preprocessing()
    """
        'create_dict' function from Preprocessing
        Given Index 0-5
        Returns dictionary of type -> (seller, buyer) : (player, fee, year) 
    """
    soccer = prep.create_dict(3)
    mapping = prep.get_universal_mapping()

    
    """
        Given a historical classification dataset
        Return a stats dictionary {team : average position, total points}
        
        & 
        
        Given an ordered community from ONLY Premier league and ALL leagues
        Map Relationship to results
    
    """
    comm = Community()
    stats = prep.average_stats()
    
    soccer = prep.dictionary_name_mapping(soccer, mapping)
    order_comm, trimmed_graph = comm.process_community_graph(soccer, False, 3)
    
    # Print ordered communites (True -> Trim community given stats dicitonary)
    ordered = data_community(order_comm, stats, True)
    
   
    """
        Given the statistics and the soccer prepped dictionary, and the ordered communities based on modularity.
        
        Return
            sc.study -> Correlation between performance and sub-communites
    """
    sc = StatsAndCommunities()
    #sc.study(ordered, stats, soccer)
    #sc.whole_league_community(stats, soccer)
    #print("Premier League ordered communites :",  ordered)
    
    """
        Study the Betweenness, closeness centrality and degree centrality of a particular community.
        Compare it to their overall performance (stats)
    
    """
    btw_centr, graph = sc.community_attributes(stats, ordered, trimmed_graph)
    
    """ Helper function to create a community index {team : comm_idx} based on a given community (ordered)"""
    community_index = prep.create_com_index(ordered)
    
    """ Plot communities """
    comm.plot_community(graph, community_index, btw_centr, 3)
    
    """ Communities
    
        Given a dictionary:
            - Plot if TRUE
    
        Returns and ordered dictionary of communities based on the greedy_modularity_communities algorithm
        and the trimmed graph
    
    """
    
    #soccer = prep.dictionary_name_mapping(soccer, mapping)
    #order_comm, trimmed_graph = comm.process_community_graph(soccer, True, 5)
    
    #ordered = data_community(order_comm)
    #print("The ordered community: ", ordered)
    
    
    # Process International Champions DATA
    # ch_process = ChampionsDataProcess()
    
    """
        Given a dictionary of all teams of all datasets
        Create small subcommunity of International Champions
        To calculate Pearson Correlation Coefficients
        Based on:
        Trophies won - Money Spent 
                    &
        Trophies won - Money Spent 
    """
    # soccer_champ = prep.create_dict(5)
    # soccer_champ = prep.dictionary_name_mapping(soccer_champ, mapping)
    # CHAMPIONS LEAGUE
    # champs_money_spent = prep.sub_champions_spent_community(soccer_champ, champ_league_winners, 0)
    # champs_money_received = prep.sub_champions_received_community(soccer_champ, champ_league_winners, 0)
    
    # # EUROPA LEAGUE
    # champs_money_spent_eur = prep.sub_champions_spent_community(soccer_champ, europa_league_winners, 1)
    # champs_money_received_eur = prep.sub_champions_received_community(soccer_champ, europa_league_winners, 1)
    
    
    # """ Calculates the Pearson Correlation Coefficient """
    # ch_process.calculating_pearson_corr(champs_money_spent, 0, True)
    # ch_process.calculating_pearson_corr(champs_money_received, 0, False)
    
    # ch_process.calculating_pearson_corr(champs_money_spent_eur, 1, True)
    # ch_process.calculating_pearson_corr(champs_money_received_eur, 1, False)
    
    
    
    """     Given arguments for 'process_data' function:
                #   0 -> Champions League
                #   1 -> Europa League
                #   True -> Money Spent
                #   False -> Money Received
        'champ_league' function: Returns winners dict (seller, buyer) : (fee, player)
        Also returns graph of sub-community of champions if plot function uncommented
    """
    # ONLY CHAMPIONS COMMUNITIES
    # win = Winners()
    # ch_winners = win.champ_league(soccer_champ, champ_league_winners)
    # ch_process.process_data(ch_winners, 0, False)
  
    # eur_winners = win.europa_league(soccer_champ, europa_league_winners)
    # ch_process.process_data(eur_winners, 1, False)

main()

"""
    TODO:   
    1. Create A Dictionary by year {team : {list of position of players transferred into team} }
        - Compare to following season records.
        - Are teams getting more cbs, strikers, gks... doing better or worse?

    2. Relegation Study:
        From dataset, collect teams in 18,19,20th position -> Relegation.
        Collect teams in 7th - 17th position -> Nothing obtained.
        Create a dictionary, of those teams : how many relegations, year of relegation. Now, go to transfer_market dataset (Prem + Championship example).
        Create a graph where nodes are teams that have been relegated, and study that spending community.
        Do the same for teams on 7th - 17th position. How have they spent that money, have they spent more after getting relegated?
        
    3. Obtain LaLiga dataset as the one of Premier LEague.
    
    4. Get The league, obtain nodes with highest attributes, map to the results
"""


import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx
import itertools

from preprocess import Preprocessing
from communities import Community
from winners import Winners
from utils import Utils
from ch_league_process import ChampionsDataProcess
from stats_comm import StatsAndCommunities
import math
    
    

"""
    Datasets
    0   ../dataset/primera-division.csv 
    1   ../dataset/1-bundesliga.csv 
    2   ../dataset/serie-a.csv 
    3   ../dataset/premier-league.csv
    4   ../dataset/ligue-1.csv
    5   ../dataset/all.csv
"""

champ_league_winners = ['Olympique Marseille', 'Ajax Amsterdam', 'Juventus FC', 'Manchester United',
                        'FC Porto', 'Liverpool FC', 'FC Barcelona', 'AC Milan', 'Chelsea FC',
                        'Bayern Munich', 'Real Madrid', 'Borussia Dortmund', 'Inter Milan']


europa_league_winners = ['Juventus FC', 'Inter Milan', 'AC Parma', 'Bayern Munich', 'FC Schalke 04',
                        'Galatasaray', 'Liverpool FC', 'Feyenoord Rotterdam', 'FC Porto', 
                        'Valencia CF', 'CSKA Moscow', 'Sevilla FC', 'Zenit S-Pb', 'Shakhtar D.', 
                        'Atlético de Madrid', 'Chelsea FC', 'Manchester United',
                        'Villarreal CF', 'Eintracht Frankfurt']


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
                    trim_teams.sort()
                    ord.update({idx+1:trim_teams})
        #print(ord)
        
    else:
        print(len(ordered))
        for i in range(len(ordered)):
            # print(ordered[i]) # Prints lists of communities
            ord.update({i+1:ordered[i]})
    return ord

''' Helper function that returns a dictionary {idx : list of teams} based on the ordered communities'''
def deconstruct_com_idx(order):
    ord = {}
    for t, idx in order.items():
        if not idx in ord.keys():
            l = []
            l.append(t)
            ord.update({idx:l})
        else:
            curr = ord.get(idx)
            curr.append(t)
            ord.update({idx:curr})
        
    return ord
def new_execution():
    
    # Preprocess the data 
    util = Utils()
    prep = Preprocessing()
    sc = StatsAndCommunities()
    comm = Community()
    
    soccer_dict, teams = util.create_dict(5)
    
    # Teams -> 314 nodes. 
    #print(sorted(teams))
    #print(len(teams))
    
    # Get communities and graph
    order_comm, graph = comm.process_community_graph_update(soccer_dict, False, 5, teams)
    
    #Top5
    # MultiGraph has 95 nodes and 6041 edges after removing nodes d<75 and no 0.0 $transfers
    # MultiGraph has 117 nodes and 7222 edges after removing nodes d<60 and no 0.0 $transfers
    # MultiGraph has 235 nodes and 10127 edges after removing no 0.0$ transfers
    # MultiGraph has 224 nodes and 38040 edges after removing nodes d<75
    
    # inlude liga nos
    # MultiGraph has 272 nodes and 10913 edges after removing 0.0$ transfers
    # MultiGraph has 122 nodes and 7682 edges after removing nodes d<60 and no 0.0 $transfers
    # MultiGraph has 139 nodes and 8449 edges after removing nodes d<50 and no 0.0 $transfers (BEST)
    
    #include eredivise
    # MultiGraph has 303 nodes and 11797 edges after removing 0.0$ transfers
    # MultiGraph has 188 nodes and 10357 edges after removing nodes d<30 and no 0.0 $transfers (BEST) 7/13 -> Group 1
    
    
    
    #print([e for e in graph.edges.data()])
    
    
    #coeff = prep.get_graph_clustering_ceff(graph)
    #print(prep.sort_dictionary_by_value(coeff))
    
    stats = prep.average_stats() # Legacy code. Needs to be removed
    ordered = data_community(order_comm, stats, False)
    
    
    # Get the money dict
    money_dict = prep.get_dict_money_spent(graph)

    # # Calculate how much each community spends.
    money_dict = sc.all_community_money(money_dict, ordered)
    print(money_dict)
    
    print(ordered)
    print(graph)
    exit()
    
    
def main(args):
    
    if args:
        new_execution()
        
    # Preprocess the data 
    prep = Preprocessing()
    """
        'create_dict' function from Preprocessing
        Given Index 0-5
        Returns dictionary of type -> (seller, buyer) : (player, fee, year), *Optional, also returns list of teams of domestic league
    """
    soccer, teams = prep.create_dict(5)
    
    teams = sorted(teams)
    mapping = prep.get_universal_mapping()
    
    
    """
        Given a historical classification dataset
        Return a stats dictionary {team : average position, total points}
        
        & 
        
        Given an ordered community from ONLY Premier league and ALL leagues
        Map Relationship to results
    
    """
    comm = Community()
    sc = StatsAndCommunities()
    stats = prep.average_stats()
 
 
    soccer = prep.dictionary_name_mapping(soccer, mapping)
    order_comm, trimmed_graph = comm.process_community_graph(soccer, False, 5, teams)
    
    # # # Print ordered communites (True -> Trim community given stats dicitonary)
    
    ordered = data_community(order_comm, stats, False)
    
   
    #print(ordered)
    #print(trimmed_graph)
    #print([e for e in trimmed_graph.edges.data()])
    
    
    """
        Get clustering coefficient of the graph given
    """
    #coeff = prep.get_graph_clustering_ceff(trimmed_graph)
    
    #print(coeff)
    
    """
        Obtain how much money has been spent by community   
    """
    # Get the money dict
    # money_dict = prep.get_dict_money_spent(trimmed_graph)

    # Calculate how much each community spends.
    # money_dict = sc.all_community_money(money_dict, ordered)
    # print(money_dict)

    
    """
        Given community index creation of based performance teams:
        Average position
        Total Money spent within community
        Plot them,
    
    """
    '''pos_com_idx, points_pos_idx = prep.organize_teams(stats)
    print("The pos_com_idx: ", pos_com_idx)
    print("\nThe points_com_idx: ", points_pos_idx)
    
    # Get ordered communities for both avg_pos, and total points
    pos_ordered = deconstruct_com_idx(pos_com_idx)
    points_ordered = deconstruct_com_idx(points_pos_idx)
    
    print("\n The position communities are: ", pos_ordered)
    print("\n The points communities are: ", points_ordered)'''
    
    # Plot the communities wrt betw centrality, and their pos, or total points community index
    # btw_centr, graph = sc.community_attributes(stats, ordered, trimmed_graph)
    # comm.plot_community(graph, pos_com_idx, btw_centr, 6)
    
    """ 
        Obtain the community total spent of a team within a sub-community
        Example: Premier league (seasons 2000 - 2022)
        stats -> Teams : avg_pos, total points
        soccer -> dict ({(seller, buyer):(fee_cleaned, player, year)})
    """
    # champs = list(stats.keys())
    # spent = prep.sub_champions_spent_community(soccer, champs, 0)
    # money_comm_idx = prep.get_money_community(spent)
    # money_comm_idx = deconstruct_com_idx(money_comm_idx)
    # print(money_comm_idx)
    
    """
        Given the statistics and the soccer prepped dictionary, and the ordered communities based on modularity.
        
        Return
            sc.study -> Correlation between performance and sub-communites
    """
    
    # sc.study(ordered, stats, soccer)
    # sc.whole_league_community(stats, soccer)
    # print("Premier League ordered communites :",  ordered)
    
    """
        Study the Betweenness, closeness centrality and degree centrality of a particular community.
        Compare it to their overall performance (stats)
    
    """
    # btw_centr, graph = sc.community_attributes(stats, ordered, trimmed_graph)
    # """ Helper function to create a community index {team : comm_idx} based on a given community (ordered)"""
    #community_index = prep.create_com_index(ordered)
    
    # """ Plot communities """
    #comm.plot_community(graph, community_index, btw_centr, 3)
    
    #btw_centr = prep.sort_dictionary_by_value(btw_centr)
    #print(btw_centr)
    
    """ Obtain omega value to calculate the small-world property of the given graph"""
    # omega = sc.obtain_omega_small_world(trimmed_graph)
    # print(omega)
    
    
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

main(True)

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


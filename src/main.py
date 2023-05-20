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
    5   ../dataset/liga-nos.csv
    6   ../dataset/eredivisie.csv
    7   ../dataset/all.csv
"""

champ_league_winners = ['Olympique Marseille', 'Ajax Amsterdam', 'Juventus FC', 'Manchester United',
                        'FC Porto', 'Liverpool FC', 'FC Barcelona', 'AC Milan', 'Chelsea FC',
                        'Bayern Munich', 'Real Madrid', 'Borussia Dortmund', 'Inter Milan']


europa_league_winners = ['Juventus FC', 'Inter Milan', 'AC Parma', 'Bayern Munich', 'FC Schalke 04',
                        'Galatasaray', 'Liverpool FC', 'Feyenoord Rotterdam', 'FC Porto', 
                        'Valencia CF', 'CSKA Moscow', 'Sevilla FC', 'Zenit S-Pb', 'Shakhtar D.', 
                        'Atlético de Madrid', 'Chelsea FC', 'Manchester United',
                        'Villareal CF', 'Eintracht Frankfurt']


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

def get_champions_league_spent_received_money(soccer, competition):
    util = Utils()
    spent = util.sub_champions_spent_community(soccer, competition)
    received = util.sub_champions_received_community(soccer, competition)
    
    return spent, received

def calc_pearson_winners(spent, received, type):
    ch_process = ChampionsDataProcess()
    ch_process.calculating_pearson_corr(spent, type)
    ch_process.calculating_pearson_corr(received, type)
    
def get_domestic_teams(teams, stats):
    prem_teams = []
    for k, v in stats.items():
        if k in teams:
            prem_teams.append(k)
    return prem_teams

def new_execution():
    
    # Preprocess the data 
    util = Utils()
    prep = Preprocessing()
    sc = StatsAndCommunities()
    comm = Community()
    ch_process = ChampionsDataProcess()
    
    #soccer_dict, teams = util.create_dict(5)
    
    # Teams -> 314 nodes. 
    #print(sorted(teams))
    #print(len(teams))
    
    """
        Get communities and graph
        MultiGraph has 188 nodes and 10357 edges after removing nodes d<30 and no 0.0 $transfers (BEST) 7/13 -> Group 1
    """
    # MultiGraph has 188 nodes and 10357 edges after removing nodes d<30 and no 0.0 $transfers (BEST) 7/13 -> Group 1
    # order_comm, graph = comm.process_community_graph_update(soccer_dict, False, 5, teams)
    
    # stats = prep.average_stats() # Legacy code. Needs to be removed
    # ordered = data_community(order_comm, stats, False)
    
    #print(ordered)
    #print(graph)
    #print([e for e in graph.edges.data()])
    
    
    """ Clustering Coefficient """
    #coeff = prep.get_graph_clustering_ceff(graph)
    #print(prep.sort_dictionary_by_value(coeff))
    

    """ 
        Obtain a dictionary {community : total money spent}
        for all communities
    """
    # money_dict = prep.get_dict_money_spent(graph)
    # money_dict = sc.all_community_money(money_dict, ordered)
    # print(money_dict)
    
    
    """
        Obtain how much money Champions League and Europa League winners have spent and received.
    """
    # spent_ch, received_ch = get_champions_league_spent_received_money(soccer_dict, champ_league_winners)
    # spent_el, received_el = get_champions_league_spent_received_money(soccer_dict, europa_league_winners)
    
    
    """ 
        Calculates the Spearman Rank Correlation Coefficient for Champions League and Europa League Winners
    """
    #calc_pearson_winners(spent_ch, received_ch, 0)
    #calc_pearson_winners(spent_el, received_el, 1)
    
    """
        Plot Spearman Rank Correlation Coefficient for Champions League and Europa League Winners
    """
    # ch_process.plotting_categorical(spent_ch, 0, True)
    # ch_process.plotting_categorical(received_ch, 0, False)
    
    # ch_process.plotting_categorical(spent_el, 1, True)
    # ch_process.plotting_categorical(received_el, 1, False)
    
    
    """
        Domestic Case study: Premier League
    """
    
    prem_soccer, _ = util.create_dict(7)
    prem_stats = prep.average_stats()
    prem_teams = list(prem_stats.keys())

    # prem_order_comm, prem_graph = comm.process_community_graph_update(prem_soccer, False, 3, prem_teams)
    
    # prem_ordered = data_community(prem_order_comm, prem_stats, False)
    #print(prem_ordered)
    #print([e for e in prem_graph.edges.data()])
    #print(prem_graph)
    #print(prem_stats)
    
    """
        Given community index creation of based performance teams:
        Average position
        Total Money spent within community
        Plot them,
    
    """
    #pos_com_idx, points_pos_idx = prep.organize_teams(prem_stats)
    #print("\nThe pos_com_idx: ", pos_com_idx)
    # print("\nThe points_com_idx: ", points_pos_idx)
    
    # # Get ordered communities for both avg_pos, and total points
    # pos_ordered = deconstruct_com_idx(pos_com_idx)
    # points_ordered = deconstruct_com_idx(points_pos_idx)
    
    # print("\n The position communities are: ", pos_ordered)
    # print("\n The points communities are: ", points_ordered)
    
    """ 
        Obtain the community total spent of a team within a sub-community
        Example: Premier league (seasons 2000 - 2022)
        prem_teams -> list teams of domestic league
        prem_soccer -> dict ({(seller, buyer):(fee_cleaned, player, year)})
    """
    # spent = util.sub_champions_spent_community(prem_soccer, prem_teams)
    # print(spent)
    # money_comm_idx = prep.get_money_community(spent)
    # money_comm_idx = deconstruct_com_idx(money_comm_idx)
    # print(money_comm_idx)
    
    """
        Study Betweenness centrality of teams in the given community.
        (There's an option to study both degree and centrality)
    """
    # btw_centr, graph = sc.community_attributes(prem_stats, prem_ordered, prem_graph)
    # btw_centr = prep.sort_dictionary_by_value(btw_centr)
    # print(btw_centr)
    
    """
        Given the statistics and the soccer prepped dictionary, and the ordered communities based on modularity.
        
        Return
            sc.study -> Correlation between performance and sub-communites
    """
    # sc.study(prem_ordered, prem_stats, prem_soccer)
    
    """ Obtain omega value to calculate the small-world property of the given graph"""
    league_soccer, league_teams = util.create_dict(6)
    #league_teams = list(league_soccer.keys())
    print(len(league_teams))
    
    league_order_comm, league_graph = comm.process_community_graph_update(league_soccer, False, 3, league_teams)
    
    league_ordered = data_community(league_order_comm, prem_stats, False)
    print(league_ordered)
    print(league_graph)
    
    omega = sc.obtain_omega_small_world(league_graph)
    print(omega)
    
    exit()
    
    
def main(args):
    
    if args:
        new_execution()
    

main(True)



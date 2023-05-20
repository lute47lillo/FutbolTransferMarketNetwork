import networkx as nx
import pandas as pd
import math
from preprocess import Preprocessing

class Utils:
    """
        Given:
            league_n: int [0..n]. Representing dataset from where to construct dictionary
        
        Returns:
            soccer: dict {(seller, buyer): transfer_list}, where transfer_list is a list
            of tuples of all transfers between seller -> buyer
            transfer_list: list [(player, fee, year)]
            
            league: list of teams that only participate in that given league.
    """
    def create_dict(self, league_n):
        
        prep = Preprocessing()
        league = prep.select_league(league_n)
        df = pd.read_csv(league)
        G = nx.from_pandas_edgelist(df, source='club_name', target='club_involved_name',
                                    edge_attr=['player_name', 'transfer_movement', 'fee_cleaned', 'year'],
                                    create_using=nx.MultiDiGraph())
        
        
        # Get all edge labels from graph attributes
        fee_cleaned_edge_labels = nx.get_edge_attributes(G, "fee_cleaned")
        year_edge_labels = nx.get_edge_attributes(G, "year")
        player_edge_labels = nx.get_edge_attributes(G, "player_name")
        move_edge_labels = nx.get_edge_attributes(G, "transfer_movement")
        
        # Clean-up data
        soccer_dict = {}
        league = []
        for (teams, move), (_,player), (_,year),  (_, fee_cleaned) in zip(move_edge_labels.items(),
                                                                                player_edge_labels.items(),
                                                                                year_edge_labels.items(),
                                                                                fee_cleaned_edge_labels.items()):
                
            # n_transaction is a count of number of edges between seller and buyer
            seller, buyer, n_transaction = teams
            
            if seller not in league:
                league.append(seller)
                
            if move == 'in':
                temp = buyer
                buyer = seller
                seller = temp
                
            # Clean fee inconsistencies
            if isinstance(fee_cleaned, str):
                fee_cleaned = float(fee_cleaned)
                    
            if math.isnan(fee_cleaned):
                fee_cleaned = 0.0
            
            # Remove double edges (Ex: 2 Transactions happen, in and out. Keep only out transactions)
            #if int(year) >= 2000: # Domestic Case: Premier League
            if (seller, buyer) not in soccer_dict.keys():
                transfers_list = []
                        
                transfers_list.append((player, fee_cleaned, year))
                soccer_dict.update({(seller, buyer) : transfers_list})
                    
            else:
                current = soccer_dict.get((seller, buyer))
            
                if (player, fee_cleaned, year) not in current:
                    current.append((player, fee_cleaned, year))
                    soccer_dict.update({(seller, buyer) : current})
                    
        return soccer_dict, league
    
    """ Creates a sub-community of international champions teams - money spent"""
    def sub_champions_spent_community(self, soccer, champs):
        prep = Preprocessing()
        spent = {}
        for ((seller, buyer), transfer_list) in soccer.items():
            if buyer in champs:
                for transfer in transfer_list:
                    player, fee_cleaned, year = transfer 
                    
                    # Update spent dictionary
                    if buyer not in spent:
                        spent.update({ buyer : fee_cleaned })
                    else:
                        current_spent = spent.get(buyer)
                        spent.update({ buyer : (fee_cleaned + current_spent) })
                    
        #print(spent)
        # for k, v in spent.items():
        #     print(k, " spent ", v)
        
        spent = prep.sort_dictionary(spent)
        return spent
    
    """ Creates a sub-community of international champions teams - money received""" 
    def sub_champions_received_community(self, soccer, champs):
        prep = Preprocessing()
        received = {}
        for ((seller, buyer), transfer_list) in soccer.items():
            if seller in champs:
                
                for transfer in transfer_list:
                    player, fee_cleaned, year = transfer 
                        
                    # Update received dictionary
                    if seller not in received:
                        received.update({ seller : fee_cleaned })
                    else:
                        current_spent = received.get(seller)
                        received.update({ seller : (fee_cleaned + current_spent) })
                    
        #print(received)
        # for k, v in received.items():
        #     print(k, " received ", v)
        
        received = prep.sort_dictionary(received)
        return received


    def normalize_btw(self, btw):
        # Get minimum btw centr value
        min_k = min(btw, key=btw.get)
        min_v = btw[min_k]
            
        # Get maximum btw centr value
        max_k = max(btw, key=btw.get)
        max_v = btw[max_k]
            
        for k, v in btw.items():
            normal_v = (v - min_v) / (max_v - min_v)
            btw.update({k: normal_v})
            
        return btw
            
            

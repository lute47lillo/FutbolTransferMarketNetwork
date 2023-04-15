import networkx as nx
import pandas as pd


class Preprocessing:
    
    def select_league(self, arg_n):
        leagues = ['../dataset/primera-division.csv', '../dataset/1-bundesliga.csv',
                   '../dataset/serie-a.csv', '../dataset/premier-league.csv',
                   '../dataset/ligue-1.csv', '../dataset/all.csv']
        
        return leagues[arg_n]
        
    def create_dict(self, league_n):
        
        league = self.select_league(league_n)
        df = pd.read_csv(league)
        G = nx.from_pandas_edgelist(df, source='club_name', target='club_involved_name',
                                    edge_attr=['fee', 'year', 'player_name', 'transfer_movement', 'fee_cleaned'],
                                    create_using=nx.MultiDiGraph())
        
        
        # Get all edge labels from graph attributes
        fee_edge_labels = nx.get_edge_attributes(G, "fee")
        fee_cleaned_edge_labels = nx.get_edge_attributes(G, "fee_cleaned")
        year_edge_labels = nx.get_edge_attributes(G, "year")
        player_edge_labels = nx.get_edge_attributes(G, "player_name")
        move_edge_labels = nx.get_edge_attributes(G, "transfer_movement")
        
        # Clean-up data
        soccer_dict = {}
        winners = {}
        for (teams, move), (_,player), (_,year), (_, fee), (_, fee_cleaned) in zip(move_edge_labels.items(),
                                                                                player_edge_labels.items(),
                                                                                year_edge_labels.items(),
                                                                                fee_edge_labels.items(),
                                                                                fee_cleaned_edge_labels.items()):
                
            # n_transaction is a count of number of edges between seller and buyer
            seller, buyer, n_transaction = teams
            if move == 'in':
                temp = buyer
                buyer = seller
                seller = temp
                
            # Remove double edges (Ex: 2 Transactions happen, in and out. Keep only out transactions)
            if not ((seller, buyer), (player, fee_cleaned, year)) in soccer_dict.items():
                soccer_dict.update({(seller, buyer):(player, fee_cleaned, year)})
        
        return soccer_dict
    
    """ Helper Function that maps International Champions names on dictionary with different names """
    def dictionary_name_mapping(self, old):
        # Fix naming of clubs 
        mapping = {'Barcelona': 'FC Barcelona', 'Bor. Dortmund': 'Borussia Dortmund', 'Man Utd': 'Manchester United',
                   'Chelsea' : 'Chelsea FC', 'Liverpool' : 'Liverpool FC', 'Marseille' : 'Olympique Marseille',
                   'Inter': 'Inter Milan'}
        
        # Fix dictionary naming 
        soccer = {}
        for ((seller, buyer), (fee_cleaned, player, year)) in old.items():
            if seller in mapping: # it is a key
                seller = mapping.get(seller)
                
            if buyer in mapping:
                buyer = mapping.get(buyer)

            soccer.update({(seller, buyer):(fee_cleaned, player, year)})
        return soccer
            
    """ Helper function that sorts dictionary by key alphabetically"""
    def sort_dictionary(self, unsorted):
 
        myKeys = list(unsorted.keys())
        myKeys.sort()
        sorted_dict = {i: unsorted[i] for i in myKeys}
        
        return sorted_dict
    
    """ Creates a sub-community of international champions teams - money spent"""
    def sub_champions_spent_community(self, soccer, champs):
        soccer = self.dictionary_name_mapping(soccer)
        
        spent = {}
        for ((seller, buyer), (player, fee_cleaned, year)) in soccer.items():
            if buyer in champs:
                
                # Set fee_cleaned to float type value
                if isinstance(fee_cleaned, float):
                        fee = 0.0
                else:
                        fee = float(fee_cleaned)
                        
                # Update spent dictionary
                if buyer not in spent:
                    spent.update({ buyer : fee })
                else:
                    current_spent = spent.get(buyer)
                    spent.update({ buyer : (fee + current_spent) })
                    
        #print(spent)
        for k, v in spent.items():
            print(k, " spent ", v)
        
        spent = self.sort_dictionary(spent)
        return spent
            
    """ Creates a sub-community of international champions teams - money received"""        
                


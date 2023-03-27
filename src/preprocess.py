import networkx as nx
import pandas as pd


class Preprocessing:
    
    def select_league(self, arg_n):
        leagues = ['../dataset/primera-division.csv', '../dataset/1-bundesliga.csv',
                   '../dataset/serie-a.csv', '../dataset/premier-league.csv',
                   '../dataset/ligue-1.csv', '../dataset/all.csv']
        
        return leagues[arg_n]
        
    def create_dict(self, league_n, champs):
        
        league = self.select_league(league_n)
        print(league)
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
                
            if not ((seller, buyer), (player, fee_cleaned, year)) in winners.items():
                if seller in champs and buyer in champs:
                    winners.update({(seller, buyer):(player, fee_cleaned)})
        
        return soccer_dict, winners
                


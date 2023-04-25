import networkx as nx
import pandas as pd
import math

CH_mapping = {'Barcelona': 'FC Barcelona', 'Bor. Dortmund': 'Borussia Dortmund', 'Man Utd': 'Manchester United',
                   'Chelsea' : 'Chelsea FC', 'Liverpool' : 'Liverpool FC', 'Marseille' : 'Olympique Marseille',
                   'Inter': 'Inter Milan'}

EUR_mapping = {'Bor. Dortmund': 'Borussia Dortmund', 'Man Utd': 'Manchester United',
                   'Chelsea' : 'Chelsea FC', 'Liverpool' : 'Liverpool FC', 'Villarreal' : 'Villarreal CF',
                   'Inter': 'Inter Milan', 'Schalke 04' : 'FC Schalke 04', 'Parma' : 'Parma FC',
                   'E. Frankfurt' : 'Eintracht Frankfurt', 'Atlético Madrid' : 'Atlético de Madrid',
                   'Valencia' : 'Valencia CF'}

universal_mapping = {'Barcelona': 'FC Barcelona', 'Bor. Dortmund': 'Borussia Dortmund', 'Man Utd': 'Manchester United',
                   'Chelsea' : 'Chelsea FC', 'Liverpool' : 'Liverpool FC', 'Marseille' : 'Olympique Marseille',
                   'Inter': 'Inter Milan', 'Man Utd': 'Manchester United',
                   'Liverpool' : 'Liverpool FC', 'Villarreal' : 'Villarreal CF',
                   'Inter': 'Inter Milan', 'Schalke 04' : 'FC Schalke 04', 'Parma' : 'Parma FC',
                   'E. Frankfurt' : 'Eintracht Frankfurt', 'Atlético Madrid' : 'Atlético de Madrid',
                   'Valencia' : 'Valencia CF', 'Real Betis' : 'Real Betis Balompié', 'RCD Mallorca B':'RCD Mallorca',
                   'CF Extremadura (- 2010)':'CF Extremadura', 'Atl. Madrid B':'Atlético de Madrid', 'Real Murcia':'Real Murcia CF',
                   'Real Madrid B':'Real Madrid', 'Barcelona B':'FC Barcelona', 'RM Castilla':'Real Madrid',
                   'Albacete':'Albacete Balompié', 'Levante':'Levante UD', 'Gimnàstic':'Gimnàstic de Tarragona',
                   'Girona':'Girona FC', 'Celta Vigo B':'Celta de Vigo', 'Athletic':'Athletic Bilbao', 'Getafe ':'Getafe CF',
                   'Cádiz B': 'Cádiz CF', 'UD Almería B':'UD Almería', 'Almería':'UD Almería', 'Dep. La Coruña':'Deportivo de La Coruña',
                   'Burgos CF':'Real Burgos CF', 'Racing': 'Racing Santander', 'Real Zaragoza B':'Real Zaragoza',
                   'Recr. Huelva':'Recreativo Huelva', 'Real Sociedad B':'Real Sociedad'}

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
                if int(year) >= 2000: # Premier League Data
                    soccer_dict.update({(seller, buyer):(player, fee_cleaned, year)})
        
        return soccer_dict
    
    """ Helper function that creates 2 lists from a (K,V) pair of a dictionary """
    def create_lists_from_dict(self, soccer):
        T = []
        M = []
        
        for teams, money in soccer.items():
            T.append(teams)
            M.append(money)
        
        return T, M

    """ Helper Function that maps International Champions names on dictionary with different names """
    def dictionary_name_mapping(self, old, mapping):
        
        # Fix dictionary naming 
        soccer = {}
        for ((seller, buyer), (fee_cleaned, player, year)) in old.items():
            if seller in mapping: # it is a key
                seller = mapping.get(seller)
                
            if buyer in mapping:
                buyer = mapping.get(buyer)

            soccer.update({(seller, buyer):(fee_cleaned, player, year)})
        return soccer
    
    def get_universal_mapping(self):
        return universal_mapping
            
    """ Helper function that sorts dictionary by key alphabetically"""
    def sort_dictionary(self, unsorted):
 
        myKeys = list(unsorted.keys())
        myKeys.sort()
        sorted_dict = {i: unsorted[i] for i in myKeys}
        
        return sorted_dict
    
    """ Creates a sub-community of international champions teams - money spent"""
    def sub_champions_spent_community(self, soccer, champs, mapp):
        # if mapp == 0:
        #     soccer = self.dictionary_name_mapping(soccer, CH_mapping)
        # else:
        #     soccer = self.dictionary_name_mapping(soccer, EUR_mapping)
        
        spent = {}
        for ((seller, buyer), (player, fee_cleaned, year)) in soccer.items():
            if buyer in champs:
                
                # Set fee_cleaned to float type value
                #isinstance(fee_cleaned, float):
                #math.isnan(fee_cleaned):
                if math.isnan(fee_cleaned):
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
        # for k, v in spent.items():
        #     print(k, " spent ", v)
        
        spent = self.sort_dictionary(spent)
        return spent
            
    """ Creates a sub-community of international champions teams - money received"""        
    def sub_champions_received_community(self, soccer, champs, mapp):
        if mapp == 0:
            soccer = self.dictionary_name_mapping(soccer, CH_mapping)
        else:
            soccer = self.dictionary_name_mapping(soccer, EUR_mapping)
        
        spent = {}
        for ((seller, buyer), (player, fee_cleaned, year)) in soccer.items():
            if seller in champs:
                
                # Set fee_cleaned to float type value
                if isinstance(fee_cleaned, float):
                        fee = 0.0
                else:
                        fee = float(fee_cleaned)
                        
                # Update spent dictionary
                if seller not in spent:
                    spent.update({ seller : fee })
                else:
                    current_spent = spent.get(seller)
                    spent.update({ seller : (fee + current_spent) })
                    
        #print(spent)
        # for k, v in spent.items():
        #     print(k, " spent ", v)
        
        spent = self.sort_dictionary(spent)
        return spent    
    
    ''' Helper function to obtain the average position and points obtained by teams of a particular league '''
    def average_stats(self):

        league = '../dataset/EPL Standings 2000-2022.csv'
        df = pd.read_csv(league)
        
        
        names = []
        for name in df['Team']:
            names.append(name)
            
        points = []
        for pts in df['Pts']:
            points.append(pts)
                
        positions = []
        for pos in df['Pos']:
            positions.append(pos)
            
        
        soccer = {}
    

        for idx in range(len(names)):
            
            team = names[idx]
            new_points = points[idx]
            new_position = positions[idx]
    
            seasons_played = 1
            
            if team not in soccer.keys():
                soccer.update({ team : (new_position, new_points, seasons_played) })
    
            else:
                current_pos, current_points, curr_seasons  = soccer.get(team)
                    
                seasons_played = seasons_played + curr_seasons
                avg_position = new_position + current_pos
                
                total_points = new_points + current_points
                
                soccer.update({ team : (avg_position, total_points, seasons_played ) })
 
        
        for (team , (avg_position, total_points, seasons_played)) in soccer.items():
            avg_position = avg_position / seasons_played
            soccer.update({ team : (math.ceil(avg_position), total_points) })
        
        soccer = self.sort_dictionary(soccer)
        #print(soccer)
        return soccer
    
    def get_betweenness(self, graph):
        print("Betweenness")
        b = nx.betweenness_centrality(graph, k=30, normalized=True, endpoints=True)
        return b
        
    def get_closeness(self, graph):
        print("Closeness centrality")
        c = nx.closeness_centrality(graph)
        return c
    
    def get_deg_centrality(self, graph):
        print("Degree centrality")
        d = nx.degree_centrality(graph)
        return d
    
    def create_com_index(self, ord):
        n_ord = {}
        for k, v in ord.items():
            n = len(v)
            for i in range(n):
                n_ord.update({v[i]: k-1})
        return n_ord
import networkx as nx
import pandas as pd
import math

class Preprocessing:
    
    def select_league(self, arg_n):
        leagues = ['../dataset/primera-division.csv', '../dataset/1-bundesliga.csv',
                   '../dataset/serie-a.csv', '../dataset/premier-league.csv',
                   '../dataset/ligue-1.csv', '../dataset/liga-nos.csv',
                   '../dataset/eredivisie.csv', '../dataset/all.csv']
        
        return leagues[arg_n]
    
    def select_league_names(self, arg_n):
        leagues = ['Primera Division', 'Bundesliga',
                   'Serie A', 'Premier League', 'Ligue 1',
                   'Liga Nos', 'Eredivisie']
        
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
        league = []
        for (teams, move), (_,player), (_,year), (_, fee), (_, fee_cleaned) in zip(move_edge_labels.items(),
                                                                                player_edge_labels.items(),
                                                                                year_edge_labels.items(),
                                                                                fee_edge_labels.items(),
                                                                                fee_cleaned_edge_labels.items()):
                
            # n_transaction is a count of number of edges between seller and buyer
            seller, buyer, n_transaction = teams
            if seller not in league:
                league.append(seller)
                
            if move == 'in':
                temp = buyer
                buyer = seller
                seller = temp
            
            # Remove double edges (Ex: 2 Transactions happen, in and out. Keep only out transactions)
            if ((seller, buyer), (player, fee_cleaned, year)) not in soccer_dict.items():
                if isinstance(fee_cleaned, str):
                    fee_cleaned = float(fee_cleaned)
                if math.isnan(fee_cleaned):
                    fee_cleaned = 0.0
                soccer_dict.update({(seller, buyer):(player, fee_cleaned, year)})
        
        return soccer_dict, league
    
    """ Helper function that creates 2 lists from a (K,V) pair of a dictionary """
    def create_lists_from_dict(self, soccer):
        T = []
        M = []
        
        for teams, money in soccer.items():
            T.append(teams)
            M.append(money)
        
        return T, M
            
    """ Helper function that sorts dictionary by key alphabetically"""
    def sort_dictionary(self, unsorted):
 
        myKeys = list(unsorted.keys())
        myKeys.sort()
        sorted_dict = {i: unsorted[i] for i in myKeys}
        
        return sorted_dict
    
    def sort_dictionary_by_value(self, unsorted):
 
        sort = sorted(unsorted.items(), key=lambda x:x[1])
        return sort
    
            
    """ 
        Creates a sub-community of teams - money spent
        Given 
            soccer: dict -> {(seller, buyer): transfer_list},
            where transfer_list is a list of tuples of all transfers between seller -> buyer
            
                transfer_list: list -> [(player, fee, year)]
                
            teams: list of teams of community
            
        Returns
            spent: dict -> {team : total spent}
    """
    def spent_community_multi(self, soccer, teams):
        
        spent = {}
        for ((seller, buyer), transfer_list) in soccer.items():
            if buyer in teams:
                for transfer in transfer_list:
                    player, fee_cleaned, year = transfer 
                        
                    # Update spent dictionary
                    if buyer not in spent:
                        spent.update({ buyer : fee_cleaned })
                    else:
                        current_spent = spent.get(buyer)
                        spent.update({ buyer : (fee_cleaned + current_spent) })
                        
        spent = self.sort_dictionary(spent)    
        #print(spent)
        # for k, v in spent.items():
        #     print(k, " spent ", v)
        
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
                
                soccer.update({ team : (avg_position, total_points, seasons_played)})
 
        
        for (team , (avg_position, total_points, seasons_played)) in soccer.items():
            avg_position = avg_position / seasons_played
            soccer.update({ team : (math.ceil(avg_position), total_points) })
        
        soccer = self.sort_dictionary(soccer)
        #print(soccer)
        return soccer
    
    def get_betweenness(self, graph):
        #print("Betweenness")
        b = nx.betweenness_centrality(graph, k=44, normalized=False, endpoints=False)
        return b
        
    def get_closeness(self, graph):
        #print("Closeness centrality")
        c = nx.closeness_centrality(graph)
        return c
    
    def get_deg_centrality(self, graph):
        #print("Degree centrality")
        d = nx.degree_centrality(graph)
        return d
    
    def create_com_index(self, ord):
        n_ord = {}
        for k, v in ord.items():
            n = len(v)
            for i in range(n):
                n_ord.update({v[i]: k-1})
        return n_ord
    
    """ 
        Helper function. 
        Given a dictionary {team: avg position, total points} 
        Return performance communities
    """
    def organize_teams(self, stats):
        int_n = 6
        mid_n = 17
        
        pos = {}
        mon = {}
        for t, (avg_pos, points) in stats.items():
            
            # Create a pos_dict_community index based on performance positions
            if avg_pos <= int_n:
                pos.update({t:1})
            elif avg_pos > int_n and avg_pos <= mid_n:
                pos.update({t:2})
            else:
                pos.update({t:3})
                
            # Create a comm_index based on points spent
            if points <= 350:
                mon.update({t:4})
            elif points > 350 and points <= 700:
                mon.update({t:3})
            elif points > 700 and points <= 1000:
                mon.update({t:2})
            else:
                mon.update({t:1})
                
        return pos, mon
    
    """ 
        Helper function.
        Given a dictionary {team : total spent}
        Returns a community index
    """
    def get_money_community(self, stats):
        mon = {}
        for t, m in stats.items():
            if m <= 300:
                mon.update({t:4})
            elif m > 300 and m <= 600:
                mon.update({t:3})
            elif m > 600 and m <= 1100:
                mon.update({t:2})
            else:
                mon.update({t:1})
        return mon
    
    """
        Given a graph
        Returns total money spent by each buyer.
    """
    def get_dict_money_spent(self, graph):
        edges = [e for e in graph.edges.data()]
        buys = {}

        n = len(edges)
        for i in range(n):
            seller, buyer, fee = edges[i]
            fee = fee.get('fee')
            
            if buyer not in buys:
                buys.update({buyer:fee})
            else:
                curr = buys.get(buyer)
                buys.update({buyer:fee + curr})
                
        return buys
    
    """
        Helper function
        Given a dictionary -> soccer
        Returns the teams that are part of that specific League during the period 1992-2022
    """
    def get_teams_from_league(self, soccer):
        league = []
        for keys, values in soccer.items():
            seller, buyer = keys
            
            if seller not in league:
                league.append(seller)
                
        return league
    
    """
        Given a graph. Convert it to normal graph.
        Returns clustering coefficient for all nodes in the graph.
    """
    def get_graph_clustering_ceff(self, graph):
        graph = nx.DiGraph(graph)
        coeff = nx.clustering(graph) 
        return coeff
    
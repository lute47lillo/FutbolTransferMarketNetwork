""" Study teams on same community and map them to their performance across the years """
from preprocess import Preprocessing
import scipy as sp
import numpy as np
import math
import networkx as nx

# TODO: YOu have studied for small communites based on modularity.
# MISSING: Study Premier League as a one big community
class StatsAndCommunities:
    
    """
        stats -> {team : average position, total points}
        communities -> {com_idx : list of teams in community}
        soccer -> (seller, buyer) : (player, fee, year) 
    """

    def study(self, communities, stats, soccer):
        prep = Preprocessing()
        n_com = len(communities)
        
        for i in range(n_com):
            teams = communities.get(i+1)
            
            spent_community = prep.sub_champions_spent_community(soccer, teams, 1)
            
            sub_comm_pos = {}
            sub_comm_points = {}
            sub_teams = []
            for team, (avg_pos, points) in stats.items():
                if team in spent_community:
                    money = spent_community.get(team)
                    sub_teams.append(team)
                    
                    sub_comm_pos.update({ money : avg_pos})
                    sub_comm_points.update({money:  points})
                    
                    #print(team, "spends ", money, " million euros to achieve ", avg_pos, " average position")
                    #print(team, "spends ", money, " million euros to achieve ", points, " points")
            
            position_corr = self.calculating_pearson_corr_stats(sub_comm_pos)
            print("The position - money corr. coeff. for teams ", sub_teams, " is ", position_corr, "\n")
            
            
            points_corr = self.calculating_pearson_corr_stats(sub_comm_points)
            print("The points - money corr. coeff. for teams ", sub_teams, " is ", points_corr, "\n")
                    
                    
    def whole_league_community(self, stats, soccer):
        
        prep = Preprocessing()
        
        teams = []
        for team, (_,_) in stats.items():
            teams.append(team)
            
        spent_community = prep.sub_champions_spent_community(soccer, teams, 0)
        
        sub_comm_pos = {}
        sub_comm_points = {}
        
        for team in teams:
            money = spent_community.get(team)
            avg_pos, points = stats.get(team)
            
            sub_comm_pos.update({ money : avg_pos})
            sub_comm_points.update({money:  points})
            
            
            #print(team, "spends ", money, " million euros to achieve ", avg_pos, " average position")
            #print(team, "spends ", money, " million euros to achieve ", points, " points")
        
        position_corr = self.calculating_pearson_corr_stats(sub_comm_pos)
        print("The position - money corr. coeff. for teams ", teams, " is ", position_corr, "\n")
             
        points_corr = self.calculating_pearson_corr_stats(sub_comm_points)
        print("The points - money corr. coeff. for teams ", teams, " is ", points_corr, "\n")
        
        
    def calculating_pearson_corr_stats(self, data):
        money = list(data.keys())
        other_value = list(data.values())
        
        y = np.array(other_value)
        x = np.array(money)
        corr_coeff = sp.stats.spearmanr(y, x)
        
        return corr_coeff
            
    """
        Given a sub-community, a graph of that community, and the statistics of the community:
        
        Study:
            - The Betweenness: a way of detecting the amount of influence a node has over the flow of information in a graph
            - The Closeness Centrality: indicates how close a node is to all other nodes in the network
            - The Degree Centrality: The degree centrality of a node is simply its degree—the number of edges it has.
                                     The higher the degree, the more central the node is. 
            
        Compare how the sub-community does wrt to the bigger community.
        Compare their influence wrt to their performance.
    """
    def community_attributes(self, stats, communities, graph):
        prep = Preprocessing()
        n_com = len(communities)
        
        # Create an unfrozen copy of the graph and narrow by community of stats
        unfrozen_graph = nx.Graph(graph)
        graph = self.narrow_graph(unfrozen_graph, stats)
        
        # Obtain attributes of the graph community
        betw = prep.get_betweenness(graph)
        close = prep.get_closeness(graph)
        deg_centrality = prep.get_deg_centrality(graph)
        
        for i in range(n_com):
            
            teams = communities.get(i+1)
            print("\nCommunity nº: ", i+1)
            for team, (avg_pos, points) in stats.items():
                if team in graph.nodes() and team in teams:
                    pass
                    #print(f"Betweenness Centrality {team:2} {betw[team]:.3f}")
                    #print(f"Closeness Centrality { team:2} {close[team]:.3f}")
                    #print(f"Degree Centrality {team:2} {deg_centrality[team]:.3f}\n")
        
        self.study_betwenneess(betw, stats)
        self.study_closenes(close, stats)
        self.study_degree(deg_centrality, stats)
            
                  
    """ Helper function to narrow the graph by deleting nodes not in the target community """  
    def narrow_graph(self, graph, stats):
        non_community_nodes = []
        for nodes in graph.nodes():
            if nodes not in stats:
                non_community_nodes.append(nodes)
        graph.remove_nodes_from(non_community_nodes) 
            
        return graph
    
    """
        A node with higher betweenness centrality would have more control over the network,
        because more information will pass through that node.
        Therefore, order by betw centrality. Are higher nodes (more transfers through). better off?
    """    
    def study_betwenneess(self, betw, stats):
        b_points = {}
        b_pos = {}
        for team, (avg_pos, points) in stats.items():
            if team in betw:
                print(f"Betweenness Centrality {team:2} {betw[team]:.3f}")
                b_points.update({points:betw[team]})
                b_pos.update({avg_pos:betw[team]})
                
        points_corr = self.calculating_pearson_corr_stats(b_points)
        print("The points - betwenneess corr. coeff. for teams is ", points_corr, "\n")
        
        position_corr = self.calculating_pearson_corr_stats(b_pos)
        print("The position - betwenneess corr. coeff. for teams is ", position_corr, "\n")
        
    def study_closenes(self, close, stats):
        b_points = {}
        b_pos = {}
        for team, (avg_pos, points) in stats.items():
            if team in close:
                print(f"Closeness Centrality { team:2} {close[team]:.3f}")
                b_points.update({points:close[team]})
                b_pos.update({avg_pos:close[team]})
                
        points_corr = self.calculating_pearson_corr_stats(b_points)
        print("The points - closenes corr. coeff. for teams is ", points_corr, "\n")
        
        position_corr = self.calculating_pearson_corr_stats(b_pos)
        print("The position - closenes corr. coeff. for teams is ", position_corr, "\n")
        
    def study_degree(self, deg, stats):
        b_points = {}
        b_pos = {}
        for team, (avg_pos, points) in stats.items():
            if team in deg:
                print(f"Degree Centrality {team:2} {deg[team]:.3f}")
                b_points.update({points:deg[team]})
                b_pos.update({avg_pos:deg[team]})
                
        points_corr = self.calculating_pearson_corr_stats(b_points)
        print("The points - degree centrality corr. coeff. for teams is ", points_corr, "\n")
        
        position_corr = self.calculating_pearson_corr_stats(b_pos)
        print("The position - degree centrality corr. coeff. for teams is ", position_corr, "\n")
                
            
            
            
            
      
            
    
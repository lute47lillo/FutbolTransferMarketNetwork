""" Study teams on same community and map them to their performance across the years """
from preprocess import Preprocessing
import scipy as sp
import numpy as np
import math

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
        print(money)
        other_value = list(data.values())
        
        y = np.array(other_value)
        x = np.array(money)
        corr_coeff = sp.stats.spearmanr(y, x)
        
        return corr_coeff
        
      
            
    
import networkx as nx
import pandas as pd
import math
from preprocess import Preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np


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
    
    """
        Given:
            league_n: int [0..n]. Representing dataset from where to construct dictionary
        
        Returns:
            soccer: dict {(seller, buyer): transfer_list}, where transfer_list is a list
            of tuples of all transfers between seller -> buyer
            transfer_list: list [(player, fee, year)]
            
            league: list of teams that only participate in that given leagues.
    """
    def create_double_dict(self, league_n, lg1, lg2):
        
        prep = Preprocessing()
        league = prep.select_league(league_n)
        
        # Get pair league names
        leagues_names = []
        l1 = prep.select_league_names(lg1)
        l2 = prep.select_league_names(lg2)
        leagues_names.append(l1)
        leagues_names.append(l2)
        
        df = pd.read_csv(league)
        G = nx.from_pandas_edgelist(df, source='club_name', target='club_involved_name',
                                    edge_attr=['player_name', 'transfer_movement', 'fee_cleaned', 'year', 'league_name'],
                                    create_using=nx.MultiDiGraph())
        
        
        # Get all edge labels from graph attributes
        fee_cleaned_edge_labels = nx.get_edge_attributes(G, "fee_cleaned")
        year_edge_labels = nx.get_edge_attributes(G, "year")
        player_edge_labels = nx.get_edge_attributes(G, "player_name")
        move_edge_labels = nx.get_edge_attributes(G, "transfer_movement")
        league_edge_labels = nx.get_edge_attributes(G, "league_name")
        
        # Clean-up data
        soccer_dict = {}
        league_1 =[]
        league_2 =[]
        for (teams, move), (_,player), (_,year),  (_, fee_cleaned), (_, league_name) in zip(move_edge_labels.items(),
                                                                                player_edge_labels.items(),
                                                                                year_edge_labels.items(),
                                                                                fee_cleaned_edge_labels.items(),
                                                                                league_edge_labels.items()):
            # If is any of the 2 leagues being compared
            if league_name in leagues_names:
                # n_transaction is a count of number of edges between seller and buyer
                seller, buyer, n_transaction = teams
                
                # Add to correct league group
                if league_name == l1 and seller not in league_1:
                    league_1.append(seller)
                    
                elif league_name == l2 and seller not in league_2:
                    league_2.append(seller)
                  
                # Set all transfers to seller -> buyer
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
                if (seller, buyer) not in soccer_dict.keys():
                    transfers_list = []
                            
                    transfers_list.append((player, fee_cleaned, year))
                    soccer_dict.update({(seller, buyer) : transfers_list})
                        
                else:
                    current = soccer_dict.get((seller, buyer))
                
                    if (player, fee_cleaned, year) not in current:
                        current.append((player, fee_cleaned, year))
                        soccer_dict.update({(seller, buyer) : current})
                    
        final_league = []
        final_league.append(league_1)
        final_league.append(league_2)
        return soccer_dict, final_league
    
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
    
    def normalize_pair_league_omegas(self):
        df = pd.read_csv('../dataset/omegas.csv')
        G = nx.from_pandas_edgelist(df, source='league1', target='league2',
                                    edge_attr=['omegas', 'teams', 'transfers'],
                                    create_using=nx.MultiGraph())
        
        omega_labels = nx.get_edge_attributes(G, "omegas")
        teams_labels = nx.get_edge_attributes(G, "teams") # number of teams in the pair leagues
        transfers_labels = nx.get_edge_attributes(G, "transfers") # number of sinlge edge transfers between leagues.
        
        dict_omegas ={}
        plot_dict = {}
        for(leagues, omega), (_, teams), (_, transfers) in zip(omega_labels.items(),
                                                               teams_labels.items(),
                                                               transfers_labels.items()):
            
            l1 = leagues[0]
            l2 = leagues[1]
            
            plot_dict.update({(l1,l2):(omega, teams, transfers)})
            dict_omegas.update({(l1,l2):omega})
            
        dict_omegas = self.normalize_btw(dict_omegas)
        
        return dict_omegas, plot_dict, G
    
    """ 
        Plot scatter description:
            node = unique IDentifier for joint pair league (1-21)
            x = number of teams participating in transfers
            y = number of edges (transfers)
            node size = normalized omega value
    """
    def plot_omegas(self, data, omegas_norm):
        
        keys = list(data.keys()) # names of leagues
        y_omegas = list(omegas_norm.values())
        
        
        # Assing Unique Identifier
        id_leagues = {}
        for i in range(len(keys)):
            id_leagues.update({keys[i]:i+1})
        
        ids_names = list(id_leagues.keys())
        ids = list(id_leagues.values())
        
        x_transfers = []
        for (omega, _, transfers) in data.values():
            x_transfers.append(transfers)
    

        print(x_transfers, y_omegas)
        fig, ax = plt.subplots()
        scatter = ax.scatter(x_transfers, y_omegas)

        for i, txt in enumerate(ids):
            ax.annotate(txt, (x_transfers[i], y_omegas[i]))
            print(ids_names[i], txt, x_transfers[i], y_omegas[i])
            
        # plt.xlabel("Nº transfers", fontsize = 15, c = "black")
        # plt.ylabel("Omega", fontsize = 15, c = "black")     
        # sns.regplot(x=x_transfers, y=y_omegas)
        
        # plt.title('Pairs of Leagues - Small World')
        # plt.savefig("../plots/omegas_league_trasnfers_regression.png", format="PNG")
        # plt.show()
        
    """ 
        Plot Btw Centrality vs money and positions
            Do a mapping to dictionary where
            {team:(position, money, btw_centr, money_community)}
            
        x -> Positions or money spent.
        y -> Betweenness centrality value.
    """
    def objective(self, x, a, b, c, d, e, f):
        return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f
    
    def objective4(self, x, a, b, c, d, e):
        return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + e
    
    def objective2(self, x, a, b, c,):
        return (a * x) + (b * x**2) + c
    
    def plot_betwenness(self, btw_centr, prem_stats, money_comm_idx, spent):
        
        btw_plot = {}
        # Assing Unique Identifier to team
        id_leagues = {}
        for i in range(len(btw_centr)):
            team, bc = btw_centr[i]
            id_leagues.update({team:i+1})
            
            # Get average historical position per team
            pos, _ = prem_stats.get(team)
            
            # Get total money spent per teams
            money = spent.get(team)
            
            # Get waht group of money is from
            money_comm = money_comm_idx.get(team)
            print(team, money_comm)
            
            btw_plot.update({team:(pos,money,bc, money_comm)})
        
        
        ids_names = list(id_leagues.keys())
        ids = list(id_leagues.values())
        print("The id _leagues \n:", id_leagues)
        
        x_money = []
        x_pos = []
        y_bc = []
        m_comms = []
        for (pos, money, bc, money_comm) in btw_plot.values():
            y_bc.append(bc)
            x_money.append(money)
            x_pos.append(pos)
            m_comms.append(money_comm)
            
        fig, ax = plt.subplots()
        
        # list of length 44, 1-4 representing what community a team is
        money_groups = ['$ > 1100€', '€ > 600 and € <= 1100','€ < 600 and € >= 300','€ < 300']
        
        # Draw a polynomial fit curve based on results
        popt,_ = curve_fit(self.objective, x_pos, y_bc)
        a, b, c, d, e, f = popt
        
        scatter = plt.scatter(x_pos, y_bc, c = m_comms)
        
        x_line = np.arange(min(x_pos), max(x_pos), 1)
        y_line = self.objective(x_line, a, b, c, d, e, f)
        
        plt.plot(x_line, y_line, '--', color='r', alpha=0.5)
        plt.legend(handles=scatter.legend_elements()[0], labels=money_groups,
                   loc='upper center', bbox_to_anchor=(0.5, 1.25),
                   ncol=2, fancybox=True, shadow=True)
        
    
        for i, txt in enumerate(ids):
            ax.annotate(txt, (x_pos[i], y_bc[i]))
            
    
        plt.xlabel("Average Position", fontsize = 15, c = "black")
        plt.ylabel("Betwenness Centrality", fontsize = 15, c = "black")     
        
        plt.title('Betwenness Centrality - Average Position')
        plt.savefig("../plots/btw_position_regressionPol5.png", format="PNG")
        plt.show()
    

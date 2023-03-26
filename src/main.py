import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx
import itertools

from preprocess import Preprocessing
from communities import Community

"""
    Datasets
    0   ../dataset/primera-division.csv 
    1   ../dataset/1-bundesliga.csv 
    2   ../dataset/serie-a.csv 
    3   ../dataset/premier-league.csv
    4   ../dataset/ligue-1.csv
"""

    
def main():
    
    # Preprocess the data 
    prep = Preprocessing()
    soccer = prep.create_dict(3)
    
    # Execute functions
    # Communities
    comm = Community()
    ordered = comm.process_community_graph(soccer, True, 3)
    
    print("The ordered communities: ", ordered)


main()
# def draw_graph(G):
#     fig, ax = plt.subplots(1, 1, figsize=(12,7))
#     edge_collection = nx.draw_networkx(G, pos=nx.circular_layout(G),
#                                    ax=ax, node_size=170, font_size=5, width=0.7)
    
#     edge_labels = nx.get_edge_attributes(G, "fee")
#     nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G),
#                                 edge_labels=edge_labels, font_color='k',
#                                 font_family='sans-serif', ax=ax, font_size=7)

#     plt.tight_layout()
#     fig.suptitle('example')
#     plt.show()
    
# # club_name, player_name ,age, position, club_involved_name, fee,
# # transfer_movement, transfer_period, fee_cleaned, league_name, year,season

# # Read data and create graph
# df = pd.read_csv('../dataset/primera-division.csv')
# Graphtype = nx.Graph()
# G = nx.from_pandas_edgelist(df, source='club_name', target='club_involved_name' ,edge_attr=['fee', 'year', 'player_name', 'transfer_movement', 'fee_cleaned'], create_using=nx.DiGraph())

# # Get all edge labels from graph attributes
# fee_edge_labels = nx.get_edge_attributes(G, "fee")
# fee_cleaned_edge_labels = nx.get_edge_attributes(G, "fee_cleaned")
# year_edge_labels = nx.get_edge_attributes(G, "year")
# player_edge_labels = nx.get_edge_attributes(G, "player_name")
# move_edge_labels = nx.get_edge_attributes(G, "transfer_movement")

# # Clean-up data
# soccer_dict = {}
# for (teams, move), (_,player), (_,year), (_, fee), (_, fee_cleaned) in zip(move_edge_labels.items(),
#                                              player_edge_labels.items(),
#                                              year_edge_labels.items(),
#                                              fee_edge_labels.items(),
#                                              fee_cleaned_edge_labels.items()):
    
#     # Make all transactions out Seller -> Buyer. Weight is fee and 'name' of player
#     seller, buyer = teams
#     if move == 'in':
#         temp = buyer
#         buyer = seller
#         seller = temp
    
#     # Remove double edges (Ex: 2 Transactions happen, in and out. Keep only out transactions)
#     if not ((seller, buyer), (player, fee_cleaned, year)) in soccer_dict.items():
#         soccer_dict.update({(seller, buyer):(player, fee_cleaned, year)})
        
# #print(soccer_dict)

# # Create trimmed graph from previously created dictionary
# # TODO: If ADDED all communities from other datasets, maybe we can see something more
# trim_graph = nx.Graph()
# trim_graph.add_nodes_from(soccer_dict.keys())

# #print(trim_graph) # 5672 nodes

# # EDIT trim graph to be more efficient to work with
# for ((seller, buyer), (player, fee_cleaned, year)) in soccer_dict.items():
#     #print(seller, buyer)
#     trim_graph.add_weighted_edges_from(ebunch_to_add=[(seller, buyer, fee_cleaned)], weight="fee")
    
# low_degree = [n for n, d in trim_graph.degree() if d < 20]
# trim_graph.remove_nodes_from(low_degree) 

# components = nx.connected_components(trim_graph)
# largest_component = max(components, key=len)
# trim_graph = trim_graph.subgraph(largest_component)

# # # compute centrality
# centrality = nx.betweenness_centrality(trim_graph, k=50, normalized=True, endpoints=True)

# # Modularity is a measure of the structure of a graph, measuring the density of connections within a module or community.
# # Graphs with a high modularity score will have many connections within a community but only few pointing outwards to other communities.

# comm = nx.community.greedy_modularity_communities(trim_graph, best_n=10)

# community_index = {n: i for i, com in enumerate(comm) for n in com}

# order_comm = {}
# for team, community in community_index.items():
#     if not (community, team) in order_comm.items():
#         order_comm.setdefault(community, []).append(team)
        

# print(order_comm)

# #### draw graph ####
# fig, ax = plt.subplots(figsize=(20, 15))
# pos = nx.spring_layout(trim_graph, k=0.15, seed=4572321)
# node_color = [community_index[n] for n in trim_graph]
# node_size = [v * 20000 for v in centrality.values()]
# nx.draw_networkx(
#     trim_graph,
#     pos=pos,
#     with_labels=True,
#     node_color=node_color,
#     node_size=node_size,
#     edge_color="gainsboro",
#     alpha=0.4,
# )

# # Title/legend
# font = {"color": "k", "fontweight": "bold", "fontsize": 20}
# ax.set_title("LaLiga association network for TransferMarket", font)
# # Change font color for legend
# font["color"] = "r"

# ax.text(
#     0.80,
#     0.10,
#     "node color = community structure",
#     horizontalalignment="center",
#     transform=ax.transAxes,
#     fontdict=font,
# )
# ax.text(
#     0.80,
#     0.06,
#     "node size = betweenness centrality",
#     horizontalalignment="center",
#     transform=ax.transAxes,
#     fontdict=font,
# )

# # Resize figure for label readability
# ax.margins(0.1, 0.05)
# fig.tight_layout()
# plt.axis("off")
# plt.savefig("LaLigaGraphSmaller.png", format="PNG")
# #plt.show()



#fee_edge_labels = nx.get_edge_attributes(trim_graph, 'fee')

"""
    TODO:
    1. Create a Dictionary {team : (total_fee_spent, total_fee_received)}
        - Divide teams by clusters with threshold of total fee spent
        - Now, map them to their major trophy wins (We should see that more money = more trophies)
        - Number of relegations, which teams are getting relegated more? More or less money spent?
        
    2. Create A Dictionary by year {team : {list of position of players transferred into team} }
        - Compare to following season records.
        - Are teams getting more cbs, strikers, gks... doing better or worse?


"""


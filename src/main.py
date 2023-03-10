import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx


def draw_graph(G):
    fig, ax = plt.subplots(1, 1, figsize=(12,7))
    edge_collection = nx.draw_networkx(G, pos=nx.circular_layout(G),
                                   ax=ax, node_size=170, font_size=5, width=0.7)
    
    edge_labels = nx.get_edge_attributes(G, "fee")
    nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G),
                                edge_labels=edge_labels, font_color='k',
                                font_family='sans-serif', ax=ax, font_size=7)

    plt.tight_layout()
    fig.suptitle('example')
    plt.show()
    
# club_name, player_name ,age, position, club_involved_name, fee,
# transfer_movement, transfer_period, fee_cleaned, league_name, year,season

# Read data and create graph
df = pd.read_csv('dataset/primera-division.csv')
Graphtype = nx.Graph()
G = nx.from_pandas_edgelist(df, source='club_name', target='club_involved_name' ,edge_attr=['fee', 'year', 'player_name', 'transfer_movement', 'fee_cleaned'], create_using=nx.DiGraph())

# Get all edge labels from graph attributes
fee_edge_labels = nx.get_edge_attributes(G, "fee")
fee_cleaned_edge_labels = nx.get_edge_attributes(G, "fee_cleaned")
year_edge_labels = nx.get_edge_attributes(G, "year")
player_edge_labels = nx.get_edge_attributes(G, "player_name")
move_edge_labels = nx.get_edge_attributes(G, "transfer_movement")

# Clean-up data
soccer_dict = {}
for (teams, move), (_,player), (_,year), (_, fee) in zip(move_edge_labels.items(),
                                             player_edge_labels.items(),
                                             year_edge_labels.items(),
                                             fee_edge_labels.items()):
    
    # Make all transactions out Seller -> Buyer. Weight is fee and 'name' of player
    seller, buyer = teams
    if move == 'in':
        temp = buyer
        buyer = seller
        seller = temp
    
    # Remove double edges (Ex: 2 Transactions happen, in and out. Keep only out transactions)
    if not ((seller, buyer), (player, fee, year)) in soccer_dict.items():
        soccer_dict.update({(seller, buyer):(player, fee, year)})
        
#print(soccer_dict)

# Create trimmed graph from previously created dictionary
trim_graph = nx.DiGraph()
trim_graph.add_nodes_from(soccer_dict.keys())

print(trim_graph) # 5672 nodes

for ((seller, buyer), (player, fee, year)) in soccer_dict.items():
    print(seller, buyer)
    trim_graph.add_weighted_edges_from(ebunch_to_add=[(seller, buyer, fee)], weight="fee")
    

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


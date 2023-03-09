import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# club_name, player_name ,age, position, club_involved_name, fee,
# transfer_movement, transfer_period, fee_cleaned, league_name, year,season

df = pd.read_csv('dataset/primera-division.csv')
Graphtype = nx.Graph()

# I can add multiple edge attributes as a list = ['x1','x2']
G = nx.from_pandas_edgelist(df, source='club_name', target='club_involved_name' ,edge_attr=['fee', 'year', 'player_name', 'transfer_movement'], create_using=nx.DiGraph())

#print(nx.degree_histogram(G))
#nx.draw_networkx(G)


# Use Matplot to plot the graph with nodes and edges corresponding with the mentioning
# fig, ax = plt.subplots(1, 1, figsize=(12,7))
# edge_collection = nx.draw_networkx(G, pos=nx.kamada_kawai_layout(G),
#                                    ax=ax, node_size=170, font_size=5, width=0.7)

# Dictionary -> {(Team selling, Team buying) : Money}
# Money can be in millions (€1.75m), in thousands (€800th), loan (loan transfer goes A to B) or (End of loanJun 30, 2022, goes back to original team) or no data ('-')
fee_edge_labels = nx.get_edge_attributes(G, "fee")
year_edge_labels = nx.get_edge_attributes(G, "year")
player_edge_labels = nx.get_edge_attributes(G, "player_name")
move_edge_labels = nx.get_edge_attributes(G, "transfer_movement")

# for teams, fee in fee_edge_labels.items():
#     seller, buyer = teams
        
#     if seller == 'Real Madrid':
#         temp_cmp = fee[0:3]
#         if temp_cmp == 'End':  
#             fee = 'Returns to club from loan'
#         print(seller, " -> ", buyer, " for ", fee)
        
        
        
# for teams, year in year_edge_labels.items():
#     seller, buyer = teams
        
#     if seller == 'Real Madrid':
#         print(seller, " -> ", buyer, " in ", year)
        
for (teams, move), (_,player), (_,year), (_, fee) in zip(move_edge_labels.items(),
                                             player_edge_labels.items(),
                                             year_edge_labels.items(),
                                             fee_edge_labels.items()):
    seller, buyer = teams
    if move == 'in':
        temp = buyer
        buyer = seller
        seller = temp
        
    if seller == 'Real Madrid':
        print(seller, " sold ", player, " to ", buyer, " in ", year, " for ", fee)
        
    if buyer == 'Real Madrid':
        print(buyer, " bought ", player, " from ", seller, " in ", year, " for ", fee)
        
        
    
    
    
    
 



#print(type(edge_labels))

# nx.draw_networkx_edge_labels(G, pos=nx.kamada_kawai_layout(G),
#                                 edge_labels=edge_labels, font_color='k',
#                                 font_family='sans-serif', ax=ax, font_size=7)

# plt.tight_layout()
# fig.suptitle('example')
# plt.show()


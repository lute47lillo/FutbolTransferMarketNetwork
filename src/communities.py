import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as approx
import itertools


titles = ["LaLiga association network for TransferMarket", "Bundesliga association network for TransferMarket",
          "Serie A association network for TransferMarket", "PremierLeague association network for TransferMarket",
          "Ligue 1 association network for TransferMarket"]

fig_names = ["../plots/LaLigaSGraph.png", "../plots/BundesligaSGraph.png",
          "../plots/Serie_ASGraph.png", "../plots/PremierLeagueSGraph.png",
          "../plots/Ligue_1SGraph.png"]

class Community:
    
    def plot_community(self, graph, com_index, centrality, n):
        
        #### draw graph ####
        fig, ax = plt.subplots(figsize=(20, 15))
        pos = nx.spring_layout(graph, k=0.15, seed=4572321)
        node_color = [com_index[n] for n in graph]
        node_size = [v * 20000 for v in centrality.values()]
        nx.draw_networkx(
            graph,
            pos=pos,
            with_labels=True,
            node_color=node_color,
            node_size=node_size,
            edge_color="gainsboro",
            alpha=0.4,
        )

        # Title/legend
        font = {"color": "k", "fontweight": "bold", "fontsize": 20}
        title = titles[n]
        ax.set_title(title, font)
        
        # Change font color for legend
        font["color"] = "r"

        ax.text(
            0.80,
            0.10,
            "node color = community structure",
            horizontalalignment="center",
            transform=ax.transAxes,
            fontdict=font,
        )
        ax.text(
            0.80,
            0.06,
            "node size = betweenness centrality",
            horizontalalignment="center",
            transform=ax.transAxes,
            fontdict=font,
        )

        # Resize figure for label readability
        ax.margins(0.1, 0.05)
        fig.tight_layout()
        plt.axis("off")
        fig_name = fig_names[n]
        plt.savefig(fig_name, format="PNG")
        plt.show()
        
        
    def process_community_graph(self, soccer_dict, is_plotting, title_text):
        
        trim_graph = nx.MultiGraph()
        trim_graph.add_nodes_from(soccer_dict.keys())

        # Trimmed graph with only fee_cleaned weight
        for ((seller, buyer), (player, fee_cleaned, year)) in soccer_dict.items():
            trim_graph.add_weighted_edges_from(ebunch_to_add=[(seller, buyer, fee_cleaned)], weight="fee")
            
        fee_trim_graph = trim_graph
        
        # buyer, seller is oppositte as how it should be, but result is correct
        low_fee_edges = [(seller, buyer) for (buyer, seller, attrs) in trim_graph.edges(data=True) if attrs["fee"] < 8]
        high_fee_edges = [(seller, buyer) for (buyer, seller, attrs) in trim_graph.edges(data=True) if attrs["fee"] > 8]
    
        fee_trim_graph.remove_edges_from(high_fee_edges)
        
        
        # REMOVE innecesary and noise nodes form the graph
        low_degree = [n for n, d in trim_graph.degree() if d < 20]
        trim_graph.remove_nodes_from(low_degree) 

        components = nx.connected_components(trim_graph)
        largest_component = max(components, key=len)
        trim_graph = trim_graph.subgraph(largest_component)

        # Compute centrality
        centrality = nx.betweenness_centrality(trim_graph, k=50, normalized=True, endpoints=True)

        # Run algorithm
        comm = nx.community.greedy_modularity_communities(trim_graph, best_n=10)
        community_index = {n: i for i, com in enumerate(comm) for n in com}

        order_comm = {}
        for team, community in community_index.items():
            if not (community, team) in order_comm.items():
                order_comm.setdefault(community, []).append(team)
                
        if is_plotting:
            self.plot_community(trim_graph, community_index, centrality, title_text)
            
        return order_comm, trim_graph
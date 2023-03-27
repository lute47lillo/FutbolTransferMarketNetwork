import networkx as nx
import matplotlib.pyplot as plt

class Winners:
    
    
    def plot_winners(self, graph, centrality):
        
        fig, ax = plt.subplots(figsize=(20, 15))
        pos = nx.spring_layout(graph, k=0.15, seed=4572321)
        node_size = [v * 20000 for v in centrality.values()]
        nx.draw_networkx(
            graph,
            pos=pos,
            with_labels=True,
            node_size=node_size,
            edge_color="gainsboro",
            alpha=0.4,
        )
        edge_labels = nx.get_edge_attributes(graph, "fee")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)
        
        font = {"color": "k", "fontweight": "bold", "fontsize": 20}
        ax.set_title("Champions League ass. network for TransferMarket", font)

        ax.margins(0.1, 0.05)
        fig.tight_layout()
        plt.axis("off")
        plt.savefig("../plots/champ_league.png", format="PNG")
        plt.show()
 
        
    def champ_league(self, soccer, champs):
    
        winners_graph = nx.Graph()
        
        # Transfers between Champions League winners since 1992/1993
        winners= {}
        for ((seller, buyer), (player, fee_cleaned, year)) in soccer.items():
            if seller in champs and buyer in champs:
                winners.update({(seller, buyer):(fee_cleaned, player)})
        winners_graph.add_nodes_from(winners.keys())

        # Trimmed graph with only fee_cleaned weight
        for ((seller, buyer), (fee_cleaned, player)) in winners.items():
            winners_graph.add_weighted_edges_from(ebunch_to_add=[(seller, buyer, fee_cleaned)], weight="fee")
            
        # Fix naming of clubs 
        mapping = {'Barcelona': 'FC Barcelona', 'Bor. Dortmund': 'Borussia Dortmund', 'Man Utd': 'Manchester United',
                   'Chelsea' : 'Chelsea FC', 'Liverpool' : 'Liverpool FC', 'Marseille' : 'Olympique Marseille'}
        winners_graph = nx.relabel_nodes(winners_graph, mapping)

        # Induced subgraph of larger connected components
        components = nx.connected_components(winners_graph)
        largest_component = max(components, key=len)
        winners_graph = winners_graph.subgraph(largest_component)
        
        # # Compute centrality
        centrality = nx.betweenness_centrality(winners_graph, k=5, normalized=True, endpoints=True)

        self.plot_winners(winners_graph, centrality)
        
        return winners
        
    
            
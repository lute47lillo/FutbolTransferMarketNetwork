import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class ChampionsDataProcess:
    
    def process_data(self, winners):
        
        teams = []
        money = []
        for ((seller, buyer), (fee_cleaned, player)) in winners.items():
        
            if buyer not in teams:
                teams.append(buyer)
                if isinstance(fee_cleaned, float):
                    money.append(0.0)
                else:
                    money.append(float(fee_cleaned))
            else:
                index = teams.index(buyer)
                current_spent = money[index]
                
                if isinstance(fee_cleaned, float):
                    new_total = current_spent
                else:
                    new_total = float(fee_cleaned) + current_spent
                    
                money[index] = new_total

        data = dict(zip(teams, money))
        self.plotting_categorical(data)

    def plotting_categorical(self, data):
        names = list(data.keys())
        values = list(data.values())
        trophies = [6, 1, 3, 6, 5, 1, 2, 2, 3, 7, 14, 4, 2]
        
        fig, axs = plt.subplots(figsize=(18, 6), sharey=True)
        
        plt.bar(names, values, color ='green',
        width = 0.4)
        
        title = "Champions League Winner's - Transactions"
        axs.set_ylabel('Money Spent')
        axs.set_title(title)
        
        fig.autofmt_xdate()  # make space for and rotate the x-axis tick labels
        plt.savefig("../plots/CLW_Transactions.png", format="PNG")
        plt.show()
        
        
        fig2, axs2 = plt.subplots(figsize=(18, 6), sharey=True)
        axs2.set_ylabel('Trophies won')
        plt.bar(names, trophies, color='blue', width=0.4)
        fig2.autofmt_xdate()
        
        title = "Champions League Winner's - Trophies"
        axs2.set_ylabel('Trophies Won')
        axs2.set_title(title)
        
        plt.savefig("../plots/CLW_Trophies.png", format="PNG")
        plt.show()
        
        
            
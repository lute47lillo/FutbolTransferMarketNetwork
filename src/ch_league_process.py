import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


titles = ["Champions League Winner's - Trophies - Transactions", "Europa League Winner's - Trophies - Transactions",
          "Champions League Winner's - Trophies - Money Received", "Europa League Winner's - Trophies - Money Received"]

fig_names = ["../plots/CLW_Trophies.png", "../plots/EURW_Trophies.png",
             "../plots/CLW_Received.png", "../plots/EURW_Received.png"]


class ChampionsDataProcess:
    
    def process_data(self, winners, n, dinero):
        
        teams = []
        money = []
        
        if dinero:
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
        else:     
            for ((seller, buyer), (fee_cleaned, player)) in winners.items():
            
                if seller not in teams:
                    teams.append(seller)
                    if isinstance(fee_cleaned, float):
                        money.append(0.0)
                    else:
                        money.append(float(fee_cleaned))
                else:
                    index = teams.index(seller)
                    current_spent = money[index]
                    
                    if isinstance(fee_cleaned, float):
                        new_total = current_spent
                    else:
                        new_total = float(fee_cleaned) + current_spent
                        
                    money[index] = new_total

        print(teams)
        data = dict(zip(teams, money))
        #self.plotting_categorical(data, n, dinero)

    def plotting_categorical(self, data, n, dinero):
        names = list(data.keys())
        values = list(data.values())
        
        if n == 0:
            trophies = [6, 1, 3, 6, 5, 1, 2, 2, 3, 7, 14, 4, 2]
            if not dinero:
                n = 2
            
        else:
            trophies = [1,1,2,6,1,2,3,3,1,3,3,1,2,1,2,1,1,2,1]
            if not dinero:
                n = 3
        
    
            
            
        df = pd.DataFrame(list(zip(values, trophies)),
               columns =['Money', 'Trophies'])
        
        df = df.set_axis(names)

        # print(df) # Print list of the names
        fig = plt.figure() # Create matplotlib figure
        axs = fig.add_subplot(111) # Create matplotlib axes
        ax2 = axs.twinx() # Create another axes that shares the same x-axis as ax.

        width = 0.4

        df.Money.plot(kind='bar', color='green', ax=axs, width=width, position=1)
        df.Trophies.plot(kind='bar', color='blue', ax=ax2, width=width, position=0)

        axs.set_xlabel('Team')
        axs.set_ylabel('Money Received')
        ax2.set_ylabel('Trophies Won')
        
        fig.autofmt_xdate()
        
        title = titles[n]
        axs.set_title(title)
        
        fig_name = fig_names[n]
        plt.savefig(fig_name, format="PNG")
        plt.show()
        
        
            
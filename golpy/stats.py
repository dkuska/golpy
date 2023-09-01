import os
import numpy as np
import pandas as pd

class Statistics():
    def __init__(self) -> None:
        self.stats = []
        self.df_columns = ['Generation', "Deaths", "Births", "AliveRate", "DeadRate"]
    
    def collect_generation_stats(self, generation: int, old_field: np.ndarray, new_field: np.ndarray):
        deaths, births = self.get_changes_between_generations(old_field, new_field)
        alive_rate = self.get_alive_rate(new_field)
        dead_rate = 1 - alive_rate
        
        stats_item = [generation, deaths, births, alive_rate, dead_rate]
        self.stats.append(stats_item)
        pass
    
    def get_changes_between_generations(self, old_field: np.ndarray, new_field: np.ndarray):
        """ 
        Calculate the differences between two generations.
        
        Args:
            old_field - before updating
            new_filed - after updating
        """
        unchanged_entries = np.where(old_field == new_field)

        deaths = None
        births = None
        
        return deaths, births
    
    def get_alive_rate(self, field: np.ndarray) -> float:
        """
        
        Args:
            field - field at current generation
        """
        alive_rate = np.mean(field)
        return alive_rate
    
    def save_statistics(self, save_folder):
        os.makedirs(save_folder, exist_ok=True)
        save_path = save_folder + 'stats.csv'  # TODO: Add unique file-name such as time-stamp 
        
        
        stats_df = pd.DataFrame(self.stats, columns=self.df_columns)
        stats_df.to_csv(save_path)

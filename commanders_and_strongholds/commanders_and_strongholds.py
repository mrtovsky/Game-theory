import numpy as np 
import pandas as pd

from collections import Counter
from itertools import combinations_with_replacement, product
from math import factorial


class CommanderGame(object):
    """Commanders and strongholds game. 

    Every player starts with fixed number of troops. Their goal is to march 
    into as many strongholds as possible. Whenever competing troops meet each 
    other in the given strongholds the fight begins. Player with a larger number 
    of units seconded to the given stronghold wins and gains as many points as 
    opponent's defeated units plus one for the taken out stronghold. In case of 
    the same number of units in both armies, the result of the battle for this 
    concrete stronghold is 0 (nobody gains or loses anything). The final result 
    is the sum of the results from the battles for all strongholds. 
    
    Note: Matrix solver can be found under the link:
    https://www.math.ucla.edu/~tom/gamesolve.html     
    
    Parameters:
    ----------
    armies_sizes: list, length = 2
        Sizes of the armies of the competing players represented with integers.
    
    n_strongholds: int
        Number of strongholds.

    Attributes:
    -----------
    armies_orders_: list, length = 2
        All possible orders represented as the list of lists of disposition of
        the number of units to each stronghold. 

    game_matrix_: np.array, dim = 2
        2-dimensional array representing the game matrix.

    """
    def __init__(self, armies_sizes, n_strongholds):
        self.armies_sizes = armies_sizes
        self.n_strongholds = n_strongholds

    def fit_army_orders(self):
        """Creates all possible combinations of orders."""
        soldier_order = np.identity(self.n_strongholds, dtype=int)
        armies_orders = []

        for army_size in self.armies_sizes:
            combinations = combinations_with_replacement(
                soldier_order, army_size)
            army_orders = np.array(
                [sum(army_order) for army_order in combinations])
            armies_orders.append(army_orders)

        self.armies_orders_ = armies_orders

        return self
    
    def fit_game_matrix(self):
        """Creates game matrix."""
        try:
            getattr(self, 'armies_orders_')
        except AttributeError:
            raise RuntimeError('Could not find the "armies_orders_" attribute.'
                               '\nFitting is necessary before you do '
                               'the further calculations.')
        matrix_size = []
        for army_size in self.armies_sizes:
            param = (
                factorial(army_size + self.n_strongholds - 1) 
                / (factorial(self.n_strongholds - 1) * factorial(army_size))
            )
            matrix_size.append(int(param))

        matrix = np.zeros(matrix_size)
        for row, row_order in enumerate(self.armies_orders_[0]):
            for col, col_order in enumerate(self.armies_orders_[1]):
                matrix[row, col] = self._score_battles(row_order, col_order)

        self.game_matrix_ = matrix

        return self

    def show_submatrixes(self, orders_lists=None):
        """Shows game submatrixes with orders replaced with sets of orders 
        without distinction of strongholds.

        Parameters:
        -----------
        orders_lists: list, length = 2
            List of lists containing lists of divisions of units. If nothing 
            is specified by default it shows all of the submatrixes existing 
            in the given game.

        """
        try:
            getattr(self, 'game_matrix_')
        except AttributeError:
            raise RuntimeError('Could not find the "game_matrix_" attribute.\n'
                               'Fitting is necessary before you do '
                               'the further calculations.')
        if orders_lists is None:
            orders_lists = []
            for army_orders in self.armies_orders_:
                unique_orders = []
                for army_order in army_orders:
                    uniq = [
                        Counter(unique_order) for unique_order in unique_orders
                    ]
                    if Counter(army_order) not in uniq:
                        unique_orders.append(army_order)
                orders_lists.append(unique_orders)
        
        pattern_lists = []
        for idx, orders_list in enumerate(orders_lists):
            pattern_list = np.array(
                [Counter(army_order) for army_order in self.armies_orders_[idx]]
            )
            pattern_lists.append(pattern_list)
        
        for row_order, col_order in product(*orders_lists):
            row_cond = pattern_lists[0] == Counter(row_order)
            col_cond = pattern_lists[1] == Counter(col_order)
            smaller_game = self.game_matrix_[row_cond, :][:, col_cond]
            game_matrix = pd.DataFrame(
                smaller_game,
                index=[
                    str(order_list) 
                    for order_list 
                    in self.armies_orders_[0][row_cond]
                ],
                columns=[
                    str(order_list) 
                    for order_list 
                    in self.armies_orders_[1][col_cond]
                ] 
            )
            print(f'Orders for the first player: {tuple(row_order)}', 
                  f'\nOrders for the second player: {tuple(col_order)} \n', 
                  game_matrix, '\n')
    
    def _score_battles(self, first_order, second_order):
        """Returns outcome of the specified orders for two armies."""
        assert len(first_order) == len(second_order) == self.n_strongholds, \
            'Orders must be specified for all of the strongholds.'

        final_score = 0
        for first_regiment, second_regiment in zip(first_order, second_order):
            if first_regiment > second_regiment:
                final_score += second_regiment + 1
            elif first_regiment == second_regiment:
                continue
            else:
                final_score -= first_regiment + 1
        return final_score 


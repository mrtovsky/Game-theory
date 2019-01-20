from commanders_and_strongholds import CommanderGame 


def main():
    """Example game where the row player and column player has 4 and 3 units
    respectively. The number of strongholds is equal 3."""
    g = CommanderGame([4, 3], 3)
    g.fit_army_orders()
    g.fit_game_matrix()
    g.show_submatrixes([
        [[4, 0, 0]],
        [[2, 1, 0], [1, 1, 1]],
    ])

if __name__ == '__main__':
    main()
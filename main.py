# wykonanie programu
import game
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # określenie ile gier szkoleniowych trzeba przeprowadzić
    number_of_games_learning = 100000

    wins = []
    draws = []
    gra = game.Game()

    # uczenie się lub wczytanie danych - wybieramy jedno z nich poprzez zakomentowanie niepotrzebnego
    gra.read_ai()
    # gra.learn_ai(number_of_games_learning)

    # odkomentować jeśli chcemy zapisać wyniki uczenia się
    # gra.save_ai()

    # rozgrywanie gier z graczem losowym
    numb_of_games = 100000

    wins_x, draws_x, loses_x = gra.random_vs_ai_x(numb_of_games)
    wins.append(wins_x)
    draws.append(draws_x)
    wins_o, draws_o, loses_o = gra.random_vs_ai_o(numb_of_games)
    wins.append(wins_o)
    draws.append(draws_o)
    wins_r, draws_r, loses_r = gra.random_vs_random(numb_of_games)
    wins.append(wins_r)
    draws.append(draws_r)
    print(f'Wins_x = {wins_x}, Draws_x={draws_x}, Loses_x={loses_x}')
    print(f'Wins_o = {wins_o}, Draws_o={draws_o}, Loses_o={loses_o}')
    wins.append(numb_of_games - (wins_r + draws_r))
    draws.append(draws_r)

    # rysowanie wykresu
    labels = ['Gracz X', 'Gracz O', 'Losowy X', 'Losowy O']
    x = np.arange(len(labels))
    width = 0.45

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, wins, width, label='Zwyciestwa')
    rects2 = ax.bar(x + width / 2, draws, width, label='Remisy')
    ax.set_ylabel('Liczba gier')
    ax.set_title('Gry wygrane i zremisowane')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()
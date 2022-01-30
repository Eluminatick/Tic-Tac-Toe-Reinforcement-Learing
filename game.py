import numpy as np
import ast
import time
from board import Board

# Główna klasa gracza komputerowego
# Przetrzymuje 3 wartości: swój znak, znane stany, oraz tablicową reprezentację funkcji wartości akcji jako q_vals
# Dodatkowo, zdefiniowane są parametry  alfa gamma i epsilon - zgodnie ze parametrami algorytmu Q-learning i strategii
# epsilon zachłannych


class Ai_player:
    # Tu można zmienić parametry algorytmu
    def __init__(self, symbol, alpha=0.9, gamma=0.9, eps=0.5):
        self.symbol = symbol
        self.known_states = [('end',)]
        self.q_vals = {(('end',), -1): 0}

        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps

    # metoda wybiera najlepszy ruch na podstawie wartości funkcji akcji
    # porównuje wszystkie możliwości, a następnie wybiera jedną z nich w sposób losowy
    def choose_best_move(self, board):
        best_move = [board.available_actions[0]]
        best_move_qval = self.q_vals[(tuple(board.theBoard), best_move[0])]
        for move in board.available_actions:
            if self.q_vals[(tuple(board.theBoard), move)] > best_move_qval:
                best_move = [move]
            elif self.q_vals[(tuple(board.theBoard), move)] == best_move_qval:
                best_move.append(move)
        return np.random.choice(best_move)

    # wybiera ruch uczący się tzn. zgodny ze strategią epsilonowo zachłanną
    def choose_learning_move(self,board):
        if np.random.random() < self.eps:
            return np.random.choice(board.available_actions)
        else:
            return self.choose_best_move(board)

    # dodaje planszę jako nowy stan i tworzy odpowiednie pozycje w tabeli funkcji wartości akcji
    def add_state(self, board):
        self.known_states.append(tuple(board.theBoard))
        for move in board.available_actions:
            self.q_vals[(tuple(board.theBoard), move)] = 0

    # algorytm q-learning - jako argumenty przyjmuje 4 pozycje: stan który aktualizuje, ruch który wykonał w tym stanie
    # nagrodę oraz planszę po wykonaniu akcji
    def q_val_update(self, state_to_update: tuple, move: int, reward: int, new_board: Board):
        current_q_val = self.q_vals[(state_to_update, move)]
        best_move_for_new_state = self.choose_best_move(new_board)
        max_q_for_new_state = self.q_vals[(tuple(new_board.theBoard)), best_move_for_new_state]
        self.q_vals[(state_to_update, move)] = current_q_val + self.alpha*(reward +
                                                                self.gamma*max_q_for_new_state - current_q_val)
        return None


# klasa Gra, czy środowisko które łączy ze sobą klasę planszę oraz gracza Ai
class Game:
    def __init__(self):
        self.ai_playerX = Ai_player('X')
        self.ai_playerO = Ai_player('O')
        self.board = Board()

    # serce programu: funkcja która wykonuje określoną liczbę gier komputerowych w trakcie których gracze komputerowi
    # się uczą
    def learn_ai(self, rep):
        start_time = time.time()
        for loop in range(rep):
            # do śledzenia postępów nauki
            if loop % 10000 == 0:
                print('number of loop ',loop)
            self.board.clear_board()

            for turn in range(3**3):
                # Tura gracza X
                if not turn % 2:
                    # Pozanie nowego stanu jeśli nie był poznany wcześniej
                    if tuple(self.board.theBoard) not in self.ai_playerX.known_states:
                        self.ai_playerX.add_state(self.board)
                    # zapamiętanie wartości do aktualizacji i wykonanie ruchu
                    state_to_update_x = tuple(self.board.theBoard)
                    move_x = self.ai_playerX.choose_learning_move(self.board)
                    self.board.new_move(move_x, 'X')
                    # moment uczenia się gracza O - ma sens tylko dla gdy to jest już 2 ruch gracza X
                    if turn > 0:
                        # sprawdzenie zwycięstwa gracza X
                        if self.board.victory_check():
                            self.board.theBoard = ['end']
                            self.board.available_actions = [-1]
                            self.ai_playerO.q_val_update(state_to_update_o, move_o, -10, self.board)
                            self.ai_playerX.q_val_update(state_to_update_x, move_x, 10, self.board)
                            break
                        # sprawdzenie czy nie nastał remis
                        if turn == 8:
                            self.board.theBoard = ['end']
                            self.board.available_actions = [-1]
                            self.ai_playerO.q_val_update(state_to_update_o, move_o, 0, self.board)
                            self.ai_playerX.q_val_update(state_to_update_x, move_x, 0, self.board)
                            break
                        # jeżeli nic z powyższego nie nastąpiło to dodajemy nowy stan do znanych przez gracza O i uczymy
                        if tuple(self.board.theBoard) not in self.ai_playerO.known_states:
                            self.ai_playerO.add_state(self.board)

                        self.ai_playerO.q_val_update(state_to_update_o, move_o, 0, self.board)
                #Tura gracza O
                else:
                    if tuple(self.board.theBoard) not in self.ai_playerX.known_states:
                        self.ai_playerO.add_state(self.board)
                    state_to_update_o = tuple(self.board.theBoard)
                    move_o = self.ai_playerO.choose_learning_move(self.board)
                    self.board.new_move(move_o, 'O')
                    # Uczenie się gracza X
                    if self.board.victory_check():
                        self.board.theBoard = ['end']
                        self.board.available_actions = [-1]
                        self.ai_playerO.q_val_update(state_to_update_o, move_o, 10, self.board)
                        self.ai_playerX.q_val_update(state_to_update_x, move_x, -10, self.board)
                        break

                    if tuple(self.board.theBoard) not in self.ai_playerX.known_states:
                        self.ai_playerX.add_state(self.board)

                    self.ai_playerX.q_val_update(state_to_update_x, move_x, 0, self.board)
        print('learning finished')
        print("Uczenie zajelo --- %s seconds ---" % (time.time() - start_time))
    # zapisanie funkcji wartości akcji w pliku
    def save_ai(self):
        with open('ai_val_x', 'w') as plik:
            plik.write(repr(self.ai_playerX.q_vals))
        with open('ai_val_o', 'w') as plik:
            plik.write(repr(self.ai_playerO.q_vals))
    # wczytanie funkcji wartości akcji z pliku
    def read_ai(self):
        with open('ai_val_x', 'r') as plik:
            self.ai_playerX.q_vals = ast.literal_eval(plik.read())
        with open('ai_val_o', 'r') as plik:
            self.ai_playerO.q_vals = ast.literal_eval(plik.read())

    # gra komputerowego gracza X z przeciwnikiem losowym
    def random_vs_ai_x(self, n):
        wins = 0
        draws = 0
        loses = 0
        for i in range(n):
            self.board.clear_board()
            while True:
                self.board.new_move(self.ai_playerX.choose_best_move(self.board),'X')
                if self.board.victory_check():
                    wins += 1
                    break
                if not self.board.available_actions:
                    draws += 1
                    break
                self.board.new_move(np.random.choice(self.board.available_actions),'O')
                if self.board.victory_check():
                    loses += 1
                    break
        print(f"Wins:{wins}, draws:{draws}, loses:{loses}")
        return wins, draws, loses

    # gra komputerowego gracza O z przeciwnikiem losowym
    def random_vs_ai_o(self, n):
        wins = 0
        draws = 0
        loses = 0
        for i in range(n):
            self.board.clear_board()
            while True:
                self.board.new_move(np.random.choice(self.board.available_actions), 'X')
                if self.board.victory_check():
                    loses += 1
                    break
                if not self.board.available_actions:
                    draws += 1
                    break
                self.board.new_move(self.ai_playerO.choose_best_move(self.board), 'O')
                if self.board.victory_check():
                    wins += 1
                    break
        return wins, draws, loses

    # gra losowego przeciwnika z losowym
    def random_vs_random(self,n):
        wins = 0
        draws = 0
        loses = 0
        for i in range(n):
            self.board.clear_board()
            while True:
                self.board.new_move(np.random.choice(self.board.available_actions), 'X')
                if self.board.victory_check():
                    wins += 1
                    break
                if not self.board.available_actions:
                    draws += 1
                    break
                self.board.new_move(np.random.choice(self.board.available_actions), 'O')
                if self.board.victory_check():
                    loses += 1
                    break
        return wins, draws, loses
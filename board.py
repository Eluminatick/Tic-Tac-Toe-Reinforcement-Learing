# Klasa ta zawiera planszę oraz metody przydatne z nią związane
# Sama plansza to nic innego jak lista od 1 do 9, która posiada jednocześnie informację o pozostałych wolnych polach

class Board:
    def __init__(self):
        self.theBoard = [x+1 for x in range(3**2)]
        self.available_actions = [x+1 for x in range(3**2)]

# dodaje nowy ruch poprzez zastąpienie odpowiedniego miejsca na planszy symbolem oraz usunięciem danej akcji
    def new_move(self, place: int, char: str):
        self.theBoard[place - 1] = char
        self.available_actions.remove(place)

# metoda restartująca planszę
    def clear_board(self):
        self.theBoard = [x+1 for x in range(3 ** 2)]
        self.available_actions = [x+1 for x in range(3 ** 2)]
# metoda do wizualizacji planszy
    def print_board(self):
        for i in range(2):
            print('|'.join([str(x) for x in self.theBoard[i * 3:(i + 1) * 3]]))
            print('-+' * 2 + '-')
        print(r'|'.join([str(x) for x in self.theBoard[(3 - 1) * 3:3 ** 2]]))

# metoda zwracająca True w przypadku gdy któraś ze stron odniosła na planszy zwycięstwo
# ogólny pomysł: używając slicingu tworzymy listy zawierające wiersze/kolumny/przekątne a następnie konwertujemy je do
# zbiory by pozbyć się duplikatów. Gdy zbiór będzie jednoelementowy, oznacza to że został tylko symbol "X" lub "O" i
# nastąpiło zwycięstwo
    def victory_check(self):
        check = False
        for i in range(3):
            row = self.theBoard[i*3:(i+1)*3]

            if len(set(row)) == 1:
                check = True
                break

            column = {self.theBoard[x] for x in range(3**2) if x % 3 == i}
            if len(column) == 1:
                check = True
                break

        diag1 = {self.theBoard[x*3 + x] for x in range(3)}
        if len(diag1) == 1:
            check = True

        diag2 = {self.theBoard[((x+1)*3 - x - 1)] for x in range(3)}
        if len(diag2) == 1:
            check = True

        return check


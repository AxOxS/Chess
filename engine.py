#Failas, atsakingas už šachmatų partijos informacijos saugojimą ir manipuliavimą. Tuo pačiu atsakingas už leistinų ėjimų tikrinimą ir senų ėjimų saugojimą.

class GameState():
    def __init__(self):
        #Šachmatų lentos atvaizdavimas, naudojant du dimensinius masyvus. Kiekvienas elementas masyvuose atstoja šachmatų figūrą
        #arba tuščią langelį. kiekviena figūra pavaizduojama dviem simboliais, pirmas simbolis nurodo spalvą, o antras figūros tipą.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.whiteToMove = True
        self.moveLog = []
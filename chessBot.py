import random

#Figūrų vertė
rating = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

#Pozicijos vertės kiekvienai figūrai, kad atliekant ėjimus botas vertintų ne tik pagal figūrų vertę, bet ir savo figūrų poziciją
Queens = [[1, 1, 1, 3, 1, 1, 1, 1],
          [1, 2, 3, 3, 3, 1, 1, 1],
          [1, 4, 3, 3, 3, 4, 2, 1],
          [1, 2, 3, 3, 3, 2, 2, 1],
          [1, 2, 3, 3, 3, 2, 2, 1],
          [1, 4, 3, 3, 3, 4, 2, 1],
          [1, 1, 2, 3, 3, 1, 1, 1],
          [1, 1, 1, 3, 1, 1, 1, 1]]

Rooks = [[4, 3, 4, 4, 4, 4, 3, 4],
         [4, 4, 4, 4, 4, 4, 4, 4],
         [1, 1, 2, 3, 3, 2, 1, 1],
         [1, 2, 3, 4, 4, 3, 2, 1],
         [1, 2, 3, 4, 4, 3, 2, 1],
         [1, 1, 2, 3, 3, 2, 1, 1],
         [4, 4, 4, 4, 4, 4, 4, 4],
         [4, 3, 4, 4, 4, 4, 3, 4]]

Bishops = [[4, 3, 2, 1, 1, 2, 3, 4],
           [3, 4, 3, 2, 2, 3, 4, 3],
           [2, 3, 4, 3, 3, 4, 3, 2],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [2, 3, 4, 3, 3, 4, 3, 2],
           [3, 4, 3, 2, 2, 3, 4, 3],
           [4, 3, 2, 1, 1, 2, 3, 4]]

Knights = [[1, 1, 1, 1, 1, 1, 1, 1],
           [1, 2, 2, 2, 2, 2, 2, 1],
           [1, 2, 3, 3, 3, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 3, 3, 3, 2, 1],
           [1, 2, 2, 2, 2, 2, 2, 1],
           [1, 1, 1, 1, 1, 1, 1, 1]]

whitePawns = [[8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [5, 6, 6, 7, 7, 6, 6, 5],
              [2, 3, 3, 5, 5, 3, 3, 2],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 1, 1, 0, 0, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawns = [[0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 0, 0, 1, 1, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [2, 3, 3, 5, 5, 3, 3, 2],
              [5, 6, 6, 7, 7, 6, 6, 5],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8]]

#Kiekvienai vertei priskiriama jos figūra
pieceScores = {"Q": Queens, "R": Rooks, "B": Bishops, "N": Knights, "wP": whitePawns, "bP": blackPawns}

#Nustatomos ėjimų didžiausios ir mažiausios vertės + ėjimų gylis (Kiek ėjimų į priekį botas peržiūri)
checkMate = 1000
staleMate = 0
DEPTH = 1

#Funkcija, kuri randa random ėjimą iš galimų ėjimų (Testavimo tikslais/atsarginis naudojamas nerandant ėjimo/šiaip paįvairinti boto ėjimams)
def findRandMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

#Ši funkcija įvertina žaidimo stadiją ir grąžina rezultatą taškais
def scoreBoard(gs):
    #Patikrinam ar žaidimas baigėsi šachmatu ar lygiosiomis ir grąžiname atitinkama rezultatą pagal žaidėją
    if gs.checkMate:
        if gs.whiteToMove:
            return -checkMate
        else:
            return checkMate
    elif gs.staleMate:
        return staleMate

    #Praeinam pro visus langelius lentoje ir pažiūrim į kiekvieną langelį, kuris nėra tuščias ir nėra karaliaus langelis.
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--": #and square[1] in pieceScores:
                pieceScore = 0
                if square[1] != "K":
                    #Gaunam kiekvienos figūros įvertinimą pagal jos poziciją lentoje (aprašytos viršuje).
                    #Pawns aprašome atskirai, kadangi turime du skirtingus vertinimus pagal figūros spalvą.
                    if square[1] == "P":
                        pieceScore = pieceScores[square][row][col]
                    else:
                        pieceScore = pieceScores[square[1]][row][col]
                #Pagal figūros spalvą vertinimas bus arba + arba -, kad būtų skirtumas iš a žaidėjo perspektyvos į b žaidėją.
                if square[0] == 'w':
                    score += rating[square[1]] + pieceScore * 0.1
                elif square[0] == 'b':
                    score -= rating[square[1]] + pieceScore * 0.1

    return score

#Rndamas geriausias ėjimas, naudojant metodą su alfa beta pruning
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    #random.shuffle(validMoves)
    counter = 0
    #Šaukiama geriausio ėjimo paieška su alfa beta optimizacija (alfa - blogiausia baltam, beta - blogiausia juodam)
    #turnMultiplier 1 jeigu baltas, -1 jeigu juodas, kad algoritmas įvertintu poziciją iš esamo žaidėjo perspektyvos.
    findMoveMinMaxAlphaBeta(gs, validMoves, DEPTH, -checkMate, checkMate, 1 if gs.whiteToMove else -1)
    print(counter)
    #Grąžinamas geriausias ėjimas ir įdedamas į queue, multiprocesiškumui.
    returnQueue.put(nextMove)

#Funkcija, kuri ieško geriausio ėjimo naudojant Minimax algoritmą su Alpha-Beta optimizacija.
#Parametruose perduodam: gamestate, kuri atsakinga už žaidimo stadiją;
# galimus padaryti ėjimus; 
# Gylį, kokiame turi žiūrėti ėjimus botas; 
# Alpha ir Beta reikšmes, kurios padeda optimizuoti algoritmą;
# turnMultiplier, kuris nurodo ar šiuo metu žaidžia baltasis ar juodasis (1 arba -1).
def findMoveMinMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter #Globalūs kintamieji, kurie naudojami funkcijos viduje
    counter += 1
    #Patikrinam ar esame gilumo pabaigoje ir grąžiname ėjimo vertę atitinkamam žaidėjui. Rekursija baigiasi čia.
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #Pradinis maxScore = pats mažiausias įmanomas, kad būtų galima rasti didesnę vertę.
    maxScore = -checkMate
    #Einam per visus galimus ėjimus ir bandom juos atlikti. Ir gauname kitus ėjimus po atlikto ėjimo.
    #Rekursiškai iškviečiama ši funkcija su nauju gamestate ir naujais galimais ėjimais, pamažinus gylį (lipam iš rekursijos)
    #alfa beta reikšmės padaromos minusinėmis, nes rekursijoje keičiamos žaidėjų vietos.
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllValidMoves()
        score = -findMoveMinMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        #Jei ėjimas yra geresnis už prieš tai buvusį, tai jis tampa nauju geriausiu ėjimu.
        if score > maxScore:
            maxScore = score
            #Jeigu depth lygi max depth, tai įrašomas ėjimas į nextMove kintamąjį. Kad giliausiame lygmenyje būtų galima grąžinti geriausią ėjimą.
            if depth == DEPTH:
                nextMove = move
        #Po ėjimo paieškos - atstatome gamestate stadiją su undo metodu backtrackinimui.
        gs.undo()
        #Alfa beta optimizacija. Jeigu ėjimas yra geresnis už alfa reikšmę, tai alfa reikšmė tampa ėjimo reikšme.
        #Jei alpha geresnis už beta, tai nutraukiama paieška, nes vadinasi, kad priešo ėjimas bus geresnis ir paiešką galim terminuoti ankščiau.
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    #Gražinama geriausias galimas ėjimas pagal esamą poziciją ir patikrinus tam tikrame lygmenyje.
    return maxScore
from FreeBet import FreeBet
from Game import Game
from itertools import combinations, permutations
from GameResult import GameResult, TeamType


def main():
    free_bets = [
        FreeBet("FanDuel", 1000),
        FreeBet("BetMGM", 1000),
        FreeBet("Caesars", 1250),
        FreeBet("BetRivers", 500),
    ]

    games = [
        Game("Lions", "-135", "Vikings", "+115"),
        Game("Jaguars", "+160", "Titans", "-190")
    ]

    RunGame(games, free_bets)


def RunGame(games, free_bets):
    combos = list(permutations(free_bets))

    for combo in combos:
        RunCombo(games, combo)


def RunCombo(games, combo):
    print(
        f'{combo[0].name} places {combo[0].amount} on {games[0].team0} {games[0].odds0}')
    print(
        f'{combo[1].name} places {combo[1].amount} on {games[0].team0} {games[0].odds0}')
    print(
        f'{combo[2].name} places {combo[2].amount} on {games[0].team1} {games[0].odds1}')
    print(
        f'{combo[3].name} places {combo[3].amount} on {games[0].team1} {games[0].odds1}')

    print(
        f'\n{combo[0].name} places {combo[0].amount} on {games[1].team0} {games[1].odds0} (Free Bet)')
    print(
        f'{combo[1].name} places {combo[1].amount} on {games[1].team1} {games[1].odds1} (Free Bet)')
    print(
        f'{combo[2].name} places {combo[2].amount} on {games[1].team0} {games[1].odds0} (Free Bet)')
    print(
        f'{combo[3].name} places {combo[3].amount} on {games[1].team1} {games[1].odds1} (Free Bet)')

    netChange0, probability0 = evaluateBet(
        games, combo, GameResult.WIN, GameResult.WIN)

    netChange1, probability1 = evaluateBet(
        games, combo, GameResult.WIN, GameResult.LOSE)

    netChange2, probability2 = evaluateBet(
        games, combo, GameResult.LOSE, GameResult.WIN)

    netChange3, probability3 = evaluateBet(
        games, combo, GameResult.LOSE, GameResult.LOSE)

    expectedProfit = (netChange0 * probability0
                      + netChange1 * probability1
                      + netChange2 * probability2
                      + netChange3 * probability3)

    print(f'\n{round(netChange0, 2)} | {round(probability0 * 100, 2)}%')
    print(f'{round(netChange1, 2)} | {round(probability1 * 100, 2)}%')
    print(f'{round(netChange2, 2)} | {round(probability2 * 100, 2)}%')
    print(f'{round(netChange3, 2)} | {round(probability3 * 100, 2)}%')

    print(f'\nExpected Value: ${round(expectedProfit, 2)}')


def evaluateBet(games, combo, game1Result, game2Result):
    balance = 0

    oddsOfEvent = 1.00
    oddsOfEvent *= calculateTheoreticalOdds(
        games[0].odds0, games[0].odds1, game1Result)
    oddsOfEvent *= calculateTheoreticalOdds(
        games[1].odds0, games[1].odds1, game2Result)

    if (game1Result == GameResult.WIN):
        balance += calculateReturns(combo[0].amount,
                                    games[0].odds0, GameResult.WIN)
        balance += calculateReturns(combo[1].amount,
                                    games[0].odds0, GameResult.WIN)
        balance += calculateReturns(combo[2].amount,
                                    games[0].odds1, GameResult.LOSE)
        balance += calculateReturns(combo[3].amount,
                                    games[0].odds1, GameResult.LOSE)

        if (game2Result == GameResult.WIN):
            balance += calculateReturns(combo[2].amount,
                                        games[1].odds0, GameResult.WIN)
            balance += calculateReturns(combo[3].amount,
                                        games[1].odds1, GameResult.LOSE_FREEBET)

            y = 1
        else:
            balance += calculateReturns(combo[2].amount,
                                        games[1].odds0, GameResult.LOSE_FREEBET)
            balance += calculateReturns(combo[3].amount,
                                        games[1].odds1, GameResult.WIN)

    else:
        balance += calculateReturns(combo[0].amount,
                                    games[0].odds0, GameResult.LOSE)
        balance += calculateReturns(combo[1].amount,
                                    games[0].odds0, GameResult.LOSE)
        balance += calculateReturns(combo[2].amount,
                                    games[0].odds1, GameResult.WIN)
        balance += calculateReturns(combo[3].amount,
                                    games[0].odds1, GameResult.WIN)

        if (game2Result == GameResult.WIN):
            balance += calculateReturns(combo[0].amount,
                                        games[1].odds0, GameResult.WIN)
            balance += calculateReturns(combo[1].amount,
                                        games[1].odds1, GameResult.LOSE_FREEBET)
        else:
            balance += calculateReturns(combo[0].amount,
                                        games[1].odds0, GameResult.LOSE_FREEBET)
            balance += calculateReturns(combo[1].amount,
                                        games[1].odds1, GameResult.WIN)

    return balance, oddsOfEvent


def calculateTheoreticalOdds(odds0, odds1, gameResult):
    implied0 = calculateImpliedProbability(odds0)
    implied1 = calculateImpliedProbability(odds1)

    if gameResult == GameResult.WIN:
        return implied0 / (implied0 + implied1)
    else:
        return implied1 / (implied0 + implied1)


def calculateImpliedProbability(moneyline):
    betType = moneyline[0]
    oddsAmount = int(moneyline[1:])

    if betType == '-':
        return oddsAmount / (oddsAmount + 100)
    else:
        return 100 / (oddsAmount + 100)


def calculateReturns(betAmount, odds, gameResult):
    if gameResult == GameResult.LOSE:
        return -betAmount
    elif gameResult == GameResult.LOSE_FREEBET:
        return 0

    betType = odds[0]
    oddsAmount = int(odds[1:])

    if betType == '-':
        return 100 * betAmount / oddsAmount

    return betAmount * oddsAmount / 100


if __name__ == '__main__':
    main()

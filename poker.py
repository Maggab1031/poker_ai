import random
from enum import Enum
from hand import Hand_of_Cards, Hand_Value, Rank, Suit, Card

#todo: folding/losing conditions
#todo: make rounds run consecutively


face_cards = set()
for i in [Rank.JACK,Rank.QUEEN,Rank.KING,Rank.ACE,Rank.TEN]:
    face_cards.add(i)

class Round_Stage(Enum):
    SMALL_BLIND = 0
    BIG_BLIND = 1
    DEAL_TWO = 2
    FIRST_ROUND_BETTING = 3
    THE_FLOP = 4
    SECOND_ROUND_BETTING = 5
    THE_TURN =6
    THIRD_ROUND_BETTING = 7
    THE_RIVER = 8
    FOURTH_ROUND_BETTING = 9
    THE_SHOWDOWN = 10
    THE_END = 11


class Deck(object):

    def __init__(self):
        cards = []
        for x in list(Suit):
            for y in list(Rank):
                cards.append(Card(x, y))
        random.shuffle(cards)
        self.cards = cards


    def draw_card(self):
        return self.cards.pop()

class Player(object):
    def __init__(self,game,bank:int,name:str):
        self.hand = Hand_of_Cards(self)
        self.game = game
        self.bank = bank
        self.name = name

    def fold(self):
        self.game.get_current_round().remove_player(self)

    def add_to_hand(self,card):
        self.hand.add_card(card)
        print(self.name," Added",str(card))

    def get_info(self):
        print("Hello, ",self.name)
        print("Your hand is ",str(self.hand))
        print("Your bank is ",str(self.bank))
        if self.game.current_round.shared_card_strings()!=[]:
            print("The shared cards are: ",str(self.game.current_round.shared_card_strings()))
        print("Your highest value is ",str(self.hand.highest_value()[0]))
        print("Your current bet is ",str(self.game.current_round.debts[self.name]))

    def propose_bet(self,amount:int):
        decision = ""
        while not (decision=="bet" or decision=="fold" or decision=="raise"):
            self.get_info()
            decision = input("Bet, fold, or raise?  Answer bet/fold/raise.")
        if decision=="bet":
            if int(amount) > self.bank:
                print("You cannot bet. You must fold.")
                return self.propose_bet(amount)
            elif int(amount)==self.bank:
                print("ALL IN")
                return (True, int(amount), True)
            else:
                return (True,int(amount),False)
        elif decision=="fold":
            return (False,-1,False)
        elif decision=="raise":
            proposed = ""
            while not proposed.isdigit():
                proposed = input("How much would you like to bet?")
            while int(proposed)>self.bank:
                proposed = input("Please input an amount less than or equal to your bank: ")
            while int(proposed)<= amount:
                proposed = input("Please input a number greater than the previous bet")
            amount = int(proposed)
            if int(amount)==self.bank:
                print("ALL IN")
                return (True,int(amount),True)
            return (True,int(amount),False)

    def blind(self,amount):
        print(self.name," Blind of ",amount)
        if self.bank>=amount:
            self.bank -= amount
            return True
        else:
            return False

class Game(object):
    def __init__(self):
        self.players = []
        self.dealer_index = 0
        self.blind = 5

    def get_current_round(self):
        return self.current_round

    def get_current_stage(self):
        return self.current_round.stage

    def new_round(self):
        self.current_round = Poker_Round(self, self.players,self.dealer_index,self.blind)
        if self.dealer_index>=(len(self.players)-1):
            self.dealer_index = 0
        else:
            self.dealer_index +=1
        return self.current_round

    def add_player(self,player):
        self.players.append(player)

class Poker_Round(object):

    def __init__(self, game,players,dealer_index,small_blind):
        self.dealer_index = dealer_index
        self.small_blind = small_blind
        self.players = players
        if self.dealer_index ==len(self.players)-1:
            self.smbi = 0
            self.bbi = 1
        elif self.dealer_index==len(self.players)-2:
            self.smbi = self.dealer_index+1
            self.bbi = 0
        else:
            self.smbi = self.dealer_index + 1
            self.bbi = self.dealer_index + 2
        self.game = game
        self.deck = Deck()
        self.pot = 0
        self.limit = False
        self.stage = Round_Stage.SMALL_BLIND
        self.shared_cards = set()
        self.paid = {}
        self.debts = {}
        for i in range(len(self.players)):
            self.paid[self.players[i].name]=0
            if i == self.smbi:
                self.debts[self.players[i].name]=self.small_blind
            elif i == self.bbi:
                self.debts[self.players[i].name]=0
            else:
                self.debts[self.players[i].name] = self.small_blind * 2

    def remove_player(self,player):
        if player in self.players:
            self.players.remove(player)

    def deal_cards(self):
        for i in range(self.smbi,len(self.players)):
            self.players[i].add_to_hand(self.deck.draw_card())
        for i in range(0,self.smbi):
            self.players[i].add_to_hand(self.deck.draw_card())

    def total_hand(self,player):
        hand:Hand_of_Cards = player.hand.copy()
        for card in self.shared_cards:
            hand.add_card(card)
        return hand

    def end_round(self):
        print("ended")
        num_pl = len(self.players)
        for player in self.players:
            player.bank += int(self.pot/num_pl)


    def round_of_bets(self,index=None,players=None):
        #set the starting index to the player next in rotation after the given index
        if index==None:
            index = self.dealer_index
        if index==len(self.players)-1:
            index = 0
        if players == None:
            # make a list starting with the starting index
            players=self.players
        new_players = []
        for i in range(index, len(players)):
            new_players.append(players[i])
        for i in range(0, index):
            new_players.append(players[i])
        #loop through the list
        for player in new_players:
            amount = self.debts[player.name]
            # query the debt
            response = player.propose_bet(amount)
            # if the player did not fold
            if response[0]:
                # add the amount bet to the pot
                self.pot += response[1]
                # add how much they paid to the paid dict
                self.paid[str(player.name)] += response[1]
                # if the player went all in, set boolean up
                if response[2]:
                    self.limit = True
                # the amount each other player must pay is the amount this player raised
                to_pay = (response[1] - self.debts[str(player.name)])
                # add the raise to each debt
                for player_str in self.debts.keys():
                    self.debts[player_str] += to_pay
                # the player has finished their debts
                self.debts[str(player.name)] = 0
            else:
                #if the player folds, remove them from all dicts and the player list
                del self.debts[str(player.name)]
                del self.paid[str(player.name)]
                self.players.remove(player)
                # if one player remains, the round is over
                if len(self.players)==1:
                    self.end_round()
                    break
        print("loop beginning")
        loop = True
        for i in self.debts.keys():
            loop = self.debts[i]==0 and loop
        if not loop:
            print("recursion")
            if index == len(new_players)-1:
                index = 0
            else:
                index +=1
            self.round_of_bets(index=index,players=new_players)
        else:
            for i in self.paid.keys():
                self.paid[i]=0

    def shared_card_strings(self):
        shared = []
        for card in self.shared_cards:
            shared.append(str(card))
        return shared

    def shared_card_objects(self):
        return self.shared_cards

    def run_round(self):
        self.stage = Round_Stage.SMALL_BLIND
        self.players[self.smbi].blind(self.small_blind)
        self.stage = Round_Stage.BIG_BLIND
        self.players[self.bbi].blind(self.small_blind*2)
        self.stage = Round_Stage.DEAL_TWO
        self.deal_cards()
        self.deal_cards()
        #first round of betting
        self.stage =Round_Stage.FIRST_ROUND_BETTING
        self.round_of_bets(index=self.bbi)
        #THE FLOP
        self.stage = Round_Stage.THE_FLOP
        self.shared_cards.add(self.deck.draw_card())
        self.shared_cards.add(self.deck.draw_card())
        self.shared_cards.add(self.deck.draw_card())
        #second round of betting
        self.stage = Round_Stage.SECOND_ROUND_BETTING
        self.round_of_bets()
        #the turn
        self.stage = Round_Stage.THE_TURN
        self.shared_cards.add(self.deck.draw_card())
        #third round of betting
        self.stage = Round_Stage.THIRD_ROUND_BETTING
        self.round_of_bets()
        #the river
        self.stage = Round_Stage.THE_RIVER
        self.shared_cards.add(self.deck.draw_card())
        #fourth round of betting
        self.stage = Round_Stage.FOURTH_ROUND_BETTING
        self.round_of_bets()
        #the showdown
        self.stage = Round_Stage.THE_SHOWDOWN
        #the end
        self.stage = Round_Stage.THE_END
        self.end_round()
        return None

def main():
    game = Game()
    for i in range(0,5):
        game.add_player(Player(game,bank=500,name=str(i)))
    round: Poker_Round= game.new_round()
    round.run_round()



if __name__ == '__main__':
    main()
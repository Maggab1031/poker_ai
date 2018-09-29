import random
from enum import Enum
from hand import Hand_of_Cards

#todo: folding/losing conditions
#todo: make rounds run consecutively



class Hand_Value(Enum):
    ROYAL_FLUSH =9
    STRAIGHT_FLUSH=8
    FOUR_OF_A_KIND=7
    FULL_HOUSE=6
    FLUSH=5
    STRAIGHT=4
    THREE_OF_A_KIND=3
    TWO_PAIR=2
    PAIR =1
    NONE =0

class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

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

class Suit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

class Card(object):

    def __init__(self, suit:Suit, rank:Rank):
        self.suit = suit
        self.rank = rank

    def get_rank(self):
        return self.rank

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def same_suit(self,card):
        return card.get_suit()==self.suit

    def same_rank(self,card):
        return card.get_rank()==self.rank

    def get_string(self):
        return self.rank.name+" of "+self.suit.name

    def __str__(self):
        return self.rank.name + " of " + self.suit.name

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
    def __init__(self,game,bank,name):
        self.hand = Hand_of_Cards(self)
        self.game = game
        self.bank = bank
        self.name = name

    def get_hand(self):
        return self.hand

    def fold(self):
        self.game.get_current_round().remove_player(self)

    def add_to_hand(self,card):
        self.hand.add_card(card)
        print(self.name," Added",str(card))

    def get_info(self):
        print("Your hand is ",str(self.hand))
        print("Your bank is ",str(self.bank))



    def propose_bet(self,amount:int,round):
        decision = ""
        while not (decision=="bet" or decision=="fold" or decision=="raise"):
            decision = input("Hello, "+self.name+" Bet "+str(amount)+", Fold, or raise? You hand is "+str(round.total_hand(self))+" Answer bet/fold/raise.")
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
        self.current_round = Poker_Round(self, self.players,self.dealer_index, self.blind)

    def get_current_round(self):
        return self.current_round

    def new_round(self):
        if self.dealer_index>=(len(self.players)-1):
            self.dealer_index = 0
        else:
            self.dealer_index +=1
        self.current_round = Poker_Round(self, self.players,self.dealer_index,self.blind)
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

    def remove_player(self,player):
        if player in self.players: self.players.remove(player)

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
        num_pl = len(self.players)
        for player in self.players:
            player.bank += int(self.pot/num_pl)

    def round_of_bets(self,amount=0,index=None,dicts=None,players=None):
        #set the starting index to the player next in rotation after the given index
        if index==None:
            index = self.dealer_index
        if index!=len(self.players)-1:
            index = index +1
        else:
            index = 0
        #initialize the dicts for tracking debts and paid
        if dicts==None:
            debts = {}
            paid = {}
            debt = amount
            for player in self.players:
                debts[str(player.name)] = debt
                paid[str(player.name)] = 0
        else:
            debts = dicts[0]
            paid = dicts[1]
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
            amount = debts[player.name]
            # query the debt
            response = player.propose_bet(amount, self)
            # if the player did not fold
            if response[0]:
                # add the amount bet to the pot
                self.pot += response[1]
                # add how much they paid to the paid dict
                paid[str(player.name)] += response[1]
                # if the player went all in, set boolean up
                if response[2]:
                    self.limit = True
                # the amount each other player must pay is the amount this player raised
                to_pay = (response[1] - debts[str(player.name)])
                # add the raise to each debt
                for player_str in debts.keys():
                    debts[player_str] += to_pay
                # the player has finished their debts
                debts[str(player.name)] = 0
                print(debts)
                print(paid)
            else:
                #if the player folds, remove them from all dicts and the player list
                del debts[str(player.name)]
                del paid[str(player.name)]
                self.players.remove(player)
                # if one player remains, the round is over
                if len(self.players)==1:
                    self.end_round()
                    break
        loop = True
        for i in debts.keys():
            loop = debts[i]==0 and loop
        if not loop:
            if index == len(new_players)-1:
                index = 0
            else:
                index +=1
            self.round_of_bets(index=index,dicts=(debts,paid),players=new_players)

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
        self.round_of_bets(amount=self.small_blind*2,index=self.bbi)
        #THE FLOP
        self.stage = Round_Stage.THE_FLOP
        self.shared_cards.add(self.deck.draw_card())
        self.shared_cards.add(self.deck.draw_card())
        self.shared_cards.add(self.deck.draw_card())
        print("The shared cards are: ",self.shared_card_strings())
        #second round of betting
        self.stage = Round_Stage.SECOND_ROUND_BETTING
        self.round_of_bets()
        #the turn
        self.stage = Round_Stage.THE_TURN
        self.shared_cards.add(self.deck.draw_card())
        print("The shared cards are: ", self.shared_card_strings())
        #third round of betting
        self.stage = Round_Stage.THIRD_ROUND_BETTING
        self.round_of_bets()
        #the river
        self.stage = Round_Stage.THE_RIVER
        self.shared_cards.add(self.deck.draw_card())
        print("The shared cards are: ", self.shared_card_strings())
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
    deck = Deck()
    hand = Hand_of_Cards()
    for i in range(5):
        hand.add_card(deck.draw_card())
    print(hash(hand))
    """
    game = Game()
    for i in range(0,5):
        game.add_player(Player(game,bank=500,name=str(i)))
    round: Poker_Round= game.get_current_round()
    round.run_round()
    """


if __name__ == '__main__':
    main()
import random
from enum import Enum


#todo: make it so the round doesn't end until all debts are paid
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

class Hand_of_Cards(object):
    def __init__(self,player=None,cards=None):
        if cards==None:
            cards = set()
            self.cards = cards
            self.player = player
        else:
            self.cards = cards
            self.player = player
            self.value = self.highest_value()

    def __str__(self):
        a = ""
        for card in self.cards:
            a += str(card)+", "
        return a

    def better_hand_than(self,other_hand):
        if self.highest_value()[0].value > other_hand.highest_value()[0].value:
            return True
        elif self.highest_value()[0].value < other_hand.highest_value()[0].value:
            return False
        else:
            print("tie")
            return True

    def copy(self):
        return Hand_of_Cards(self.player,self.cards)

    def add_card(self,card):
        self.cards.add(card)

    def get_cards(self):
        return self.cards

    def to_list_of_strings(self):
        strings = []
        for x in self.cards:
            strings.append(x.get_string())
        return strings

    def is_pair(self):
        rank_dict = {}
        for card in self.cards:
            if str(card.get_rank()) not in rank_dict:
                rank_dict[str(card.get_rank())] = 0
            rank_dict[str(card.get_rank())] = rank_dict[str(card.get_rank())] + 1
            if rank_dict[str(card.get_rank())] > 1:
                return True
        return False

    def is_three_of_a_kind(self):
        rank_dict = {}
        for card in self.cards:
            if str(card.get_rank()) not in rank_dict:
                rank_dict[str(card.get_rank())] = 0
            rank_dict[str(card.get_rank())] = rank_dict[str(card.get_rank())] +1
            if rank_dict[str(card.get_rank())]>2:
                return True
        return False

    def is_four_of_a_kind(self):
        rank_dict = {}
        for card in self.cards:
            if str(card.get_rank()) not in rank_dict:
                rank_dict[str(card.get_rank())] = 0
            rank_dict[str(card.get_rank())] = rank_dict[str(card.get_rank())] + 1
            if rank_dict[str(card.get_rank())] > 3:
                return True
        return False

    def is_two_pair(self):
        rank_dict = {}
        for card in self.cards:
            if str(card.get_rank()) not in rank_dict:
                rank_dict[str(card.get_rank())] = 0
                rank_dict[str(card.get_rank())] = rank_dict[str(card.get_rank())] + 1
        total = 0
        for rank in rank_dict:
            if rank_dict[rank]>1:
                total += 1
        return total>1

    def is_straight(self):
        cards = self.cards
        ranks = []
        for card in cards:
            ranks.append(card.get_rank().value)
        ranks.sort(reverse=True)
        if (len(self.cards)==5):
            i=len(ranks)-1
            while i > 1:
                if ranks[i-1]!=ranks[i]-1:
                    return False
                else:
                    i-=1
            return True

    def is_flush(self):
        list= []
        for x in self.cards:
            list.append(x.get_suit())
        if list.count(list[0])==5:
            return True
        else:
            return False

    def is_full_house(self):
        rank_dict = {}
        for card in self.cards:
            if str(card.get_rank()) not in rank_dict.keys():
                rank_dict[str(card.get_rank())] = 0
            rank_dict[str(card.get_rank())] = rank_dict[str(card.get_rank())] + 1
        for rank in rank_dict:
            if rank_dict[rank]==2:
                for rank in rank_dict:
                    if rank_dict[rank]==3:
                        return True
            if rank_dict[rank]==3:
                for rank in rank_dict:
                    if rank_dict[rank] == 2:
                        return True
        return False

    def is_straight_flush(self):
        return self.is_flush() and self.is_straight()

    def is_royal_flush(self):
        suits ={}
        for card in self.cards:
            if str(card.get_suit()) not in suits.keys():
                suits[str(card.get_suit())] = 0
            suits[str(card.get_suit())] = suits[str(card.get_suit())] +1
            if card.rank not in face_cards:
                return False
        if len(suits.keys())==1 and len(self.cards)==5:
            return True

    def highest_value(self):
        if self.is_royal_flush():
            return (Hand_Value.ROYAL_FLUSH,self.cards)
        elif self.is_straight_flush():
            return (Hand_Value.STRAIGHT_FLUSH,self.cards)
        elif self.is_four_of_a_kind():
            return (Hand_Value.FOUR_OF_A_KIND,self.cards)
        elif self.is_full_house():
            return (Hand_Value.FULL_HOUSE,self.cards)
        elif self.is_flush():
            return (Hand_Value.FLUSH,self.cards)
        elif self.is_straight():
            return (Hand_Value.STRAIGHT,self.cards)
        elif self.is_three_of_a_kind():
            return (Hand_Value.THREE_OF_A_KIND,self.cards)
        elif self.is_two_pair():
            return (Hand_Value.TWO_PAIR,self.cards)
        elif self.is_pair():
            return (Hand_Value.PAIR,self.cards)
        else:
            return (Hand_Value.NONE,self.cards)

    def reveal_to_player(self):
        self.player.see_hand()

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
            new_players = []
            for i in range(index, len(self.players)):
                new_players.append(self.players[i])
            for i in range(0, index):
                new_players.append(self.players[i])
        else:
            new_players = self.players
        #loop through the list
        for player in new_players:
            #if a player has gone all in, they cannot bet any more
            if self.limit:
                amount = 0
            else:
                # otherwise the player must play the debt that they owe
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
            self.round_of_bets(dicts=(debts,paid))

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
    game = Game()
    for i in range(0,5):
        game.add_player(Player(game,bank=500,name=str(i)))
    round: Poker_Round= game.get_current_round()
    round.run_round()

if __name__ == '__main__':
    main()
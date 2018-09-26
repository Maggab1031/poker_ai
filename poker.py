import random
import numpy
from enum import Enum


#todo: betting - make it so after a raise happens the players that bet beforehand have a chance to call.
#todo: make it so the game ends exactly when there is one player left.
#todo: implement blinds closer to irl game



def all_permutations(list,size):
    if len(list)==size:
        return [list]
    else:
        my_list = []
        for i in range(len(list)):
            combos = all_permutations(list[i + 1:], size - 1)
            for j in combos:
                sublist = [list[i]]+j
                my_list.append(sublist)
        return my_list

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



    def add_card(self,card):
        self.cards.add(card)
        #self.value = self.highest_value()

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
            return Hand_Value.ROYAL_FLUSH
        elif self.is_straight_flush():
            return Hand_Value.STRAIGHT_FLUSH
        elif self.is_four_of_a_kind():
            return Hand_Value.FOUR_OF_A_KIND
        elif self.is_full_house():
            return Hand_Value.FULL_HOUSE
        elif self.is_flush():
            return Hand_Value.FLUSH
        elif self.is_straight():
            return Hand_Value.STRAIGHT
        elif self.is_three_of_a_kind():
            return Hand_Value.THREE_OF_A_KIND
        elif self.is_two_pair():
            return Hand_Value.TWO_PAIR
        elif self.is_pair():
            return Hand_Value.PAIR
        else:
            return Hand_Value.NONE

    def reveal_to_player(self):
        self.player.see_hand()

def main():
    dict = {}
    for i in range(0,100000):
        deck = Deck()
        hand = Hand_of_Cards()
        for i in range(0,5):
            hand.add_card(deck.draw_card())
        val = (hand.highest_value())
        if val not in dict.keys():
            dict[val]=0
        dict[val] +=1
    for key in dict.keys():
        print(key," ",str((100*dict[key])/10000))

if __name__ == '__main__':
    main()
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

    def __init__(self,player=None,cards=set()):
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
        ranks = set()
        for card in self.cards:
            ranks.add(card.get_rank())
        return len(ranks)!=len(self.cards)

    def is_three_of_a_kind(self):
        list = []
        for x in self.cards:
            list.append(x.get_rank())
        for x in list:
            if list.count(x) >= 3:
                return True
        return False

    def is_four_of_a_kind(self):
        list = []
        for x in self.cards:
            list.append(x.get_rank())
        for x in list:
            if list.count(x) >= 4:
                return True
        return False

    def is_two_pair(self):
        list = []
        for x in self.cards:
            list.append(x.get_rank())
        sublist = []
        i=0
        while(i<len(list)):
            if list[i] in sublist:
                list.remove(list[i])
                break
            else:
                sublist.append(list[i])
                list.remove(list[i])
        for x in list:
            if list.count(x)>=2:
                return True
        return False

    def is_straight(self):
        list = []
        for x in self.cards:
            list.append(x.get_rank())
        list.sort(key=None, reverse=True)
        for x in range(0,len(list)-1):
            if list[x+1] != list[x]-1:
                return False
        return True and len(self.cards)==5

    def is_flush(self):
        list= []
        for x in self.cards:
            list.append(x.get_suit())
        if len(list)!=5:
            return False
        if list.count(list[0])==5:
            return True
        else:
            return False

    def is_full_house(self):
        list = []
        for x in self.cards:
            list.append(x.get_rank())
        sublist = []
        i = 0
        while (i < len(list)):
            if list[i] in sublist:
                list.remove(list[i])
                break
            else:
                sublist.append(list[i])
                list.remove(list[i])
        for x in list:
            if list.count(x) >= 2 and sublist[0] in list:
                return True
        return False

    def is_straight_flush(self):
        return self.is_flush() and self.is_straight()

    def is_royal_flush(self):
        list = []
        for x in self.cards:
            list.append(x.get_rank())
        list.sort()
        list.sort(key=None, reverse=True)
        if list == [13,12,11,10,1]:
            return True and self.is_flush()
        else:
            return False

    def highest_value(self):
        if self.is_royal_flush():
            return 0
        elif self.is_straight_flush():
            return 1
        elif self.is_four_of_a_kind():
            return 2
        elif self.is_full_house():
            return 3
        elif self.is_flush():
            return 4
        elif self.is_straight():
            return 5
        elif self.is_three_of_a_kind():
            return 6
        elif self.is_two_pair():
            return 7
        elif self.is_pair():
            return 8
        else:
            return 9

    def reveal_to_player(self):
        self.player.see_hand()

def main():
    hand = Hand_of_Cards()
    hand.add_card(Card(Suit.CLUBS,Rank.ACE))
    hand.add_card(Card(Suit.DIAMONDS,Rank.ACE))
    hand.add_card(Card(Suit.HEARTS,Rank.ACE))
    hand.add_card(Card(Suit.SPADES,Rank.ACE))
    print(hand.is_pair())

if __name__ == '__main__':
    main()
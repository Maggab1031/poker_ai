from enum import Enum

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

class Hand_of_Cards(object):
    def __init__(self,player=None,cards=None):
        if cards==None:
            cards = frozenset()
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

    def __add__(self, other: 'Hand_of_Cards') -> 'Hand_of_Cards':
        return Hand_of_Cards(cards = (self.cards + other.cards))

    def __sub__(self, other: 'Hand_of_Cards') -> 'Hand_of_Cards':
        return Hand_of_Cards(cards = (self.cards - other.cards))

    def __ge__(self, other: 'Hand_of_Cards') -> bool:
        if self.highest_value()[0].value != other.highest_value()[0].value:
            return self.highest_value()[0].value>other.highest_value()[0].value
        elif self.highest_rank()[0]!=other.highest_rank()[0]:
            return self.highest_rank()[0]>other.highest_rank()[0]
        else:
            return self.highest_rank()[1].suit.value>other.highest_rank()[1].suit.value


    def __lt__(self, other: 'Hand_of_Cards') -> bool:
        if self.highest_value()[0].value!=other.highest_value()[0].value:
            return self.highest_value()[0].value<other.highest_value()[0].value
        elif self.highest_rank()[0]!=other.highest_rank()[0]:
            return self.highest_rank()[0]<other.highest_rank()[0]
        else:
            return self.highest_rank()[1].suit.value<other.highest_rank()[1].suit.value

    def __eq__(self, other) -> bool:
        return self.cards==other.cards

    def __hash__(self) -> int:
        return hash((self.cards,self.player))



    def highest_rank(self):
        val = 0
        the_card = None
        for card in self.cards:
            if card.get_rank().value>val:
                val = card.get_rank().value
                the_card = card
        return val,the_card


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
        new = frozenset([card])
        self.cards = self.cards.union(new)

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
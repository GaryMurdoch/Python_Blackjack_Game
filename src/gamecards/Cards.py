import os, copy, random

######################################################################

def stop():
    _ = input("\n\n Press <Enter> to quit ")
    print()

def pause():
    _ = input(" Press <Enter> to continue ")

def clear(msg=""):
    if not msg == "":
        _ = input("\u0020{}\u0020".format(msg))
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

######################################################################

random.seed()

_all_suits = {
      "spades": "\u2660",
    "diamonds": "\u2666",    
       "clubs": "\u2663",
      "hearts": "\u2665"
}
    
_all_values = {
      "ace": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
       "10": 10,
     "jack": 10,
    "queen": 10,
     "king": 10
}

######################################################################

class Card:
    def __init__(self, value_in, suit_in, hidden_in=False, values_dict_in = _all_values, suits_dict_in = _all_suits):
        self.value = value_in.strip().lower()
        self.suit = suit_in.strip().lower()        
        self.hidden = hidden_in
        self.values_dict = values_dict_in
        self.suits_dict = suits_dict_in
        self._protected_points = self.values_dict[self.value]

    @property
    def name(self):
        return (self.value.capitalize() + " of " + self.suit.capitalize())

    @property
    def symbol(self):
        value_length = 2 if self.value=="10" else 1 
        return (self.value[0:value_length].capitalize() + self.suits_dict[self.suit])

    @property
    def points(self):
        return self._protected_points
    
    def unhide(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def show(self):
        multi_show(self)

######################################################################

class Hand:
    def __init__(self, cards_in=[]):
        self.cards = cards_in if type(cards_in)==list else [cards_in]

    @property
    def count(self):
        return len(self.cards)
    
    @property
    def points(self):
        return sum(_card.points for _card in self.cards)

    @property
    def points_showing(self):
        _showing = 0
        for _card in self.cards:
            _known = _card.points if not _card.hidden else 0
            _showing += _known
        return _showing

    def add(self, cards_in):
        _add_list = cards_in if type(cards_in)==list else [cards_in]
        self.cards += _add_list

    def discard(self, cards_in):
        _in_list = cards_in if type(cards_in)==list else [cards_in]
        _remove_list = [_card for _card in _in_list if _card in self.cards]
        for _card in _remove_list:
            self.cards.remove(_card)

    def show(self):
        multi_show(self.cards, 5)

    def showall(self):
        _cards_copy = copy.deepcopy(self.cards)
        for _card in _cards_copy:
            _card.unhide()
        multi_show(_cards_copy, 5)
        del _cards_copy

    def tostring(self):
        _result = ""
        for _i in range(1, len(self.cards)):
            _result += (self.cards[_i-1].symbol + 3*"\u0020")
        _result += self.cards[len(self.cards)-1].symbol
        return _result
		
    def report(self):
        print(" Number of cards in hand: " + str(self.count))
        i=0
        for _card in self.cards:
            i += 1
            if not _card.hidden:
                print("\t{}. {}, {}, {} points"
                      .format(i, _card.name, _card.symbol, _card.points))
            else:
                print("\t{}. a face-down card... [it's the {}, {}, {} pts]"
                      .format(i, _card.name, _card.symbol, _card.points))
        print(" Total points showing: " + str(self.points_showing))
        print(" Total points including face-down: " + str(self.points))

######################################################################

class Deck:
    def __init__(self, values_dict_in, suits_dict_in):
        self.values_dict = values_dict_in
        self.suits_dict = suits_dict_in
        self.hidden = True
        self.cards = None
        self.reset()

    def reset(self):
        _cards=[]
        
        _suits = (list(self.suits_dict.keys()))[0:2]
        _values = list(self.values_dict.keys())
        _hidden = [self.hidden]*len(_values)
        for _i in range(0, len(_suits)):
            for _j in range(0, len(_values)):
                _new = Card(_values[_j], _suits[_i], _hidden[_j], self.values_dict, self.suits_dict)
                _cards.append(_new)

        _suits = (list(self.suits_dict.keys()))[2:4]
        _values.reverse()
        for _i in range(0, len(_suits)):
            for _j in range(0, len(_values)):
                _new = Card(_values[_j], _suits[_i], _hidden[_j], self.values_dict, self.suits_dict)
                _cards.append(_new)

        self.cards = _cards

    @property
    def count(self):
        return len(self.cards)

    def remove(self, cards_in):
        _in_list = cards_in if type(cards_in)==list else [cards_in]
        _remove_list = [_card for _card in _in_list if _card in self.cards]
        for _card in _remove_list:
            self.cards.remove(_card)

    def take(self, positions_in):
        _positions_list = positions_in if type(positions_in)==list else [positions_in]
        _take_list = [self.cards[num] for num in _positions_list if 0<=num and num<len(self.cards)]
        for _card in _take_list:
            self.cards.remove(_card)
        return _take_list

    def deal(self, number=1, position="top"):
        if number < 1:
            return None
        elif number > len(self.cards):
            _number = len(self.cards)
        else:
            _number = number
        _position = "bottom" if position.lower()=="bottom" else "top"
        if _position == "top":
            _card_indices = list(range(0, _number, 1))
        elif _position == "bottom":
            _card_indices = list(range(len(self.cards)-1, len(self.cards)-1-_number, -1))
        return self.take(_card_indices)

    def shuffle(self):
        random.shuffle(self.cards)

    def replace(self, cards_in, position="bottom"):
        _in_list = cards_in if type(cards_in)==list else [cards_in]
        _add_list = [_card for _card in _in_list if _card not in self.cards]
        try:
            _index = int(position)
        except:
            _index = 0 if position.lower()=="top" else len(self.cards)
        for _card in _add_list:
            self.cards.insert(_index, _card)
            _index += 1

    def show(self):
        _cards_copy = copy.deepcopy(self.cards)
        for _card in _cards_copy:
            _card.unhide()
        multi_show(_cards_copy, 6)
        del _cards_copy
        
    def show_insuits(self):
        _cards_copy = copy.deepcopy(self.cards)
        for _card in _cards_copy:
            _card.unhide()
        _insuit = dict()
        for _suit in self.suits_dict.keys():
            _insuit[_suit] = []
        for _card in _cards_copy:
            _insuit[_card.suit].append(_card)
        for _suit in _insuit.keys():
            print("\n" + 3*"\u0020" + _suit.upper() + ":", end="")
            multi_show(_insuit[_suit], 7)
        del _cards_copy, _insuit

    def tostring(self):
        _result = ""
        for _i in range(1, len(self.cards)+1):
            _result += ("\u0020" + self.cards[_i-1].symbol + 2*"\u0020")
            if _i % 13 == 0 or _i == len(self.cards): _result += "\n"
        return _result

    def tostring_insuits(self):
        _insuit = dict()
        for _suit in self.suits_dict.keys():
            _insuit[_suit] = []
        for _card in self.cards:
            _insuit[_card.suit].append(_card)
        _result = ""
        for _suit in _insuit.keys():
            for _i in range(1, len(_insuit[_suit])+1):
                _result += ("\u0020" + (_insuit[_suit])[_i-1].symbol + 2*"\u0020")
                if _i % 13 == 0 or _i == len(_insuit[_suit]): _result += "\n"
        del _insuit
        return _result

######################################################################

def multi_show(cards_in, max_on_row=-1):
    _cards_in = cards_in if type(cards_in)==list else [cards_in]
    _line_max = len(_cards_in) if max_on_row < 0 else max_on_row   
    _top = "\u250F" + 11*"\u2501" + "\u2513"
    _first = "\u2503{}{}\u2503"
    _middle = "\u2503" + 5*"\u0020" + "{}" + 5*"\u0020" + "\u2503"        
    _last = ("\u2503{}{}{}\u2503")
    _empty = "\u2503" + 11*"\u0020" + "\u2503"
    _hidden = "\u2503\u0020" + 9*"\u2591" + "\u0020\u2503"
    _bottom = "\u2517" + 11*"\u2501" + "\u251B"
    
    print()
    _count = 0
    _lines = [""]*9        
    for _card in _cards_in:
        _count += 1
        _lines[0] += (_top + 2*"\u0020")
        _lines[8] += (_bottom + 2*"\u0020")        
        if not _card.hidden:
            _lines[1] += (_first.format(_card.symbol, (11-len(_card.symbol))*"\u0020")
                           + 2*"\u0020")
            for _i in range(2,4):
                _lines[_i] += (_empty + 2*"\u0020")
            _lines[4] += (_middle.format(_card.symbol[-1]) + 2*"\u0020")
            for _i in range(5,7):
                _lines[_i] += (_empty + 2*"\u0020")
            _lines[7] += (_last.format((11-len(_card.symbol))*"\u0020",
                                       _card.symbol[len(_card.symbol)-1],
                                       _card.symbol[0:len(_card.symbol)-1]) + 2*"\u0020")
        else:
            for _i in range(1,8):
                _lines[_i]  += (_hidden + 2*"\u0020")

        if _count % _line_max == 0 or _count == len(cards_in):
            _lines = [(2*"\u0020" + line) for line in _lines]
            print(*_lines, sep="\n")
            _lines = [""]*9    

######################################################################

def card_demo():
    """
    print(str(suits) + "\n" + str(all_values))
    print()
    print(list(suits.keys()))
    print(list(suits.values()))
    print()
    print(list(all_values.keys()))
    print(list(all_values.values()))
    """
    print()
    clear("Press <Enter> to continue")
	
    print("\n The suits in a standard deck of cards are:")
    for key in _all_suits.keys():
        print("{}{}\t[{}, {}]".format(6*"\u0020",key, _all_suits[key], key.capitalize()))
    print()

    print(" Each suit has the following cards in it (face value and points):",
          end="\n" + 6*"\u0020")
    i=0
    for key in _all_values.keys():
        i += 1
        if (i == int(len(list(_all_values.keys()))/2)+1):
            end_string = ",\n" + 6*"\u0020"
        elif (i == len(list(_all_values.keys()))):
            end_string = "\n\n"
        else:
            end_string = ",\u0020\u0020"
        print("{} [{} pts]".format(key.capitalize(), _all_values[key]), end=end_string)
 
    ten_clubs = Card("10", "clubs")
    print(" Here's the {} [{}, {} points]:".format(ten_clubs.name, ten_clubs.symbol, ten_clubs.value))
    ten_clubs.show()

    print()
    clear("Press <Enter> to continue")

    my_hand = Hand(ten_clubs)
    my_hand.add(Card("ace", "hearts"))
    more_cards = [Card("9", "diamoNDS"), Card("King", "SPADes")]
    my_hand.add(more_cards)
    new_suits = ["spades", "spades", "diamonds", "CLUBS", "HearTs"]
    new_values = ["6", "ACE", "JacK", "King", "2"]
    new_hidden = [True, None, True, True, False]
    new_cards = []
    for i in range(0, len(new_suits)):
        new_card = Card(new_values[i], new_suits[i], new_hidden[i], _all_values, _all_suits)
        new_cards.append(new_card)
    my_hand.add(new_cards)
    
    print("\n Here's a hand of several cards in addition to the {} ... some face-up, some face-down:"
          .format(ten_clubs.name))
    my_hand.show()
    my_hand.report()

    print()
    clear("Press <Enter> to continue")

    example = my_hand.cards[3]
    print("\n Here's the same hand with the {} also face-down:".format(example.symbol))
    example.hide()
    my_hand.show()
    print("\n Now only {} points are showing, but there are still {} points total in the hand."
          .format(my_hand.points_showing, my_hand.points))
    
    print()
    clear("Press <Enter> to continue")

    my_hand.discard(example)
    print("\n Taking the {} out of the hand leaves {} cards worth {} points:"
          .format(example.name, my_hand.count, my_hand.points))
    my_hand.show()

    print()
    clear("Press <Enter> to continue")

    my_hand.add(example)
    example.unhide()
    print("\n But the {} can be returned to the hand ... bringing it back to {} cards and {} points:"
          .format(example.symbol, my_hand.count, my_hand.points))
    my_hand.show()

    print()
    clear("Press <Enter> to continue")

    print("\n Two (or more!) cards can be taken out at once: ")
    my_hand.discard([my_hand.cards[0], my_hand.cards[2]])   
    my_hand.show()
    my_hand.report()

    print("\n *** END OF DEMO ***")
    clear("Press <Enter> to continue")

######################################################################
    
def deck_demo():
    print()
    clear("Press <Enter> to continue")
    
    my_deck = Deck(_all_values, _all_suits)
    print("\n A brand-new deck with no jokers has a total of {} cards.".format(my_deck.count))

    example_number = 18
    example = my_deck.cards[example_number]
    print("\n Card no. {} in an unshuffled, joker-free deck is the {} [{}, {} points]."
          .format(example_number+1, example.name, example.symbol, example.points))
    
    example = my_deck.take(example_number)[0]
    print(" Taking it out of the deck leaves {} cards. Here they are:".format(my_deck.count))
    my_deck.show()
    
    print("\n The {} still exists, though, and it is face-down by default:".format(example.name))
    example.show()

    print()
    clear("Press <Enter> to continue")
    
    print("\n The {} can be put back anywhere in the deck ... in its original position, for example:"
          .format(example.symbol))
    my_deck.replace(example, example_number)
    my_deck.show_insuits()
    print("\n The deck has {} cards again, in their original order.".format(my_deck.count))

    print()
    clear("Press <Enter> to continue")

    top_hand = Hand(my_deck.deal(5))
    print("\n A five-card hand dealt from the top of the unshuffled deck:")
    top_hand.showall()
    
    bottom_hand = Hand(my_deck.deal(3, "BOTTOM"))
    print("\n Then a hand of {} cards dealt from the bottom of the deck:".format(bottom_hand.count))
    bottom_hand.showall()

    print()
    clear("Press <Enter> to continue")

    print("\n This leaves {} cards still in the deck:".format(my_deck.count))
    print(my_deck.tostring_insuits())

    my_deck.replace(top_hand.cards, "top")
    bottom_hand.cards.reverse()
    my_deck.replace(bottom_hand.cards)
    print(" After putting everything back where it came from, the deck has {} cards once more:"
          .format(my_deck.count))    
    print(my_deck.tostring())

    # top_hand.discard(top_hand.cards)
    # bottom_hand.discard(bottom_hand.cards)
    # top_hand.show()
    # bottom_hand.show()
    del top_hand, bottom_hand

    print(" Shuffling the deck puts the cards in this order:")
    my_deck.shuffle()    
    print(my_deck.tostring())

    print("\n Now a five-card hand dealt off the top of the deck is:")
    dealt_cards_list = my_deck.deal(5)
    top_hand = Hand(dealt_cards_list)
    # for card in top_hand.cards: card.unhide()
    # top_hand.show()
    # for card in top_hand.cards: card:hide()
    top_hand.showall()
    print(" (The cards are actually dealt face-down; this is \"peeking\").")

    print("\n Dealing three more cards into the hand makes it (peeking again!):")
    top_hand.add(my_deck.deal(3))
    top_hand.showall()
    top_hand.report()
    
    print("\n So, {} cards are left in the deck:".format(my_deck.count))
    print(my_deck.tostring_insuits())

    print(" Putting the hand back, on the bottom of the deck:")
    my_deck.replace(top_hand.cards)
    top_hand.discard(top_hand.cards)
    print(my_deck.tostring())
    
    print(" After shuffling again:")
    my_deck.shuffle()
    print(my_deck.tostring())

    print(" And finally, re-setting the whole thing:")
    my_deck.reset()
    print(my_deck.tostring())

    print("\n *** END OF DEMO ***")
    clear("Press <Enter> to continue")
 
######################################################################
 

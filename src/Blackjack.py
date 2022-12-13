import os
from datetime import datetime, date
from gamecards import standard_cards as cards
from gamecards import cards_people as people

globals()["_space"] = 4*"\u0020"

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

class Session:
    def __init__(self, date, dealer, casino, deck, players, filename, dirname):
        self.date = date
        self.dealer = dealer
        self.casino = casino
        self.deck = deck
        self.players = players
        self._protected_file = filename
        self._protected_dir = dirname
        self._set_globals()
        self._make_file()

    @property
    def datestring(self):
        return self.date.strftime("%d-%b-%Y")

    @property
    def file(self):
        return self._protected_dir + "/" + self._protected_file
    
    def _set_globals(self):   
        self.min_age = 18
        self.min_deposit = 10
        self.min_bet = 5
        self.winning_score = 21
        self.stand_or_hit = 17
        self.min_deck_count = int(self.deck.count/2)
		
    def _make_file(self):
        if not os.path.exists(self._protected_dir):
            try:
                os.mkdir(self._protected_dir)
            except:
                self._protected_dir = os.getcwd()
        if not os.path.exists(self.file):
            _the_file = open(self.file, "wt")
            print(("#\n# All Python blackjack games played, beginning {}\n#\n\n" + 70*"#")
                  .format(self.datestring), file=_the_file)
            _the_file.close() 

######################################################################

def make_deposit(player, mindeposit):
    amount = -1
    while amount < mindeposit:
        try:
            amount = float(input(" Enter amount to add [${:0.2f} minimum]: $"
                                 .format(mindeposit)).strip())
        except:
            continue
    amount = round(amount, 2)
    player.give_money(amount)
    print(" Done. Updated wallet: ${:0.2f}".format(player.wallet))

######################################################################

def adjust_aces(hand, threshold):
    if hand.points > threshold:
        for card in hand.cards:
            if card.symbol[0] == "A" and card.points == 11:
                card._protected_points = 1
                break

######################################################################

def play(player, session):
    if session.deck.count < session.min_deck_count:
        print(("\n There are only {} un-dealt cards left. " +
               "The deck will be replenished and shuffled.").format(session.deck.count))
        session.deck.reset()
        session.deck.shuffle()
    
    print("\n Player {} ... current wallet: ${:0.2f}".format(player.fullname, player.wallet))

    if player.wallet < session.min_bet:
        print(" Money must be added to this wallet.")
        make_deposit(player, session.min_deposit)
    else:
        answer = ""
        while not answer=="Y" and not answer=="N":
            answer = input(" Do you wish to add to this wallet? [Y/N]: ").strip()
            if not answer == "":
                answer = answer[0].upper()
        if answer == "Y":
            make_deposit(player, session.min_deposit)

    print()
    bet = -1
    while bet < session.min_bet or bet > player.wallet:
        try:
            bet = float(input(" Place a bet [${:0.2f} minimum]: $".format(session.min_bet)).strip())
        except:
            continue
        if bet > player.wallet:
            print(" *** SORRY: THE WALLET ONLY HAS ${:0.2f} ***".format(player.wallet))
    bet = round(bet, 2)

    print()
    clear()
    
    player_hand = cards.Hand(session.deck.deal(2))
    for card in player_hand.cards:
        card.unhide()
    adjust_aces(player_hand, session.winning_score)
    
    dealer_hand = cards.Hand(session.deck.deal(2))
    dealer_hand.cards[1].unhide()
    adjust_aces(dealer_hand, session.winning_score)

    dealer_playing = False
    dealer_won = False
    player_playing = True
    player_won = False
    
    while player_playing:
        print("\n Card(s) dealt. Number remaining in deck: {}".format(session.deck.count))
        print(" Player: {}\n Current wallet: ${:0.2f}\n Current bet: ${:0.2f}\n"
              .format(player.fullname, player.wallet, bet))
        print("\n ***** PLAYER'S ROUND *****\n")
    
        print("\n PLAYER's hand:", end="")
        player_hand.show()
        print("PLAYER: {}".format(player_hand.points))

        print("\n\n DEALER's hand:", end="")
        dealer_hand.show()
        print("DEALER: {}".format(dealer_hand.points_showing))

        print("\n")
        
        if player_hand.points == session.winning_score:
            dealer_playing = True
            player_playing = False
            _ = input(" *** PLAYER HAS {} !!! *** Press <Enter> to reveal Dealer's hand "
                      .format(session.winning_score))
            dealer_hand.cards[0].unhide()
            clear()
            continue
        if player_hand.points > session.winning_score:
            dealer_won = True
            player_playing = False
            print(" ***** PLAYER BUSTS ... DEALER WINS *****")
            continue
        
        action = ""
        while not action=="H" and not action=="S":
            action = input(" ACTION?  Hit [H] or Stand [S]: ").strip()
            if not action == "":
                action = action[0].upper()
        if action == "H":
            next_cards = session.deck.deal()
            next_cards[0].unhide()
            player_hand.add(next_cards)
            adjust_aces(player_hand, session.winning_score)
            clear()
        elif action == "S":
            dealer_playing = True
            player_playing = False
            dealer_hand.cards[0].unhide()
            _ = input("\n PLAYER STANDS on {}. Press <Enter> to reveal Dealer's hand "
                      .format(player_hand.points))
            clear()

    while dealer_playing:
        print("\n Card(s) dealt. Number remaining in deck: {}".format(session.deck.count))
        print(" Player: {}\n Current wallet: ${:0.2f}\n Current bet: ${:0.2f}\n"
              .format(player.fullname, player.wallet, bet))
        print("\n ***** DEALER'S ROUND *****\n")       
    
        print("\n PLAYER's hand:", end="")
        player_hand.show()
        print(" TOTAL for PLAYER: {}".format(player_hand.points))

        print("\n\n DEALER's hand:", end="")
        dealer_hand.show()
        print(" TOTAL for DEALER: {}".format(dealer_hand.points_showing))

        print("\n")

        if dealer_hand.points == session.winning_score and dealer_hand.points > player_hand.points:
            dealer_won = True
            dealer_playing = False
            print(" ***** DEALER GETS {} !!! DEALER WINS *****".format(session.winning_score))
            continue
        if dealer_hand.points > session.winning_score:
            player_won = True
            dealer_playing = False
            print(" ***** DEALER BUSTS ... PLAYER WINS *****")
            continue
        if dealer_hand.points >= session.stand_or_hit and dealer_hand.points < player_hand.points:
            player_won = True
            dealer_playing = False
            print(" ***** DEALER MUST STAND ON {} ... PLAYER WINS *****"
                  .format(dealer_hand.points))
            continue
        if dealer_hand.points >= session.stand_or_hit and dealer_hand.points == player_hand.points:
            dealer_playing = False
            print(" ***** DEALER STANDS ON {} ... TIE *****"
                  .format(dealer_hand.points))
            continue        
        if dealer_hand.points >= session.stand_or_hit and dealer_hand.points > player_hand.points:
            dealer_won = True
            dealer_playing = False
            print(" ***** DEALER WINS *****")
            continue

        _ = input(" Dealer has less than {} and must take another card. Press <Enter> "
                  .format(session.stand_or_hit))
        next_cards = session.deck.deal()
        next_cards[0].unhide()
        dealer_hand.add(next_cards)
        adjust_aces(dealer_hand, session.winning_score)
        clear()

    player_status = "TIED"
    if player_won:
        player.give_money(bet)
        player_status = "WON"
    elif dealer_won:
        player.take_money(bet)
        player_status = "LOST"

    print()
    clear("Press <Enter> to continue")

    print("\n {} {} that hand. Their wallet is now: ${:0.2f}"
          .format(player.fullname, player_status, player.wallet))

    thefile = open(session.file, "at")
    print("Player: {}".format(player.tostring()), end="", file=thefile)
    print("\n{}Player's hand: {} points [ {} ]"
          .format(_space, player_hand.points, player_hand.tostring()), end="", file=thefile)
    print("\n{}Dealer's hand: {} points [ {} ]"
          .format(_space, dealer_hand.points, dealer_hand.tostring()), end="", file=thefile)
    print("\n{}Player {}".format(_space, player_status), end="", file=thefile)
    if player_status == "TIED":
        print("\n", file=thefile)
    else:
        print(" ${:0.2f}\n".format(bet), file=thefile)
    thefile.close()

######################################################################

def new_player(session):
    if len(session.players) > 0:
        print("\n Previous players in this session:")
        for i in range(1, len(session.players)+1):
            print(_space + "{}. {}".format(i, session.players[i-1].tostring()))
        choice = -1
        while choice < 0:
            str_choice = input(" Choose one by number OR press <Enter> for a new player: ").strip()
            if str_choice == "":
                choice = 0
            else:
                try:
                    choice = int(str_choice)
                except:
                    continue
            if choice > len(session.players):
                 choice = -1
        if choice > 0:
            return session.players[choice-1]

    print("\n REGISTER NEW PLAYER.....")
    
    first = ""
    while first == "":
        first = input(_space + "First name: ").strip()
        if (first == ""):
            print(_space + "*** FIRST NAME CANNOT BE BLANK ***")

    last = ""
    while last == "":
        last = input(_space + "Last name: ").strip()
        if (last == ""):
            print(_space + "*** LAST NAME CANNOT BE BLANK ***")

    good_date = False
    while not good_date:
        dob = input(_space + "Date of birth (in YYYY/MM/DD format): ").strip()
        try:
            dob_date = datetime.strptime(dob, "%Y/%m/%d").date()
        except:
            print(_space + "*** INVALID DATE OR BAD FORMAT ***")
            continue
        if (dob_date > session.date):
            print(_space + "*** DATE OF BIRTH CANNOT BE IN THE FUTURE ***")
        else:
            good_date =True

    newguy = people.Player(first, last, dob_date)
    if (newguy.age >= session.min_age):
        print("\n New player registered as " + newguy.tostring())
        session.players.append(newguy)
    else:
        print("\n *** NOT ALLOWED: {} YEARS OF AGE IS TOO YOUNG TO PLAY ***"
              .format(newguy.age))
    return newguy

######################################################################

def game_setup():
    session = Session(date = date.today(),
                  dealer = people.Dealer("Bob", "Builder", date(1986, 7, 16),
                                         "Cards R Us", "L16730W332-AB"),
                  casino = "The Best Casino",
                  deck = cards.Deck(cards._all_values, cards._all_suits),
                  players = [],
                  filename = "all_games.txt",
                  dirname = "Games History")
    session.deck.shuffle()
    
    print("\n WELCOME TO THE BLACKJACK TABLE AT {}".format(session.casino.upper()))
    print("\n Your dealer today:")
    print(session.dealer.tostring())

    thefile = open(session.file, "at")
    print("\nDATE: " + session.datestring, file=thefile)
    print("CASINO: " + session.casino, file = thefile)
    print("DEALER: ", file=thefile)
    print(session.dealer.tostring() + "\n", file=thefile)
    thefile.close()
    
    player = new_player(session)
    while player.age < session.min_age:
        player = new_player(session)

    keep_going = True
    while keep_going:
        play(player, session)
        
        good_answer = False
        while not good_answer:
            try:
                choice = int(input(
                             ("\n GAME MENU" +
                              "\n{}1. Play another hand (CURRENT PLAYER, SAME DECK)" +
                              "\n{}2. Play a new game (DIFFERENT PLAYER, NEW DECK)" +
                              "\n{}3. Quit" +
                              "\n Choose by number: ").format(_space, _space, _space)).strip())
            except:
                print("\n *** THAT'S NOT A NUMBER \u2014 TRY AGAIN ***")
                continue
            if choice in [1, 2, 3]:
                good_answer = True
            else:
                print("\n *** You MUST enter '1', '2', or '3'. ***")

        if choice == 1:
            pass
        elif choice == 2:
            trial_player = new_player(session)
            while trial_player.age < session.min_age:
                trial_player = new_player(session)
            player = trial_player
            session.deck.reset()
            session.deck.shuffle()
        elif choice == 3:
            keep_going = False

    thefile = open(session.file, "at")
    print(70*"#", file=thefile)
    thefile.close()

######################################################################
    
def main():
    keep_going = True
    while keep_going:
        good_answer = False
        while not good_answer:
            try:
                choice = int(input(("\n MAIN MENU" +
                                "\n{}1. Play Blackjack" +
                                "\n{}2. DEMO: classes Card and Hand" +
                                "\n{}3. DEMO: class Deck" +
                                "\n{}4. Exit" +
                                "\n Choose by number: ").format(_space, _space, _space, _space)).strip())
            except:
                print("\n *** That's not a number. Choose again. ***")
                continue
            if choice in [1, 2, 3, 4]:
                good_answer = True
            else:
                print("\n *** You MUST enter '1', '2', '3', or '4'. ***")

        if choice == 1:
            game_setup()
        elif choice == 2:
            cards.card_demo()
        elif choice == 3:
            cards.deck_demo()
        elif choice == 4:
            keep_going = False
    
    print("\n *** GOODBYE ***")

######################################################################

main()

stop()


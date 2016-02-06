# Blackjack (for CodeSkulptor)

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# useful global variables
in_play = False
outcome = "Hit or stand?"
score = 0

# globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

class Hand:
    def __init__(self):
        self.hand = []
        # create Hand object

    def __str__(self):
        return "Hand contains: " + str(self.hand)
        # return a string representation of a hand
    
    def add_card(self, card):
        return self.hand.append(str(card))
        # add a card object to a hand

    def get_value(self):
        x = 0
        y = 0
        
        for card in self.hand:
            x += VALUES[card[1:2]]
            if card[1:2] == 'A':
                y += 1
        
        if y == 1:
            x += 10
            
        return x
        # count aces as 1, if the hand has an ace, then add 10 to hand value
        # if it doesn't bust compute the value of the hand
   
    def draw(self, canvas, pos):
        x = 0
        
        for cards in self.hand:
            card = Card(cards[:1], cards[1:2])
            
            if cards == self.hand[0] and in_play:
                canvas.draw_image(card_back, (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]), CARD_BACK_SIZE,
                                  [150 + CARD_BACK_CENTER[0], 220 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
            card.draw(canvas, [pos[0] + x, pos[1]])
            
            x += 80

class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:  
                self.deck.append(str(suit+rank))	

    def shuffle(self):
        random.shuffle(self.deck) 

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        return "Deck contains: " + str(self.deck)  

#event handlers for buttons
def deal():
    global outcome, score, in_play, dealer_hand, player_hand, deck

    outcome = "Hit or stand?"
    
    if in_play:
        score -= 1
        outcome = "No! You lose!"
    
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    
    deck.shuffle()
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    print dealer_hand
    print player_hand
    
    in_play = True

def hit():
    global outcome, in_play, score, player_hand, deck
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted! New deal?"
            score -= 1
            in_play = False
            print outcome
    
    print player_hand
       
def stand():
    global outcome, in_play, score, player_hand, deck
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
       
    if in_play:
        if player_hand.get_value() > 21:
            outcome = "You are busted! New deal?"
        elif dealer_hand.get_value() > 21 or player_hand.get_value() > dealer_hand.get_value():
            outcome = "You won! New deal?"
            score += 1
        else:
            outcome = "You are busted! New deal?"
            score -= 1
        print dealer_hand
        print outcome
    
    in_play = False

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", (200, 50), 36, 'Black')
    canvas.draw_text(outcome, (20, 100), 24, 'White')
    canvas.draw_text("Score: " + str(score), (400, 100), 24, 'White')
    
    canvas.draw_text("Dealer hand", (150, 200), 24, 'Black')
    dealer_hand.draw(canvas, [150, 220])
    canvas.draw_text("Player hand", (150, 380), 24, 'Black')
    player_hand.draw(canvas, [150, 400])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

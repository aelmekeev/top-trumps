import random

class Card:
  def __init__(self, a, b, c, d):
    self.a = a  # size
    self.b = b  # cuteness
    self.c = c  # mischief
    self.d = d  # loyalty

deck = [
  Card(4, 4, 8, 5), # lion
  Card(4, 8, 9, 1), # labrador
  Card(4, 3, 6, 6), # crocodile
  Card(2, 9, 2, 4), # guinea pig
  Card(4, 4, 10, 1), # fox
  Card(10, 5, 5, 10), # elephant
  Card(2, 6, 7, 7), # bulldog
  Card(5, 4, 5, 5), # grizzly bear
  Card(1, 10, 2, 1), # duck
  Card(3, 10, 4, 4), # rabbit
  Card(5, 4, 7, 4), # polar bear
  Card(3, 5, 3, 10), # owl
  Card(5, 3, 9, 4), # gorilla
  Card(6, 2, 5, 1), # goat
  Card(5, 4, 2, 4), # giant panda
  Card(4, 5, 8, 10), # kangaroo
  Card(7, 3, 4, 3), # zebra
  Card(6, 3, 4, 5), # horse
  Card(9, 4, 5, 5), # giraffe
  Card(3, 2, 9, 7), # coyote
  Card(6, 1, 3, 1), # ostrich
  Card(8, 2, 4, 4), # camel
  Card(3, 9, 10, 1), # cat
  Card(3, 4, 8, 6), # howler monkey
  Card(6, 3, 4, 9), # deer
  Card(4, 4, 7, 3), # tiger
  Card(6, 3, 5, 2), # sheep
  Card(8, 3, 5, 8), # hippopotamus
  Card(8, 3, 5, 3), # rhino
  Card(3, 9, 3, 5), # koala
]

AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE = 8
MAX_EXCHANGES = 500
EMULATIONS = 10000

# class Hand that contains a list of cards
class Hand:
  def __init__(self, cards):
    self.cards = cards

  # method to get next card
  def next(self):
    return self.cards.pop(0)
  
  # method to add a card to the deck
  def add(self, card):
    self.cards.append(card)

# method to compare two cards based on specific attribute and return the winner
def compare_cards(card1, card2, attribute):
  if getattr(card1, attribute) > getattr(card2, attribute):
    return 1
  elif getattr(card1, attribute) < getattr(card2, attribute):
    return 2
  else:
    return 0
  
# method to shuffle the deck
def shuffle(deck):
  random.shuffle(deck)
  return deck
  
# method to deal cards from the deck to the players
def deal(deck):
  hand1 = Hand(deck[0::2])
  hand2 = Hand(deck[1::2])
  return hand1, hand2
  
# function that returns name of the Card attribute with the highest value
def find_highest_attribute(card, attribute_list = []):
  highest = 0
  highest_attribute = ""
  for attribute in card.__dict__:
    if not attribute in attribute_list and card.__dict__[attribute] > highest:
      highest = card.__dict__[attribute]
      highest_attribute = attribute
  return highest_attribute

  
def play_game(hand1, hand2, find_attribute):
  exchange = 0
  while len(hand1.cards) > 0 and len(hand2.cards) > 0 and exchange < MAX_EXCHANGES:
    card1 = hand1.next()
    card2 = hand2.next()
    turn = exchange % 2
    current_turn_card = card1 if turn == 0 else card2

    # until the winner is found compare cards by different attributes
    winner = 0
    checked_attributes = []
    while winner == 0:
      attribute = find_attribute(current_turn_card, checked_attributes)
      checked_attributes.append(attribute)
      winner = compare_cards(card1, card2, attribute)
      if winner == 1:
        hand1.add(card1)
        hand1.add(card2)
        exchange += 1
      elif winner == 2:
        hand2.add(card1)
        hand2.add(card2)
        exchange += 1
  
  # print(f"Game finished after {exchange} exchanges (~{round(exchange * 8 / 60)} minutes)")
  # print(f"Minimum number of cards: {min(len(hand1.cards), len(hand2.cards))}")

  return exchange

total_exchanges = 0
endless_games = 0
for i in range(EMULATIONS):
  hand1, hand2 = deal(shuffle(deck))
  exchanges = play_game(hand1, hand2, find_highest_attribute)
  if exchanges == MAX_EXCHANGES:
    endless_games += 1
  total_exchanges += exchanges

print(f"Average number of exchanges: {total_exchanges / EMULATIONS}")
print(f"Average number of minutes per game: {round(total_exchanges * AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE / 60 / EMULATIONS)}")
print(f"Number of endless games: {endless_games} ({round(endless_games * 100 / EMULATIONS)}%)")
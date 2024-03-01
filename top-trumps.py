import glob
import random

class Card:
  def __init__(self, a, b, c, d):
    self.a = a
    self.b = b
    self.c = c
    self.d = d

AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE = 8
MAX_EXCHANGES = 500
EMULATIONS = 10000

class Hand:
  def __init__(self, cards):
    self.cards = cards

  def next(self):
    return self.cards.pop(0)
  
  def add(self, card):
    self.cards.append(card)

# reads the deck from the csv file
def read_deck_from_csv(file_name):
  with open(file_name, 'r') as file:
    deck = []
    # skip the header
    next(file)
    for line in file:
      _, a, b, c, d = line.strip().split(';')
      deck.append(Card(int(a), int(b), int(c), int(d)))
  return deck

# compare two cards based on specific attribute and return the winner
def compare_cards(card1, card2, attribute):
  if getattr(card1, attribute) > getattr(card2, attribute):
    return 1
  elif getattr(card1, attribute) < getattr(card2, attribute):
    return 2
  else:
    return 0
  
# deal cards from the deck to the players
def deal(deck):
  hand1 = Hand(deck[0::2])
  hand2 = Hand(deck[1::2])
  return hand1, hand2
  
def choose_highest_attribute(card):
  highest = 0
  highest_attributes = []
  for attribute in card.__dict__:
    if card.__dict__[attribute] > highest:
      highest = card.__dict__[attribute]
      highest_attributes = [attribute]
    elif card.__dict__[attribute] == highest:
      highest_attributes.append(attribute)
  return random.choice(highest_attributes)

def play_game(hand1, hand2, find_attribute):
  exchange = 0
  while len(hand1.cards) > 0 and len(hand2.cards) > 0 and exchange < MAX_EXCHANGES:
    winner = 0
    bank = []
    turn = exchange % 2
    while winner == 0 and len(hand1.cards) > 0 and len(hand2.cards) > 0:
      card1 = hand1.next()
      card2 = hand2.next()
      bank.append(card1)
      bank.append(card2)

      current_turn_card = card1 if turn == 0 else card2
      attribute = find_attribute(current_turn_card)

      winner = compare_cards(card1, card2, attribute)
      if winner == 1:
        for card in bank:
          hand1.add(card)
      elif winner == 2:
        for card in bank:
          hand2.add(card)
      exchange += 1
  
  return exchange

# for each csv files in decks folder play the game and print the average number of exchanges
for deck_file in glob.glob('decks/*.csv'):
  print(f"Playing with deck: {deck_file.split('/')[1].split('.')[0]}")

  deck = read_deck_from_csv(deck_file)

  total_exchanges = 0
  endless_games = 0
  for i in range(EMULATIONS):
    random.shuffle(deck)
    hand1, hand2 = deal(deck)
    exchanges = play_game(hand1, hand2, choose_highest_attribute)
    if exchanges == MAX_EXCHANGES:
      endless_games += 1
    total_exchanges += exchanges

  print(f"Average number of exchanges: {round(total_exchanges / EMULATIONS)}")
  print(f"Average number of minutes per game: {round(total_exchanges * AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE / 60 / EMULATIONS)}")
  print(f"Number of endless games: {endless_games} ({round(endless_games * 100 / EMULATIONS)}%)")
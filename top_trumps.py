import glob
import random

NUMBER_OF_PLAYERS = 2
AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE = 8
MAX_EXCHANGES = 500
EMULATIONS = 10000

class Card:
  def __init__(self, stats):
    self.stats = stats

  def get_stat(self, index):
    return self.stats[index]
  
  # selects random stat if there are multiple stats with the same value
  def get_highest_stat_index(self):
    highest = max(self.stats)
    highest_stats = [i for i, v in enumerate(self.stats) if v == highest]
    return random.choice(highest_stats)

class Hand:
  def __init__(self, cards):
    self.cards = cards

  def next(self):
    return self.cards.pop(0)
  
  def add(self, card):
    self.cards.append(card)

def create_card_from_string(card_string):
  return Card([int(x) for x in card_string.split(';')[1:]])

def read_deck_from_csv(file_name):
  with open(file_name, 'r') as file:
    deck = []
    # skip the header
    next(file)
    for line in file:
      deck.append(create_card_from_string(line))
  return deck

# compare cards based on specific stat and return the winner card index
# if there is no winner return None
def compare_cards(cards, stat_index):
  card_stats = [card.get_stat(stat_index) for card in cards]
  max_stat = max(card_stats)
  if card_stats.count(max_stat) > 1:
    return None
  else:
    return card_stats.index(max_stat)
  
def deal(deck, number_of_players):
  random.shuffle(deck)
  hands = []
  for i in range(number_of_players):
    hands.append(Hand(deck[i::number_of_players][0:len(deck) // number_of_players]))
  return hands

def is_end_of_game(hands):
  return len([True for hand in hands if len(hand.cards) > 0]) == 1

# play the game and return the number of exchanges
def play_game(hands, max_exchanges=MAX_EXCHANGES):
  exchange = 0
  null_card = Card([0] * len(hands[0].cards[0].stats))
  while exchange < max_exchanges and not is_end_of_game(hands):
    winner = 0
    bank = []
    turn = exchange % len(hands)
    while winner == 0 and not is_end_of_game(hands):
      cards = []
      for hand in hands:
        if len(hand.cards) == 0:
          card = null_card
        else:
          card = hand.next()
          bank.append(card)
        cards.append(card)
      
      stat_index = cards[turn].get_highest_stat_index()
      winner = compare_cards(cards, stat_index)

      if winner is not None:
        for card in bank:
          hands[winner].add(card)

      exchange += 1
  
  return exchange

# for each csv files in decks folder play the game and print the average number of exchanges
def main() -> None:
  for deck_file in glob.glob('decks/*.csv'):
    print(f"Deck: {deck_file.split('/')[1].split('.')[0]}\n")

    deck = read_deck_from_csv(deck_file)

    total_exchanges = 0
    endless_games = 0
    for i in range(EMULATIONS):
      hands = deal(deck, NUMBER_OF_PLAYERS)
      exchanges = play_game(hands)
      if exchanges == MAX_EXCHANGES:
        endless_games += 1
      total_exchanges += exchanges

    print(f"Average number of exchanges: {total_exchanges // EMULATIONS}")
    print(f"Average number of minutes per game: {round(total_exchanges * AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE / 60 / EMULATIONS)}")
    print(f"Number of endless games: {endless_games} ({endless_games * 100 // EMULATIONS}%)\n\n")

if __name__ == '__main__':
    main()
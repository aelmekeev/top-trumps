from argparse import ArgumentParser
from functools import lru_cache
import glob
import random

AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE = 8

NUMBER_OF_PLAYERS = 3
MAX_EXCHANGES = 450
EMULATIONS = 10000

class Card:
  def __init__(self, stats):
    self.stats = stats

  def get_stat(self, index) -> float:
    return self.stats[index]
  
  # selects random stat if there are multiple stats with the same value
  @lru_cache
  def get_highest_stat_index(self, pack_stats) -> int:
    stats_relative = [((self.stats[i] - pack_stats.min[i]) / (pack_stats.max[i] - pack_stats.min[i])) for i in range(len(self.stats))]
    highest = max(stats_relative)
    highest_stats = [i for i, v in enumerate(stats_relative) if v == highest]
    return random.choice(highest_stats)
  
  def get_random_stat_index(self, _) -> int:
    return random.randint(0, len(self.stats) - 1)

class PackStats:
  def __init__(self, statsNumber):
    self.min = [1000000] * statsNumber
    self.max = [-1000000] * statsNumber
  
  def update(self, stats):
    for i in range(len(stats)):
      self.min[i] = min(self.min[i], stats[i])
      self.max[i] = max(self.max[i], stats[i])

class Hand:
  def __init__(self, cards):
    self.cards = cards

  def next(self) -> Card:
    return self.cards.pop(0)
  
  def add(self, card) -> None:
    self.cards.append(card)

def create_card_from_string(card_string) -> Card:
  return Card([float(x) for x in card_string.split(';')[1:]])

def read_pack_from_csv(file_name) -> list[Card]:
  with open(file_name, 'r') as file:
    pack = []
    # skip the header
    header = next(file)
    number_of_stats = len(header.split(';')) - 1
    pack_stats = PackStats(number_of_stats)
    for line in file:
      card = create_card_from_string(line)
      if len(card.stats) != number_of_stats:
        raise ValueError(f"Invalid number of stats in card: {line}")
      pack_stats.update(card.stats)
      pack.append(card)
  return pack, pack_stats

# compare cards based on specific stat and return the winner card index
# if there is no winner return None
def compare_cards(cards, stat_index):
  card_stats = [card.get_stat(stat_index) for card in cards]
  max_stat = max(card_stats)
  if card_stats.count(max_stat) > 1:
    return None
  else:
    return card_stats.index(max_stat)
  
def deal(pack, number_of_players) -> list[Hand]:
  random.shuffle(pack)
  hands = []
  for i in range(number_of_players):
    hands.append(Hand(pack[i::number_of_players][0:len(pack) // number_of_players]))
  return hands

def is_end_of_game(hands):
  return len([True for hand in hands if len(hand.cards) > 0]) == 1

# play the game and return the number of exchanges
def play_game(pack_stats, hands, max_exchanges, get_stat_index_method) -> int:
  exchange = 0
  null_card = Card([0] * len(hands[0].cards[0].stats))
  get_stat_index = getattr(Card, get_stat_index_method)
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
      
      stat_index = get_stat_index(cards[turn], pack_stats)
      winner = compare_cards(cards, stat_index)

      if winner is not None:
        for card in bank:
          hands[winner].add(card)

      exchange += 1
  
  return exchange

# for each csv files in packs folder play the game and print the average number of exchanges
def main(pack, number_of_players, emulations, max_exchanges, get_stat_index_method) -> None:
  for pack_file in glob.glob(pack):
    print(f"Pack: {pack_file.split('/')[-1].split('.')[0]}\n")

    pack, pack_stats = read_pack_from_csv(pack_file)

    total_exchanges = 0
    endless_games = 0
    for i in range(emulations):
      hands = deal(pack, number_of_players)
      exchanges = play_game(pack_stats, hands, max_exchanges, get_stat_index_method)
      if exchanges == max_exchanges:
        endless_games += 1
      total_exchanges += exchanges

    print(f"* Average number of exchanges: {total_exchanges // emulations}")
    print(f"* Average number of minutes per game: {round(total_exchanges * AVERAGE_NUMBER_OF_SECONDS_PER_EXCHANGE / 60 / emulations)}")
    print(f"* Number of endless games: {endless_games} ({endless_games * 100 // emulations}%)\n\n")

if __name__ == '__main__':
    # read parameters from the command line
    parser = ArgumentParser()
    parser.add_argument('--number_of_players', type=int, default=NUMBER_OF_PLAYERS)
    parser.add_argument('--emulations', type=int, default=EMULATIONS)
    parser.add_argument('--max_exchanges', type=int, default=MAX_EXCHANGES)
    parser.add_argument('--get_stat_index_method', type=str, default='get_highest_stat_index')
    parser.add_argument('--pack', type=str, default='packs/*.csv')
    args = parser.parse_args()
    main(args.pack, args.number_of_players, args.emulations, args.max_exchanges, args.get_stat_index_method)
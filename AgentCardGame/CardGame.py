"""
 Card Game Simulation
 Aaron Harkrider
 January 31, 2018

 This game will be played by 3 different types of Agents

 1. (type h) Agent that always plays it's highest card if possible, otherwise passes.
 2. (type l) Agent that always plays the smallest card possible thus only passes when it has nothing to play.
 3. (type r) Randomly selects a playable card if possible, otherwise passes.
 Extra Credit Agent: Agent always plays the smartest play


 After the game is played we we print percentages showing winnings.

 Environment:
 - Deck of infinite cards
    2, 3, 4, 5, 6, 7, 8, 9, 10, Jack(11), Queen(12), King(13), Ace(14), Joker(15)

 - Agents hand
 - - Starting hand of 10 cards (this could be sorted to easily play highest/lowest card)
 - - Additional card added when player passes turn and draws a card

 - Top played card on the table
"""

import random


# Represent a player
class Player:
    def __init__(self):
        self.hand = []

    # sets the players hand
    def set_hand(self):
        self.hand = sorted(deal_hand())

    # Draw a single card and add it to the players hand
    def draw(self):
        self.hand.append(draw_card())

    # Find all cards in hand that is greater then the top card on the table
    def find_playable_cards(self, top_card):
        return [card for card in self.hand if card > top_card]


# Agent that always plays the lowest card possible
class LowCardAgent(Player):

    def play_turn(self, top_card):
        # return cards from hand that are playable
        cards = self.find_playable_cards(top_card)
        if not cards:
            # no playable cards, passing turn
            self.draw()
            return None
        card = min(cards)  # find lowest card
        self.hand.remove(card)  # removed the played card from hand
        return card


# Agent that always plays the highest card
class HighCardAgent(Player):

    def play_turn(self, top_card):
        # return cards from hand that are playable
        cards = self.find_playable_cards(top_card)
        if not cards:
            # no playable cards, passing turn
            self.draw()
            return None
        card = max(cards)  # find highest card
        self.hand.remove(card)  # removed the played card from hand
        return card


# Agent that always plays a random card
class RandomCardAgent(Player):

    def play_turn(self, top_card):
        # return cards from hand that are playable
        cards = self.find_playable_cards(top_card)
        if not cards:
            # no playable cards, passing turn
            self.draw()
            return None
        card = random.choice(cards)  # pick a random card
        self.hand.remove(card)  # removed the played card from hand
        return card


# deal ten cards
def deal_hand():
    return [draw_card() for _ in range(10)]


# Draw a single random card
def draw_card():
    # 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack(11), Queen(12), King(13), Ace(14), Joker(15)
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    weight = [4] * 13 + [2]  # Probability to draw card
    return random.choices(values, weights=weight)[0]


# Return list of players reordered by starting players index
def reorder_by_starting_player(all_players, starting_player_index):
    num_players = len(all_players)
    return [all_players[(i + starting_player_index) % num_players] for i in range(num_players)]


# The full environment with all players playing the game
def play_game(all_players):
    debug = 0  # if set to 1 then true and print debug lines

    if debug == 1:
        print("playing game")

    # Deal 10 cards to all players
    for player in all_players:
        player.set_hand()

    # find starting player
    highest_cards = []
    for player in all_players:
        # Finds the highest cards from each players hand
        highest_cards.append(max(player.hand))

    highest_card = max(highest_cards)  # get the highest card from the list of all players highest cards
    players_with_highest_card = [i for i, c in enumerate(highest_cards) if highest_card == c]
    starting_player_index = random.choice(players_with_highest_card)  # if players tied for highest card pick at random

    # players ordered by the player with the highest card for the first battle
    players_in_battle = reorder_by_starting_player(all_players, starting_player_index)

    # play till one player wins the game
    winner = None
    while winner is None:
        top_card_on_table = 0

        # loop till battle is won
        while len(players_in_battle) > 1:
            # single "round of a Battle"
            for player in players_in_battle:
                card = player.play_turn(top_card_on_table)

                # check if player passed their turn
                if card is None:
                    # player passed
                    players_in_battle.remove(player)
                    if len(players_in_battle) == 1:
                        # everyone passed end of battle
                        break
                else:
                    if debug == 1:
                        print(card)
                    top_card_on_table = card
                    # check if player won the game
                    if not player.hand:
                        # player is out of cards they won
                        winner = player
                        break
        if debug == 1:
            print("- End of battle -")
        # winner of battle is the only player left in the list of players still in the battle
        winner_of_battle = all_players.index(players_in_battle[0])
        # Reset players in battle, ordered by the winner of the last battle
        players_in_battle = reorder_by_starting_player(all_players, winner_of_battle)

    if debug == 1:
        print("We have a winner, End of Game.")
    return winner


# dictionary of AGENT types to assign to players
AGENT_TYPES = dict(l=LowCardAgent, h=HighCardAgent, r=RandomCardAgent)


# Run the program for x rounds with indicated types of agents
def main(rounds, players_args):
    for arg in players_args:
        if arg != "l" and arg != "h" and arg != "r":
            raise TypeError("Arguments need to either be 'l', 'h', or 'r'")
    if len(players_args) > 6:
        print("WARNING: higher then six agents could take an extremely long time to play the game.")

    # pick out the types of agents indicated
    players_list = [AGENT_TYPES[i]() for i in players_args]

    # Play Game for x times
    winners = [play_game(players_list) for _ in range(rounds)]

    tally = [winners.count(p) for p in players_list]
    assert sum(tally) == rounds

    print([t / rounds for t in tally])


# Standard boilerplate to call the main function, if executed
if __name__ == '__main__':
    import sys

    rounds = int(sys.argv[1])
    players = sys.argv[2:]
    main(rounds, players)

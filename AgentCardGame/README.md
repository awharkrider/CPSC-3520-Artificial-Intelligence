Card Game Simulation

Author: Aaron Harkrider

Date: January 30, 2018

Documentation of Card Game Simulation
--
Classes:
* Player Class
    * Represents a single player
    * Function to set the players hand with 10 cards
    * Function to find the playable cards from the players hand
    * Function to draw a single card and add it to the players hand.
* HighCardAgent 
    * Extends the player class 
    * Function play_turn 
        * Find playable cards
        * Pass and draw a card if no cards are playable
        * Play largest of its playable cards
* LowCardAgent 
    * Extends the player class 
    * Function play_turn 
        * Find playable cards
        * Pass and draw a card if no cards are playable
        * Play smallest of its playable cards
* RandomCardAgent 
    * Extends the player class 
    * Function play_turn 
        * Find playable cards
        * Pass and draw a card if no cards are playable
        * Play a random card from its playable cards

* Function: reorder_by_starting_player
    * takes all the players and reorders them so the player to go first is at the front of the list.

* Function: play_game
    * Deal ten cards to each player.
    * Player with the highest card starts the first battle, ties broken by a random choice.
    * Play the Game till we get a winner: 
        * Start battle with no card on the table
        * Every player gets a turn to play
            * top card on table is updated when agent plays a card
            * when a player passes remove them from the turn rotation
            * When only one player is left in the rotation they have won the battle and we reset 
            and they start the next battle.

* Main
    * Runs the program for x games with list of the agents
    



Running The Card Game Simulation:
--

To run the program call call line below in the cmd line with arguments setup as specified.

    python3 CardGame.py 1000 h l r".
   
**Arguments:**
1. Program name: CardGame.py
2. Number of games to play: For example 1000 will play one thousand games. 
3. Type of agent:  "h", "l", or "r" 
    * (type h) Agent that always plays it's highest card if possible, otherwise passes.
    * (type l) Agent that always plays the smallest card possible thus only passes when it has nothing to play.
    * (type r) Randomly selects a playable card if possible, otherwise passes.
   

Write Up
--

To determine which Agent performed the best I decided to base it off the percentage of the time an agent won.
From my observations the "l" agent (who always plays the lowest card) won the majority of the time.
 When running a thousand games the LowCardAgent won on average about 90% of the time. HighCardAgent was the 
 worst losing almost all of it's games. 
 
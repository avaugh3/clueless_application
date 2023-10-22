from messaging.message import Message

"""
General inforamtion about disproving a message, it can be removed 
in the long-term
-----------------------------
 As soon as you make a Suggestion, your opponents, in turn, try to 
 prove it false. 
 
 The first to try is the player to your immediate left. 
 This player looks at his or her cards to see if one of the three cards 
 you just named is there. 
  - If the player does have one of the cards named, 
    # he or she must show it to you and no one else. 
  - If the player has more than one of the cards named, 
    # he or she selects just one to show you. 

 If that opponent has none of the cards that you named, then the chance 
 to prove your Suggestion false passes, in turn, to the next player 
# on the left. 
#
# As soon as one opponent shows you one of the cards that you 
 named, it is proof that this card cannot be in the envelope.

 End your turn by checking off this card in your notebook. 
(Some players find it helpful to mark the initials of the player 
who showed the card.) 
 If no one is able to prove your Suggestion false, you may either 
 end your turn or make an Accusation now.
"""

class DisproveSuggestionMessage(Message):
    type = 'disprove_suggestion'
    def __init__(self, contents):
        self.contents = contents

    # contents prop
    # 1. hasSuspectInSuggestion
    # 2. showSuspectToPlayerWithSuggestion 
    # 3. hasRoomInSuggestion
    # 4. showRoomToPlayerWithSuggestion
    # 5. hasWeaponInSuggestion
    # 6. showWeaponToPlayerWithSuggestion
    # 7. canDisproveSuggestion   

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"contents:")
       
        for k, v in self.contents.items():
            print(k + ":", v)
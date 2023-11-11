from gameAnswer import GameAnswer


def test_actions():
    print('Test Actions')
    testAnswer = GameAnswer(None, None, None)
    print(testAnswer)
    answer = testAnswer.GenerateAnswer()
    print(answer.character.name)
    print(answer.room.roomName)
    print(answer.weapon.name)

    print(answer.dealInventory())
test_actions()
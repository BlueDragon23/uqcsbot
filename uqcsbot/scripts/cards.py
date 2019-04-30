from random import shuffle
from uqcsbot import bot, Command

def emojify(value: int):
    if value == -1:
        return ":card-joker:"
    suit = ["hearts", "spades", "diamonds", "clubs"][value//13]
    rank = ["ace", "king", "queen", "jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"][value%13]
    return ":card-{}-{}:".format(rank, suit)
    
    

@bot.on_command("cards")
def handle_cards(command: Command):
    """
    `!cards [number] [joker]` - Deals one or more cards
    """

    # easter egg - prepare four 500 hands, and the kitty
    if command.arg == "500":
        deck = list(range(0, 0+10)) + list(range(13, 13+11)) + list(range(26, 26+10)) + list(range(39, 39+11)) + [-1]
        shuffle(deck)
        hands = [deck[ 0:10], deck[10:20], deck[20:30], deck[30:40], deck[40:]]
        [h.sort() for h in hands]
        hands = [[emojify(c) for c in h] for h in hands]
        hands[-1].extend(7*[""])
        hands = zip([":regional-indicator-n: ",":regional-indicator-e: ",":regional-indicator-s: ",":regional-indicator-w: ",":cat: "], *zip(*hands))
        hands = ["".join(h) for h in hands]
        [bot.post_message(command.channel_id, h) for h in hands]
        return
    
    deck = list(range(52))

    # add joker
    if command.has_arg() and command.arg.split(" ")[-1][0].lower() == "j":
        deck.append(-1)

    # set number to deal
    if command.has_arg() and command.arg.split(" ")[0].isnumeric():
        cards = min(max(int(command.arg.split(" ")[0]), 1), len(deck))
    else:
        cards = 1

    shuffle(deck)
    deck = deck[:cards]
    deck.sort()

    response = [emojify(i) for i in deck]

    bot.post_message(command.channel_id, "".join(response))
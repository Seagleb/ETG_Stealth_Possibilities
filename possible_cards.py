import json
import re

CARD_LIST_PATH = "F:\Development\Projects\Python\Eternal\eternal-cards.json"


def get_all_stealth_cards():
    """Returns a list of all the Stealth Cards"""

    class StealthCard:
        def __init__(self, card_info):
            self.name = card_info["Name"]
            self.img_url = card_info["ImageUrl"]
            self.cost = card_info["Cost"]
            self.description = card_info["CardText"]
            self.intrigue = False
            ## CHECK DIVISIBILITY FOR INTRIGUE % 2, whatever intrigue cost

            if "Intrigue" in card_info["CardText"]:
                self.intrigue = True

            if card_info["Influence"]:
                self.influence = {
                    "F": card_info["Influence"].count("F"),
                    "T": card_info["Influence"].count("T"),
                    "J": card_info["Influence"].count("J"),
                    "P": card_info["Influence"].count("P"),
                    "S": card_info["Influence"].count("S"),
                }
            else:
                self.influence = {"F": 0, "T": 0, "J": 0, "P": 0, "S": 0}

    all_stealth_cards = list()

    with open(CARD_LIST_PATH) as data_file:
        data = json.load(data_file)
        for row in data:
            try:
                if re.search("Stealth.*;", row["CardText"]):
                    all_stealth_cards.append(StealthCard(row))
            except KeyError:
                """Card does not contain Card Text."""
                pass

    return all_stealth_cards


def influence_req_met(card_influence, opponent_influence):
    """Compare two influence dictionaries to see if the player covers influence cost of card"""

    req_met = True
    for keys in opponent_influence:
        if card_influence[keys] > opponent_influence[keys]:
            req_met = False
    return req_met


def list_possible_cards(all_stealth_cards, cost, opponent_influence):
    """Return list of stealth cards that meet the given cost and influence requirements"""

    possible_cards = list()

    for card in all_stealth_cards:
        if (
            card.cost == cost and influence_req_met(card.influence, opponent_influence)
        ) or (
            card.cost <= cost
            and influence_req_met(card.influence, opponent_influence)
            and card.intrigue
        ):
            possible_cards.append(card)
            print(f"Name = {card.name}")
            print(f"Cost = {card.cost}")
            print(f"Influence = {card.influence}")
            print("----------")

    return possible_cards


if __name__ == "__main__":
    all_stealth_cards = get_all_stealth_cards()

    opponent_influence = {"F": 0, "T": 5, "J": 3, "P": 0, "S": 0}

    possible_cards = list_possible_cards(all_stealth_cards, 5, opponent_influence)

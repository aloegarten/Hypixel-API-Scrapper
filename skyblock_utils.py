# Importing
import requests # For HTTP req
import json 
from pprint import pprint 
import statistics # To calculate mean/median/std dev/etc

search_string = input("Enter the string you want to search for in the item names: ")
item_rarity = input("Enter the rarity of the items you want to filter by: ")
enchant = input("Enter the enchant you want to filter by: ")


AH = []
uuid = []
player = []

def get_info(call):
    r = requests.get(call)
    return r.json()

def getAH(): # Stores all the AH data values into an array

    global AH

    GrabNumPage = get_info("https://api.hypixel.net/skyblock/auctions?page=0")

    for page in range(1, GrabNumPage.get("totalPages", 0) + 1):

        get_info(f"https://api.hypixel.net/skyblock/auctions?page={page}")

        current_page = get_info(f"https://api.hypixel.net/skyblock/auctions?page={page}")
        AH += current_page.get("auctions", [])

    return AH

getAH()


idx = 0

def BINCLAIM():
    for i in AH:
        global idx
        current = AH[idx]
        currentBin = current["bin"]
        status = current["claimed"]

        if False == currentBin or True == status:
            del(AH[idx])

        idx += 1

idx2 = 0

def getUUID():
    for i in AH:
        global idx2
        current2 = AH[idx2]
        uuid.append(current2["auctioneer"])
        idx2 += 1

idx3 = 0

def printAH():
    for i in AH:
        global idx3
        get_info(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid[idx3]}")

        data = get_info(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid[idx3]}")
            
        print(AH[idx3]["item_name"],":", data["name"],":", AH[idx3]["starting_bid"])

        idx3 += 1

def filter_by_item(name, rarity):
    global AH
    AH = [auction for auction in AH if name in auction['item_name'] and auction['tier'] == rarity]

def sort_by_price():
    global AH
    AH = sorted(AH, key=lambda x: x['starting_bid'])

def filter_by_enchant(enchant):
    global AH
    AH = [auction for auction in AH if enchant in auction['item_lore']]



BINCLAIM()
filter_by_item(search_string, item_rarity)
filter_by_enchant(enchant)
sort_by_price()
getUUID()
printAH()



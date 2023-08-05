
from pathlib import Path
import json
import os


def getListGames(split="v1"):

    #  if single split, convert into a list
    if not isinstance(split, list):
        split = [split]
    
    # if an element is "v1", convert to  train/valid/test
    if "all" in split:
        split = ["train", "valid", "test", "challenge"]
    if "v1" in split:
        split.pop(split.index("v1"))
        split.append("train")
        split.append("valid")
        split.append("test")

    listgames = []
    # loop over splits
    for spl in split: 
        if spl == "train":
            jsonGamesFile = Path(__file__).parent / "data/SoccerNetGamesTrain.json"
        elif spl == "valid":
            jsonGamesFile = Path(__file__).parent / "data/SoccerNetGamesValid.json"
        elif spl == "test":
            jsonGamesFile = Path(__file__).parent / "data/SoccerNetGamesTest.json"
        elif spl == "challenge":
            jsonGamesFile = Path(__file__).parent / "data/SoccerNetGamesChallenge.json"

        with open(jsonGamesFile, "r") as json_file:
            dictionary = json.load(json_file)

        for championship in dictionary:
            for season in dictionary[championship]:
                for game in dictionary[championship][season]:

                    listgames.append(os.path.join(championship, season, game))
                    
    return listgames


if __name__ == "__main__":
    print(len(getListGames(["v1", "challenge"])))

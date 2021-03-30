from bs4 import BeautifulSoup
import requests
from urllib import request
import os
import time
import json

dataFileName = "data_file_v1.json"
nbaURL = "https://www.nba.com"

dataArray = []

try:
    r = requests.get(nbaURL + "/teams")
    source = BeautifulSoup(r.content, "html.parser")

    teamTable = source.find_all("div", attrs={"class": "TeamFigure_tfContent__2osIO"})

    teamLinks = []
    teamNames = []

    for team in teamTable:
        teamLinks.append(
            team.findAll(
                "a",
                attrs={
                    "class": "TeamFigureLink_teamFigureLink__3uOct Anchor_complexLink__2NtkO"
                },
            )[0]["href"]
        )
        teamNames.append(team.findAll("a")[0].text)

    checkFileEmpty = False

    newStartingIndex = 0
    playersInFileList = []

    if os.path.exists(dataFileName):
        with open(dataFileName, "r") as f:
            try:
                readedFile = json.load(f)
                print("loaded that: ", readedFile)
            except:
                checkFileEmpty = True
            if not checkFileEmpty:
                lastTeamName = readedFile[-1].get("team").get("teamName")
                print("last" + lastTeamName)
                for player in readedFile:
                    playersInFileList.append(player.get("playerName"))
                newStartingIndex = teamNames.index(lastTeamName)

    for teamIndex, teamLink in enumerate(teamLinks[newStartingIndex:]):
        # time.sleep(1)
        teamName = teamNames[teamIndex]

        r2 = requests.get(nbaURL + teamLink)
        teamSource = BeautifulSoup(r2.content, "html.parser")

        teamImgLink = teamSource.find_all(
            "img", attrs={"class": "TeamHeader_logo__9xcls TeamLogo_logo__1CmT9"}
        )[0]["src"]
        teamRecord = teamSource.find_all(
            "div", attrs={"class": "TeamHeader_record__609BJ"}
        )[0].text
        teamWebsiteLink = (
            teamSource.find_all("ul", attrs={"class": "flex p-0 m-0 flex-nowrap"})[0]
            .find_all("a")[0]
            .text
        )

        rosterTable = (
            teamSource.find_all(
                "div", attrs={"class": "MockStatsTable_statsTable__2edDg"}
            )[0]
            .find_all("tbody")[0]
            .find_all("tr")
        )

        for playerIndex, player in enumerate(rosterTable):
            # time.sleep(1)

            playerName = player.find_all(
                "a", attrs={"class": "Anchor_complexLink__2NtkO"}
            )[0].text

            print(playerName)
            print(playersInFileList)
            if playerName in playersInFileList:
                continue

            playerLink = player.find_all(
                "a", attrs={"class": "Anchor_complexLink__2NtkO"}
            )[0]["href"]
            playerNumber = player.find_all("td")[1].text
            playerPosition = player.find_all("td")[2].text
            playerHeight = player.find_all("td")[3].text
            playerWeight = player.find_all("td")[4].text
            playerAge = player.find_all("td")[6].text
            r3 = requests.get(nbaURL + playerLink)
            playerSource = BeautifulSoup(r3.content, "html.parser")

            playerImgLink = playerSource.find_all(
                "img",
                attrs={
                    "class": "PlayerImage_image__1smob w-10/12 mx-auto mt-16 md:mt-24"
                },
            )[0]["src"]

            data = {
                "playerName": playerName,
                "playerNumber": playerNumber,
                "playerPosition": playerPosition,
                "playerHeight": playerHeight,
                "playerWeight": playerWeight,
                "playerAge": playerAge,
                "playerLink": nbaURL + playerLink,
                "playerImgLink": playerImgLink,
                "team": {
                    "teamName": teamName,
                    "teamLink": nbaURL + teamLink,
                    "teamImgLink": teamImgLink,
                    "teamRecord": teamRecord,
                    "teamWebsiteLink": teamWebsiteLink,
                },
            }

            dataArray.append(data)
            # print(data)

        with open(dataFileName, "r+") as write_file:
            try:
                readedFile = json.load(write_file)
                print(readedFile)
                print("**")
                print(readedFile[0])
                print("**")
                print(readedFile[0][0])

                readedFile.append(dataArray)
                json.dump(readedFile, write_file, indent=4)
            except:
                json.dump(dataArray, write_file, indent=4)


except:
    with open(dataFileName, "r+") as write_file:
        try:
            readedFile = json.load(write_file)
            readedFile.append(dataArray)
            json.dump(readedFile, write_file, indent=4)
        except:
            json.dump(dataArray, write_file, indent=4)

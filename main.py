import requests
import time


def get_games():
    schedule_url = "https://statsapi.web.nhl.com/api/v1"

    schedule_response = requests.get(schedule_url + "/schedule")

    schedule_data = schedule_response.json()
    # print(schedule_data)
    TodayGames = []
    for date in schedule_data["dates"]:
        print(date["date"])
        for game in date["games"]:
            print("gameID: " + str(game["gamePk"]) + "  " + game["teams"]["away"]["team"]["name"] + " vs. " +
                  game["teams"]["home"]["team"]["name"])
            TodayGames.append(
                {'gameid': str(game["gamePk"]), 'gametitle': game["teams"]["away"]["team"]["name"] + " vs. " +
                                                             game["teams"]["home"]["team"]["name"]})

    print(TodayGames)
    return TodayGames


def get_shots(TodayGames):
    live_url = "https://statsapi.web.nhl.com/api/v1/game/"
    url_suffix = "/feed/live"

    for id in TodayGames:

        game_shots = {'GameID': id['gameid'], 'Teams': id['gametitle'], 'Shots': []}
        response_game = requests.get(live_url + id['gameid'] + url_suffix)

        game_data = response_game.json()

        if game_data['liveData']['plays']['allPlays']:
            for result in game_data['liveData']['plays']['allPlays']:
                if result['result']['eventTypeId'] == 'SHOT':
                    shot = (result['result']['description'] + " | " + "Period: " + str(
                        result['about']['period']) + " " + "Period Time Remaining : " + str(
                        result['about']['periodTimeRemaining']))
                    game_shots['Shots'].append(shot)
                else:
                    game_shots['Shots'].append("NO SHOTS")
        else:
            game_shots['Shots'].append("NO SHOTS")

        # print(game_shots)

        print('Game: ' + id['gametitle'])
        print(game_shots['Shots'][-1])
        print('________________________________________')



get_shots(get_games())
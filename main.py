import requests
import time


def get_games():
    schedule_url = "https://statsapi.web.nhl.com/api/v1"

    schedule_response = requests.get(schedule_url + "/schedule")

    schedule_data = schedule_response.json()
    print(schedule_data)
    TodayGames = []
    for date in schedule_data["dates"]:

        print(date["date"])
        for game in date["games"]:
            #if game['status']['abstractGameState'] == 'Live':
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
    full_shot_list = []
    while True:

        for id in TodayGames:


            game_shots = {'GameID': id['gameid'], 'Teams': id['gametitle'], 'Shots': []}
            response_game = requests.get(live_url + id['gameid'] + url_suffix)

            game_data = response_game.json()

            if game_data['liveData']['plays']['allPlays']:
                for result in game_data['liveData']['plays']['allPlays']:
                    if result['result']['eventTypeId'] == 'SHOT':
                        shot = (result['result']['description'] + " | " + "Period: " + str(
                            result['about']['period']) + " " + " | " +"Period Time Remaining : " + str(
                            result['about']['periodTimeRemaining']))
                        game_shots['Shots'].append(shot)


            #else:
                #game_shots['Shots'].append("NO SHOTS")

            # print(game_shots)
            if game_data['liveData']['plays']['allPlays']:
                print('Game: ' + id['gametitle'])
                #for shot in reversed(game_shots['Shots']):
                    #print(shot)
                #print('________________________________________')
                new_shot_list = game_shots['Shots']
                for item in new_shot_list:
                    if item not in full_shot_list:
                        full_shot_list.append(item)
                        print(item)


        time.sleep(10)

get_shots(get_games())

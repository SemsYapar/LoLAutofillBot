#Coded by Sems
import requests, json, time
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#lockfile info
port,password,protocol = open("C:\\Riot Games\\League of Legends\\lockfile", "r").read().split(":")[2:]
s = requests.Session()
s.auth = ("riot", password)

#create lobby
s.post(f'{protocol}://127.0.0.1:{port}/lol-lobby/v2/lobby', data=json.dumps({'queueId': 430}),verify=False)

#start find match
s.post(f'{protocol}://127.0.0.1:{port}/lol-lobby/v2/lobby/matchmaking/search',verify=False)

#when game start
while s.get(f'{protocol}://127.0.0.1:{port}/lol-gameflow/v1/session',verify=False).json()['gameClient'].get('running') == False:
    time.sleep(10)

    #when found match
    if s.get(f'{protocol}://127.0.0.1:{port}/lol-lobby/v2/lobby/matchmaking/search-state',verify=False).json().get('searchState') == 'Found':
        print("Maç bulundu")
        #accept match
        s.post(f'{protocol}://127.0.0.1:{port}/lol-matchmaking/v1/ready-check/accept',verify=False)

    #when selecting start get orderId
    if s.get(f'{protocol}://127.0.0.1:{port}/lol-champ-select/v1/session',verify=False).json().get('localPlayerCellId'):
        orderId = s.get(f'{protocol}://127.0.0.1:{port}/lol-champ-select/v1/session',verify=False).json().get('localPlayerCellId')
        #select champ
        s.patch(f'{protocol}://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{orderId}', data=json.dumps({"championId": "1", 'completed': True}),verify=False)
    

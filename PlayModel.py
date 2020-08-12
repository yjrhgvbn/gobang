import requests

def joinGame(username):

    user=str(username)
    password=str(0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14)

    response = requests.get("http://202.207.12.223:8000/join_game/?user="+user+"&password=0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14&data_type=json")
    print(response.json())
    return response.json()['game_id']

def playGame(game_id,username,c):
    straa = 'http://202.207.12.223:8000/play_game/' + str(
        game_id) + '/?user='+str(username)+'&password=0x53406d6435b10e5da360c0a73da3a92e2fd86c72570a28562e8da2137e415f9548ee6b4b104fca06ac41b8e8f9050f15e8a29a5795faa6d372cab1d7d32e6b8d8a3c33f57192fc0a8045ab31d392a7826464e4f4651d1f67e9eba6eaa399ef498e312502dbe72deb135c819dc9f389906869b6f198b1d1958ce36b1b1a70ef14&coord=' + c

    response = requests.get(straa)
    #print(response.url)
    print(response.json())
    return response.json()

def check_game(game_id):
    import requests
    response = requests.get("http://202.207.12.223:8000/check_game/"+str(game_id))
    #print(response.url)
    #print(response.json())
    return response.json()

def toChar(n):
    return chr(n + ord('a'))

def toInt(c):
    return ord(c) - ord('a')
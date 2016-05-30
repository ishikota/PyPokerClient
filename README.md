# PyPokerClient
Python poker client using websocket to communicate with [PokerServer](https://github.com/ishikota/PokerServer)

# Setup

## 1. Clone this repository
```
git clone https://github.com/ishikota/PyPokerClient
```
We assume you cloned this repository to `~/PyPokerClient` in following explanation.

## 2. Install dependencies by pip
```
cd ~/PyPokerClient
pip install -r requirements.txt
```
This poker client library uses
- [request](https://github.com/kennethreitz/requests/) as HttpClient
- [websocket-client](https://github.com/liris/websocket-client) as websocket client

## 3. Run PokerServer [Under Construction]
Run poker server by following this link and check its host name and port number.  
We assume `host="localhost"`, `port=300` in following explanation.

## 4. Run poker client and establish connection with PokerServer
Here, we use sample player which included in this repository.
You should use your own poker player if possible.
```
cd ~/PyPokerClient
./script/run_client --player_path ./poker_client/players/template_poker_player.py --host localhost --port 3000
```

## 5. Under Construction
TODO

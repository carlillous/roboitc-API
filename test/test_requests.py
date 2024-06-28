import time
import requests

#response = requests.put('http://192.168.100.34:80/motor/start')
#print(response.json())
time.sleep(3)
#TEST FORWARD
response = requests.put('http://192.168.100.34:80/motor/move',
                        json={'speed': 30,'direction': 'forward'}, headers={'Content-Type': 'application/json'})
print(response.json())
#time.sleep(1)
#response = requests.put('http://192.168.100.34:80/motor/move',
#                        json={'speed': 30,'direction': 'forward', 'turn':'right'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
#response = requests.put('http://192.168.100.34:80/motor/move',
#                        json={'speed': 30,'direction': 'forward','turn':'left'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
##TEST BACKWARD
#response = requests.put('http://192.168.100.34:80/motor/move',
#                       json={'speed': 30,'direction': 'backward'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
#response = requests.put('http://192.168.100.34:80/motor/move',
#                       json={'speed': 30,'direction': 'backward', 'turn':'right'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
#response = requests.put('http://192.168.100.34:80/motor/move',
#                       json={'speed': 30,'direction': 'backward','turn':'left'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
##TEST TURN
#response = requests.put('http://192.168.100.34:80/motor/move',
#                       json={'speed': 30,'turn':'right'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
#response = requests.put('http://192.168.100.34:80/motor/move',
#                       json={'speed': 30,'turn':'left'}, headers={'Content-Type': 'application/json'})
#print(response.json())
#time.sleep(1)
#response = requests.put('http://192.168.100.34:80/motor/stop')
#print(response.json())
#
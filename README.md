# InferenceServer
An ML inference server to serve Image classification over HTTP

## Requerements
`docker`, `docker-compose`, `curl`

On linux machine, use the following commands (uses apt)

`sudo apt install docker`

`sudo apt install docker-compose` [Install this for one step docker setup]

`sudo apt install curl`


## How to start the app (one step app setup)
Step1: Download the repo, and cd into the repo

Step2: `sudo docker-compose up`

This will start the server at localhost:5000

For developer's, if you change anything in the source, please run `sudo docker-compose build` before `sudo docker-compose up`. This re-builds the docker with changes in the source file.

## How to query inference
Once the server is on, you can either use UI or command line interface.

### Command line interface
[TODO]: Create route to upload, predict and return response
curl -F "file=@persian.jpg" http://0.0.0.0:5000/upload

### UI interface
[TODO]: Update this

Project description: https://docs.google.com/document/d/1arkxU7LA2C-KjFfyAwzbUvSG6qoIBv9FJJze2V6TzEk/edit
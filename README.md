# InferenceServer
An ML inference server to serve Image classification over HTTP

## Requirements
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
The app can be accessed via http://0.0.0.0:5000/ and images can be uploaded by clicking on or dragging images to the drop zone. To test a new image simply click on the whitespace around the thumbnail (see image below). There are also some example images you can use to test the classifier.

<p align="center">
<img src="./readme_images/ui_image.png" style="max-width:500px;"/>
</p>


Project description: https://docs.google.com/document/d/1arkxU7LA2C-KjFfyAwzbUvSG6qoIBv9FJJze2V6TzEk/edit

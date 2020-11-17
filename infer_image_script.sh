echo "Quering an image for inference and printing the string response for the inference output"
curl -X POST -F "file=@upload/cat.jpg" http://0.0.0.0:5000/uploadajax
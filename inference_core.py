import os
import torch
from torchvision import transforms
from PIL import Image
import pandas as pd
import numpy as np

class inference_engine:
    def __init__(self):
        self.processing_pipeline = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
            ])
        self.model = torch.hub.load('pytorch/vision:v0.6.0',
                                    'densenet121', pretrained=True)
        self.model.eval()
        imagenet_data = pd.read_csv(os.path.join(os.getcwd(),
                                                 'imagenet_labels.txt'),
                                    sep=' ',
                                    names=['wnid', 'id', 'name']).sort_values('wnid')
        self.IMAGENET_LABELS = np.array(imagenet_data['name'])

    def get_class_probabilities(self, image, top_k=5):
        """
        Arguments:
            image: Image buffer
            top_k: Number of classes to predict, sorted by prediction probabily
        Returns:
            a list of tuple having class label and the corresponding probability
            The list is sorted with highest probability first
            The size is the list is top_k
        """
        # Preprocess the image
        input_tensor = self.processing_pipeline(image)
        input_batched = input_tensor.unsqueeze(0)

        # Use GPU if possible
        if torch.cuda.is_available():
            input_batched = input_batched.to('cuda')
            self.model.to('cuda')
        
        # Run model
        with torch.no_grad():
            output = self.model(input_batched)
        
        # Normalize the results
        predictions = (torch.nn.functional.softmax(output[0], dim=0)).detach().numpy()

        topk_predictions = predictions.argsort()[-top_k:][::-1]
        result = []
        for idx in topk_predictions:
            label = self.IMAGENET_LABELS[idx]
            score = predictions[idx]
            result.append((label, score))
        return result

        




def make_prediction(image_path):
    # load densenet121
    model = torch.hub.load('pytorch/vision:v0.6.0', 'densenet121', pretrained=True)
    model.eval()

    # before classifying image needs to be preprocessed
    # https://pytorch.org/hub/pytorch_vision_densenet/
    input_image = Image.open(image_path)

    # apply preprocessing
    input_tensor = preprocess_image(input_image)

    # create a mini-batch
    input_batch = input_tensor.unsqueeze(0)

    # move the input batch and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    # run model
    with torch.no_grad():
        output = model(input_batch)

    predictions = (torch.nn.functional.softmax(output[0], dim=0)).detach().numpy()  # this normalizes the scores

    top5 = predictions.argsort()[-5:][::-1]
    # top1 = IMAGENET_LABELS[np.argmax(predictions)]
    print(top5)  # get top 5 locations

    prediction_str = ''
    for idx in top5:
        label = IMAGENET_LABELS[idx]
        score = predictions[idx]
        prediction_str+= f'{label}, ({score:.04f})\n'
    print(prediction_str)
    return prediction_str

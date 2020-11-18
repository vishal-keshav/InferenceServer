import os
import torch
from torchvision import transforms
import pandas as pd
import numpy as np

class inference_engine:
    def __init__(self):
        # pipeline to preprocess an image, mainly transforming and converting to tensor
        self.processing_pipeline = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
            ])
        # import densenet model
        self.model = torch.hub.load('pytorch/vision:v0.6.0',
                                    'densenet121', pretrained=True)
        self.model.eval()  # set to eval mode
        # read in image labels for imagenet data
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

        # Get the top k predictions
        topk_predictions = predictions.argsort()[-top_k:][::-1]
        result = []
        # Get labels for each of the predictions
        for idx in topk_predictions:
            label = self.IMAGENET_LABELS[idx]
            score = predictions[idx]
            result.append((label, score))
        return result

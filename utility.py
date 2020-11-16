from PIL import Image

def decode_image(image_path):
    """
    Arguments:
        image_path: path of the image
    Returns:
        An image buffer, without any processing
    """
    return Image.open(image_path)

def stringify(predictions):
    """
    Arguments:
        predictions: A list of tuple with class label and probability.
    Returns:
        A string version of the list
    """
    prediction_str = ''
    for label, score in predictions:
        prediction_str+= f'{label}, ({score:.04f})\n'
    return prediction_str

__version_info__ = ('0', '0', '53')
__version__ = '.'.join(__version_info__)
__authors__ = "Silvio Giancola"
__authors_username__ = "giancos"
__author_email__ = "silvio.giancola@kaust.edu.sa"
__github__ = 'https://github.com/SilvioGiancola/SoccerNetv2'


import logging
from SoccerNet.downloader import SoccerNetDownloader
from SoccerNet.utils import getListGames

try:
    from SoccerNet.DataLoader import VideoLoader
except:
    logging.info("Install TensorFlow/PyTorch for VideoLoader")
    pass


try:
    from SoccerNet.featureextractor import FeatureExtractor
except:
    logging.info("Install TensorFlow/PyTorch for FeatureExtractor")
    pass


# try:
# except:
#     logging.info("Install TensorFlow for FeatureExtractor")
#     pass
    
# try:
#     from SoccerNet.DataLoaderTorch import SoccerNetDataLoaderTorch
# except:
#     logging.info("Install Torch for SoccerNetDataLoaderTorch")
#     pass


try:
    from SoccerNet.DataLoaderTensorFlow import SoccerNetDataLoaderTensorFlow
except:
    logging.info("Install TensorFlow for SoccerNetDataLoaderTensorFlow")
    pass



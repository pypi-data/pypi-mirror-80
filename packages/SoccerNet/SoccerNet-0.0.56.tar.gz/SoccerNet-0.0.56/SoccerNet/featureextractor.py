import configparser
from SoccerNet.DataLoaderTorch import ClipDataset, FrameDataset
import math
from tensorflow.keras.models import Model  # pip install tensorflow (==2.3.0)
from tensorflow.keras.applications.resnet import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.preprocessing.image import load_img
from tensorflow import keras
import os
# import argparse
import numpy as np
import cv2  # pip install opencv-python (==3.4.11.41)
import imutils  # pip install imutils
import skvideo.io
from tqdm import tqdm

# from SoccerNet import getListTestGames, getListGames

import torch
import torchvision
import json

from .utils import getListGames
from .utils import getDuration
from .downloader import SoccerNetDownloader

class FeatureExtractor():
    def __init__(self, rootFolder, 
                feature="ResNET",
                video="LQ", 
                back_end="TF2", 
                overwrite=False, 
                #  array=False,
                 crop_resize="crop",
                 preprocess=False,
                 tmp_HQ_videos=None):
        self.rootFolder = rootFolder
        self.feature = feature
        self.video = video
        self.back_end = back_end
        self.verbose = True
        self.crop_resize = crop_resize
        self.overwrite = overwrite
        # self.array = array
        self.preprocess = preprocess

        self.tmp_HQ_videos = tmp_HQ_videos
        if self.tmp_HQ_videos:
            self.mySoccerNetDownloader = SoccerNetDownloader(self.rootFolder)
            self.mySoccerNetDownloader.password = "SoccerNet"

        if "TF2" in self.back_end:

            # create pretrained encoder (here ResNet152, pre-trained on ImageNet)
            base_model = keras.applications.resnet.ResNet152(include_top=True,
                                                            weights='imagenet', input_tensor=None, input_shape=None,
                                                            pooling=None, classes=1000)

            # define model with output after polling layer (dim=2048)
            self.model = Model(base_model.input, outputs=[
                        base_model.get_layer("avg_pool").output])
            self.model.trainable = False
            # model.summary()

            # sanity test for the model with random input
            # IMG_SIZE = image_size = 224
            # IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
            # input_data = np.random.rand(1, *IMG_SHAPE)
            # result = self.model.predict(input_data)
            # if (self.verbose):
            #     print(result[0].shape)

        # elif self.back_end == "PT":

        elif self.back_end == "PT" and "ResNET" in self.feature:
            class Identity(torch.nn.Module):
                def __init__(self):
                    super(Identity, self).__init__()

                def forward(self, x):
                    return x

            self.model = torchvision.models.resnet152(
                pretrained=True, progress=True).cuda()
            self.model.fc = Identity()

        elif self.back_end == "PT" and "R25D" in self.feature:
            class Identity(torch.nn.Module):
                def __init__(self):
                    super(Identity, self).__init__()

                def forward(self, x):
                    return x

            self.model = torchvision.models.video.r2plus1d_18(
                pretrained=True, progress=True).cuda()
            self.model.fc = Identity()

        

    def extractAllGames(self):
        for i_game, game in tqdm(getListGames("all")):
            self.extractGameIndex(i_game)
            # print(game)
            # if self.video =="LQ":
            #     self.extract(video_path=os.path.join(self.rootFolder, game, "1.mkv"))
            #     self.extract(video_path=os.path.join(self.rootFolder, game, "2.mkv"))
            # elif self.video =="HQ":
            #     # self.readINI()
            #     self.extract(video_path=os.path.join(self.rootFolder, game, "1_HQ.mkv"))
            #     self.extract(video_path=os.path.join(self.rootFolder, game, "2_HQ.mkv"))

    def extractGameIndex(self, index):
        print(getListGames("all")[index])
        if self.video =="LQ":
            for vid in ["1.mkv","2.mkv"]:
                self.extract(video_path=os.path.join(self.rootFolder, getListGames("all")[index], vid))
            # self.extract(video_path=os.path.join(self.rootFolder, getListGames("all")[index], "2.mkv"))
        elif self.video == "HQ":

            config = configparser.ConfigParser()
            # config.read(os.path.join(main_dir_HQ, game, 'video.ini'))
            if not os.path.exists(os.path.join(self.rootFolder, getListGames("all")[index], "video_with_duration.ini")) and self.tmp_HQ_videos is not None:
                self.mySoccerNetDownloader.downloadVideoHD(
                    game=getListGames("all")[index], file="video_with_duration.ini")

            config.read(os.path.join(self.rootFolder, getListGames("all")[index], "video_with_duration.ini"))
            for vid in config.sections():
                video_path = os.path.join(self.rootFolder, getListGames("all")[index], vid)
                remove_afterwards = False
                if not os.path.exists(video_path) and self.tmp_HQ_videos is not None:
                    remove_afterwards = True
                    self.mySoccerNetDownloader.downloadVideoHD(game=getListGames("all")[index], file=vid)

                self.extract(video_path=video_path,
                            start=float(config[vid]["start_time_second"]), 
                            duration=float(config[vid]["duration_second"]))
                if remove_afterwards:
                    os.remove(video_path)
                # self.extract(video_path=os.path.join(self.rootFolder, getListGames("all")[index], "2_HQ.mkv"), 
                #             start=float(config["2_HQ.mkv"]["start_time_second"]), 
                #             duration=float(config["2_HQ.mkv"]["duration_second"]))

    def extract(self, video_path, start=None, duration=None):
        print("extract video", video_path, "from", start, duration+start)
        # feature_path = video_path.replace(
        #     ".mkv", f"_{self.feature}_{self.back_end}.npy")
        feature_path = video_path[:-4] + f"_{self.feature}_{self.back_end}.npy"

        if os.path.exists(feature_path) and not self.overwrite:
            return
        if "TF2" in self.back_end:
            # Knowing number of frames from FFMPEG metadata w/o without iterating over all frames
            videodata = skvideo.io.FFmpegReader(video_path)
            (numframe, _, _, _) = videodata.getShape()  # numFrame x H x W x channels
            if self.verbose:
                print("shape video", videodata.getShape())

                
            # metadata = skvideo.io.ffprobe(video_path)
            # # print("metadata", metadata["video"])
            # for entry in metadata["video"]["tag"]:
            #     if list(entry.items())[0][1] == "DURATION":
            #         # print("entry", entry)
            #         duration = list(entry.items())[1][1].split(":")
            #         # print(duration)
            #         time_second = int(duration[0])*3600 + \
            #             int(duration[1])*60 + float(duration[2])
            #         # print(time_second)
            #         fps_video = numframe / time_second

            time_second = getDuration(video_path)
            fps_video = numframe / time_second
            # time_second = numframe / fps_video
            if self.verbose:
                print("duration video", time_second)

            frames = []
            videodata = skvideo.io.vreader(video_path)
            fps_desired = 2
            drop_extra_frames = fps_video/fps_desired

            for i_frame, frame in tqdm(enumerate(videodata), total=numframe):
                # print(i_frame % drop_extra_frames)
                if start is not None:
                    if i_frame < fps_video * start:
                        continue

                if duration is not None:
                    if i_frame > fps_video * (start + duration):
                        break

                if (i_frame % drop_extra_frames < 1):

                    if self.crop_resize == "resize256crop224":  # crop keep the central square of the frame
                        frame = imutils.resize(frame, height=256)  # keep aspect ratio
                        # number of pixel to remove per side
                        off_side_h = int((frame.shape[0] - 224)/2)
                        off_side_w = int((frame.shape[1] - 224)/2)
                        frame = frame[off_side_h:-off_side_h,
                                    off_side_w:-off_side_w, :]  # remove them

                    elif self.crop_resize == "crop":  # crop keep the central square of the frame
                        frame = imutils.resize(frame, height=224)  # keep aspect ratio
                        # number of pixel to remove per side
                        off_side = int((frame.shape[1] - 224)/2)
                        frame = frame[:, off_side:-off_side, :]  # remove them

                    elif self.crop_resize == "resize":  # resize change the aspect ratio
                        # lose aspect ratio
                        frame = cv2.resize(frame, (224, 224),
                                        interpolation=cv2.INTER_CUBIC)

                    else:
                        raise NotImplmentedError()
                    # if self.array:
                    #     frame = img_to_array(frame)
                    frames.append(frame)

            # create numpy aray (nb_frames x 224 x 224 x 3)
            frames = np.array(frames)
            if self.preprocess:
                frames = preprocess_input(frames)
            if duration is not None:
                time_second = duration
            if self.verbose:
                print("frames", frames.shape, "fps=", frames.shape[0]/time_second)

            # predict the featrues from the frames (adjust batch size for smalled GPU)
            features = self.model.predict(frames, batch_size=64, verbose=1)
            if self.verbose:
                print("features", features.shape, "fps=", features.shape[0]/time_second)

        elif self.back_end == "PT" and "ResNET" in self.feature:

            myClips = FrameDataset(video_path=video_path,
                                  FPS_desired=2)

            myClipsLoader = torch.utils.data.DataLoader(myClips, batch_size=1)

            features = []
            for clip in tqdm(myClipsLoader):
                clip = clip.cuda()
                # print(clip.shape)
                feat = self.model(clip)
                # print(feat.shape)
                features.append(feat.detach().cpu())
                # print(len(features))
                # del clip
                # del feat
            print(orch.cat(features).shape)
            features = torch.cat(features).numpy()
            print(features.shape)


        elif self.back_end == "PT" and "R25D" in self.feature:

            myClips = ClipDataset(video_path=video_path, FPS_desired=2, clip_len=16)

            myClipsLoader = torch.utils.data.DataLoader(myClips, batch_size=1)


            features = []
            for clip in tqdm(myClipsLoader):
                clip = clip.cuda()
                # print(clip.shape)
                feat = self.model(clip)
                features.append(feat.detach().cpu())
                # print(len(feats))
                # del clip
                # del feat
            features = torch.cat(features).numpy()
            # print(features.shape)

        # save the featrue in .npy format
        os.makedirs(os.path.dirname(feature_path), exist_ok=True)
        np.save(feature_path, features)


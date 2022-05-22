import time

import torch
import numpy as np
from torchvision import models, transforms

import cv2
from PIL import Image

torch.backends.quantized.engine = 'qnnpack'

#cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v2(pretrained=True, quantize=True)
# jit model to take it from ~20fps to ~30fps
net = torch.jit.script(net)

started = time.time()
last_logged = time.time()
frame_count = 0

fps = 0
with torch.no_grad():
    while True:
        # read frame
        ret, image = cap.read()
        if not ret:
            raise RuntimeError("failed to read frame")

        # log model performance
        frame_count += 1
        now = time.time()
        if now - last_logged > 1:
            fps = frame_count / (now-last_logged)
            print(f"{fps} fps")
            last_logged = now
            frame_count = 0

        cv2.putText(image, f"FPS:{fps}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
        cv2.imshow("img", image)
        cv2.waitKey(1)

        # convert opencv output from BGR to RGB
        image = image[:, :, [2, 1, 0]]
        permuted = image

        # preprocess
        input_tensor = preprocess(image)

        # create a mini-batch as expected by the model
        input_batch = input_tensor.unsqueeze(0)

        # run model
        output = net(input_batch)
        # do something with output ...


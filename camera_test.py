import cv2
import time
import torch
from torchvision import models, transforms

torch.backends.quantized.engine = 'qnnpack'

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 18)

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v2(pretrained=True, quantize=True)
# jit model to take it from ~20fps to ~30fps
net = torch.jit.script(net)
net.eval()

started = time.monotonic()
last_logged = time.monotonic()
frame_count = 0

fps = 0
with torch.no_grad():
    while True:
        ret, image = cap.read()
        if not ret:
            raise RuntimeError("failed to read frame")

        # log model performance
        frame_count += 1
        now = time.monotonic()
        if now - last_logged > 1:
            fps = frame_count / (now-last_logged)
            print(f"{fps} fps")
            last_logged = now
            frame_count = 0

        cv2.putText(image, f"FPS:{fps}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
        cv2.imshow("web camera v1.0", image)
        cv2.waitKey(1)

        # convert opencv output from BGR to RGB
        image = image[:, :, [2, 1, 0]]

        # preprocess
        input_tensor = preprocess(image)

        # create a mini-batch as expected by the model
        input_batch = input_tensor.unsqueeze(0)

        # run model
        output = net(input_batch)
        # do something with output ...


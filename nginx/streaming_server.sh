#!/bin/bash

ffmpeg \
    -f video4linux2 -framerate 25 -video_size 1280x720 -i /dev/video2 \
    -f alsa -ac 2 -i sysdefault:CARD=gadget \
    -c:v libx264 -b:v 1600k -preset ultrafast \
    -x264opts keyint=50 -g 25 -pix_fmt yuv420p \
    -c:a aac -b:a 128k \
    -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf: \
text='CLOUD DETECTION CAMERA 01 UTC-3 %{localtime\:%Y-%m-%dT%T}': fontcolor=white@0.8: fontsize=16: x=10: y=10: box=1: boxcolor=black: boxborderw=6" \
    -f rtp_mpegts "rtp://192.168.0.86:6000?ttl=2"


ffmpeg -f video4linux2 -framerate 25 -video_size 640x480 -i /dev/video0 \
    -f alsa -ac 2 -i sysdefault:CARD=gadget \
    -c:v libx264 -b:v 1600k -preset ultrafast \
    -x264opts keyint=50 -g 25 -pix_fmt yuv420p \
    -c:a aac -b:a 128k \
    -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf: \
text='CLOUD DETECTION CAMERA 01 UTC-3 %{localtime\:%Y-%m-%dT%T}': fontcolor=white@0.8: fontsize=16: x=10: y=10: box=1: boxcolor=black: boxborderw=6" \
    -f rtp_mpegts "rtp://192.168.0.86:5000?ttl=2"

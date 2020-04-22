# Gstreamer-analytics


Clone the Gstreamer Analtyics repo
```
mkdir -p ~/gva
# Download GVA repository
git clone https://github.com/opencv/gst-video-analytics ~/gva/gst-video-analytics
cd ~/gva/gst-video-analytics
```

Pull the latest Gstreamer analytics docker image
```
docker pull adi6496/gst-video-analytics:latest
```

 Connect the host's system X server from the Docker image. Run this command to give access to display
 ```
  xhost local:root
  ```
  
 Run container:
 ```
 docker run -it --privileged --net=host \
\
-v ~/.Xauthority:/root/.Xauthority \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=$DISPLAY \
-e HTTP_PROXY=$HTTP_PROXY \
-e HTTPS_PROXY=$HTTPS_PROXY \
-e http_proxy=$http_proxy \
-e https_proxy=$https_proxy \
\
-v ~/gva/data/models/intel:/root/intel_models:ro \
-v ~/gva/data/models/common:/root/common_models:ro \
-e MODELS_PATH=/root/intel_models:/root/common_models \
\
-v ~/gva/data/video:/root/video-examples:ro \
-e VIDEO_EXAMPLES_DIR=/root/video-examples \
\
adi6496/gst-video-analytics:latest
```
  
Inside the container you need to install youtube-dl if you want to livestream videos from youtube

Install youtube-dl library to download youtube videos
```
apt-get update
apt-get install python-pip
pip install youtube-dl
```
List of all the models
```
cd intel_models/intel && ls
```
Open up a different terminal
```
docker ps
```

Use the container id to copy files to the container
```
docker cp parse.py <container-id>:/root/ 
```
Run parse.py to start a gstreamer pipeline with webcam or a live stream from youtube and provide the path to a model with -d argument
```
python3 parse.py -d intel_models/intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml
```

The parse.py file generates index.m3u8 files and the corresponding segment files for HLS. 

To be done - This container will also contain a sender.py file which sends the m3u8 file along with segments files to Kafka http bridge endpoint.


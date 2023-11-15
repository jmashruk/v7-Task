#!/bin/bash
# COCO 2017 dataset http://cocodataset.org
# Download command: bash ./scripts/get_coco.sh

# Download/unzip labels
d='./' # unzip directory
url=https://github.com/ultralytics/yolov5/releases/download/v1.0/
f='coco2017labels-segments.zip' # or 'coco2017labels.zip', 68 MB
echo 'Downloading' $url$f ' ...'
curl -L $url$f -o $f && unzip -q $f -d $d && rm $f & # download, unzip, remove in background

# Download/unzip images
d='./coco/images' # unzip directory
url=http://images.cocodataset.org/zips/
f2='val2017.zip'   # 1G, 5k images
echo 'Downloading' $url$f2 '...'
curl -L $url$f2 -o $f2 && unzip -q $f2 -d $d && rm $f2 & # download, unzip, remove in background

wait

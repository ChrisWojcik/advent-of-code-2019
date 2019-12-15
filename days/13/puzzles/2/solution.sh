#!/bin/bash
mkdir tmp
mkdir tmp2
python program.py < input

FILE_COUNT=$(($(ls -f tmp | wc -l) - 2))

for (( i = 1; i <= $FILE_COUNT; i++ )) ; do
  convert -size 540x540 xc:black -font "CourierNew" -pointsize 16 -fill white -annotate +65+30 "@tmp/$i.txt" tmp2/$i.png
done

ffmpeg -r 60 -f image2 -s 540x540 -i tmp2/%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p visualization.mp4

rm -rf tmp
rm -rf tmp2

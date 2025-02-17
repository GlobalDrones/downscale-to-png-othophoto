# downscale-to-png-othophoto
This present code receives a directory with some orthophotos.tif and translate it into orthophotos.png with a downscale of 4096x4096 without lose the original shape.

## Requirements
- You just need to run ```pip install -r requirements.txt``` and the pip will install all necessary requirements to run the source code.
- The main directory must follow this struct:
  ***
       main_directory/
          ---------ortho_tif/
                  ---------orthophoto_1.tif
                  ---------orthophoto_2.tif
                  ---------orthophoto_3.tif
                  ---------orthophoto_4.tif
  ***

## How to use 
To use this code run the cmd:```pyhton compressor.py main_directory/path```.


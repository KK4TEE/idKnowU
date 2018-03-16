# idKnowU

Use augmented reality, facial recognition, and machine learning to create holographic name tags for the people you meet. No more awkwardly forgetting someone's name!

[unity-download]:                 https://unity3d.com/unity/whats-new/unity-2017.2.1
[unity-version-badge]:            https://img.shields.io/badge/Current%20Unity%20Editor%20Version-2017.2.1f1-green.svg
[![Github Release][unity-version-badge]][unity-download]

![HoloLens](doc/img/idKnowU_HoloLens.jpg?raw=true "A through-lens look at our idKnowU running on the HoloLens")
* [`capture.py`](/capture.py) is used to build the information and face-matching data sets.
* [OpenFace](https://github.com/cmusatyalab/openface) is used to process the data.
* [`idknowuserver.py`](/server/idknowuserver.py) is used to host the processed data to the network.
* Unity / HoloLens is used to supply streaming video to be inspected and display results to the user.


## Capture.py

| [`capture.py`](/capture.py) is used to build the information and face-matching data sets. It provides text and photo capture tools and automatically puts it into a folder structure based on the user's supplied name. |![Capture.py Demonstration](doc/img/capture_py_screenshot.png?raw=true "Information capture script used to provide training data for machine learning")|
|:-------:|:---:|



## OpenFace
Use the following commands to process the data from capture.py into usable results:

From your shell (it will open an interactive docker container with openFace already configured):
`docker run -p 9000:9000 -p 8000:8000 -v C:/idKnowU:/root/openface/idknowu -t -i bamos/openface /bin/bash -l `

From inside the openFace container:

| Function        | Command          |
| :--------: |:-------------------------------------------|
| Size up the training pictures and extract the faces from the them    | ```for N in {1..8}; do /root/openface/util/align-dlib.py /root/openface/idknowu/training-images align outerEyesAndNose /root/openface/idknowu/aligned-data --size 96 & done``` |
| Compute the features of the faces      | ```/root/openface/batch-represent/main.lua -outDir /root/openface/idknowu/features-data -data /root/openface/idknowu/aligned-data```     |
| Train the recognizer |  ```/root/openface/demos/classifier.py train /root/openface/idknowu/features-data```     |
| Test and see if it works |  ```/root/openface/demos/classifier.py infer /root/openface/idknowu/features-data/classifier.pkl /root/openface/idknowu/test/capture.jpg```|
| Start the script that will repeatedly check the filesystem for new face captures | ```python /root/openface/idknowu/openface_classifier.py infer /root/openface/idknowu/features-data/classifier.pkl /root/openface/idknowu/server/images/latest_capture.jpg``` |

The last command records and updates the file `/root/openface/idknowu/server/` with the face it detects in `server/latest_capture.jpg` and loops as quickly as possible (waiting half a second on error).


## server/idknowuserver.py
* Run this on your local machine from the server directory

## Unity Project
* Install to HoloLens or run from the editor
* Note: In Unity use 127.0.0.1 as the server if on local device or your actual local IP if from another device
* If the file fails to work on first load, you may need to scrap the cache files and rebuild. It saves more than 70MiB to load to GitHub without them, but can occasionally cause some issues on first build.

## Project History
This project was created for the Creating Reality Hackathon, hosted 2018-03-12 through 2018-03-14 at USC in Los Angeles, California, USA.


## Additional information:
* Requirements: [Python3](https://www.python.org/downloads/), [openCV](https://pypi.python.org/pypi/opencv-python), [OpenFace](https://github.com/cmusatyalab/openface)
* idKnowU License: [MIT](/LICENSE)
* Dependencies retain their own respective licenses



## References:
>https://cmusatyalab.github.io/openface
>@techreport{amos2016openface,
>  title={OpenFace: A general-purpose face recognition
>    library with mobile applications},
>  author={Amos, Brandon and Bartosz Ludwiczuk and Satyanarayanan, Mahadev},
>  year={2016},
>  institution={CMU-CS-16-118, CMU School of Computer Science},
>}

>B. Amos, B. Ludwiczuk, M. Satyanarayanan,
>"Openface: A general-purpose face recognition library with mobile applications,"
>CMU-CS-16-118, CMU School of Computer Science, Tech. Rep., 2016.
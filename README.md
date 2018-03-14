# idKnowU

Use augmented reality, facial recognition, and machine learning to create holographic name tags for the people you meet. No more awkwardly forgetting someone's name!

capture.py is used to build the information and face-matching data sets.
openFace is used to process the data.
idknowuserver.py is used to host the processed data to the network.
Unity / HoloLens is used to supply streaming video to be inspected and display results to the user.

This project was created for the Creating Reality Hackathon, hosted 2018-03-12 through 2018-03-14 at USC in Los Angeles, California, USA.

Requirements: Python3, openCV, OpenFace
License: MIT



References:
https://cmusatyalab.github.io/openface
@techreport{amos2016openface,
  title={OpenFace: A general-purpose face recognition
    library with mobile applications},
  author={Amos, Brandon and Bartosz Ludwiczuk and Satyanarayanan, Mahadev},
  year={2016},
  institution={CMU-CS-16-118, CMU School of Computer Science},
}

B. Amos, B. Ludwiczuk, M. Satyanarayanan,
"Openface: A general-purpose face recognition library with mobile applications,"
CMU-CS-16-118, CMU School of Computer Science, Tech. Rep., 2016.
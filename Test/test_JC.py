import RPi.GPIO as GPIO
from time import sleep

# Motor A
enA = 25
in1 = 23
in2 = 24
# Motor B
enB = 22
in3 = 17
in4 = 27
# Setup as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(enA, GPIO.HIGH)
GPIO.output(enB, GPIO.HIGH)


# La Croix Flavor Detector - Machine Learning on Raspberry Pi
#
# Michael D'Argenio
# mjdargen@gmail.com
# https://dargenio.dev
# https://github.com/mjdargen
# Created: February 6, 2020
# Last Modified: February 13, 2021
#
# This program uses Tensorflow and OpenCV to detect objects in the video
# captured from your webcam. This program is meant to be used with machine
# learning models generated with Teachable Machine.
#
# Teachable Machine is a great machine learning model trainer and generator
# created by Google. You can use Teachable Machine to create models to detect
# objects in images, sounds in audio, or poses in images. For more info, go to:
# https://teachablemachine.withgoogle.com/
#
# For this project, you will be generating a image object detection model. Go
# to the website, click "Get Started" then go to "Image Project". Follow the
# steps to create a model. Export the model as a "Tensorflow->Keras" model.
#
# To run this code in your environment, you will need to:
#   * Install Python 3 packages & library dependencies
#       * Use installation shell script
#   * Export your teachable machine tensorflow keras model and unzip it.
#       * You need both the .h5 file and labels.txt
#   * Update model_path to point to location of your keras model
#   * Update labels_path to point to location of your labels.txt
#   * Adjust width and height of your webcam for your system
#       * Adjust frameWidth with your video feed width in pixels
#       * Adjust frameHeight with your video feed height in pixels
#       * My RPi Camera v1.3 works well with 1024x768
#   * Set your confidence threshold
#       * conf_threshold by default is 90
#   * If video does not show up properly, use the matplotlib implementation
#       * Uncomment "import matplotlib...."
#       * Comment out "cv2.imshow" and "cv2.waitKey" lines
#       * Uncomment plt lines of code below
#   * Run "sudo python3 tm_obj_det.py"

import multiprocessing
import numpy as np
import cv2
import tensorflow.keras as tf
import pyttsx3
import math
import os
# use matplotlib if cv2.imshow() doesn't work
# import matplotlib.pyplot as plt

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def main():

    # read .txt file to get labels
    labels_path = f"{/home/pi/JCho/Test}/labels.txt"
    # open input file label.txt
    labelsfile = open(labels_path, 'r')

    # initialize classes and read in lines until there are no more
    classes = []
    line = labelsfile.readline()
    while line:
        # retrieve just class name and append to classes
        classes.append(line.split(' ', 1)[1].rstrip())
        line = labelsfile.readline()
    # close label file
    labelsfile.close()

    # load the teachable machine model
    model_path = f"{/home/pi/JCho/Test}/keras_model.h5"
    model = tf.models.load_model(model_path, compile=False)

    # initialize webcam video object
    cap = cv2.VideoCapture(0)

    # width & height of webcam video in pixels -> adjust to your size
    # adjust values if you see black bars on the sides of capture window
    frameWidth = 1024
    frameHeight = 768

    # set width and height in pixels
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
    # enable auto gain
    cap.set(cv2.CAP_PROP_GAIN, 0)

    # starting process 1 - speech
    p1.start()

    # keeps program running forever until ctrl+c or window is closed
    while True:

        # disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Create the array of the right shape to feed into the keras model.
        # We are inputting 1x 224x224 pixel RGB image.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # capture image
        check, frame = cap.read()
        # mirror image - mirrored by default in Teachable Machine
        # depending upon your computer/webcam, you may have to flip the video
        # frame = cv2.flip(frame, 1)

        # crop to square for use with TM model
        margin = int(((frameWidth-frameHeight)/2))
        square_frame = frame[0:frameHeight, margin:margin + frameHeight]
        # resize to 224x224 for use with TM model
        resized_img = cv2.resize(square_frame, (224, 224))
        # convert image color to go to model
        model_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        # turn the image into a numpy array
        image_array = np.asarray(model_img)
        # normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # load the image into the array
        data[0] = normalized_image_array

        # run the prediction
        predictions = model.predict(data)

        # confidence threshold is 90%.
        conf_threshold = 90
        confidence = []
        conf_label = ""
        threshold_class = ""
        # create black border at bottom for labels
        per_line = 2  # number of classes per line of text
        bordered_frame = cv2.copyMakeBorder(
            square_frame,
            top=0,
            bottom=30 + 15*math.ceil(len(classes)/per_line),
            left=0,
            right=0,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )
        # for each one of the classes
        for i in range(0, len(classes)):
            # scale prediction confidence to % and apppend to 1-D list
            confidence.append(int(predictions[0][i]*100))
            # put text per line based on number of classes per line
            if (i != 0 and not i % per_line):
                cv2.putText(
                    img=bordered_frame,
                    text=conf_label,
                    org=(int(0), int(frameHeight+25+15*math.ceil(i/per_line))),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(255, 255, 255)
                )
                conf_label = ""
            # append classes and confidences to text for label
            conf_label += classes[i] + ": " + str(confidence[i]) + "%; "
            # prints last line
            if (i == (len(classes)-1)):
                cv2.putText(
                    img=bordered_frame,
                    text=conf_label,
                    org=(int(0), int(frameHeight+25+15*math.ceil((i+1)/per_line))),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(255, 255, 255)
                )
                conf_label = ""
            # if above confidence threshold, send to queue
            if confidence[i] > conf_threshold:
        #        speakQ.put(classes[i])
                threshold_class = classes[i]
        # add label class above confidence threshold
        cv2.putText(
            img=bordered_frame,
            text=threshold_class,
            org=(int(0), int(frameHeight+20)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.75,
            color=(255, 255, 255)
        )

        # original video feed implementation
        cv2.imshow("Capturing", bordered_frame)
        cv2.waitKey(10)

        # # if the above implementation doesn't work properly
        # # comment out two lines above and use the lines below
        # # will also need to import matplotlib at the top
        # plt_frame = cv2.cvtColor(bordered_frame, cv2.COLOR_BGR2RGB)
        # plt.imshow(plt_frame)
        # plt.draw()
        # plt.pause(.001)

    # terminate process 1
    #p1.terminate()


if __name__ == '__main__':
    main()

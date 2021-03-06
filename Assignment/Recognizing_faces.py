# import required packages
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

# function to detect images
def detect_face(img):
    """
    Function to detect face using OpenCV
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    # if no faces are detected then return original img
    if len(faces) == 0:
        return None, None

    # under the assumption that there will be only one face
    # extract the face area
    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return gray[y:y+w, x:x+h], faces[0]

# function for data preparing
def prepare_training_data(data_folder_path):
    # ------STEP-1--------
    # get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)     # print(dirs)

    # list to hold all subject faces
    faces = []

    # list to hold labels for all subjects
    labels = []

    # let's go through each directory and read images within it
    for dir_name in dirs:

        # our subject directories start with letter 's' so
        # ignore any non-relevant directories if any
        if not dir_name.startswith('s'):
            continue

        # ------STEP-2--------
        # extract label number of subjects from dir_name
        # format of dir_name = slabel
        # so removing the letter 's' from dir_name will give us label

        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + '/' + dir_name    # print(subject_dir_path)

        # get the images names that are inside the given subject directory
        subject_image_name = os.listdir(subject_dir_path)   # print(subject_image_name)

        # ------STEP-3--------
        # go through each image name, read image
        # detect face and add face to list of faces
        for image_name in subject_image_name:

            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue

            # build image path
            # sample image path = training-data/a1/1.jpg
            image_path = subject_dir_path + '/' + image_name    # print(image_path)

            # read image
            image = cv2.imread(image_path)

            # display an image window to show the image
            cv2.imshow('Training on image...', cv2.resize(image,(400, 500)))
            cv2.waitKey(100)

            # detect face
            face, rect = detect_face(image)

            # ------STEP-4--------
            # for the purpose of this tutorial
            # we will ignore faces that are not detected
            if face is not None:

                # add face to list of faces
                faces.append(face)

                # add label for this face
                labels.append(label)

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels

# Show about data preparing
print("Preparing data...")
faces, labels = prepare_training_data("train-data")
print("Data prepared")

# print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

# subjects
subjects = ["", "Htut", "Yeemon", "Shwan"]

# create our LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# train our face recognizer of our training faces -> faces, labels
face_recognizer.train(faces, np.array(labels))
# print("labels", labels)
# print("faces", faces)

# function to draw rectangle on image
def draw_rectangle(img, rect):
    """
    Function to draw rectangle on image according to given (x, y) coordinates with given width, height
    """
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

# function to draw text on image
def draw_text(img, text, x, y):
    """
    Function to draw text on given image starting from passed (x, y) coordinates
    """
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 6)

# predict function
def predict(test_img):
    """
    Function to recognize the person in image passed and draws a rectangle around detected face with name of the subject
    """

    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    # detect face from the image
    face, rect = detect_face(img)

    # predict the image using our face recognizer
    label = face_recognizer.predict(face)

    # get name of respective label returned by face recognizer
    print(label)
    label_text = subjects[label[0]]

    # draw a rectangle around face detected
    draw_rectangle(img, rect)

    # draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1] - 5)
    return img

print("Predicting images...")

# load test images
test_img1 = cv2.imread("test-data/test1.jpg")
test_img2 = cv2.imread("test-data/test2.jpg")
test_img3 = cv2.imread("test-data/test3.jpg")

# perform a prediction
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
predicted_img3 = predict(test_img3)
print("Prediction completed")

# show image
cv2.imshow("Predicting image1", cv2.resize(predicted_img1, (300, 400)))
cv2.imshow("Predicting image2", cv2.resize(predicted_img2, (300, 400)))
cv2.imshow("Predicting image3", cv2.resize(predicted_img3, (300, 400)))

cv2.waitKey(0)
cv2.destroyAllWindows()


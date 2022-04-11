from flask import Flask, render_template, Response, request, jsonify
import imutils
import threading
from imutils.video import VideoStream
import time
from arnis_app.pose_est import pose_det
from statistics import mean

# Object Detection Modules
import tensorflow as tf
from object_detection.utils import config_util
import os
import psutil
from object_detection.builders import model_builder
import cv2
from arnis_app import app

p = psutil.Process(os.getpid())

CONFIG_PATH = "arnis_app/training_v2/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.config"

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

strt = time.time()
# Load restored checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join('arnis_app', 'training_v2', 'ckpt-10')).expect_partial()
load_model = time.time()-strt

print("obj det model loading time: ", load_model)


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
# app = Flask(__name__)

vs = VideoStream(src=0).start()
# time.sleep(2.0)
prev_frame_time = 0

# Store grades
prev_grade = 0
grade = 0
ave_grade = [0 for i in range(27)]

# Choose task
grading_ver, class_ver = False, False

# Pose key start ADDED
pose_key = 1

# Developer Options
ctgry = ""
skltn = False
shwFPS = False
shwAngl = False
scCap = False
instanceNum = "Instance number"


# Pose Grading Results Page
@app.route('/pose-grading-result', methods=['GET', 'POST'])
def results():
    global ave_grade
    grade_res = ave_grade[:]

    return render_template('results.html', resGrade=grade_res)


# Pose Grading Results Page
@app.route('/grading/switches', methods=['GET', 'POST'])
def switch_options():

    # Pose Key
    global pose_key
    if 'poseKey' in request.form:
        pose_key = int(request.form['poseKey'])

    # Grading or Classification
    global class_ver
    if 'classification' in request.form:
        class_ver = int(request.form['classification'])
        class_ver = bool(class_ver)

    global grading_ver
    if 'grading' in request.form:
        grading_ver = int(request.form['grading'])
        grading_ver = bool(grading_ver)

    # Page switches
    global skltn
    if 'skeletonOption' in request.form:
        skltn = int(request.form['skeletonOption'])
        skltn = bool(skltn)

    global shwAngl
    if 'angleOption' in request.form:
        shwAngl = int(request.form['angleOption'])
        shwAngl = bool(shwAngl)

    global shwFPS
    if 'fpsOption' in request.form:
        shwFPS = int(request.form['fpsOption'])
        shwFPS = bool(shwFPS)

    return jsonify({'result': 'switched', 'message': 'message'})


# Read poses from camera input
def camera():
    global vs, outputFrame, lock, prev_frame_time, grade, prev_grade, ave_grade, grading_ver, scCap, instanceNum, shwFPS, shwAngl, skltn, pose_key, class_ver, grading_ver
    blur_end = False
    fnt = cv2.FONT_HERSHEY_DUPLEX
    file_speed = 'speed.txt'
    file_mem = ''
    mem_usage = 0
    end_time, start = 0, 0

    # Change number per participant
    # instanceNum = 0
    label = ''

    # grab global references to the video stream, output frame, and
    # lock variables
    while True:
        if grading_ver:
            # print('Grade: ', grade, ' Prev grade: ', prev_grade)
            # Pause 2 sec if pose passed
            if prev_grade >= 75:
                time.sleep(2.0)

        # read the next frame from the video stream, resize it,
        frame = vs.read()
        raw_frame = frame
        frame = imutils.resize(frame, width=800)

        # ADDED: get frame dimension
        h, w, c = frame.shape
        # print('Height: ', h, 'Width: ', w)

        if grading_ver:
            # file_speed = "speed_grade.txt"
            # file_mem = "mem_grade.txt"
            # added arg: pose key, added var: grade
            # start = time.time()
            frame, grade = pose_det(frame, detection_model, skltn, shwAngl, pose_key, grading_ver)
            # end_time = time.time()
        elif class_ver:
            # file_speed = "speed_dir/speed_classi_" + str(instanceNum) + ".txt"
            # file_mem = "memory_dir/mem_usage_" + str(instanceNum) + ".txt"
            # start = time.time()
            frame, label = pose_det(frame, detection_model, skltn, shwAngl)
            # mem_usage = p.memory_info().rss / 1024 / 1024
            # end_time = time.time()

        # If Capture is pressed then the raw image is saved
        # if scCap:
        #     if not os.path.exists('test_inst_dir'):
        #         os.mkdir('test_inst_dir')
        #     if not os.path.exists('test_inst_dir/test' + str(instanceNum)):
        #         os.mkdir('test_inst_dir/test' + str(instanceNum))
        #     cv2.imwrite('test_inst_dir/test' + str(instanceNum) + '/' + label + '.jpg', raw_frame)
        #     scCap = False
        #
        # if not os.path.exists('speed_dir'):
        #     os.mkdir('speed_dir')
        #
        # if not os.path.exists('memory_dir'):
        #     os.mkdir('memory_dir')

        # Run if grading method
        if grading_ver:
            # font color for grade
            clr_grd = (0, 0, 255)

            # Compute overall grade
            ave_grade[pose_key] = grade

            # Threshold ADDED
            # next pose when threshold is greater than 74
            if grade >= 75:
                clr_grd = (0, 255, 0)

                # next pose key until 23rd pose
                if pose_key < 26:
                    pose_key = pose_key + 1
                else:
                    pose_key = 0
                    blur_end = True

            if pose_key > 0:
                blur_end = False
                # Visualize grade
                txt_grd = "Grade:" + str(grade)
                txt_grdsz = cv2.getTextSize(txt_grd, fnt, 1.2, 2)[0]

                frame = cv2.rectangle(frame, (w, 0), (w - txt_grdsz[0], txt_grdsz[1]), (255, 255, 255), cv2.FILLED)
                frame = cv2.putText(frame, txt_grd, (w - txt_grdsz[0], txt_grdsz[1]), fnt, 1.2, clr_grd, 2, cv2.LINE_AA)
                # print(str(pose_key) + " " + str(grade))

            if grade >= 75:
                # Save frame of pose done by user
                cv2.imwrite('static/' + str(pose_key - 1) + '.jpg', frame)

        if grading_ver or class_ver:
            if end_time - start > 0:
                print('inference time: ', end_time - start, 'Memory usage: ', mem_usage)
                # Save memory usage in text file
                with open(file_mem, 'a') as f2:
                    f2.write(str(mem_usage) + ", ")

                # Save prediction/classification time in text file
                with open(file_speed, 'a') as f:
                    f.write(str(end_time - start) + ", ")

        try:
            if shwFPS:
                # FPS
                new_frame_time = time.time()
                fps = int(1/(new_frame_time - prev_frame_time))
                prev_frame_time = new_frame_time
                fps = str(fps)
                frame = cv2.putText(frame, "FPS: " + fps, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        except:
            pass

        if grading_ver:
            # Store grade to another var
            prev_grade = grade
            # Check whether the last pose is done
            if blur_end:
                # Blur video feed after completing 24 needed poses
                overlay = frame.copy()
                output = frame.copy()
                overlay = cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
                frame = cv2.addWeighted(overlay, 0.7, output, 0.3, 0, output)

                # Put text after completing all poses
                txt1 = "YOU HAVE COMPLETED"
                txt2 = "THE 24 BASIC TECHNIQUES OF ARNIS"
                txt3 = "GRADE: " + str(round(mean(ave_grade[3:]), 2))
                text_sz1 = cv2.getTextSize(txt1, fnt, 1, 2)[0]
                text_sz2 = cv2.getTextSize(txt2, fnt, 1, 2)[0]
                text_sz3 = cv2.getTextSize(txt3, fnt, 2, 2)[0]

                txtX1 = int((output.shape[1] - text_sz1[0]) / 2)
                txtY1 = int(((output.shape[0] + text_sz1[1]) / 2) - (text_sz1[1] / 2))

                txtX2 = int((output.shape[1] - text_sz2[0]) / 2)
                txtY2 = int(((output.shape[0] + text_sz1[1]) / 2) + (text_sz1[1]))

                txtX3 = int((output.shape[1] - text_sz3[0]) / 2)
                txtY3 = int(((output.shape[0] + text_sz1[1]) / 4))

                frame = cv2.putText(frame, txt1, (txtX1, txtY1), fnt, 1, (255, 255, 255), 2)
                frame = cv2.putText(frame, txt2, (txtX2, txtY2), fnt, 1, (255, 255, 255), 2)
                frame = cv2.putText(frame, txt3, (txtX3, txtY3), fnt, 2, (0, 255, 0), 2)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


# Generate video output in the webpage
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


# @app.route('/video_feed')
# def video_feed():
#     # return the response generated along with the specific media
#     # type (mime type)
#     return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# if __name__ == '__main__':
#     # construct the argument parser and parse command line arguments
#     t = threading.Thread(target=camera)
#     t.daemon = True
#     t.start()
#     # start the flask app
#     app.run(debug=True, threaded=True, use_reloader=False)
# # release the video stream pointer
# vs.stop()
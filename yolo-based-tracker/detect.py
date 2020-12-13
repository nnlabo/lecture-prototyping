import argparse
import tensorflow as tf
import cv2
import sys

from core.utils import load_class_names, load_image, draw_boxes, draw_boxes_frame
from core.yolo_tiny import YOLOv3_tiny
from core.yolo import YOLOv3

# added
import numpy as np
import time
# for Raspberry pi
import RPi.GPIO as GPIO
zero_pose = 7.25
# servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 50)
p.start(0.0)
p.ChangeDutyCycle(zero_pose)
time.sleep(1.0)


def main(mode, tiny, iou_threshold, confidence_threshold, path):
  # servo
  input_x = 7.25

  class_names, n_classes = load_class_names()
  if tiny:
    model = YOLOv3_tiny(n_classes=n_classes,
                        iou_threshold=iou_threshold,
                        confidence_threshold=confidence_threshold)
  else:
    model = YOLOv3(n_classes=n_classes,
                   iou_threshold=iou_threshold,
                   confidence_threshold=confidence_threshold)
  inputs = tf.placeholder(tf.float32, [1, *model.input_size, 3])
  detections = model(inputs)
  saver = tf.train.Saver(tf.global_variables(scope=model.scope))

  with tf.Session() as sess:
    saver.restore(sess, './weights/model-tiny.ckpt' if tiny else './weights/model.ckpt')

    if mode == 'image':
      image = load_image(path, input_size=model.input_size)
      result = sess.run(detections, feed_dict={inputs: image})
      draw_boxes(path, boxes_dict=result[0], class_names=class_names, input_size=model.input_size)
      return

    elif mode == 'video':
      cv2.namedWindow("Detections")
      video = cv2.VideoCapture(path)
      fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
      fps = video.get(cv2.CAP_PROP_FPS)
      frame_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
      out = cv2.VideoWriter('./detections/video_output.mp4', fourcc, fps, frame_size)
      print("Video being saved at \"" + './detections/video_output.mp4' + "\"")
      print("Press 'q' to quit")
      while True:
        retval, frame = video.read()
        if not retval:
          break
        resized_frame = cv2.resize(frame, dsize=tuple((x) for x in model.input_size[::-1]), interpolation=cv2.INTER_NEAREST)
        result = sess.run(detections, feed_dict={inputs: [resized_frame]})
        draw_boxes_frame(frame, frame_size, result, class_names, model.input_size)
        cv2.imshow("Detections", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        out.write(frame)
      cv2.destroyAllWindows()
      video.release()
      return

    elif mode == 'webcam':
      cap = cv2.VideoCapture(0)
      while True:
        ret, frame = cap.read()
        frame_size = (frame.shape[1], frame.shape[0])
        resized_frame = cv2.resize(frame, dsize=tuple((x) for x in model.input_size[::-1]), interpolation=cv2.INTER_NEAREST)
        result = sess.run(detections, feed_dict={inputs: [resized_frame]})
        draw_boxes_frame(frame, frame_size, result, class_names, model.input_size)
        cv2.imshow('frame', frame)
        # servo
        boxes_dict = result[0]
        resize_factor = (frame_size[0] / model.input_size[1], frame_size[1] / model.input_size[0])
        for cls in range(len(class_names)):
          boxes = boxes_dict[cls]
          color = (0, 0, 255)
          if np.size(boxes) != 0 and class_names[cls] == 'person':
            for box in boxes:
              xy = box[:4]
              xy = [int(xy[i] * resize_factor[i % 2]) for i in range(4)]
              object_center_xy = (int((xy[0]+xy[2])/2), int((xy[1]+xy[3])/2))
              # cv2.circle(frame, object_center_xy, 5, (0,0,255), -1)
              frame_center_xy = (int(frame_size[0]/2), int(frame_size[1]/2))
              # cv2.circle(frame, frame_center_xy, 5, (0,0,255), -1)
              dx = frame_center_xy[0] - object_center_xy[0]
              input_x = input_x + 0.0015 * dx
              if input_x > 12.0:
                input_x = 12.0
              elif input_x < 2.5:
                input_x = 2.5
              p.ChangeDutyCycle(input_x)
              time.sleep(0.3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      cap.release()
      cv2.destroyAllWindows()
      return

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--tiny", action="store_true", help="enable tiny model")
  parser.add_argument("mode", choices=["video", "image", "webcam"], help="detection mode")
  parser.add_argument("iou", metavar="iou", type=float, help="IoU threshold [0.0, 1.0]")
  parser.add_argument("confidence", metavar="confidence", type=float, help="confidence threshold [0.0, 1.0]")
  if 'video' in sys.argv or 'image' in sys.argv:
    parser.add_argument("path", type=str, help="path to file")

  args = parser.parse_args()
  if args.mode == 'video' or args.mode == 'image':
    main(args.mode, args.tiny, args.iou, args.confidence, args.path)
  else:
    main(args.mode, args.tiny, args.iou, args.confidence, '')

# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import threading
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image, ImageFont, ImageDraw
from roboid import Runner
from roboidai import Camera
from roboidai import Window


class ImageProject(object):
    _FONT = ImageFont.truetype('malgun.ttf', 36)

    def __init__(self, cam_id=0, cam_flip=None, win_id=0):
        self._loaded = False
        self._model = None
        self._labels = None
        self._confidences = None
        self._result_image = None
        self._result_labels = None
        self._label2id = {}
        self._data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self._disposed = False
        self._cam = Camera(cam_id, cam_flip)
        self._win = Window(win_id)
        Runner.register_component(self)
        self._init()

    def _run(self):
        try:
            while self._running:
                if self._loaded:
                    image = self._cam.read()
                    self.predict(image)
                    self._win.show(self.get_result_image())
                self._win.wait_key()
                if self._win.is_esc_key():
                    break
            self._cam.dispose()
            self._win.dispose()
            self.dispose()
        except:
            pass

    def _init(self):
        self._running = True
        thread = threading.Thread(target=self._run)
        self._thread = thread
        thread.daemon = True
        thread.start()

    def dispose(self):
        if self._disposed == False:
            self._disposed = True
            self._running = False
            thread = self._thread
            self._thread = None
            if thread:
                thread.join()
        Runner.unregister_component(self)

    def load_h5_model(self, model_path, label_path):
        self._loaded = False
        self._model = tf.keras.models.load_model(model_path)
        labels = np.genfromtxt(label_path, encoding='utf8', dtype=None)
        self._labels = []
        self._label2id = {}
        for id, label in labels:
            self._labels.append(label)
            self._label2id[label] = id
        self._labels = np.array(self._labels)
        self._loaded = True

    def _crop_image(self, image):
        width = image.shape[1]
        height = image.shape[0]
        if height > width:
            start = (height - width) // 2
            image = image[start:start+width, :]
        else:
            start = (width - height) // 2
            image = image[:, start:start+height]
        return cv2.resize(image, dsize=(224, 224))

    def predict(self, image, result_image=True):
        if self._loaded and image is not None:
            resized_image = self._crop_image(image)
            self._data[0] = (resized_image.astype(np.float32) / 127.0) - 1
            confidences = self._confidences = self._model.predict(self._data)[0]
            ids = confidences.argsort()[::-1]
            labels = self._result_labels = self._labels[ids]
            confidences = confidences[ids]
            if result_image:
                pil_image = Image.fromarray(image)
                draw = ImageDraw.Draw(pil_image)
                draw.text((30, 30), "{} {}".format(labels[0], str(round(confidences[0], 4))), font=ImageProject._FONT, fill=(0, 0, 0))
                self._result_image = np.asarray(pil_image)
            else:
                self._result_image = image

    def is_running(self):
        return self._running

    def get_result_image(self):
        return self._result_image

    def best_label(self, threshold=-1):
        if self._result_labels is not None:
            label = self._result_labels[0]
            if threshold >= 0:
                return label if self.confidence(label) > threshold else None
            return label
        return None

    def confidence(self, label):
        if label in self._label2id and self._confidences is not None:
            id = self._label2id[label]
            if id < len(self._confidences):
                return self._confidences[id]
        return 0

np.set_printoptions(suppress=True)

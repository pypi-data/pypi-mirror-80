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

from roboid import Runner
import cv2


class Camera:
    @staticmethod
    def test():
        caps = {}
        for id in range(10):
            cap = cv2.VideoCapture(id)
            if cap.isOpened():
                caps[id] = cap
        while True:
            for id in caps:
                ret, frame = caps[id].read()
                if ret:
                    cv2.putText(frame, 'press ESC key to quit', (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    cv2.imshow('camera {}'.format(id), frame)
            if cv2.waitKey(1) == 27:
                break
        for id in caps:
            caps[id].release()
        cv2.destroyAllWindows()

    def __init__(self, id=0, flip=None):
        self._id = id
        self._flip = flip
        self._cap = None
        if self.open():
            Runner.register_component(self)

    def dispose(self):
        if self._cap is not None:
            self._cap.release()
        Runner.unregister_component(self)

    def open(self):
        cap = cv2.VideoCapture(self._id)
        ret = cap.isOpened()
        if ret:
            self._cap = cap
        else:
            print("Cannot open camera {}".format(self._id))
        return ret

    def read(self):
        if self._cap is not None:
            ret, frame = self._cap.read()
            if ret:
                if self._flip is not None:
                    frame = cv2.flip(frame, self._flip)
                return frame
        return None

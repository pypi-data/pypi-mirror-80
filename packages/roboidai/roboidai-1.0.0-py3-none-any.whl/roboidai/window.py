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


class Window:
    def __init__(self, id=0):
        self._id = id
        self._pressed_key = -1
        Runner.register_component(self)

    def dispose(self):
        cv2.destroyWindow('window {}'.format(self._id))
        Runner.unregister_component(self)

    def show(self, image):
        if image is not None:
            cv2.imshow('window {}'.format(self._id), image)

    def wait_key(self, delay=1):
        self._pressed_key = cv2.waitKey(delay)
        return self._pressed_key

    def is_key(self, key):
        return self._pressed_key == ord(key)

    def is_esc_key(self):
        return self._pressed_key == 27

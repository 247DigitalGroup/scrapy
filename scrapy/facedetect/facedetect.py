# facedetect: a simple face detector
# Copyright(c) 2013 by wave++ "Yuri D'Elia" <wavexx@thregr.org>
# Distributed under GPL2 (see COPYING) WITHOUT ANY WARRANTY.

import cv2
import numpy as np
import math
import os
import sys


CASCADE_PATH = '/usr/local/share/haarcascade_frontalface_alt2.xml'

# CV compatibility stubs
if 'IMREAD_GRAYSCALE' not in dir(cv2):
    cv2.IMREAD_GRAYSCALE = 0L

def rank(im, rects):
    scores = []

    for i in range(len(rects)):
        rect = rects[i]
        b = min(rect[2], rect[3]) / 10.
        rx = (rect[0] + b, rect[0] + rect[2] - b)
        ry = (rect[1] + b, rect[1] + rect[3] - b)
        roi = im[ry[0]:ry[1], rx[0]:rx[1]]
        s = (rect[2] + rect[3]) / 2.

        scale = 100. / max(rect[2], rect[3])
        dsize = (int(rect[2] * scale), int(rect[3] * scale))
        roi_n = cv2.resize(roi, dsize, interpolation=cv2.INTER_CUBIC)
        roi_l = cv2.Laplacian(roi_n, cv2.CV_8U)
        e = np.sum(roi_l) / (dsize[0] * dsize[1])

        dx = im.shape[1] / 2 - rect[0] + rect[2] / 2
        dy = im.shape[0] / 2 - rect[1] + rect[3] / 2
        d = math.sqrt(dx ** 2 + dy ** 2) / (max(im.shape) / 2)

        scores.append({'s': s, 'e': e, 'd': d})

    if not scores:
        return None

    sMax = max([x['s'] for x in scores])
    eMax = max([x['e'] for x in scores])

    for i in range(len(scores)):
        s = scores[i]
        sN = s['sN'] = s['s'] / sMax
        eN = s['eN'] = s['e'] / eMax
        f = s['f'] = eN * 0.7 + (1 - s['d']) * 0.1 + sN * 0.2

    ranks = range(len(scores))
    ranks = sorted(ranks, reverse=True, key=lambda x: scores[x]['f'])
    # for i in range(len(scores)):
    #     scores[ranks[i]]['RANK'] = i

    return ranks[0]

def detect(pil_image):
    " detect faces in image "

    image = cv2.cvtColor(np.asarray(pil_image), cv2.COLOR_BGR2GRAY)
    flags = cv2.CV_HAAR_SCALE_IMAGE

    # frontal faces
    classifier = cv2.CascadeClassifier(CASCADE_PATH)
    features = classifier.detectMultiScale(image, 1.1, 5, flags)
    best = rank(image, features)
    if best:
        return True
    return False 
        
        # features = features[best]
        # return {
        #     'x': int(features[0]),
        #     'y': int(features[1]),
        #     'w': int(features[2]),
        #     'h': int(features[3]),
        # }
        # return {}


if __name__ == '__main__':
    print detect(sys.argv[1])

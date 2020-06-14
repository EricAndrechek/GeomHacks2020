from pyzbar.pyzbar import decode
import cv2
import subprocess
import json
import math
import imutils
import numpy as np
import base64
import os
# import objectifyer
    
class measure():
    def __init__(self, qr, img, item_number):
        self.image = img
        self.txt = qr.data.decode()
        if self.txt.split(':')[0] == 'PaccuratePad':
            self.valid = True
            self.real_width = float(self.txt.split(':')[1])
            self.real_height = float(self.txt.split(':')[2])
            (self.x, self.y, self.w, self.h) = qr.rect

            self.get_corners(qr.polygon)

            self.scale = self.real_width / self.image_width # inches per pixel
            # so at this depth, self.scale * pixels = dimension in inches
            height = img.shape[0]
            width = img.shape[1]
            self.item = True
            if self.txt.split(':')[3] != 'Back':
                # self.draw_circle((255, 0, 0))
                font = cv2.FONT_HERSHEY_SIMPLEX

                my = 0
                mx = 0
                for p in self.points:
                    mx += p[0]
                    my += p[1]
                mx = mx / 4
                my = my / 4
                bottomLeftCornerOfText = (int(mx) - 100, int(my) + 100)

                fontScale = 10
                fontColor = (255, 255, 255)
                lineType = 30

                corns = []
                for corn in self.corners:
                    corns.append(list(corn))
                corn = np.array(corns)

                mask = np.full((img.shape[0], img.shape[1]), 0, dtype=np.uint8)
                cv2.fillPoly(mask, [corn], (255, 255, 255))
                mask = cv2.bitwise_not(mask)
                self.image = cv2.bitwise_or(self.image, self.image, mask=mask)

                cv2.putText(self.image, str(item_number), bottomLeftCornerOfText, font, fontScale, fontColor, lineType, cv2.LINE_AA)
            else:
                self.item = False
            self.depth = self.depth_finder(self.image_width, self.real_width, width)
        else:
            valid = False

    def depth_finder(self, object_width, real_width, width):
        object_width = 3559 / width * object_width
        perceived = (math.pi / 180 * 0.021315384) * object_width
        object_distance = real_width / 2 / math.tan( perceived / 2 )
        return object_distance
    
    def get_corners(self, poly):
        self.corners = poly
        self.points = []
        for corner in self.corners:
            (x2, y2) = corner
            self.points.append((x2, y2))
        self.points = tuple(self.points)
        self.image_width = math.sqrt( ((self.points[0][0] - self.points[1][0]) ** 2) + ((self.points[0][1] - self.points[1][1]) ** 2) )

    def draw_circle(self, colors):
        for n, p in enumerate(self.points):
            cv2.circle(self.image, p, 50, colors, -1)


def read_heic(path, fn):
    s = subprocess.Popen(['heif-convert', 'images/{}'.format(path), 'images/{}.jpg'.format(fn)], stdout=subprocess.PIPE)
    s = s.stdout.read().decode().replace('\n', '')
    print(s)


def read_png(path, fn):
    s = subprocess.Popen(['convert', 'images/{}'.format(path), 'images/{}.jpg'.format(fn)], stdout=subprocess.PIPE)
    s = s.stdout.read().decode().replace('\n', '')
    print(s)


def get_zoom(path):
    s = subprocess.Popen(['exiftool', '-G', '-j', 'images/{}'.format(path)], stdout=subprocess.PIPE)
    s = s.stdout.read().strip()
    s.decode('utf-8').rstrip('\r\n')
    md = json.loads(s)
    zoom = 1
    for key in md[0]:
        if 'digitalzoomratio' in key.lower():
            zoom = float(md[0][key])
    return zoom

def runner(img_path):
    og = img_path
    ft = img_path.split('.')[1].lower()
    fn = img_path.split('.')[0]
    if ft == 'heic':
        read_heic(img_path, fn)
        img_path = '{}.jpg'.format(fn)
        ft = 'jpg'
        os.remove("images/{}".format(og))
    if ft == 'png':
        read_png(img_path, fn)
        img_path = '{}.jpg'.format(fn)
        ft = 'jpg'
        os.remove("images/{}".format(og))
    if ft != 'jpg' and ft != 'jpeg':
        os.remove("images/{}".format(og))
        return {'error': 'Unaccepted image filetype {}. Please submit jpg, png, and heic only.'.format(ft)}, img_path
    img = cv2.imread('images/{}'.format(img_path))
    try:
        temp = img.shape[0]
    except AttributeError:
        return {'error': 'Could not read image data. Make sure you uploaded a valid image and try again'}, img_path
    if img.shape[1] < img.shape[0]:
        img = imutils.rotate_bound(img, 90)
    zoom = get_zoom(img_path)
    qr = decode(img)
    if len(qr) < 2:
        return {'error': 'Oops, try that picture again, we couldn\'t find all your QR codes.'}, img_path
    background_depth = None
    items = []
    item_number = 1
    for q in qr:
        m = measure(q, img, item_number)
        if m.valid:
            img = m.image
            if m.item:
                # run Jainil code with m.points
                # expects a width and length in pixels
                # I'll just use the number of pixels in the QR code for now
                # this is an example of what the data should look like:
                #       corners = ((0, 10), (0, 20), (14, 20), (10, 10))
                corners = m.points
                # ^ change the above values for the corners of the actual box
                width = math.sqrt( ((corners[0][0] - corners[1][0]) ** 2) + ((corners[0][1] - corners[1][1]) ** 2) )
                height = math.sqrt( ((corners[1][0] - corners[2][0]) ** 2) + ((corners[1][1] - corners[2][1]) ** 2) )
                color = (0, 204, 102)
                thickness = 20
                cv2.line(img, corners[0], corners[1], color, thickness)
                cv2.line(img, corners[1], corners[2], color, thickness)
                cv2.line(img, corners[2], corners[3], color, thickness)
                cv2.line(img, corners[3], corners[0], color, thickness)
                items.append({'item_number': item_number, 'item_width': round(width * m.scale, 2), 'item_height': round(height * m.scale, 2), 'item_depth': m.depth})
                item_number += 1
            else:
                background_depth = m.depth
    for obj in items:
        obj['item_depth'] = round( background_depth - obj['item_depth'], 2 )
    _, im_arr = cv2.imencode('.jpg', img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    data = {'image': 'data:image/jpeg;base64,{}'.format(im_b64.decode()), 'objects': items}
    return data, img_path


if __name__ == "__main__":
    items, fn = runner('test6.JPG')
    f = open('image.html', 'w')
    # now u can just open image.html in your browser to see the image
    f.write('<img src="{}">'.format(items['image']))
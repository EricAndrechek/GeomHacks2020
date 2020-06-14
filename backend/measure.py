from pyzbar.pyzbar import decode
import cv2
import subprocess
import json
import math
import imutils
# import objectifyer
    
class measure():
    def __init__(self, qr, img, focal_length, sf):
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
            self.center = (float(width/2.0), float(height/2.0))
            try:
                if self.txt.split(':')[3] == 'Back':
                    self.draw_circle((255, 0, 0))
                else:
                    self.draw_circle((0, 255, 0))
            except IndexError:
                self.draw_circle((0, 255, 0))
            j = width/height
            self.depth = self.depth_finder(self.image_width, self.real_width, j, 1, sf, width, focal_length)
        else:
            valid = False

    def depth_finder(self, object_width, real_width, j, k, scale_factor, image_width, focal_length):
        print(object_width, real_width, j, k, scale_factor, image_width, focal_length)
        real_image_width = j * math.sqrt( 43.27 / scale_factor ) / math.sqrt( math.pow(j, 2) * math.pow(k, 2) )
        object_distance = focal_length * real_width / (object_width / real_image_width * image_width)
        return object_distance
    
    def get_corners(self, poly):
        self.corners = poly
        self.points = []
        for corner in self.corners:
            (x2, y2) = corner
            self.points.append([x2, y2])
        # print(self.points[0][0], self.points[0][1])
        # print(self.points[1][0], self.points[1][1])
        self.image_width = math.sqrt( ((self.points[0][0] - self.points[1][0]) ** 2) + ((self.points[0][1] - self.points[1][1]) ** 2) )

    def draw_circle(self, colors):
        for n, p in enumerate(self.points):
            cv2.circle(self.image, tuple(p), 25, colors, -1)

def get_focal_length(path):
    s = subprocess.Popen(['exiftool', '-G', '-j', 'img-resources/{}'.format(path)], stdout=subprocess.PIPE)
    s = s.stdout.read().strip()
    s.decode('utf-8').rstrip('\r\n')
    md = json.loads(s)
    fl = None
    sf = None
    for key in md[0]:
        if 'focallength' in key.lower():
            fl = md[0][key]
        if 'scalefactor' in key.lower():
            sf = float(md[0][key])
    if fl is not None and sf is not None:
        fl = float(fl.split()[0]) # convert mm to inches
        fl = fl / 25.4
    return fl, sf

def runner(img_path):
    img = cv2.imread('img-resources/{}'.format(img_path))
    if img.shape[1] < img.shape[0]:
        img = imutils.rotate_bound(img, 90)
        print('rotated')
    fl, sf = get_focal_length(img_path)
    qr = decode(img)
    for q in qr:
        m = measure(q, img, fl, sf)
        if m.valid:
            img = m.image
            print(m.depth)
    return img



def main():
    img = runner('work.JPG')
    cv2.imshow("Image", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

main()
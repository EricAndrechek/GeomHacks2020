from pyzbar.pyzbar import decode
import cv2
import subprocess
import json
# import objectifyer
    
class measure():
    def __init__(self, qr, img, focal_length):
        self.image = img
        self.txt = qr.data.decode()
        if self.txt.split(':')[0] == 'PaccuratePad':
            self.valid = True
            self.real_width = float(self.txt.split(':')[1])
            self.real_height = float(self.txt.split(':')[2])
            (self.x, self.y, self.image_width, self.image_height) = qr.rect
            self.width_scale = self.real_width / self.image_width
            self.height_scale = self.real_height / self.image_height
            # so at this depth, width_scale * pixels = width in inches and same for height
            try:
                if self.txt.split(':')[3] == 'Back':
                    cv2.rectangle(self.image, (self.x, self.y), (self.x + self.image_width, self.y + self.image_height), (255, 0, 0), 5)
                else:
                    cv2.rectangle(self.image, (self.x, self.y), (self.x + self.image_width, self.y + self.image_height), (0, 255, 0), 5)
            except IndexError:
                cv2.rectangle(self.image, (self.x, self.y), (self.x + self.image_width, self.y + self.image_height), (0, 255, 0), 5)
            self.depth = self.depth_finder(self.real_width, focal_length, self.image_width)
        else:
            valid = False
    def depth_finder(self, known_width, focal_length, pixel_width):
        return (known_width * focal_length) / pixel_width

def runner(img_path):
    img = cv2.imread('img-resources/{}'.format(img_path))
    fl = get_focal_length(img_path)
    if fl is not None:
        qr = decode(img)
        for q in qr:
            m = measure(q, img, fl)
            if m.valid:
                img = m.image
                print(m.depth)
    return img

def get_focal_length(path):
    s = subprocess.Popen(['exiftool', '-G', '-j', 'img-resources/{}'.format(path)], stdout=subprocess.PIPE)
    s = s.stdout.read().strip()
    s.decode('utf-8').rstrip('\r\n')
    md = json.loads(s)
    fl = None
    for key in md[0]:
        if 'focallength' in key.lower():
            fl = md[0][key]
    if fl is not None:
        fl = float(fl.split()[0]) / 25.4 # convert mm to inches
    return fl

def main():
    img = runner('test1.JPG')
    cv2.imshow("Image", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

main()
from PIL import ImageChops  # $ pip install pillow
from pyscreenshot import grab  # $ pip install pyscreenshot
import time
from ar_text_shooter import ARTextShooter


class ARMonitorChangeDetector():
    def detect_pixel_changes(self):
        im = grab()
        while True:  # http://effbot.org/zone/pil-comparing-images.htm
            time.sleep(1)
            diff = ImageChops.difference(grab(), im)
            bbox = diff.getbbox()
            if bbox is not None:  # exact comparison
                break
        return [diff.crop(bbox), bbox]

    def monitor_screen(self, window):
        ar_text_shooter = ARTextShooter()
        while True:
            changed_area = self.detect_pixel_changes()
            print("Area Changed: "+str(changed_area))
            start = time.time()
            content_to_buttonize = ar_text_shooter.shoot(changed_area[0], changed_area[1])
            end = time.time()
            print("Time OCR: "+str(end - start))
            if len(content_to_buttonize)>1:
                print("Detected text: "+content_to_buttonize)
                window.buttonize(content_to_buttonize)
            else:
                print("No text detected")


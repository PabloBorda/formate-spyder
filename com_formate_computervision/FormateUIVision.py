import ocrspace

from com_formate_computervision.FormateVisionInput import FormateVisionInput


class FormateUIVision(FormateVisionInput):
    def __init__(self):
        self.api = ocrspace.API()
        #self.api.ocr_url('URL of image goes here')
        self.api.ocr_file('image.jpg')


import ocrspace

api = ocrspace.API()
        #self.api.ocr_url('URL of image goes here')
a =  api.ocr_file('allfin.png')
print("result: " + str(a))

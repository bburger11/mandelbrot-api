import json
import cherrypy
import hashlib
import os
import subprocess
from PIL import Image
import io

BASENAME = "bitmap.py"

class BitmapController(object):
    def __init__(self):
        pass

    def image_to_byte_array(self, image:Image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
        print(type(imgByteArr))
        return imgByteArr

    def GET_BITMAP(self, filename):
        path = "/root/mandelbrot-api/mandel/images/{}".format(filename)
        output = {'result': 'success'}
        if os.path.isfile(path):
            print("{}: file {} found. Returning image".format(BASENAME, filename))
            cherrypy.response.headers['Content-Type'] = "image/bmp"
            cherrypy.response.headers['Content-Disposition'] = "attachment; filename=\"{};\"".format(path)
            try:  
                img  = Image.open(path)
                bytez = self.image_to_byte_array(img)
                return bytez
            except: 
                output['result'] = error
                return json.dumps(output)
        else:
            print("{}: file {} not found. Returning error".format(BASENAME, filename))
            output['result'] = 'error'
        return json.dumps(output)

    def POST_ARGS(self, s, x, y):
        '''
        Post request to send arguments for mandel.
        '''
        output = {'result': 'success'}
        output['filename'] = None
        # Hash inputs to get unique filename
        params = "s:{}x:{}y:{}".format(s, x, y)
        hash_object = hashlib.md5(params.encode('utf-8'))
        filename = hash_object.hexdigest()

        if os.path.isfile("/root/mandelbrot-api/mandel/images/{}.bmp".format(filename)):
            # Get filename from server
            print("{}: file already found. returning file {}".format(BASENAME, "{}.bmp".format(filename)))
            output['filename'] = "{}.bmp".format(filename)
        else:
            # Execute mandel
            command = ["/root/mandelbrot-api/mandel/bin/mandel", "-s", s, "-x", x, "-y", y, "-o", "/root/mandelbrot-api/mandel/images/{}.bmp".format(filename)]
            print("{}: starting mandel".format(BASENAME))
            p = subprocess.call(command)
            if not p:
                print("{}: image generated".format(BASENAME))
                output['filename'] = "{}.bmp".format(filename)
            else:
                print("{}: error creating image".format(BASENAME))
                output['result'] = 'error'
        return json.dumps(output)

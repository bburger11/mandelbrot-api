import cherrypy
import json

# Import database and controllers
from controllers.bitmap import BitmapController

class optionsController:
    def OPTIONS(self, *args, **kwargs):
        return ""

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

def start_service():
    # Declare controller objects
    bcon     = BitmapController()

    # Declare dispatcher object
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    # Connect to bitmap controller
    dispatcher.connect('bitmap_get', '/bitmap/:filename/', controller=bcon, action='GET_BITMAP', conditions=dict(method=['GET']))
    dispatcher.connect('bitmap_post', '/bitmap/:s/:x/:y/', controller=bcon, action='POST_ARGS', conditions=dict(method=['POST']))
    
    # Configuration
    conf = {
            'global' : {
                'server.socket_host' : '138.197.0.13',
                'server.socket_port' : 51018,
                },
            '/' : {'request.dispatch' : dispatcher,
                   'tools.CORS.on': True
                  }
            }
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

# Main
if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    start_service()
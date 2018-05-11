from flask import *
import os
import time


app = Flask(__name__)


#######################Response Codes########################

SUCCESS='success'
UNSUCCESS='unsuccess'
YES='yes'
NO='no'
####################### End  Response codes ########################

@app.route('/isenablesystem')
def isenablethesystem():
    if app.config['enablesystem']:
    	resp=make_response(YES)
    else:
        resp=make_response(NO)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/enablesystem')
def enablethesystem():
    
    app.config['enablesystem']=True
    resp=make_response(SUCCESS)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/disablesystem')
def disablethesystem():
    app.config['enablesystem']=False
    resp=make_response(SUCCESS)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.errorhandler(404)
def not_found(error):
    print(error)
    return make_response(render_template('error.html'), 404)


if __name__ == '__main__':
    
    EMAIL = 'proantitheft@gmail.com'
    PASSWORD = 'sciencesciences8307'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.config['BASE_DIR'] = BASE_DIR
    app.config['enablesystem'] = True
    app.run('0.0.0.0', 3000, True)

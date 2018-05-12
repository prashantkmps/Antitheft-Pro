import os
import time
import threading
from flask import *

app = Flask(__name__)


# ################ Connection Setup ####################

# light = pin 16 ( GPIO 23 )
# siren = pin 18 ( GPIO 24 )
# pir = pin 22 ( GPIO 25 )
# ServoMotor ( Gas ) = pin 32 ( GPIO 12 )
# DistanceSensor = pin 38 ( GPIO 10 ), pin 39 ( GPIO 20 )
# ServoMotor ( Gate ) = pin 7 ( GPIO 4 )

# ################ End  Connection Setup ####################



# ################ Response Codes ####################

SUCCESS = 'success'
UNSUCCESS = 'unsuccess'
YES = 'yes'
NO = 'no'


# ################ End  Response codes ####################

@app.route('/isenablesystem')
def isenablethesystem():
    if app.secret_key == request.args.get('secretkey'):
        if app.config['enablesystem']:
            resp = make_response(YES)
        else:
            resp = make_response(NO)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/enablesystem')
def enablethesystem():
    if app.secret_key == request.args.get('secretkey'):
        app.config['enablesystem'] = True
        resp = make_response(SUCCESS)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/disablesystem')
def disablethesystem():
    if app.secret_key == request.args.get('secretkey'):
        app.config['enablesystem'] = False
        resp = make_response(SUCCESS)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("Run recurring task")
            if app.config['enablesystem']:
                if detectmotion():
                    light(True)
                    if not verifyface(30):
                        alarm(True)
                        mail()
                        gas(True)
                        door(True)
                        while True:
                            if not app.config['enablesystem']:
                                alarm(False)
                                gas(False)
                                door(False)
                                break
                            time.sleep(0.1)
                    else:
                        if islighton():
                            light(False)
            time.sleep(0.1)
    threading.Thread(target=run_job).start()


if __name__ == '__main__':
    EMAIL = 'proantitheft@gmail.com'
    PASSWORD = 'sciencesciences8307'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    app.secret_key = 'VA7e5qS/5SSS5~8DF!kKK{KN5/.@4T'
    app.config['BASE_DIR'] = BASE_DIR
    app.config['enablesystem'] = True
    app.run('0.0.0.0', 3000, True)

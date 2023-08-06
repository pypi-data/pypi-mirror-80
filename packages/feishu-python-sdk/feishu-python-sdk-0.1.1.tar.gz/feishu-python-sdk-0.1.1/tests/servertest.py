from feishu import setup_event_blueprint, Event
from flask import Flask, Blueprint

app = Flask(__name__)

PATH_EVENT = '/feishu/event/callback'
VERIFY_TOKEN = ''  # 为空则不校验verify_token
ENCRYPT_KEY = ''  # 飞书应用没启用encrypt_key的话可以不填


def on_event(event: Event):
    print(event)


event_app = Blueprint(name="event_app", import_name=__name__)
setup_event_blueprint("flask", blueprint=event_app, path=PATH_EVENT,
                      on_event=on_event, verify_token=VERIFY_TOKEN, encrypt_key=ENCRYPT_KEY)
app.register_blueprint(event_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

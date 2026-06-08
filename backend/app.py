from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading
from assistant import (
    get_voice_input,
    generate_reply,
    speak_text,
    stop_voice
)

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('index.html')


# Speak selected message
@app.route('/speak', methods=['POST'])
def speak():

    data = request.get_json()

    text = data.get("text", "")

    stop_voice()

    threading.Thread(
        target=speak_text,
        args=(text,),
        daemon=True
    ).start()

    return jsonify({
        "status": "success"
    })

# Listen from microphone
@app.route('/listen')
def listen():

    try:

        user_text = get_voice_input()

        if not user_text:

            return jsonify({
                "user": "",
                "reply": "Please speak again"
            })

        print("User:", user_text)

        reply = generate_reply(user_text)

        print("Reply:", reply)

        threading.Thread(
            target=speak_text,
            args=(reply,),
            daemon=True
        ).start()

        return jsonify({
            "user": user_text,
            "reply": reply
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "user": "",
            "reply": str(e)
        })


# Stop voice
@app.route('/stop')
def stop():

    stop_voice()

    return jsonify({
        "status": "stopped"
    })


if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )
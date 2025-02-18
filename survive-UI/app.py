import os
import json
import webbrowser
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory

app = Flask(__name__, static_folder="static")
app.secret_key = 'my_secret_key'  # Replace with a secure secret key

# Load game data from survive/survive.json
with open(os.path.join('survive', 'survive.json'), 'r', encoding='utf-8') as f:
    game_data = json.load(f)

# Serve files from the survive folder (for image resources)
@app.route('/survive/<path:filename>')
def survive_static(filename):
    return send_from_directory('survive', filename)

def init_game():
    session['state'] = "1"
    session['entered'] = True

@app.route('/')
def index():
    # If the user hasn't entered the game yet, show the cover page.
    if not session.get('entered'):
        cover_url = url_for('survive_static', filename='cover.jpg')
        return render_template('cover.html', cover_url=cover_url)

    # Main game page
    state_key = session.get('state', "1")
    chapter = game_data.get(state_key)
    if not chapter:
        return "未知状态: " + state_key

    text = chapter.get("text", "没有描述")
    options = chapter.get("options", [])
    
    # Use the scene image if exists (from survive/[state_key].jpg)
    image_path = os.path.join("survive", f"{state_key}.jpg")
    if os.path.exists(image_path):
        image_url = url_for('survive_static', filename=f"{state_key}.jpg")
    else:
        image_url = None

    return render_template('index.html', text=text, options=options, image=image_url)

@app.route('/action', methods=['POST'])
def action():
    next_state = request.form.get("next")
    if next_state:
        session['state'] = next_state
    return redirect(url_for('index'))

@app.route('/enter')
def enter():
    init_game()
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")  # Open the browser
    app.run(debug=True)
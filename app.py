from flask import Flask, request, render_template_string
import WazeRouteCalculator
from werkzeug.serving import run_simple
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_address = request.form.get('from_address')
        to_address = request.form.get('to_address')

        region = 'IL'
        route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
        route_time, route_distance = route.calc_route_info()

        result = f'מ{from_address} ל{to_address} משך נסיעה {route_time} דקות, מרחק {route_distance} ק"מ.'
        return result

    # Render the form when accessed via GET
    return render_template_string('''
        <form method="post">
            From: <input type="text" name="from_address"><br>
            To: <input type="text" name="to_address"><br>
            <input type="submit" value="Calculate Route">
        </form>
    ''')

def run():
    run_simple('localhost', 5000, app)

# Running the Flask app in a separate thread
thread = Thread(target=run)
thread.start()

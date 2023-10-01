from flask import Flask, request, render_template
import WazeRouteCalculator
from werkzeug.serving import run_simple
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_address = request.form.get('from_address')
        to_addresses = request.form.getlist('to_address_choices')
        
        custom_address = request.form.get('to_address_custom')
        if custom_address:
            to_addresses.append(custom_address)
        
        results = []
        for to_address in to_addresses:
            region = 'IL'
            route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
            route_time, route_distance = route.calc_route_info()
            result = f'מ{from_address} ל{to_address} משך נסיעה %d דקות, מרחק %d ק"מ.' % (route_time, route_distance)
            results.append(result)

        result_text = '<br>'.join(results)
        return render_template('response.html', result_text=result_text)

    # Render the form when accessed via GET
    return render_template('index.html')

def run():
    run_simple('localhost', 5000, app)

# Running the Flask app in a separate thread
thread = Thread(target=run)
thread.start()

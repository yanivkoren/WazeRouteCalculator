from flask import Flask, request, render_template
import WazeRouteCalculator
from werkzeug.serving import run_simple
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_address = request.form.get('from_address')
        from_address_name = request.form.get('from_address_name')
        to_addresses = request.form.getlist('to_address_choices')
        to_address_labels = request.form.get('to_address_labels').split('##')
        
        custom_address = request.form.get('to_address_custom')
        if custom_address:
            to_addresses.append(custom_address)
        
        results = []
        #for to_address in to_addresses:
        for to_address, to_address_label in zip(to_addresses, to_address_labels):
            region = 'IL'
            route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
            route_time, route_distance = route.calc_route_info()
            result = f'מ{from_address_name} ל{to_address_label} משך נסיעה %d דקות, מרחק %d ק"מ.' % (route_time, route_distance)
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

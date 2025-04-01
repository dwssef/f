from flask import Flask, render_template_string
import inspect
import threading

app = Flask(__name__)

def get_help_info(func):
    help_info = {}
    for i in dir(func):
        attribute = getattr(func, i)
        doc = inspect.getdoc(attribute)
        help_info[i] = {
            'type': str(type(attribute)),
            'doc': doc if doc else "No documentation available."
        }
    return help_info

def hhelp(object):
    help_info = get_help_info(object)

    @app.route('/')
    def index():
        return render_template_string('''
            <h1>python object help documentation</h1>
            <ul>
            {% for name, info in help_info.items() %}
                <li><a href="/help/{{ name }}">{{ name }}</a></li>
            {% endfor %}
            </ul>
        ''', help_info=help_info)

    @app.route('/help/<name>')
    def help_page(name):
        info = help_info.get(name)
        if info:
            return render_template_string('''
                <h1>Help for {{ name }}</h1>
                <p><strong>Type:</strong> {{ info['type'] }}</p>
                <p><strong>Documentation:</strong></p>
                <pre>{{ info['doc'] }}</pre>
                <a href="/">Back to Index</a>
            ''', name=name, info=info)
        return "Help not found", 404

    def run_flask():
        app.run(host="0.0.0.0", port=5000, use_reloader=False, threaded=True)
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
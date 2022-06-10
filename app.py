from flask import Flask
from flask import request
import stop_loading

app = Flask(__name__)

@app.route('/')
def load():
    url = request.args.get('url') #may have to url encode
    load_time = request.args.get('load_time', default=0.5)

    # #set up driver to return as soon as possible (before the ads kick in)
    # options = Options()
    # options.add_experimental_option("detach", True)
    # options.page_load_strategy = 'eager'
    # driver = webdriver.Chrome(options=options)

    try:
        load_time = float(load_time)
    except TypeError:
        load_time = 0.5

    return stop_loading.stop_loading_after_seconds(url, load_time)






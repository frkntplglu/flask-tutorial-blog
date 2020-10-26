from flask import Flask # import flas

# Bu en basitçe bir flask uygulaması başlatmanın yolu ama proje büyüdükçe hatalara sebep olabilir.
app = Flask(__name__) # initialize flask

@app.route('/') # Decorator as a router
def hello():
    return "Hello World"
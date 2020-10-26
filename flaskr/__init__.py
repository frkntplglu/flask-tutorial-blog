import os

from flask import Flask
from . import db
from . import auth
from . import blog
    

# Global olarak Flask instance tanımlamak yerine bunu bir fonksiyon içinde yapacağız
# Bu instanceı başlatacağımız fonksiyona Application Factory denir.
def create_app(test_config=None):
    # create and configure the app
    # ikinci parametre config dosyasının instance ile aynı klasörde olduğunu söyler.Burada flaskr klasörü.
    app = Flask(__name__, instance_relative_config=True)

    # bu fonksiyon default konfigurasyonları ayarlamak için kullanılır.
    # SECRET_KEY : burası productionda random value ile overridden edilmelidir.
    # DATABASE : burası da SQLite database dosyasının kaydedileceği yeri belirtir.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not nesting
        # Default konfigurasyonların üstüne yazan konfigurasyon dosyasını belirtiyoruz.
        # Mesala bu deploy ederken SECRET_KEY'i tanımlamak için kullanılır.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # Flask instance folderı otomatik yaratmaz o yüzden biz burada garantiye alıyoruz.
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "Hello World!"

    db.init_app(app)
    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
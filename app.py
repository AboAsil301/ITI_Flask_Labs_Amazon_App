from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/',endpoint='index')
def hello_world():
     # return 'Hello World!'
     return render_template('productes/index.html')

if __name__ == '__main__':
    app.run()
#
#
# products = [{'id': 1, "name": 'Ahmed', 'category': 'python'},
#             {'id': 2, "name": 'Abdelrahman', 'category': 'python'},
#             {'id': 3, "name": 'Eman', 'category': 'python'},
#             {'id': 4, "name": 'Enas', 'category': 'python'}]
#
#
# @app.rote('/landing', endpoint='landing')
# def land():
#     return render_template('land/landing.html',products = products)
# @app.route('/landing/<int:id>', endpoint='product.profile')
# def product_profile(id):
#     filtered_products = list(filter(lambda std: std['id'] == id, products))
#     if filtered_products:
#         product = filtered_products[0]
#         return render_template('land/profile.html', product=product)
#     # return 'Not Found', 404
#     return render_template('errors/page_not_found.html'), 404

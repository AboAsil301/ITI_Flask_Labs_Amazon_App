from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'static/products/images/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# another option to the application
if __name__ == '__main__':
    app.run(debug=True)

# from terminal
"""
    export FLASK_APP=app  
    export DEBUG=True
    to run pp 
    flask run --debug
"""

""" Connect to database ====> sqlite """
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)  # this will create instance folder --> contains db


# define db models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    instock = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __str__(self):
        return f"{self.name}"

    def get_image_url(self):
        return  f'products/images/{self.image}'

@app.route('/',endpoint='index')
def home():
    products = Product.query.all()
    return render_template('products/index.html', products=products)


@app.route('/products/', endpoint='products.index')
def products_index():
    products = Product.query.all()
    return  render_template('products/index.html', products=products)
@app.route('/products/<int:id>', endpoint='products.show')
def product_show(id):
    product = Product.query.get_or_404(id)
    return render_template('products/show.html', product=product)


@app.route('/products/edit/<int:id>', endpoint='products.edit')
def product_edit(id):
    product = Product.query.get_or_404(id)
    return render_template('products/edit.html', product=product)


# Function to generate the filename in the format "product-{product_id}.jpg"
def generate_unique_filename(product_id, filename):
    # Extract the file extension from the original filename
    file_extension = os.path.splitext(filename)[1]

    # Combine the product's ID and the desired format
    unique_filename = f"product-{product_id}{file_extension}"

    return unique_filename

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'], endpoint='products.update')
def update(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.instock = request.form.get('instock') == 'on'

        # Check if a new image was uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])  # Create the directory if it doesn't exist

                if product.image:
                    # Remove the old image if it exists
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Generate a unique filename based on the product ID
                unique_filename = generate_unique_filename(product.id, filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                file.save(file_path)
                product.image = unique_filename  # Update the product's image

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('products.index'))

    return render_template('products/edit.html', product=product)


## create new object
@app.route('/products/create', methods=['GET', 'POST'], endpoint='products.create')
def create():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            instock=request.form.get('instock') == 'on'
        )

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)

                # Generate a unique filename based on the product ID
                # Assuming you have an ID column as the primary key
                product_id = db.session.query(Product).count() + 1  # Increment product ID
                unique_filename = generate_unique_filename(product_id, filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                file.save(file_path)
                product.image = unique_filename  # Update the product's image in the database

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.index'))

    return render_template('products/create.html')



ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@app.route('/products/delete/<int:id>', endpoint='products.delete')
def delete(id):
    product = Product.query.get_or_404(id)

    # Remove the product's image file, if it exists
    if product.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.index'))


@app.route('/contact', methods=['GET'], endpoint='contact')
def contact():
    return render_template('land/contact_us.html')

@app.route('/abouts', methods=['GET'], endpoint='abouts')
def contact():
    return render_template('land/about.html')

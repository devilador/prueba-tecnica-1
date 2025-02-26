from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

BASE_API_URL = os.getenv("PRODUCT_API_URL", "http://product-service:8000")

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    try:
        response = requests.get(f"{BASE_API_URL}/products/")
        response.raise_for_status()
        products = response.json()

        # Filtrar los productos según la búsqueda y la categoría
        if search_query:
            products = [product for product in products if search_query.lower() in product['name'].lower()]
        if category_filter:
            products = [product for product in products if product['category'] == category_filter]

        return render_template('index.html', products=products)
    except requests.exceptions.RequestException as e:
        flash('No se pudo obtener la lista de productos. Intente más tarde.')
        return render_template('index.html', products=[])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])

        # Validar que el precio sea mayor a 0
        if price <= 0:
            flash('El precio debe ser mayor a 0.', 'danger')
            return redirect(url_for('create'))
        
        product_data = {
            "name": name,
            "description": request.form['description'],
            "category": request.form['category'],
            "price": price,
            "quantity": int(request.form['quantity'])
        }

        # Verificar si el producto ya existe
        try:
            response = requests.get(f"{BASE_API_URL}/products/")
            response.raise_for_status()
            products = response.json()
            existing_product = next((product for product in products if product['name'].lower() == name.lower()), None)
            if existing_product:
                flash('El producto ya existe.', 'danger')
                return redirect(url_for('create'))

            response = requests.post(f"{BASE_API_URL}/products/", json=product_data)
            response.raise_for_status()
            flash('Producto creado exitosamente!', 'success')
        except requests.exceptions.RequestException as e:
            flash('No se pudo crear el producto. Intente más tarde.', 'danger')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update(product_id):
    if request.method == 'POST':
        product_data = {
            "name": request.form['name'],
            "description": request.form['description'],
            "category": request.form['category'],
            "price": float(request.form['price']),
            "quantity": int(request.form['quantity']),
            "sold_date": request.form.get('sold_date', None),
            "sold_quantity": request.form.get('sold_quantity', None),
            "sold_price": request.form.get('sold_price', None)
        }
        try:
            response = requests.put(f"{BASE_API_URL}/products/{product_id}", json=product_data)
            response.raise_for_status()
            flash('Producto actualizado exitosamente!', 'success')
        except requests.exceptions.RequestException as e:
            flash('No se pudo actualizar el producto. Intente más tarde.', 'danger')
        return redirect(url_for('index'))
    else:
        try:
            response = requests.get(f"{BASE_API_URL}/products/{product_id}")
            response.raise_for_status()
            product = response.json()
            return render_template('update.html', product=product)
        except requests.exceptions.RequestException as e:
            flash('No se pudo obtener el producto. Intente más tarde.', 'danger')
            return redirect(url_for('index'))

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete(product_id):
    try:
        response = requests.delete(f"{BASE_API_URL}/products/{product_id}")
        response.raise_for_status()
        flash('Producto eliminado exitosamente!', 'success')
    except requests.exceptions.RequestException as e:
        flash('No se pudo eliminar el producto. Intente más tarde.', 'danger')
    return redirect(url_for('index'))

@app.route('/stock/<int:product_id>', methods=['GET', 'POST'])
def add_stock(product_id):
    if request.method == 'POST':
        additional_quantity = int(request.form['additional_quantity'])

        # Validar que la cantidad adicional sea mayor a 0
        if additional_quantity <= 0:
            flash('La cantidad adicional debe ser mayor a 0.', 'danger')
            return redirect(url_for('add_stock', product_id=product_id))

        try:
            response = requests.get(f"{BASE_API_URL}/products/{product_id}")
            response.raise_for_status()
            product = response.json()
            
            product['quantity'] += additional_quantity
            
            response = requests.put(f"{BASE_API_URL}/products/{product_id}", json=product)
            response.raise_for_status()
            flash('Stock actualizado exitosamente!', 'success')
        except requests.exceptions.RequestException as e:
            flash('No se pudo actualizar el stock. Intente más tarde.', 'danger')
        return redirect(url_for('index'))
    else:
        try:
            response = requests.get(f"{BASE_API_URL}/products/{product_id}")
            response.raise_for_status()
            product = response.json()
            return render_template('stock.html', product=product)
        except requests.exceptions.RequestException as e:
            flash('No se pudo obtener el producto. Intente más tarde.', 'danger')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

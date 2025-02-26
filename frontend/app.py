
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

BASE_API_URL = "http://backend:8000"

@app.route('/')
def index():
    try:
        response = requests.get(f"{BASE_API_URL}/products/")
        response.raise_for_status()
        products = response.json()
        return render_template('index.html', products=products)
    except requests.exceptions.RequestException as e:
        flash('No se pudo obtener la lista de productos. Intente más tarde.')
        return render_template('index.html', products=[])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        product_data = {
            "name": request.form['name'],
            "description": request.form['description'],
            "category": request.form['category'],
            "price": float(request.form['price']),
            "quantity": int(request.form['quantity'])
        }
        try:
            response = requests.post(f"{BASE_API_URL}/products/", json=product_data)
            response.raise_for_status()
            flash('Producto creado exitosamente!')
        except requests.exceptions.RequestException as e:
            flash('No se pudo crear el producto. Intente más tarde.')
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
            "quantity": int(request.form['quantity'])
        }
        try:
            response = requests.put(f"{BASE_API_URL}/products/{product_id}", json=product_data)
            response.raise_for_status()
            flash('Producto actualizado exitosamente!')
        except requests.exceptions.RequestException as e:
            flash('No se pudo actualizar el producto. Intente más tarde.')
        return redirect(url_for('index'))
    else:
        try:
            response = requests.get(f"{BASE_API_URL}/products/{product_id}")
            response.raise_for_status()
            product = response.json()
            return render_template('update.html', product=product)
        except requests.exceptions.RequestException as e:
            flash('No se pudo obtener el producto. Intente más tarde.')
            return redirect(url_for('index'))

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete(product_id):
    try:
        response = requests.delete(f"{BASE_API_URL}/products/{product_id}")
        response.raise_for_status()
        flash('Producto eliminado exitosamente!')
    except requests.exceptions.RequestException as e:
        flash('No se pudo eliminar el producto. Intente más tarde.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
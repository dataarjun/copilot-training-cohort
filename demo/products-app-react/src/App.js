import React, { useState, useEffect } from 'react';
import ProductList from './components/ProductList';
import ProductForm from './components/ProductForm';
import ProductService from './services/ProductService';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const products = await ProductService.getProducts();
      setProducts(products);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const addProduct = async (product) => {
    try {
      await ProductService.addProduct(product);
      fetchProducts();
    } catch (error) {
      console.error('Error adding product:', error);
    }
  };

  const updateProduct = async (product) => {
    try {
      await ProductService.updateProduct(product);
      fetchProducts();
    } catch (error) {
      console.error('Error updating product:', error);
    }
  };

  const deleteProduct = async (productId) => {
    try {
      await ProductService.deleteProduct(productId);
      fetchProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
    }
  };

  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/add-product">
            <ProductForm addProduct={addProduct} />
          </Route>
          <Route path="/edit-product/:productId">
            <ProductForm products={products} updateProduct={updateProduct} />
          </Route>
          <Route path="/">
            <ProductList products={products} deleteProduct={deleteProduct} />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
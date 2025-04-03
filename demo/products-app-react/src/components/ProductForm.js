import React, { useState, useEffect } from 'react';
import productService from '../services/ProductService';
import { useParams, useHistory } from 'react-router-dom';

const ProductForm = () => {
  const { productId } = useParams();
  const history = useHistory();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');

  useEffect(() => {
    if (productId) {
      productService.getProduct(productId)
        .then(product => {
          setName(product.name);
          setDescription(product.description);
          setPrice(product.price);
          setQuantity(product.quantity);
        });
    }
  }, [productId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const productData = { 
      name, 
      description, 
      price, 
      quantity 
    };

    if (productId) {
      productService.updateProduct(productId, productData)
        .then(() => {
          console.log('Product updated successfully');
          history.push('/products');
        })
        .catch((error) => {
          console.error('Error updating product:', error);
        });
    } else {
      productService.createProduct(productData)
        .then(() => {
          console.log('Product created successfully');
          history.push('/products');
        })
        .catch((error) => {
          console.error('Error creating product:', error);
        });
    }
  };

  const operationType = productId ? 'Update Product' : 'Create Product';

  return (
    <div>
      <h2>{operationType}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input name ="name" type="text" value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div>
          <label>Description:</label>
          <textarea name = "description" value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>
        <div>
          <label>Price:</label>
          <input name = "price" type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
        </div>
        <div>
          <label>Quantity:</label>
          <input name = "quantity" type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
        </div>
        <button type="submit">{operationType}</button>    
      </form>
    </div>
  );
};
export default ProductForm;
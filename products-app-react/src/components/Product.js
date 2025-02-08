import React from 'react';

const Product = ({ id, name, description, price, quantity }) => {
  return (
    <div className="product">
      <h3>{name}</h3>
      <p>{description}</p>
      <p>Price: ${price}</p>
      <p>Quantity: {quantity}</p>
    </div>
  );
};

export default Product;
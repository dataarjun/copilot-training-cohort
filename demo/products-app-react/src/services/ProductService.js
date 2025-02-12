class ProductService {
  baseUrl = 'http://localhost:5000'; // Replace with your Python API base URL

  async getProducts() {
    const response = await fetch(`${this.baseUrl}/products`);
    const data = await response.json();
    return data;
  }

  async getProduct(id) {
    const response = await fetch(`${this.baseUrl}/products/${id}`);
    const data = await response.json();
    return data;
  }

  async createProduct(product) {
    const response = await fetch(`${this.baseUrl}/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(product),
    });
    const data = await response.json();
    return data;
  }

  async updateProduct(id, product) {
    const response = await fetch(`${this.baseUrl}/products/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(product),
    });
    const data = await response.json();
    return data;
  }

  async deleteProduct(id) {
    const response = await fetch(`${this.baseUrl}/products/${id}`, {
      method: 'DELETE',
    });
    const data = await response.json();
    return data;
  }
}

const productService = new ProductService();
export default productService; 
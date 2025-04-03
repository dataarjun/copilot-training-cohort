import productService from './ProductService';
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

beforeEach(() => {
  fetchMock.resetMocks();
});

test('getProducts returns the expected data', async () => {
  const mockData = [{ id: 1, name: 'Product 1' }, { id: 2, name: 'Product 2' }];
  fetchMock.mockResponseOnce(JSON.stringify(mockData));

  const data = await productService.getProducts();

  expect(data).toEqual(mockData);
  expect(fetchMock.mock.calls.length).toEqual(1);
  expect(fetchMock.mock.calls[0][0]).toEqual(`${productService.baseUrl}/products`);
});

test('getProduct returns the expected data', async () => {
  const mockData = { id: 1, name: 'Product 1' };
  fetchMock.mockResponseOnce(JSON.stringify(mockData));

  const data = await productService.getProduct(1);

  expect(data).toEqual(mockData);
  expect(fetchMock.mock.calls.length).toEqual(1);
  expect(fetchMock.mock.calls[0][0]).toEqual(`${productService.baseUrl}/products/1`);
});

test('createProduct sends the expected data', async () => {
  const mockData = { id: 1, name: 'Product 1' };
  fetchMock.mockResponseOnce(JSON.stringify(mockData));

  const data = await productService.createProduct(mockData);

  expect(data).toEqual(mockData);
  expect(fetchMock.mock.calls.length).toEqual(1);
  expect(fetchMock.mock.calls[0][0]).toEqual(`${productService.baseUrl}/products`);
  expect(fetchMock.mock.calls[0][1]).toEqual({
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(mockData),
  });
});

test('updateProduct sends the expected data', async () => {
    const mockData = { id: 1, name: 'Product 1' };
    fetchMock.mockResponseOnce(JSON.stringify(mockData));
    
    const data = await productService.updateProduct(1, mockData);
    
    expect(data).toEqual(mockData);
    expect(fetchMock.mock.calls.length).toEqual(1);
    expect(fetchMock.mock.calls[0][0]).toEqual(`${productService.baseUrl}/products/1`);
    expect(fetchMock.mock.calls[0][1]).toEqual({
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mockData),
    });
});

test('deleteProduct sends the expected data', async () => {
  const mockData = { id: 1, name: 'Product 1' };
  fetchMock.mockResponseOnce(JSON.stringify(mockData));
  
  const data = await productService.deleteProduct(1);
  
  expect(data).toEqual(mockData);
  expect(fetchMock.mock.calls.length).toEqual(1);
  expect(fetchMock.mock.calls[0][0]).toEqual(`${productService.baseUrl}/products/1`);
  expect(fetchMock.mock.calls[0][1]).toEqual({
    method: 'DELETE',
  });
});


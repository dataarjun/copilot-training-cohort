# products-app-react

This is a ReactJS application that consumes the REST endpoints exposed by the `products-app-python` Python application for performing CRUD operations on products.

## Project Structure

```
products-app-react
├── public
│   └── index.html
├── src
│   ├── App.js
│   ├── index.js
│   ├── components
│   │   ├── ProductList.js
│   │   ├── ProductForm.js
│   │   └── Product.js
│   ├── services
│   │   └── ProductService.js
│   └── styles
│       └── App.css
├── package.json
├── .gitignore
└── README.md
```

## File Descriptions

- `public/index.html`: Entry point of the React application.
- `src/App.js`: Main component of the React application.
- `src/index.js`: Entry point of the React application.
- `src/components/ProductList.js`: Component that displays a list of products.
- `src/components/ProductForm.js`: Component that provides a form to create or update a product.
- `src/components/Product.js`: Component that represents a single product.
- `src/services/ProductService.js`: Service class for interacting with the Python API endpoints.
- `src/styles/App.css`: CSS styles for the `App` component.
- `package.json`: Configuration file for npm.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: Documentation for the project.

## Getting Started

1. Clone the repository.
2. Install the dependencies using `npm install`.
3. Start the development server using `npm start`.
4. Access the application at `http://localhost:3000`.

## Usage

- The `ProductList` component displays a list of products fetched from the Python API.
- The `ProductForm` component provides a form to create or update a product. It sends the product data to the Python API.
- The `Product` component represents a single product and displays its details.

## Dependencies

- React
- React DOM
- Axios (for making HTTP requests)
- Bootstrap (for styling)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
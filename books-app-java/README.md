# books-app-java

This is a Spring Boot application that exposes CRUD operations on Books as REST APIs.

## Project Structure

```
books-app-java
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── firstlink
│   │   │           └── books
│   │   │               ├── BooksApplication.java
│   │   │               ├── controller
│   │   │               │   └── BookController.java
│   │   │               ├── service
│   │   │               │   └── BookService.java
│   │   │               ├── repository
│   │   │               │   └── BookRepository.java
│   │   │               └── model
│   │   │                   └── Book.java
│   │   └── resources
│   │       └── application.properties
│   └── test
│       └── java
│           └── com
│               └── firstlink
│                   └── books
│                       ├── controller
│                       │   └── BookControllerTest.java
│                       └── service
│                           └── BookServiceTest.java
├── build.gradle
└── README.md
```

## Files

### `src/main/java/com/firstlink/books/BooksApplication.java`

This file is the entry point of the Spring Boot application. It contains the main method to start the application.

### `src/main/java/com/firstlink/books/controller/BookController.java`

This file exports a class `BookController` which handles the REST API endpoints for CRUD operations on books. It delegates the calls to the `BookService` class.

### `src/main/java/com/firstlink/books/service/BookService.java`

This file exports a class `BookService` which contains the business logic for handling book operations. It delegates the calls to the `BookRepository` class for data access.

### `src/main/java/com/firstlink/books/repository/BookRepository.java`

This file exports an interface `BookRepository` which defines the methods for accessing the book data from the H2 database.

### `src/main/java/com/firstlink/books/model/Book.java`

This file exports a class `Book` which represents the book entity. It has attributes `id`, `title`, and `author`.

### `src/main/resources/application.properties`

This file contains the configuration properties for the application, including the H2 database connection settings.

### `src/test/java/com/firstlink/books/controller/BookControllerTest.java`

This file contains unit tests for the `BookController` class. It tests the REST API endpoints for CRUD operations on books.

### `src/test/java/com/firstlink/books/service/BookServiceTest.java`

This file contains unit tests for the `BookService` class. It tests the business logic for book operations.

### `build.gradle`

This file is the Gradle build script for the project. It defines the project dependencies and build configurations.

## Getting Started

To run the application, follow these steps:

1. Clone the repository.
2. Open the project in your preferred IDE.
3. Build the project using Gradle.
4. Run the `BooksApplication` class to start the application.
5. Access the REST API endpoints for CRUD operations on books.

## Dependencies

The project dependencies are managed using Gradle. The following dependencies are included:

- Spring Boot
- Spring Data JPA
- H2 Database
- JUnit 5

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
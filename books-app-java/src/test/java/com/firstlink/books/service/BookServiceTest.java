package com.firstlink.books.service;

import com.firstlink.books.model.Book;
import com.firstlink.books.repository.BookRepository;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Row;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

public class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private BookService bookService;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testGetAllBooks() {
        List<Book> books = new ArrayList<>();
        Book book1 = new Book();
        book1.setId(1L);
        book1.setTitle("Book 1");
        book1.setAuthor("Author 1");
        books.add(book1);

        Book book2 = new Book();
        book2.setId(2L);
        book2.setTitle("Book 2");
        book2.setAuthor("Author 2");
        books.add(book2);

        when(bookRepository.findAll(Specification.where(null), Pageable.unpaged())).thenReturn(new PageImpl<Book>(books));

        Page<Book> result = bookService.getAllBooks(Specification.where(null), Pageable.unpaged());

        assertEquals(2, result.getContent().size());
        assertEquals("Book 1", result.getContent().get(0).getTitle());
        assertEquals("Author 1", result.getContent().get(0).getAuthor());
        assertEquals("Book 2", result.getContent().get(1).getTitle());
        assertEquals("Author 2", result.getContent().get(1).getAuthor());

        verify(bookRepository, times(1)).findAll(Specification.where(null), Pageable.unpaged());
    }



    @Test
    public void testGetBookById() {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));

        Optional<Book> result = bookService.getBookById(1L);

        assertEquals("Book 1", result.get().getTitle());
        assertEquals("Author 1", result.get().getAuthor());

        verify(bookRepository, times(1)).findById(1L);
    }

    @Test
    public void testCreateBook() {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookRepository.save(book)).thenReturn(book);

        Book result = bookService.createBook(book);

        assertEquals("Book 1", result.getTitle());
        assertEquals("Author 1", result.getAuthor());

        verify(bookRepository, times(1)).save(book);
    }

    @Test
    public void testUpdateBook() {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
        when(bookRepository.save(book)).thenReturn(book);

        Book result = bookService.updateBook(1L, book);

        assertEquals("Book 1", result.getTitle());
        assertEquals("Author 1", result.getAuthor());

        verify(bookRepository, times(1)).findById(1L);
        verify(bookRepository, times(1)).save(book);
    }

    @Test
    public void testDeleteBook() {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));

        bookService.getBookById(1L);
        bookService.deleteBook(1L);

        verify(bookRepository, times(2)).findById(1L);
        verify(bookRepository, times(1)).delete(book);
    }

    @DisplayName("Should create Excel file with correct data when books exist")
    @Test
    public void createExcelFile_BooksExist_ReturnsCorrectData() {
        Book book1 = new Book();
        book1.setId(1L);
        book1.setTitle("Book 1");
        book1.setAuthor("Author 1");

        Book book2 = new Book();
        book2.setId(2L);
        book2.setTitle("Book 2");
        book2.setAuthor("Author 2");

        List<Book> books = Arrays.asList(book1, book2);

        when(bookRepository.findAll()).thenReturn(books);

        Workbook workbook = bookService.createExcelFile();
        Sheet sheet = workbook.getSheetAt(0);
        Row row1 = sheet.getRow(1);
        Row row2 = sheet.getRow(2);

        assertEquals(1L, (long) row1.getCell(0).getNumericCellValue());
        assertEquals("Book 1", row1.getCell(1).getStringCellValue());
        assertEquals("Author 1", row1.getCell(2).getStringCellValue());

        assertEquals(2L, (long) row2.getCell(0).getNumericCellValue());
        assertEquals("Book 2", row2.getCell(1).getStringCellValue());
        assertEquals("Author 2", row2.getCell(2).getStringCellValue());
    }

    @DisplayName("Should create Excel file with no data when no books exist")
    @Test
    public void createExcelFile_NoBooksExist_ReturnsNoData() {
        when(bookRepository.findAll()).thenReturn(Arrays.asList());

        Workbook workbook = bookService.createExcelFile();
        Sheet sheet = workbook.getSheetAt(0);

        assertEquals(1, sheet.getPhysicalNumberOfRows()); // Only header row
    }

    @DisplayName("Should return books by title and author when they exist")
    @Test
    public void getBooksByTitleAndAuthor_BooksExist_ReturnsBooks() {
        Book book1 = new Book();
        book1.setId(1L);
        book1.setTitle("Book 1");
        book1.setAuthor("Author 1");

        Book book2 = new Book();
        book2.setId(2L);
        book2.setTitle("Book 2");
        book2.setAuthor("Author 2");

        List<Book> books = Arrays.asList(book1, book2);

        when(bookRepository.findAll(any(Specification.class))).thenReturn(books);

        Specification<Book> spec = bookService.getBooksByTitleAndAuthor("Book", "Author");
        List<Book> result = bookRepository.findAll(spec);

        assertEquals(2, result.size());
        assertEquals("Book 1", result.get(0).getTitle());
        assertEquals("Author 1", result.get(0).getAuthor());
        assertEquals("Book 2", result.get(1).getTitle());
        assertEquals("Author 2", result.get(1).getAuthor());
    }

    @DisplayName("Should return no books by title and author when they do not exist")
    @Test
    public void getBooksByTitleAndAuthor_NoBooksExist_ReturnsNoBooks() {
        when(bookRepository.findAll((Specification<Book>) null)).thenReturn(Arrays.asList());

        Specification<Book> spec = bookService.getBooksByTitleAndAuthor("Nonexistent", "Nonexistent");
        List<Book> result = bookRepository.findAll(spec);

        assertEquals(0, result.size());
    }
}
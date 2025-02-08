package com.firstlink.books.controller;

import com.firstlink.books.model.Book;
import com.firstlink.books.service.BookService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

public class BookControllerTest {

    private MockMvc mockMvc;

    @Mock
    private BookService bookService;

    @InjectMocks
    private BookController bookController;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.initMocks(this);
        mockMvc = MockMvcBuilders.standaloneSetup(bookController).build();
    }

    @Test
    public void testGetAllBooks() throws Exception {
        Book book1 = new Book();
        book1.setId(1L);
        book1.setTitle("Book 1");
        book1.setAuthor("Author 1");

        Book book2 = new Book();
        book2.setId(2L);
        book2.setTitle("Book 2");
        book2.setAuthor("Author 2");

        List<Book> books = Arrays.asList(book1, book2);

        when(bookService.getAllBooks(any(Specification.class), any(Pageable.class))).thenReturn(new PageImpl<>(books));

        mockMvc.perform(get("/books")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].id").value(1))
                .andExpect(jsonPath("$.content[0].title").value("Book 1"))
                .andExpect(jsonPath("$.content[0].author").value("Author 1"))
                .andExpect(jsonPath("$.content[1].id").value(2))
                .andExpect(jsonPath("$.content[1].title").value("Book 2"))
                .andExpect(jsonPath("$.content[1].author").value("Author 2"));

        verify(bookService, times(1)).getAllBooks(any(Specification.class), any(Pageable.class));
        verifyNoMoreInteractions(bookService);
    }

    @Test
    public void testGetBookById() throws Exception {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookService.getBookById(1L)).thenReturn(Optional.of(book));

        mockMvc.perform(get("/books/1")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.title").value("Book 1"))
                .andExpect(jsonPath("$.author").value("Author 1"));

        verify(bookService, times(1)).getBookById(1L);
        verifyNoMoreInteractions(bookService);
    }

    @Test
    public void testCreateBook() throws Exception {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookService.createBook(any(Book.class))).thenReturn(book);

        mockMvc.perform(post("/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\":\"Book 1\",\"author\":\"Author 1\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.title").value("Book 1"))
                .andExpect(jsonPath("$.author").value("Author 1"));

        verify(bookService, times(1)).createBook(any(Book.class));
        verifyNoMoreInteractions(bookService);
    }

    @Test
    public void testUpdateBook() throws Exception {
        Book book = new Book();
        book.setId(1L);
        book.setTitle("Book 1");
        book.setAuthor("Author 1");

        when(bookService.updateBook(any(Long.class), any(Book.class))).thenReturn(book);

        mockMvc.perform(put("/books/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\":\"Book 1\",\"author\":\"Author 1\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.title").value("Book 1"))
                .andExpect(jsonPath("$.author").value("Author 1"));

        verify(bookService, times(1)).updateBook(any(Long.class), any(Book.class));
        verifyNoMoreInteractions(bookService);
    }

    @Test
    public void testDeleteBook() throws Exception {
        mockMvc.perform(delete("/books/1")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk());

        verify(bookService, times(1)).deleteBook(1L);
        verifyNoMoreInteractions(bookService);
    }
}
package com.firstlink.books.service;

import com.firstlink.books.model.Book;
import com.firstlink.books.repository.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import javax.persistence.criteria.Predicate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class BookService {

    private final BookRepository bookRepository;

    @Autowired
    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public Page<Book> getAllBooks(Specification<Book> spec, Pageable pageable) {
        return bookRepository.findAll(spec, pageable);
    }

    public Specification<Book> getBooksByTitleAndAuthor(String title, String author) {
        return (root, query, criteriaBuilder) -> {
            List<Predicate> predicates = new ArrayList<>();
            if (title != null) {
                predicates.add(criteriaBuilder.like(root.get("title"), "%" + title + "%"));
            }
            if (author != null) {
                predicates.add(criteriaBuilder.like(root.get("author"), "%" + author + "%"));
            }
            return criteriaBuilder.and(predicates.toArray(new Predicate[predicates.size()]));
        };
    }

    public Optional<Book> getBookById(Long id) {
        return bookRepository.findById(id);
    }

    public Book createBook(Book book) {
        return bookRepository.save(book);
    }

    public Book updateBook(Long id, Book book) {
        Optional<Book> existingBook = bookRepository.findById(id);
        if (existingBook.isPresent()) {
            book.setId(id);
            return bookRepository.save(book);
        } else {
            throw new IllegalArgumentException("Book not found with id: " + id);
        }
    }

    public void deleteBook(Long id) {
        Book book = bookRepository.findById(id).orElseThrow(() -> new RuntimeException("Book not found with id " + id));
        bookRepository.delete(book);
    }

     public Workbook createExcelFile() {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Books");
        createHeaderRow(sheet);

        List<Book> books = bookRepository.findAll();
        for (int i = 0; i < books.size(); i++) {
            createBookRow(sheet, i + 1, books.get(i));
        }

        return workbook;
    }

    private void createHeaderRow(Sheet sheet) {
        Row headerRow = sheet.createRow(0);
        headerRow.createCell(0).setCellValue("ID");
        headerRow.createCell(1).setCellValue("Title");
        headerRow.createCell(2).setCellValue("Author");
    }

    private void createBookRow(Sheet sheet, int rowIndex, Book book) {
        Row row = sheet.createRow(rowIndex);
        row.createCell(0).setCellValue(book.getId());
        row.createCell(1).setCellValue(book.getTitle());
        row.createCell(2).setCellValue(book.getAuthor());
    }

}
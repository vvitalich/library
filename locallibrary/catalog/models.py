from django.db import models
from django.urls import reverse
import uuid


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)
       Модель, представляющая язык (например, английский, французский, японский и т. Д.)
    """
    name = models.CharField(max_length=200,
                            help_text="Введите естественный язык книги (например, английский, французский, японский и т. Д.)", verbose_name='Язык')

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).

    Модель, представляющая жанр книги (например, научная фантастика,
    научно-популярная литература).
    """
    name = models.CharField(max_length=200, help_text="Укажите жанр книги (например, научная фантастика, французская поэзия и т. Д.)", verbose_name='Жанр')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)

        Строка для представления объекта модели (на сайте администратора и т. Д.)
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    Модель, представляющая книгу (но не конкретный экземпляр книги).
    """
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    # Используется внешний ключ, потому что у книги может быть только один автор, но у авторов может быть несколько книг
    # Автор как строка, а не объект, потому что он еще не был объявлен в файле.

    summary = models.TextField(max_length=2000, help_text="Введите краткое описание книги", verbose_name='Описание')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для этой книги. Удерживайте нажатой клавишу «Control» или «Command» на Mac, чтобы выбрать более одного жанра.", verbose_name='Жанр')

    # Используется  ManyToManyField, поскольку жанр может содержать много книг. Книги могут охватывать многие жанры.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, verbose_name='Язык')

    def __str__(self):
        """
        String for representing the Model object.
        Строка для представления объекта модели
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        Возвращает URL-адрес для доступа к конкретному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Создает строку для жанра. Это необходимо для отображения жанра в админке.
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанр'


class Author(models.Model):
    """
    Model representing an author.
    Модель, представляющая автора.
    """
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    date_of_death = models.DateField(null=True, blank=True, verbose_name='Дата смерти')

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        Возвращает URL-адрес для доступа к конкретному экземпляру автора
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        Строка для представления объекта модели.
        """
        return '%s, %s' % (self.last_name, self.first_name)


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    Модель, представляющая конкретный экземпляр книги (то есть который можно взять из библиотеки).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='Название')
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True, verbose_name='Возврат' )

    LOAN_STATUS = (
        ('m', 'Обслуживание'),
        ('o', 'Выдан'),
        ('a', 'Доступен'),
        ('r', 'Зарезервированна'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability', verbose_name='Состояние')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """
        String for representing the Model object
        Строка для представления объекта модели
        """
        return '%s (%s)' % (self.book.title, self.id)


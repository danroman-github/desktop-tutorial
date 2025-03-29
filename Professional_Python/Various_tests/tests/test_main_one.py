import unittest
from unittest import TestCase

from main_one import documents, directories, get_name, get_directory, add_new_document

class TestMainOne(TestCase):
    """Набор тестов для программы 'Секретарь'."""

    def setUp(self):
        """Сохраняем исходные данные перед каждым тестом"""
        self.original_documents = documents.copy()
        self.original_directories = {k: v.copy() for k, v in directories.items()}

    def tearDown(self):
        """Восстанавливаем исходные данные после каждого теста"""
        global documents, directories
        documents = self.original_documents.copy()
        directories = {k: v.copy() for k, v in self.original_directories.items()}

    def test_get_name_existing(self):
        """Тест поиска владельца для существующих номеров документов"""
        self.assertEqual(get_name("2207 876234"), "Василий Гупкин")
        self.assertEqual(get_name("10006"), "Аристарх Павлов")

    def test_get_name_non_existing(self):
        """Тест поиска владельца для несуществующих номеров документов"""
        self.assertEqual(get_name("12345"), "Документ не найден")

    def test_get_directory_existing(self):
        """Тест номера полки, для существующих номеров документов"""
        self.assertEqual(get_directory("10006"), '2')
        self.assertEqual(get_directory("11-2"), '1')

    def test_get_directory_non_existing(self):
        """Тест номера полки, для несуществующих номеров документов"""
        self.assertEqual(get_directory("12345"), "Полки с таким документом не найдено")

    def test_add_new_document_existing(self):
        """Тест добавления документа в список documents на существующую полку"""
        add_new_document("test", "112233", "Тестируемый", '1')

        self.assertEqual(documents[-1]["type"], "test")
        self.assertEqual(documents[-1]["number"], "112233")
        self.assertEqual(documents[-1]["name"], "Тестируемый")
        self.assertIn("112233", directories['1'])

    def test_add_new_document_to_new_shelf(self):
        """Тест добавления документа на новую полку"""
        add_new_document("test2", "441144", "Тест на новую полку", 4)



import unittest
import requests


class TestMainTwo(unittest.TestCase):

    def setUp(self):
        self.yandex_token = "Введите сюда токен ЯндексДиска"

        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Authorization": f"OAuth {self.yandex_token}",
            "Content-Type": "application/json",
        }
        self.folder_name = "test_folder"
        self.folder_path = f"{self.base_url}?path={self.folder_name}"

    def tearDown(self):
        """Удаляем тестовую папку после каждого теста (если она существует)"""
        requests.delete(
            f"{self.base_url}?path={self.folder_name}",
            headers=self.headers,
        )

    def test_create_folder_integration(self):
        """Тест на успешное создание папки, код 201."""
        response = requests.put(
            self.folder_path,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("href", response.json())

    def test_delete_folder_success(self):
        """Тест на успешное удаление папки, код 204."""
        requests.put(
            f"{self.base_url}?path={self.folder_name}",
            headers=self.headers,
        )
        response = requests.delete(
            f"{self.base_url}?path={self.folder_name}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)

    def test_create_folder_already_exists(self):
        """Тест папка уже существует, код 409."""
        requests.put(
            f"{self.base_url}?path={self.folder_name}",
            headers=self.headers,
        )
        response = requests.put(
            f"{self.base_url}?path={self.folder_name}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 409)  # Conflict
        self.assertEqual(response.json()["error"], "DiskPathPointsToExistentDirectoryError")

    def test_get_nonexistent_folder(self):
        """Тест папка не существует, код 404."""
        response = requests.get(
            f"{self.base_url}?path=nonexistent_folder",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)  # Not Found
        self.assertEqual(response.json()["error"], "DiskNotFoundError")


if __name__ == "__main__":
    unittest.main()
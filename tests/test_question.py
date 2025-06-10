import pytest
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks.task_manager import add_task, find_task_with_keyword, get_longest_task, remove_task, filter_long_tasks, is_even_task_count, reverse_tasks, sort_tasks, total_character_count, uppercase_tasks

def test_add_task():
    tasks = ["Ring delivery"]
    result = add_task(tasks.copy(), "Defeat Sauron")
    assert result == ["Ring delivery", "Defeat Sauron"]

def test_remove_task():
    tasks = ["Ring delivery", "Defeat Sauron"]
    result = remove_task(tasks.copy(), "Defeat Sauron")
    assert result == ["Ring delivery"]

def test_filter_long_tasks():
    tasks = ["Ring", "Destroy the One Ring", "Fight", "Talk to Elrond"]
    result = filter_long_tasks(tasks)
    assert result == ["Destroy the One Ring", "Talk to Elrond"]

def test_is_even_task_count_true():
    tasks = ["A", "B"]
    assert is_even_task_count(tasks) == True

def test_is_even_task_count_false():
    tasks = ["A", "B", "C"]
    assert is_even_task_count(tasks) == False

def test_uppercase_tasks():
    tasks = ["Find the ring", "Fight orcs"]
    assert uppercase_tasks(tasks) == ["FIND THE RING", "FIGHT ORCS"]

def test_reverse_tasks():
    tasks = ["A", "B", "C"]
    assert reverse_tasks(tasks) == ["C", "B", "A"]

def test_find_task_with_keyword():
    tasks = ["Destroy the ring", "Visit Rivendell", "Talk to Elrond"]
    assert find_task_with_keyword(tasks, "ring") == ["Destroy the ring"]

def test_get_longest_task():
    tasks = ["Run", "Walk to Mordor", "Fight"]
    assert get_longest_task(tasks) == "Walk to Mordor"

def test_sort_tasks():
    tasks = ["Fight", "Destroy", "Attack"]
    assert sort_tasks(tasks) == ["Attack", "Destroy", "Fight"]

def test_total_character_count():
    tasks = ["ABC", "DEF", "GHIJ"]
    assert total_character_count(tasks) == 10

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://edugen-backend-487d2168bc6c.herokuapp.com/projectLog/"
    payload = {
        "user_id": 203,
        "project_id": 100,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()
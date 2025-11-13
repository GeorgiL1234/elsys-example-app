import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os
from main import app, STORAGE_DIR

client = TestClient(app)

TEST_STORAGE_DIR = STORAGE_DIR
TEST_FILE_CONTENT = b"Hello, FastAPI!"
TEST_FILE_NAME = "test_file.txt"

def setup_module(module):
    """Създава тестови файл преди всички тестове"""
    TEST_STORAGE_DIR.mkdir(exist_ok=True)

def teardown_module(module):
    """Почиства тестовата директория след всички тестове"""
    for f in TEST_STORAGE_DIR.iterdir():
        if f.is_file():
            f.unlink()

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "endpoints" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_store_file():
    response = client.post(
        "/files",
        files={"file": (TEST_FILE_NAME, TEST_FILE_CONTENT, "text/plain")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == TEST_FILE_NAME
    assert data["size"] == len(TEST_FILE_CONTENT)

def test_get_file():
    client.post("/files", files={"file": (TEST_FILE_NAME, TEST_FILE_CONTENT, "text/plain")})
    
    response = client.get(f"/files/{TEST_FILE_NAME}")
    assert response.status_code == 200
    assert response.content == TEST_FILE_CONTENT

def test_list_files():

    client.post("/files", files={"file": (TEST_FILE_NAME, TEST_FILE_CONTENT, "text/plain")})
    
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert TEST_FILE_NAME in data["files"]
    assert data["count"] >= 1

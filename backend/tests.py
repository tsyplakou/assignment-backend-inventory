import os
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage.models import Base, StorageSpace, ItemType, Item
from settings.dependencies import get_db, session

from main import app

engine = create_engine(os.environ['DB_URL'], echo=True)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def clean_db():
    with session(bind=engine) as s:
        s.query(StorageSpace).delete()
        s.query(ItemType).delete()
        s.query(Item).delete()


class TestStorageSpace:
    def _retrieve_storage_spaces_count(self):
        with engine.connect() as con:
            rs = con.execute('SELECT count(*) FROM storage_space')
        return rs.one()[0]

    @classmethod
    def setup(cls):
        clean_db()
        with session(bind=engine) as s:
            for index in range(1, 3):
                storage_space = StorageSpace(
                    name=f'Space{index}',
                    is_refrigerated=bool(index % 2),
                    max_capacity=index * 5,
                )
                s.add(storage_space)
        cls.storage_space = s.query(StorageSpace).first()

    def test_storage_spaces_list(self):
        with engine.connect() as con:
            rs = con.execute('SELECT count(*) FROM storage_space')

        response = client.get('/storage_spaces/')
        assert response.status_code == 200
        assert len(response.json()) == rs.one()[0]

    def test_storage_spaces_create(self):
        response = client.post(
            '/storage_spaces/',
            json={
                'name': 'New refrigerated storage',
                'is_refrigerated': True,
                'max_capacity': 35,
            },
        )

        assert response.status_code == 200
        assert self._retrieve_storage_spaces_count() == 3

    def test_storage_space_retrieving_by_id_returns_correct_storage_space(self):
        response = client.get(f'/storage_spaces/{self.storage_space.id}/')

        assert response.status_code == 200
        assert response.json() == {
            'id': self.storage_space.id,
            'name': self.storage_space.name,
            'is_refrigerated': self.storage_space.is_refrigerated,
            'max_capacity': self.storage_space.max_capacity,
        }


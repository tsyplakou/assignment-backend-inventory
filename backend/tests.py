import os
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from settings.dependencies import get_db, session
from storage.models import Base, StorageSpace, ItemType, Item

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
        s.query(Item).delete()
        s.query(StorageSpace).delete()
        s.query(ItemType).delete()


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
                    name=('Refrigerator', 'Shelves')[index-1],
                    is_refrigerated=bool(index % 2),
                    max_capacity=index * 5,
                )
                s.add(storage_space)
                item_type = ItemType(
                    name=('Ice-cream', 'Cookies')[index-1],
                    is_kept_cold=bool(index % 2),
                )
                s.add(item_type)
                s.commit()
                s.refresh(storage_space)
                s.refresh(item_type)
                s.add(Item(
                    name=('Ben & Jerry`s', 'Oreo')[index - 1],
                    expiration_date=(datetime.now() + timedelta(days=3)).date(),
                    item_type_id=item_type.id,
                    storage_space_id=storage_space.id,
                ))
        cls.storage_space = s.query(StorageSpace).first()
        cls.related_item = s.query(Item).first()

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

    def test_update_storage_space_validates_data_and_updates_instance(self):
        response = client.put(
            f'/storage_spaces/{self.storage_space.id}/',
            json={
                'name': self.storage_space.name + ' new',
                'is_refrigerated': not self.storage_space.is_refrigerated,
            }
        )

        assert response.status_code == 400
        assert response.json() == {
            'detail': (
                'Storage space refregerating can\'t be updated when items '
                'inside.'
            ),
        }

        response = client.put(
            f'/storage_spaces/{self.storage_space.id}/',
            json={
                'name': self.storage_space.name + ' new',
                'is_refrigerated': self.storage_space.is_refrigerated,
            }
        )
        assert response.status_code == 200
        assert response.json()['name'] == self.storage_space.name + ' new'

    def test_delete_storage_space_validates_data_and_deletes_instance(self):
        response = client.delete(f'/storage_spaces/{self.storage_space.id}/')

        assert response.status_code == 400
        assert response.json() == {
            'detail': 'Storage space contains items. It can\'t be deleted.'
        }

        with session(bind=engine) as s:
            s.add(StorageSpace(
                name='To be removed',
                is_refrigerated=True,
                max_capacity=10,
            ))
        response = client.delete(
            '/storage_spaces/{}/'.format(s.query(StorageSpace).order_by(
                StorageSpace.id.desc()
            ).first().id)
        )
        assert response.status_code == 204


    def test_read_items_in_storage_place_returns_list_of_related_items(self):
        response = client.get(f'/storage_spaces/{self.storage_space.id}/items/')

        assert response.status_code == 200
        assert response.json() == [{
            'id': self.related_item.id,
            'name': self.related_item.name,
            'expiration_date': self.related_item.expiration_date.isoformat(),
            'item_type_id': self.related_item.item_type_id,
            'storage_space_id': self.storage_space.id,
        }]

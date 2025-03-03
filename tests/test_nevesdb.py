import pytest
from sqlalchemy import Integer, String

from nevesdb import SQLAdapter, NevesDB, Model


class Note(Model):
    id: Integer
    title: String

@pytest.fixture
def db_uri():
    return f'mysql+aiomysql://root:password@localhost:3306/test'


@pytest.fixture
def db(db_uri):
    db_instance = NevesDB(db_uri,SQLAdapter)
    yield db_instance

@pytest.mark.asyncio
async def test_register_models(db):
    models = [Note]
    db.register_models(models)
    assert len(db.adapter.model_classes) == len(models)

@pytest.mark.asyncio
async def test_add(db):
    note = Note(title="testing")
    await db.add(Note, note)

    notes = await db.get_all(Note)
    assert len(notes) == 1
    assert notes[0].title == "testing"

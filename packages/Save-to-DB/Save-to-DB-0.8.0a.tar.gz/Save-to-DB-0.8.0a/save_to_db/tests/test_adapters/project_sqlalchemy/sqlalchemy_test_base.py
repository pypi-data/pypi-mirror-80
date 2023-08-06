from save_to_db.utils.test_base import TestBase
from .config import Base, engine, session


class SqlalchemyTestBase(TestBase):
    def setUp(self):
        # preparing database
        session.rollback()
        session.expunge_all()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        super().setUp()

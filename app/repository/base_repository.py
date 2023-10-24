class BaseRepository:
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        return entity

    def remove(self, entity, document_id: int):
        document = self.session.query(entity).filter(entity.id == document_id).first()
        self.session.delete(document)
        self.session.commit()

    def update(self, entity, document_id: int, document: dict):
        self.session.query(entity).filter(entity.id == document_id).update(document)
        self.session.commit()

    def get_by_id(self, entity, document_id: int):
        return self.session.query(entity).filter(entity.id == document_id).first()

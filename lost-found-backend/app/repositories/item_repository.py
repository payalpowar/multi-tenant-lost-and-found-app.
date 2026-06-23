from sqlalchemy.orm import Session

from models.item import Item


class ItemRepository:

    @staticmethod
    def create_item(
        db: Session,
        item_data: dict
    ):
        item = Item(**item_data)

        db.add(item)
        db.commit()
        db.refresh(item)

        return item

    @staticmethod
    def get_item_by_id(
        db: Session,
        item_id: int,
        tenant_id: int
    ):
        return db.query(Item).filter(
            Item.item_id == item_id,
            Item.tenant_id == tenant_id
        ).first()

    @staticmethod
    def get_all_items(
        db: Session,
        tenant_id: int
    ):
        return db.query(Item).filter(
            Item.tenant_id == tenant_id
        ).all()

    @staticmethod
    def update_item(
        db: Session,
        item: Item,
        item_data: dict
    ):
        for key, value in item_data.items():
            if value is not None:
                setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item

    @staticmethod
    def delete_item(
        db: Session,
        item: Item
    ):
        db.delete(item)
        db.commit()

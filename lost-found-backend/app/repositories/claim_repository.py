from sqlalchemy.orm import Session

from models.claim import Claim
from models.item import Item
from models.user import User


class ClaimRepository:

    @staticmethod
    def create_claim(
        db: Session,
        claim_data: dict
    ):
        claim = Claim(**claim_data)

        db.add(claim)
        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def get_claim_by_id(
        db: Session,
        claim_id: int,
        tenant_id: int
    ):
        return (
            db.query(Claim)
            .join(Item, Claim.item_id == Item.item_id)
            .filter(
                Claim.claim_id == claim_id,
                Item.tenant_id == tenant_id
            )
            .first()
        )

    @staticmethod
    def get_all_claims(
        db: Session,
        tenant_id: int
    ):
        return (
            db.query(Claim)
            .join(Item, Claim.item_id == Item.item_id)
            .filter(Item.tenant_id == tenant_id)
            .all()
        )

    @staticmethod
    def get_claims_by_item(
        db: Session,
        item_id: int,
        tenant_id: int
    ):
        return (
            db.query(Claim)
            .join(Item, Claim.item_id == Item.item_id)
            .filter(
                Claim.item_id == item_id,
                Item.tenant_id == tenant_id
            )
            .all()
        )

    @staticmethod
    def get_claims_by_user(
        db: Session,
        user_id: int,
        tenant_id: int
    ):
        return (
            db.query(Claim)
            .join(User, Claim.user_id == User.user_id)
            .filter(
                Claim.user_id == user_id,
                User.tenant_id == tenant_id
            )
            .all()
        )

    @staticmethod
    def update_claim(
        db: Session,
        claim: Claim,
        claim_data: dict
    ):
        for key, value in claim_data.items():
            if value is not None:
                setattr(claim, key, value)

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def delete_claim(
        db: Session,
        claim: Claim
    ):
        db.delete(claim)
        db.commit()

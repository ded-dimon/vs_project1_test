from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from app.database import Base


if TYPE_CHECKING:
    from app.models.products import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        
        #только сохранение, обновление
        cascade="save-update, merge"
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="children",
        remote_side="Category.id"
    )

    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent"
    )


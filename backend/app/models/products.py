from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database import Base


if TYPE_CHECKING:
    from app.models.categories import Category
    from app.models.users import User
    from app.models.reviews import Review



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    rating: Mapped[float] = mapped_column(default=0.0, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    seller: Mapped["User"] = relationship("User", back_populates="products")
    
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="product")
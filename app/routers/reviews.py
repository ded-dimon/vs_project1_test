from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update, select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_async_db
from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.auth import get_current_seller, get_current_buyer, get_current_admin
from app.models import User as UserModel


router = APIRouter(prefix="/reviews", tags=["reviews"])


async def update_product_rating(db: AsyncSession, product_id: int):
    product = await db.get(ProductModel, product_id)
    if product is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    stmt_avg = select(func.avg(ReviewModel.grade)).where(ReviewModel.product_id == product_id, ReviewModel.is_active == True)
    result_reviews_avg = await db.execute(stmt_avg)
    avg_reviews = result_reviews_avg.scalar_one_or_none()

    avg_rating = avg_reviews or 0.0

    product.rating = avg_rating
    await db.commit()


@router.get("/", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает все комментарии
    """
    stmt = select(ReviewModel).where(ReviewModel.is_active == True)
    result_reviews = await db.execute(stmt)
    return result_reviews.scalars().all()


@router.get("/products/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_product_reviews(product_id: int, db: AsyncSession = Depends(get_async_db)):
    stmt_product = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    result_product = await db.execute(stmt_product)
    product = result_product.scalar()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    stmt_reviews = select(ReviewModel).where(ReviewModel.product_id == product.id, ReviewModel.is_active == True)
    result_reviews = await db.execute(stmt_reviews)
    reviews = result_reviews.scalars().all()
    return reviews


@router.post("/", response_model=ReviewSchema)
async def create_reviews(review: ReviewCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_buyer)):
    stmt_product = select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active == True)
    result_product = await db.execute(stmt_product)
    product = result_product.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if review.grade > 5 or review.grade < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Wrong grade"
        )

    stmt_check = select(ReviewModel).where(
        ReviewModel.product_id == review.product_id,
        ReviewModel.user_id == current_user.id,
        ReviewModel.is_active == True
        )
    result_stmt_check = await db.execute(stmt_check)
    db_check_review = result_stmt_check.scalar_one_or_none()
    if db_check_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )

    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)

    await update_product_rating(db=db, product_id=review.product_id)

    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_admin)):
    """
    Удаляет отзыв
    """
    stmt_review = select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True)
    result_review = await db.execute(stmt_review)
    db_review = result_review.scalar()
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    await db.execute(
        update(ReviewModel)
        .where(ReviewModel.id == db_review.id)
        .values(is_active=False)
    )

    await db.commit()
    await db.refresh(db_review)
    
    await update_product_rating(db=db, product_id=db_review.product_id)

    return {"message": "Review deleted"}

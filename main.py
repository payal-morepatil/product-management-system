from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models

from database import engine, get_db

from schemas import ProductCreate, ProductResponse


# Create database tables
models.Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(title="Product Management System")


# Welcome API
@app.get("/")
def home():

    return {
        "message": "Welcome to Product Management System",
        "status": "API is running successfully"
    }


# CREATE PRODUCT
@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category=product.category
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return new_product


# GET ALL PRODUCTS
@app.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):

    products = db.query(models.Product).all()

    return products



# UPDATE PRODUCT
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name

    product.description = product_data.description

    product.price = product_data.price

    product.quantity = product_data.quantity

    product.category = product_data.category

    db.commit()

    db.refresh(product)

    return product


# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)

    db.commit()

    return {
        "message": "Product deleted successfully"
    }
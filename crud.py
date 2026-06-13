from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import CustomerCreate, CustomerOut
from logger import logger
import database
import models

def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer ID: {customer_id}")
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Listing customers with skip={skip}, limit={limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    logger.info(f"Created new customer with ID: {db_customer.id}")
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
        logger.warning(f"Deleted customer ID: {customer_id}")
        return True
    return False


def _count_rows(table_name: str, label: str) -> int:
    logger.info(f"Starting count query for {label}")
    db = database.SessionLocal()
    try:
        result = db.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
        count = int(result.scalar_one())
        logger.info(f"Completed count query for {label} with count={count}")
        return count
    except Exception:
        logger.exception(f"Database error while counting {label}")
        raise
    finally:
        db.close()
        logger.info(f"Database session closed after counting {label}")


def count_customers():
    return _count_rows("customers", "customers")


def count_orders():
    return _count_rows("orders", "orders")


def count_products():
    return _count_rows("products", "products")


def count_employees():
    return _count_rows("employees", "employees")


def count_offices():
    return _count_rows("offices", "offices")


def count_payments():
    return _count_rows("payments", "payments")


def count_orderdetails():
    return _count_rows("orderdetails", "orderdetails")


def count_productlines():
    return _count_rows("productlines", "productlines")
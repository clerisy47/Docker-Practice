from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import asyncio
from time import perf_counter
import crud
import schemas
import database
from logger import logger

router = APIRouter(prefix="/customers", tags=["Customers"])
counts_router = APIRouter(tags=["Counts"])


async def _run_count_endpoint(table_name: str, count_callable):
    logger.info(f"Incoming request for /{table_name}/count")
    try:
        count = await asyncio.to_thread(count_callable)
        logger.info(f"Request for /{table_name}/count completed successfully with status=200")
        return {table_name: count}
    except Exception:
        logger.exception(f"Request for /{table_name}/count failed with status=500")
        raise HTTPException(status_code=500, detail=f"Failed to fetch {table_name} count")


@counts_router.get("/customers/count")
async def customers_count():
    return await _run_count_endpoint("customers", crud.count_customers)


@counts_router.get("/orders/count")
async def orders_count():
    return await _run_count_endpoint("orders", crud.count_orders)


@counts_router.get("/products/count")
async def products_count():
    return await _run_count_endpoint("products", crud.count_products)


@counts_router.get("/employees/count")
async def employees_count():
    return await _run_count_endpoint("employees", crud.count_employees)


@counts_router.get("/offices/count")
async def offices_count():
    return await _run_count_endpoint("offices", crud.count_offices)


@counts_router.get("/payments/count")
async def payments_count():
    return await _run_count_endpoint("payments", crud.count_payments)


@counts_router.get("/orderdetails/count")
async def orderdetails_count():
    return await _run_count_endpoint("orderdetails", crud.count_orderdetails)


@counts_router.get("/productlines/count")
async def productlines_count():
    return await _run_count_endpoint("productlines", crud.count_productlines)


@counts_router.get("/overall_counts")
async def overall_counts():
    logger.info("Incoming request for /overall_counts")
    start_time = perf_counter()
    count_tasks = {
        "customers": asyncio.to_thread(crud.count_customers),
        "orders": asyncio.to_thread(crud.count_orders),
        "products": asyncio.to_thread(crud.count_products),
        "employees": asyncio.to_thread(crud.count_employees),
        "offices": asyncio.to_thread(crud.count_offices),
        "payments": asyncio.to_thread(crud.count_payments),
        "orderdetails": asyncio.to_thread(crud.count_orderdetails),
        "productlines": asyncio.to_thread(crud.count_productlines),
    }

    try:
        logger.info("Starting concurrent count tasks for /overall_counts")
        results = await asyncio.gather(*count_tasks.values())
        logger.info("asyncio.gather completed for /overall_counts")
        response = dict(zip(count_tasks.keys(), results))
        elapsed_seconds = perf_counter() - start_time
        logger.info(f"/overall_counts completed successfully with status=200 in {elapsed_seconds:.4f} seconds")
        return response
    except Exception:
        elapsed_seconds = perf_counter() - start_time
        logger.exception(f"/overall_counts failed with status=500 after {elapsed_seconds:.4f} seconds")
        raise HTTPException(status_code=500, detail="Failed to fetch overall counts")

@router.get("/", response_model=List[schemas.CustomerOut])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(database.get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        logger.error(f"Customer {customer_id} not found.")
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    return crud.create_customer(db=db, customer=customer)
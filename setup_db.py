import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from faker import Faker

# Database setup and Faker initialization
Base = declarative_base()
fake = Faker()

# --- 1. TABLE MODELS (SCHEMA) ---

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    loyalty_score = Column(Integer) # 1-100 range
    registration_date = Column(DateTime)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    cost = Column(Float)
    stock_quantity = Column(Integer)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    order_date = Column(DateTime)
    quantity = Column(Integer)
    discount_applied = Column(Float)
    shipping_delay_days = Column(Integer)
    status = Column(String) # Completed, Returned, Cancelled

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    rating = Column(Integer) # 1-5 range
    review_text = Column(Text)

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float)

# --- 2. DATA GENERATION (SEEDING) ---

def generate_fake_data(session):
    print("Generating fake data, this might take a few seconds...")
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys']
    statuses = ['Completed', 'Completed', 'Completed', 'Returned', 'Cancelled']
    
    # 1. Campaigns (3 Items)
    for i in range(3):
        camp = Campaign(
            name=f"Campaign 202{2+i}",
            start_date=fake.date_time_between(start_date='-2y', end_date='-1y'),
            end_date=fake.date_time_between(start_date='-1y', end_date='now'),
            budget=round(random.uniform(5000.0, 20000.0), 2)
        )
        session.add(camp)
        
    # 2. Customers (100 Items)
    customers = []
    for _ in range(100):
        c = Customer(
            name=fake.name(),
            age=random.randint(18, 70),
            country=fake.country(),
            city=fake.city(),
            loyalty_score=random.randint(1, 100),
            registration_date=fake.date_time_between(start_date='-3y', end_date='now')
        )
        session.add(c)
        customers.append(c)
    session.commit()

    # 3. Products (20 Items)
    products = []
    for _ in range(20):
        price = round(random.uniform(10.0, 500.0), 2)
        p = Product(
            name=fake.word().capitalize(),
            category=random.choice(categories),
            price=price,
            cost=round(price * random.uniform(0.4, 0.8), 2), # Cost should be lower than price
            stock_quantity=random.randint(0, 500)
        )
        session.add(p)
        products.append(p)
    session.commit()

    # 4. Orders (500 Items)
    orders = []
    for _ in range(500):
        o = Order(
            customer_id=random.choice(customers).id,
            product_id=random.choice(products).id,
            order_date=fake.date_time_between(start_date='-2y', end_date='now'),
            quantity=random.randint(1, 5),
            discount_applied=round(random.uniform(0.0, 0.3), 2), # Discount between 0% and 30%
            shipping_delay_days=random.randint(0, 10),
            status=random.choice(statuses)
        )
        session.add(o)
        orders.append(o)
    session.commit()

    # 5. Reviews (Test Data for AI Anomaly Analysis)
    # Adding logical reviews to a sample of orders
    for o in random.sample(orders, 150):
        # If shipping is delayed or order returned, give a bad rating and review
        if o.shipping_delay_days > 4 or o.status == 'Returned':
            rating = random.randint(1, 2)
            text = fake.sentence(nb_words=6) + " Very bad experience, delayed or returned."
        else:
            rating = random.randint(4, 5)
            text = fake.sentence(nb_words=5) + " Great product, highly recommended!"
            
        r = Review(
            customer_id=o.customer_id,
            product_id=o.product_id,
            rating=rating,
            review_text=text
        )
        session.add(r)
    
    session.commit()
    print("Awesome! Database successfully created: 'sample_company.db'")

if __name__ == "__main__":
    # Initialize SQLite database engine
    engine = create_engine('sqlite:///sample_company.db')
    
    # Drop existing tables and create new ones for a clean slate
    Base.metadata.drop_all(engine) 
    Base.metadata.create_all(engine)
    
    # Start database session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Generate and save data
    generate_fake_data(session)
    session.close()
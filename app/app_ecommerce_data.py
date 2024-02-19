from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from kafka import KafkaProducer
import json

fake = Faker()

# Define products
products = ['Laptop', 'Smartphone', 'Headphones', 'Charger', 'Camera', 'Tablet', 'Smartwatch']

# Kafka Producer Configuration
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Function to generate transaction data
def generate_transaction(start_date, end_date, num_transactions):
    transaction_data = []
    for _ in range(num_transactions):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        price_per_item = round(random.uniform(10.0, 1500.0), 2)
        total_price = round(quantity * price_per_item, 2)
        purchase_date = start_date + (end_date - start_date) * random.random()
        transaction_data.append({"product": product, "quantity": quantity, "price_per_item": price_per_item, "total_price": total_price, "purchase_date": purchase_date.isoformat()})
    return transaction_data

# Function to generate user interaction data
def generate_user_interaction(num_users, start_date, end_date):
    user_interaction_data = []
    actions = ['Page View', 'Product View', 'Add to Cart', 'Purchase']
    for _ in range(num_users):
        user_id = fake.uuid4()
        session_id = fake.uuid4()
        action = random.choice(actions)
        product = random.choice(products) if action != 'Page View' else None
        interaction_date = start_date + (end_date - start_date) * random.random()
        user_interaction_data.append({"user_id": user_id, "session_id": session_id, "action": action, "product": product, "interaction_date": interaction_date.isoformat()})
    return user_interaction_data

# Function to generate inventory data
def generate_inventory_data(products, start_date, end_date, num_updates):
    inventory_data = []
    for _ in range(num_updates):
        product = random.choice(products)
        stock_level = random.randint(0, 1000)
        update_date = start_date + (end_date - start_date) * random.random()
        inventory_data.append({"product": product, "stock_level": stock_level, "update_date": update_date.isoformat()})
    return inventory_data

# Main function to generate and send data to Kafka
def main():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Generate data
    transactions = generate_transaction(start_date, end_date, 10000)
    user_interactions = generate_user_interaction(50000, start_date, end_date)
    inventory_updates = generate_inventory_data(products, start_date, end_date, 2000)

    # Stream data to Kafka
    for transaction in transactions:
        producer.send('transactions', value=transaction)
    
    for interaction in user_interactions:
        producer.send('user_interactions', value=interaction)
    
    for inventory_update in inventory_updates:
        producer.send('inventory_updates', value=inventory_update)
    
    producer.flush()

if __name__ == "__main__":
    main()


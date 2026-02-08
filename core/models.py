users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT FALSE,
    is_login BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

products_table = """
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

menu_products = """
CREATE TABLE IF NOT EXISTS menu_products (
    id SERIAL PRIMARY KEY,
    date_of_menu DATE NOT NULL,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    amount INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

durations = """
CREATE TABLE IF NOT EXISTS durations (
    id SERIAL PRIMARY KEY,
    from_time TIME NOT NULL,
    to_time TIME NOT NULL,
    seats INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

orders = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    menu_product_id INT REFERENCES menu_products(id),
    amount INT NOT NULL,
    duration_id INT REFERENCES durations(id),
    status BOOLEAN DEFAULT FALSE,
    order_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

codes = """
CREATE TABLE IF NOT EXISTS codes (
    email VARCHAR(100),
    code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

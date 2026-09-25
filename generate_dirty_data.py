import random
import csv
import os

os.makedirs(r"c:\Users\Vitesh\Downloads\DataMorph AI\sample_data", exist_ok=True)
target_file = r"c:\Users\Vitesh\Downloads\DataMorph AI\sample_data\global_enterprise_dirty_dataset.csv"

# Diverse product names with intentional casing & typo variations
products = [
    ("iPhone 15 Pro", ["iPhone 15 Pro", "iphone 15 pro", "IPHONE 15 PRO", "iPhone 15 pro", "iphone15pro"], "Electronics", 999.00),
    ("MacBook Pro 16\"", ["MacBook Pro 16\"", "macbook pro 16", "MACBOOK PRO 16\"", "MacBookPro16", "macbook pro 16-inch"], "Computers", 2499.00),
    ("Sony WH-1000XM5", ["Sony WH-1000XM5", "sony wh-1000xm5", "SONY WH1000XM5", "Sony Headphones XM5"], "Audio", 399.99),
    ("Dell XPS 15", ["Dell XPS 15", "dell xps 15", "DELL XPS 15", "Dell XPS15"], "Computers", 1899.50),
    ("Samsung Galaxy S24 Ultra", ["Samsung Galaxy S24 Ultra", "samsung galaxy s24 ultra", "SAMSUNG GALAXY S24 ULTRA", "Galaxy S24 Ultra"], "Electronics", 1299.00),
    ("Logitech MX Master 3S", ["Logitech MX Master 3S", "logitech mx master 3s", "LOGITECH MX MASTER", "Logitech Mouse MX3S"], "Accessories", 99.00),
    ("Apple Watch Ultra 2", ["Apple Watch Ultra 2", "apple watch ultra 2", "APPLE WATCH ULTRA 2", "AppleWatchUltra2"], "Wearables", 799.00),
    ("LG OLED 65\" TV", ["LG OLED 65\" TV", "lg oled 65", "LG OLED 65 TV", "LG 65-inch OLED"], "Displays", 1699.00),
    ("Bose QuietComfort 45", ["Bose QuietComfort 45", "bose quietcomfort 45", "BOSE QC45", "Bose QC 45"], "Audio", 329.00),
    ("iPad Pro 12.9\"", ["iPad Pro 12.9\"", "ipad pro 12.9", "IPAD PRO 12.9\"", "iPadPro 12.9"], "Tablets", 1099.00)
]

regions = [
    ["North America", "north america", "NORTH AMERICA", "NA Region", "N. America"],
    ["Europe West", "europe west", "EUROPE WEST", "EU-West", "Europe-W"],
    ["Asia Pacific", "asia pacific", "ASIA PACIFIC", "APAC", "Asia-Pac"],
    ["Latin America", "latin america", "LATAM", "S. America"],
    ["Middle East", "middle east", "MENA", "Mid East"]
]

channels = ["Direct Sales", "Online Store", "Enterprise Partner", "Wholesale Retail", "Third-Party Marketplace"]
segments = ["Enterprise", "Mid-Market", "Small Business", "Direct Consumer", "Government"]
payment_methods = ["Corporate Wire", "Credit Card", "ACH Transfer", "PayPal", "Purchase Order", "Cryptocurrency"]
statuses = ["Delivered", "In Transit", "Processing", "Cancelled", "Refunded", "Pending Approval"]

headers = [
    "Transaction_ID",
    "Invoice_Date",
    "Product_Name",
    "Product_Category",
    "Sales_Region",
    "Base_Price",
    "Units_Ordered",
    "Discount_Percentage",
    "Tax_Amount",
    "Total_Invoice_USD",
    "Payment_Method",
    "Customer_Segment",
    "Fulfillment_Status",
    "Customer_Rating"
]

rows = []

# Generate 320 records
for i in range(1, 321):
    tx_id = f"TXN-2024-{10000 + i}"
    
    # Inconsistent Date Formats
    year = 2024
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    date_choice = random.randint(1, 6)
    if date_choice == 1:
        inv_date = f"{year}-{month:02d}-{day:02d}"  # ISO
    elif date_choice == 2:
        inv_date = f"{month:02d}/{day:02d}/{year}"  # US format
    elif date_choice == 3:
        inv_date = f"{day:02d}-{month:02d}-{year}"  # European dash
    elif date_choice == 4:
        months_str = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        inv_date = f"{day:02d} {months_str[month-1]} {year}"
    elif date_choice == 5:
        inv_date = f"{year}.{month:02d}.{day:02d}"
    else:
        inv_date = f"{year}/{month:02d}/{day:02d}"
        
    prod_tuple = random.choice(products)
    prod_name = random.choice(prod_tuple[1])
    cat = prod_tuple[2]
    base_price = prod_tuple[3]
    
    # Occasional messy category casing
    if random.random() < 0.2:
        cat = cat.lower() if random.random() < 0.5 else cat.upper()
        
    reg = random.choice(random.choice(regions))
    
    # Units ordered (with occasional outlier)
    if random.random() < 0.04:
        units = random.randint(150, 600)  # Enterprise bulk outlier
    elif random.random() < 0.03:
        units = ""  # Missing value
    else:
        units = random.randint(1, 25)
        
    # Inconsistent currency strings
    curr_style = random.randint(1, 6)
    if curr_style == 1:
        price_str = f"${base_price:,.2f}"
    elif curr_style == 2:
        price_str = f"₹{base_price * 83:,.0f}"
    elif curr_style == 3:
        price_str = f"€{base_price * 0.92:,.2f}"
    elif curr_style == 4:
        price_str = f"{base_price:.2f} USD"
    elif curr_style == 5:
        price_str = f"{base_price:.2f}"
    else:
        price_str = f"${base_price:,.0f}"
        
    # Discount percentage
    disc_val = random.choice([0, 5, 10, 15, 20, 25, 30])
    disc_str = f"{disc_val}%" if random.random() < 0.7 else f"0.{disc_val:02d}"
    
    # Missing / Tax
    if random.random() < 0.05:
        tax_str = "N/A"
    elif random.random() < 0.05:
        tax_str = ""
    else:
        tax_str = f"${(base_price * 0.08):.2f}"
        
    # Total calculation
    numeric_units = units if isinstance(units, int) else 1
    gross = base_price * numeric_units * (1 - (disc_val / 100.0))
    
    # Inconsistent total notation (refund negative parenthesis, comma separators, currency symbols)
    if random.random() < 0.03:
        total_str = f"({gross:,.2f})"  # Negative refund
    elif random.random() < 0.2:
        total_str = f"${gross:,.2f}"
    elif random.random() < 0.2:
        total_str = f"{gross:,.2f}"
    elif random.random() < 0.2:
        total_str = f"₹{gross * 83:,.0f}"
    else:
        total_str = f"${gross:.2f}"
        
    pm = random.choice(payment_methods) if random.random() > 0.04 else "null"
    seg = random.choice(segments) if random.random() > 0.03 else "---"
    stat = random.choice(statuses)
    
    # Rating (1 to 5, with occasional null / string)
    if random.random() < 0.06:
        rating = "Pending"
    elif random.random() < 0.04:
        rating = ""
    else:
        rating = random.choice([3.0, 3.5, 4.0, 4.2, 4.5, 4.8, 5.0, 1.0, 2.0])
        
    row = [
        tx_id,
        inv_date,
        prod_name,
        cat,
        reg,
        price_str,
        str(units),
        disc_str,
        tax_str,
        total_str,
        pm,
        seg,
        stat,
        str(rating)
    ]
    rows.append(row)

# Add intentional duplicate rows to test AI deduplication
for _ in range(12):
    dup_row = list(random.choice(rows[:30]))
    rows.append(dup_row)

with open(target_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Successfully generated {len(rows)} messy rows at {target_file}")

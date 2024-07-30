import mysql.connector
import random
from colorama import Fore, Style, init

init(convert=True)

mycon = mysql.connector.connect(host='localhost', user='root', passwd='1234', database='railway')
cursor = mycon.cursor()
mycon.autocommit = True

# Create tables if they don't exist
sl = "create table if not exists railway(name varchar(100),\
Phno varchar(15) primary key,age int(4),gender varchar(50),\
from_f varchar(100),to_t varchar(100),date_d varchar(20))"
cursor.execute(sl)

sl = "create table if not exists user_accounts(fname varchar(100),\
Iname varchar(100),user_name varchar(100),\
password varchar(100) primary key, \
Phno varchar(15),gender varchar(50),dob varchar(50),age varchar(4))"
cursor.execute(sl)

# Create PNR table if it doesn't exist
sl = "create table if not exists pnr(pnr_number varchar(20) primary key,\
Phno varchar(15),status varchar(100))"
cursor.execute(sl)

# Create catering orders table
sl = "create table if not exists catering_orders(order_number varchar(20) primary key,\
pnr_number varchar(20), food_items varchar(200), status varchar(100), total_cost float)"
cursor.execute(sl)

# Create food items table
sl = "create table if not exists food_items(item_id int auto_increment primary key,\
item_name varchar(100), price float)"
cursor.execute(sl)

# Function Definitions
def signin():
    a = input(Fore.CYAN + 'USER NAME:')
    b = input('PASSWORD:')
    s = "select user_name from user_accounts where password='{}'".format(b)
    cursor.execute(s)
    data = cursor.fetchone()
    if data and data[0] == a:
        print("\t\t\t\t--------------------------------------------")
        print(Fore.GREEN + "\t\t\t\t\t\tLOGIN SUCCESSFULLY")
        print("\t\t\t\t--------------------------------------------")
        main()
    else:
        print(Fore.RED + 'ACCOUNT DOES NOT EXIST or WRONG ENTRY')

def signup():
    f = input('FIRST NAME:')
    l = input("LAST NAME:")
    a = input('USER NAME:')
    b = input('PASSWORD:')
    c = input('RE-ENTER YOUR PASSWORD:')
    ph = input("PHONE NUMBER:")
    print('M=MALE', '\n', 'F=FEMALE', '\n', 'N=NOT TO MENTION')
    gen = input('ENTER YOUR GENDER:')
    print("ENTER YOUR DATE OF BIRTH")
    d = input("DD:")
    o = input("MM:")
    p = input("YYYY:")
    dob = d + '/' + o + '/' + p
    age = input('YOUR AGE:')
    v = {'m': 'MALE', 'f': 'FEMALE', 'n': 'NOT TO MENTION'}
    if b == c:
        c1 = "insert into user_accounts values('{}','{}','{}','{}','{}','{}','{}','{}')".format(f, l, a, b, ph, v[gen], dob, age)
        cursor.execute(c1)
        print("\t\t\t\t--------------------------------------------")
        print(Fore.GREEN + "\t\t\t\t\t\tSIGN UP SUCCESSFULLY")
        print("\t\t\t\t--------------------------------------------")
        main()
    else:
        print(Fore.RED + 'BOTH PASSWORDS ARE NOT MATCHING')


def ticket_cancelling():
    phno = input('enter your phone number:')
    s = "select Phno from railway where phno='{}'".format(phno)
    cursor.execute(s)
    data = cursor.fetchone()

    if data and data[0] == phno:
        # Display a notification about cancellation rules and fees
        print("\t\t\t\t-------------------------------------------------")
        print(Fore.YELLOW + "\t\t\t\t\t\tPlease Note:")
        print(Fore.YELLOW + "\t\t\t\t\t\t1. Ticket cancellation may result in a deduction of a cancellation fee.")
        print(Fore.YELLOW + "\t\t\t\t\t\t2. The cancellation fee may vary depending on the time of cancellation.")
        print("\t\t\t\t-------------------------------------------------")

        # Ask for confirmation before proceeding with cancellation
        confirm = input("Are you sure you want to cancel this ticket? (yes/no): ")
        if confirm.lower() == 'yes':
            # Perform the ticket cancellation
            sl = "delete from railway where phno='{}'".format(phno)
            cursor.execute(sl)
            print("\t\t\t\t-------------------------------------------------")
            print(Fore.GREEN + "\t\t\t\t\t\tTICKET CANCELLED SUCCESSFULLY")
            print("\t\t\t\t-------------------------------------------------")
        else:
            print("Ticket cancellation canceled.")
    else:
        print(Fore.RED + 'TICKET DOES NOT EXIST or WRONG ENTRY')

def generate_pnr():
    # Generate a random 6-digit PNR number
    pnr_number = ''.join(random.choice('0123456789') for _ in range(6))
    return pnr_number

def ticket_booking():
    nm = input('enter your name:')
    phno = input('Enter your phone number:')
    age = int(input('enter your age:'))
    print('M=MALE', '\t', 'F=FEMALE', '\t', 'N=NOT TO MENTION')
    gender = input('enter your gender:')
    Gender = gender.upper()
    fr = input('enter your starting point:')
    to = input('enter your destination:')
    date1 = input('enter date(dd):')
    date2 = input('enter month(mm):')
    date3 = input('enter year(yyyy):')
    date = date1 + '/' + date2 + '/' + date3
    a = {'M': 'MALE', 'F': 'FEMALE', 'N': 'NOT TO MENTION'}
    v = a.get(Gender, 'NOT TO MENTION')

    # Generate a PNR number
    pnr_number = generate_pnr()

    sl = "insert into railway values('{}','{}','{}','{}','{}','{}','{}')".format(nm, phno, age, v, fr, to, date)
    cursor.execute(sl)

    # Insert the PNR information into the PNR table
    pnr_insert = "insert into pnr values('{}','{}','BOOKED')".format(pnr_number, phno)
    cursor.execute(pnr_insert)

    print("\t\t\t\t--------------------------------------------")
    print(Fore.GREEN + "\t\t\t\t\t\tTICKET BOOKED SUCCESSFULLY")
    print(f"\t\t\t\t\t\tYour PNR Number is: {pnr_number}")
    print("\t\t\t\t--------------------------------------------")

def display():
    a = input('USERNAME:')
    b = input('PASSWORD:')
    s1 = "select user_name from user_accounts where password='{}'".format(b)
    cl = "select fname,Iname from user_accounts where password='{}'".format(b)
    cursor.execute(cl)
    data1 = cursor.fetchall()
    if data1:
        data1 = list(data1[0])
        full_name = data1[0] + ' ' + data1[1]
        cursor.execute(s1)
        data = cursor.fetchone()
        if data and data[0] == a:
            x = ['FIRST NAME', 'LAST NAME', 'PHONE NUMBER', 'GENDER', 'DATE OF BIRTH', 'AGE']
            sl = "select fname,Iname,Phno,gender,dob,age from user_accounts where password='{}'".format(b)
            cursor.execute(sl)
            data = cursor.fetchone()
            if data:
                data = list(data)
                print(Fore.CYAN + x[0], '::::', data[0])
                print(x[1], '::::', data[1])
                print(x[2], '::::', data[2])
                print(x[3], '::::', data[3])
                print(x[4], '::::', data[4])
                print(x[5], '::::', data[5])
    else:
        print(Fore.RED + 'ACCOUNT DOES NOT EXIST')

def pnr_status():
    pnr_number = input('Enter PNR Number:')
    s = "select * from pnr where pnr_number='{}'".format(pnr_number)
    cursor.execute(s)
    data = cursor.fetchone()
    if data:
        a = ['PNR NUMBER', 'PHONE NUMBER', 'STATUS']
        data = list(data)
        print(a[0], '::::', data[0])
        print(a[1], '::::', data[1])
        print(a[2], '::::', data[2])
    else:
        print(Fore.RED + 'PNR NUMBER DOES NOT EXIST')

# Insert food items and their prices into the food_items table if they don't exist
food_items_data = [
    ("RAJASTHANI THALI", 175),
    ("MAHARAJA THALI", 200),
    ("SOUTH INDIAN THALI", 160),
    ("JAIN THALI", 185),
    ("IDLI SAMBHAR", 60),
    ("MASALA DOSA", 80),
    ("DAL BAATI", 90),
    ("BURGER", 50),
    ("NORMAL PIZZA", 85),
    ("TEA", 15),
    ("COFFEE", 20),
]

for item_data in food_items_data:
    item_name, price = item_data
    check_item_query = "SELECT item_name FROM food_items WHERE item_name = %s"
    cursor.execute(check_item_query, (item_name,))
    existing_item = cursor.fetchone()

    if not existing_item:
        insert_food_item = "INSERT INTO food_items (item_name, price) VALUES (%s, %s)"
        cursor.execute(insert_food_item, (item_name, price))
mycon.commit()

def catering_service():
    print(Fore.MAGENTA + "Welcome to Catering Services")
    print("\t\t\t\t--------------------------------------------")
    print(Fore.MAGENTA + "\t\t\t\t\t\t1.Order Food")
    print(Fore.MAGENTA + "\t\t\t\t\t\t2.Check Order Status")
    print(Fore.MAGENTA + "\t\t\t\t\t\t3.Cancel Order")
    print(Fore.MAGENTA + "\t\t\t\t\t\t4.Go Back")
    print("\t\t\t\t--------------------------------------------")

    choice = int(input("\t\t\t\tENTER YOUR CHOICE:"))

    if choice == 1:
        order_food()
    elif choice == 2:
        check_order_status()
    elif choice == 3:
        cancel_order()
    elif choice == 4:
        return
    else:
        print(Fore.RED + 'ERROR 404: ERROR PAGE NOT FOUND')

def order_food():
    pnr_number = input('Enter your PNR number:')

    # Display food items and their prices
    display_food_items()

    food_items_str = input('Enter food items (comma-separated, e.g., 1,3):')
    quantity_str = input('Enter quantity for each item (comma-separated):')

    # Split the input strings into lists of integers
    food_items = [int(item_id) for item_id in food_items_str.split(',')]
    quantity = [int(qty) for qty in quantity_str.split(',')]

    # Calculate the total cost based on food items and quantity
    total_cost = calculate_total_cost(food_items, quantity)

    # Generate a unique order number
    order_number = generate_order_number()

    # Insert the catering order into the catering_orders table
    insert_order = "insert into catering_orders values('{}','{}','{}','ORDERED',{})".format(order_number, pnr_number, food_items_str, total_cost)
    cursor.execute(insert_order)

    print("\t\t\t\t--------------------------------------------")
    print(Fore.GREEN + "\t\t\t\t\t\tFood Order Placed Successfully")
    print(f"\t\t\t\t\t\tYour Order Number is: {order_number}")
    print(f"\t\t\t\t\t\tTotal Cost: ₹{total_cost:.2f}")
    print("\t\t\t\t--------------------------------------------")

def calculate_total_cost(food_items, quantity):
    total_cost = 0

    # Fetch prices of selected food items from the database
    select_items = "select item_id, price from food_items"
    cursor.execute(select_items)
    data = cursor.fetchall()

    # Calculate the total cost based on food items and quantity
    for item_id, price in data:
        if item_id in food_items:
            index = food_items.index(item_id)
            total_cost += price * quantity[index]

    return total_cost

def display_food_items():
    # Fetch and display food items and their prices
    print("Food Items:")
    print("\tID\tName\tPrice")
    select_items = "select item_id, item_name, price from food_items"
    cursor.execute(select_items)
    data = cursor.fetchall()
    for row in data:
        item_id, item_name, price = row
        print(f"\t{item_id}\t{item_name}\t₹{price:.2f}")

def generate_order_number():
    # Generate a random 6-digit order number
    order_number = ''.join(random.choice('0123456789') for _ in range(6))
    return order_number

def check_order_status():
    order_number = input('Enter your Order Number:')
    s = "select * from catering_orders where order_number='{}'".format(order_number)
    cursor.execute(s)
    data = cursor.fetchone()
    if data:
        a = ['ORDER NUMBER', 'PNR NUMBER', 'FOOD ITEMS', 'STATUS']
        data = list(data)
        print(a[0], '::::', data[0])
        print(a[1], '::::', data[1])
        print(a[2], '::::', data[2])
        print(a[3], '::::', data[3])
    else:
        print(Fore.RED + 'ORDER NUMBER DOES NOT EXIST')

def cancel_order():
    order_number = input('Enter your Order Number:')

    # Check if the order exists and is not already canceled
    order_check = "select status from catering_orders where order_number='{}'".format(order_number)
    cursor.execute(order_check)
    data = cursor.fetchone()

    if data and data[0] == 'ORDERED':
        # Update the order status to "CANCELLED"
        update_order = "update catering_orders set status='CANCELLED' where order_number='{}'".format(order_number)
        cursor.execute(update_order)
        print("\t\t\t\t--------------------------------------------")
        print(Fore.GREEN + "\t\t\t\t\t\tOrder Cancelled Successfully")
        print("\t\t\t\t--------------------------------------------")
    else:
        print(Fore.RED + 'ORDER NUMBER DOES NOT EXIST or ALREADY CANCELLED')

# Main function 
def main():
    while True:
        print("\t\t\t\t--------------------------------------------")
        print("\t\t\t\t\t\t1.TICKET BOOKING")
        print("\t\t\t\t\t\t2.PNR STATUS")
        print("\t\t\t\t\t\t3.TICKET CANCELLING")
        print("\t\t\t\t\t\t4.ACCOUNT DETAILS")
        print("\t\t\t\t\t\t5.CATERING SERVICES")
        print("\t\t\t\t\t\t6.LOG OUT")
        print("\t\t\t\t--------------------------------------------")
        ch = int(input("\t\t\t\tENTER YOUR CHOICE:"))
        if ch == 1:
            ticket_booking()
        elif ch == 2:
            pnr_status()
        elif ch == 3:
            ticket_cancelling()
        elif ch == 4:
            display()
        elif ch == 5:
            catering_service()
        elif ch == 6:
            print(Fore.YELLOW + 'THANK YOU')
            break
        else:
            print(Fore.RED + 'ERROR 404: ERROR PAGE NOT FOUND')

if __name__ == "__main__":
    print(Fore.BLUE + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    while True:
        print(Fore.BLUE + "\t\t\t\tWELCOME TO ONLINE RAILWAY RESERVATION SYSTEM")
        print("\t\t\t\t--------------------------------------------")
        print(Fore.BLUE + "\t\t\t\t\t\t1.SIGN IN")
        print(Fore.BLUE + "\t\t\t\t\t\t2.SIGN UP")
        print(Fore.BLUE + "\t\t\t\t\t\t3.EXIT")
        print("\t\t\t\t--------------------------------------------")
        print(Fore.BLUE + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        ch = int(input('\t\t\t\tENTER YOUR CHOICE:'))
        if ch == 1:
            signin()
        elif ch == 2:
            signup()
        elif ch == 3:
            print(Fore.YELLOW + "\t\t\t\t--------------------------------------------")
            print(Fore.YELLOW + "\t\t\t\t\t\tTHANK YOU")
            print(Fore.YELLOW + "\t\t\t\t--------------------------------------------")
            break
        else:
            print(Fore.RED + 'ERROR 404.PAGE NOT FOUND')
            break

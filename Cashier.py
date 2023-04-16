"""
This is the main module.
User can select items from catalog or input them manually,
edit, delete, and reset their ordered item before finally check out their order
"""

# Import necessary libarary
# Import sqlite3 to establish connection with database
import sqlite3
# Import tabulate to print dictionaries as table
from tabulate import tabulate as tb
# Import datetime to create timestamp as user inserts their id
from datetime import datetime as dt
# Import sys to later quit the program
import sys

# Creating the user_id dictionary to store user's id and timestamp
user_id = {'User ID': [], 'Date': []}

# Creating order_detail dictionary to store user's order details
order_detail = {'No': [], 'Item': [], 'Qty': [], 'Price': [], 
                    'Total Price': [], 'Discount': [], 'Price After Discount': [] }

# Established so the id can be autoincrement
order_id = 0

# Creating the catalog where user can choose item from
catalog = {}
catalog ['ID'] = [1, 2, 3, 4, 5]
catalog ['Item'] = ['apple', 'orange', 'lemon', 'melon', 'grape']
catalog ['Price'] = [1000, 2000, 750, 1500, 2500]

# Check out function: insert the order_detail and user_info to the database
def check_out():
    while True:
        
        # show the order so far and ask for confirmation 
        print('-'*60)
        print ('CHECK OUT ORDERS') 
        print('-'*60)
        print(tb(order_detail, headers="keys")) 
        proceed = input('Do you want to check out your orders? (Y/N): ') 
        
        # proceed to check out 
        if proceed.upper() in ['Y', 'YES', 'YA']: 
            conn = sqlite3.connect('Cashier.db') # Establishing connection to database 
            
            data1 = [(user, date) for user, date in zip(user_id['User ID'], user_id['Date'])] # map the user_info
            conn.executemany("INSERT INTO user_info (user, date) VALUES (?, ?)", data1) # inserting the data
            print(tb(user_id, headers="keys")) 
            print('User info has been added') # letting the user know their id has been submitted
            
            order_detail['user_id'] = [] # creating new column for the user_id in order detail
            for i in range(len(order_detail['No'])): # populating the column
                order_detail['user_id'].append(user_id['User ID'][0])
            data2 = [(user, item, qty, price, total_price, discount, price_after_discount) # map the order_detail
                     for user, item, qty, price, total_price, discount, price_after_discount 
                     in zip(order_detail['user_id'], order_detail['Item'],  order_detail['Qty'],
                             order_detail['Price'], order_detail['Total Price'], order_detail['Discount'],
                              order_detail['Price After Discount'])]
            conn.executemany("""INSERT INTO orders_detail (user, item, qty, price, total_price, discount, price_after_discount) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""", data2) # inserting the data
            
            order_detail.pop('user_id') # remove the user_id column from order detail

            # letting the user know their order has been checked out
            print(tb(order_detail, headers="keys"))
            total_order = sum(order_detail['Total Price'])
            print(f'Your order with total price {total_order} has been added') 
            
            conn.commit() # commit to database
            conn.close() # close the connection
            sys.exit() # exit the system
        
         # if no, return to previous menu
        elif proceed.upper() in ['N', 'NO']:
            return
        
        # letting the user know there's an error then return to previous menu
        else :
            print('Invalid input') 
            return

# edit item function: edit the item name, quantity, and price
def edit_item():
    try:
        while True:
            print('-'*60)
            print ('EDIT ITEM') 
            print('-'*60)
            print(tb(order_detail, headers="keys"))
            edit = int(input('''Enter item's number to edit (or "0" to go back): ''')) 
            seen = set(order_detail['Item']) 
            if edit == 0: 
                return 
            else : 
                index = order_detail['No'].index(edit)
                current_item = order_detail['Item'][index]
                quantity = 0
                new_quantity = 0
                decision = input(f'Do you want to edit {current_item}? (Y/N): ') 
                if decision.upper() in ['Y', 'YES', 'YA']:
                    new_item = input('Enter item name (or "0" to go back): ') 
                    if new_item == '0': 
                        return  
                    elif new_item in seen: 
                        print('Item is already in your orders') 
                        edit_quantity = input('Do you want to edit the quantity? (Y?N): ') 
                        if edit_quantity.upper() in ['Y', 'YES', 'YA']:
                            new_quantity = int(input('Enter new quantity: ')) 
                            order_detail ['Qty'][catalog['Item'].index(new_item.lower())] = new_quantity
                            price = catalog['Price'][catalog['Item'].index(new_item.lower())]
                            total_price = price*new_quantity
                            if total_price > 500_000:  discount = 0.07
                            elif total_price > 300_000:  discount = 0.06
                            elif total_price > 200_000:  discount = 0.05
                            else : discount = 0       
                            price_after_discount = total_price - (total_price*discount)
                            order_detail ['Price'][catalog['Item'].index(new_item.lower())] = price
                            order_detail ['Total Price'][catalog['Item'].index(new_item.lower())] = total_price
                            order_detail ['Discount'][catalog['Item'].index(new_item.lower())] = discount
                            order_detail ['Price After Discount'][catalog['Item'].index(new_item.lower())] = price_after_discount
                            print(tb(order_detail, headers="keys"))
                            print(f'Your order has been successfully updated with {new_quantity} {new_item}(s) at a cost of IDR {price} each.')
                        elif edit_quantity.upper() in ['N', 'NO']:
                            return
                        else :
                            print('Invalid input')
                            return
                    elif new_item not in seen:
                        quantity = int(input('Enter quantity: '))
                        order_detail ['Qty'][index] = quantity               
                        if new_item.lower() in catalog['Item']:
                            price = catalog['Price'][catalog['Item'].index(new_item.lower())]
                        else:
                            price = float(input('Enter price: '))
                        total_price = price*quantity
                        if total_price > 500_000:  discount = 0.07
                        elif total_price > 300_000:  discount = 0.06
                        elif total_price > 200_000:  discount = 0.05
                        else : discount = 0       
                        price_after_discount = total_price - (total_price*discount)
                        order_detail ['Item'][index] = new_item
                        order_detail ['Price'][index] = price
                        order_detail ['Total Price'][index] = total_price
                        order_detail ['Discount'][index] = discount
                        order_detail ['Price After Discount'][index] = price_after_discount
                        print(tb(order_detail, headers="keys"))
                        print(f'Your order has been successfully updated with {quantity} {new_item}(s) at a cost of IDR {price} each.')
                elif decision.upper() in ['N', 'NO']:
                    return
                else: 
                    print('Invalid input')
    except:
        print('Something went wrong. Please check your input6')

# delete item function: delete the whole row of a choosen item from order
def delete_item():
    try:
        while True:
            # show the order so far and ask which item to delete
            print('-'*60)
            print ('DELETE ITEM')
            print('-'*60)
            print(tb(order_detail, headers="keys"))
            delete = int(input('''Enter item's number to delete (or "0" to go back): '''))
            
            # return to previous menu
            if delete == 0: 
                return
            

            elif delete in order_detail['No'] : 
                
                # ask for confirmation
                index = order_detail['No'].index(delete)
                to_be_deleted = order_detail['Item'][order_detail['No'].index(index)+1]
                confirm = input(f'Are you sure want to delete {to_be_deleted}? (Y/N): ')
                
                # delete the item and adjust the "No"
                if confirm.upper() in ['Y', 'YES', 'YA']:
                    order_detail['No'].clear()
                    order_detail['Item'].pop(index)
                    order_detail['Qty'].pop(index)
                    order_detail['Price'].pop(index)
                    order_detail['Total Price'].pop(index)
                    order_detail['Discount'].pop(index)
                    order_detail['Price After Discount'].pop(index)
                    for i in range(len(order_detail['Item'])):
                        order_detail['No'].append(i+1)
                    print('The selected item has been deleted')

                # return to previous menu        
                elif confirm.upper() in ['N', 'NO']:
                    return
                
# letting the user know there's an error then return to previous menu                
            else: 
                print('Invalid Input')
                return 
    except:
        print('Something went wrong. Please check your input5')

# reset function: delete the whole order
def reset():
    # show the order so far and ask for confirmation
    print('-'*60)
    print ('RESET ORDERS')
    print('-'*60)
    print(tb(order_detail, headers="keys"))
    confirm = input('''Your orders will be deleted. Are you sure want to proceed? (Y/N): ''')
    
    try: 
        if confirm.upper() in ['Y', 'YES', 'YA']:
            
            # clear all input from dictionary and let the user know
            order_detail['No'].clear()
            order_detail['Item'].clear()
            order_detail['Qty'].clear()
            order_detail['Price'].clear()
            order_detail['Total Price'].clear()
            order_detail['Discount'].clear()
            order_detail['Price After Discount'].clear()
            global order_id
            order_id = 0
            print('-'*60)
            print('Your orders has been deleted')
            print('-'*60)
            
        elif confirm.upper() in ['N', 'NO']:
            return # return to previous menu
        
# letting the user know there's an error then return to previous menu 
        else: 
            print('Invalid Input')
            return
    except:
        print('Something went wrong. Please check your input')

# orders check function: checking the order so far, user can choose to edit, delete, or reset their order
def orders_check():
    try: 
        while True:
            # show the menu and ask user to input task
            print('-'*60)
            print ('YOUR ORDERS')
            print('-'*60)
            print(tb(order_detail, headers="keys"))
            print('''
            1. Edit item
            2. Delete item
            3. Reset orders
            0. Back to Main Menu
            ''')
            action = int(input('Enter task number: '))

            # the inputted number will take the user to responding function/menu
            if action == 1:
                edit_item()
            elif action == 2:
                delete_item()
            elif action == 3:
                reset()
            elif action == 0:
                return
            elif action == False:
                sys.exit()

# letting the user know there's an error then return to previous menu
            else :
                print('Invalid Input')
    except:
        print('Something went wrong. Please check your input')

# catalog function: user can choose item from catalog or edit the quantity if the item is already in their order
def open_catalog():
    try: 
        while True:
            # show menu tittle and ask user to input the item id from catalog
            print('-'*60)
            print ('ITEM CATALOG')
            print('-'*60)
            print(tb(catalog, headers="keys"))
            catalog_choice = int(input('Enter item ID (or "0" to go back): '))
            
            # setup condition
            seen = set(order_detail['Item'])
            choosen_item_quantity = 0
            new_quantity = 0
            
            if catalog_choice == 0: # return to previous menu
                return
            
            # item is in catalog
            elif catalog_choice in catalog['ID']:
                choosen_item = catalog['Item'][catalog['ID'].index(catalog_choice)]
                
                # item not yet in their order
                if choosen_item not in seen:
                    
                    # select price
                    choosen_item_price = catalog['Price'][catalog['ID'].index(catalog_choice)]
                    choosen_item_quantity = int(input('Enter quantity: '))
                    total_price = choosen_item_price*choosen_item_quantity
                    
                    # check for discount
                    if total_price > 500_000:  discount = 0.07
                    elif total_price > 300_000:  discount = 0.06
                    elif total_price > 200_000:  discount = 0.05
                    else : discount = 0
                    price_after_discount = total_price - (total_price*discount)
                    
                    # update the order
                    global order_id
                    order_id += 1
                    order_detail['No'].append(order_id)
                    order_detail['Item'].append(choosen_item)
                    order_detail['Qty'].append(choosen_item_quantity)
                    order_detail['Price'].append(choosen_item_price)
                    order_detail['Total Price'].append(total_price)
                    order_detail['Discount'].append(discount)
                    order_detail['Price After Discount'].append(price_after_discount)

                    # show the user their updatted order
                    print(tb(order_detail, headers="keys"))
                    print(f'Your order has been successfully updated with {choosen_item_quantity} {choosen_item}(s) at a cost of IDR {choosen_item_price} each.')
                
                # item is in their order
                elif choosen_item in seen:
                    
                    # let the user know and offer to edit the quantity
                    print('Item is already in your orders')
                    edit_quantity = input('Do you want to edit the quantity? (Y?N): ')
                    
                    if edit_quantity.upper() in ['Y', 'YES', 'YA']:
                        # set the condition and ask for new quantity
                        choosen_item_price = catalog['Price'][catalog['ID'].index(catalog_choice)]
                        new_quantity = int(input('Enter new quantity: '))
                        order_detail ['Qty'][order_detail['Item'].index(choosen_item)] = new_quantity
                        total_price = choosen_item_price*new_quantity
                        
                        # check for discount
                        if total_price > 500_000:  discount = 0.07
                        elif total_price > 300_000:  discount = 0.06
                        elif total_price > 200_000:  discount = 0.05
                        else : discount = 0
                        price_after_discount = total_price - (total_price*discount)
                        
                        # update the order
                        order_detail ['Total Price'][order_detail['Item'].index(choosen_item)] = total_price
                        order_detail ['Discount'][order_detail['Item'].index(choosen_item)] = discount
                        order_detail ['Price After Discount'][order_detail['Item'].index(choosen_item)] = price_after_discount
                        
                        # show the user their updatted order
                        print(tb(order_detail, headers="keys"))
                        print(f'Your order has been successfully updated with {new_quantity} {choosen_item}(s) at a cost of IDR {choosen_item_price} each.')
                    
                    # return to previous menu
                    elif edit_quantity.upper() in ['N', 'NO']:
                        return 
                    
# letting the user know there's an error then return to previous menu
                    else :
                        print('Invalid input')
                        return
            else:
                print('Invalid ID')
    except:
        print('Something went wrong. Please check your input')

# manual input function: user can input item that not in our catalog or edit the quantity if the item is already in their order
def manual_input():
    try:
        while True: 
            # show menu tittle and ask user to input the item name
            print('-'*60)
            print ('MANUAL ITEM INPUT')
            print('-'*60)
            item_name = input('Enter item name (or "0" to go back): ')
            
            # setup condition
            seen = set(order_detail['Item']) 
            quantity = 0
            new_quantity = 0
            
            if item_name == '0':
                return  # return to previous menu
            
            #item is already in their order
            elif item_name in seen:
                print('Item is already in your orders')
                edit_quantity = input('Do you want to edit the quantity? (Y?N): ') # offer to edit the quantity instead
                if edit_quantity.upper() in ['Y', 'YES', 'YA']:
                    # user input new quantity and price (if item is not in catalog) then update the order detail
                    new_quantity = int(input('Enter quantity: '))
                    order_detail ['Qty'][order_detail['Item'].index(item_name)] = new_quantity
                    
                    # select or input price
                    if item_name.lower() in catalog['Item']:
                        price = catalog['Price'][catalog['Item'].index(item_name.lower())]
                    else:
                        price = float(input('Enter price: '))
                    total_price = price*new_quantity
                    
                    # check for discount
                    if total_price > 500_000:  discount = 0.07
                    elif total_price > 300_000:  discount = 0.06
                    elif total_price > 200_000:  discount = 0.05
                    else : discount = 0
                    price_after_discount = total_price - (total_price*discount)
                    
                    # update the order
                    order_detail ['Total Price'][order_detail['Item'].index(item_name)] = total_price
                    order_detail ['Discount'][order_detail['Item'].index(item_name)] = discount
                    order_detail ['Price After Discount'][order_detail['Item'].index(item_name)] = price_after_discount
                    
                    # show the user their updatted order
                    print(tb(order_detail, headers="keys"))
                    print(f'Your order has been successfully updated with {new_quantity} {item_name}(s) at a cost of IDR {price} each.')
                
                # return to previous menu if user choose not to edit the amount or if there is an error
                elif edit_quantity.upper() in ['N', 'NO']:
                    return 
                else :
                    print('Invalid input')
                    return
                
            # item is not on the order yet
            elif item_name not in seen:
                # user input quantity and price (if item is not in catalog) then update the order detail
                quantity = int(input('Enter quantity: '))
                
                # select or input price
                if item_name.lower() in catalog['Item']:
                    price = catalog['Price'][catalog['Item'].index(item_name.lower())]
                else:
                    price = float(input('Enter price: '))
                total_price = price*quantity
                
                # update the order
                global order_id
                order_id += 1
                order_detail['No'].append(order_id)
                order_detail['Item'].append(item_name.lower())
                order_detail['Qty'].append(quantity)
                order_detail['Price'].append(price)
                order_detail['Total Price'].append(total_price)
                
                # check for discount
                if total_price > 500_000:  discount = 0.07
                elif total_price > 300_000:  discount = 0.06
                elif total_price > 200_000:  discount = 0.05
                else : discount = 0       
                price_after_discount = total_price - (total_price*discount)
                
                # update the order
                order_detail['Discount'].append(discount)
                order_detail['Price After Discount'].append(price_after_discount)
                
                # show the user their updatted order
                print(tb(order_detail, headers="keys"))
                print(f'Your order has been successfully updated with {quantity} {item_name}(s) at a cost of IDR {price} each.')
    except:
        print('Something went wrong. Please check your input') # letting the user know there's an error then return to previous menu

# quit function: exit the program
def quit():
    while True:
        # asking the user are they really want to exit the program
        print('-'*60)
        print ('QUIT SHOPPING')
        print('-'*60)
        confirm = input('''Your orders will not be saved. \n Are you sure want to quit? (Y/N): ''')
        if confirm.upper() in ['Y', 'YES', 'YA']:
            # letting the user know they quit the program before exit the program
            print('-'*60)
            print('Thank you for coming :)')
            print('-'*60)
            sys.exit()
        elif confirm.upper() in ['N', 'NO']:
            return # return to previous menu
        else: 
            print('Invalid Input')  # let the user know there is an error in their input

# main menu function: open a list of task user can choose to do
def main():
    while True: 
        # show the main menu and ask user to input task 
        print('-'*60)
        print ('MAIN MENU')
        print('-'*60)
        print('''
             1. Open Catalog
             2. Manual Input
             3. Orders Check
             4. Check Out
             5. Quit
             ''')
        choice = input('Enter task number:')

        # the inputted number will take the user to responding function/menu
        if choice.lower() == '1': open_catalog()
        elif choice.lower() == '2': manual_input()
        elif choice.lower() == '3': orders_check()
        elif choice.lower() == '4': check_out()
        elif choice.lower() == '5': quit()
        
        # let the user know there is an error in their input
        else: 
            print('Invalid Input')

# welcome function: welcoming page where user can input their ID which upon submission timestamp collected automatically
def welcome():
    print('-'*60)
    print ('WELCOME TO OUR SHOP') # Printing page tittle
    print('-'*60)
    id = input('Create your ID(or "q" to quit): ') # input user ID
    if id.lower() == 'q':
        # letting the user know they quit the program before exit the program
        print('-'*60)
        print('Thank you for coming :)') 
        print('-'*60)
        sys.exit() 
    elif id.lower() != 'q':
        # collecting user id and timestamp to user_id dictionary then jump to main menu
        date = dt.now()
        user_id['User ID'].append(id)
        user_id['Date'].append(date)
        main() 

# run the welcome funtion    
welcome()

# Cashier-Project
Input data to order's list and submitting to database at check out

# Background
A shop need a system where customer can input their order and do a self-check out.
They have to be able to add, edit, delete, reset, and check out their order from the system.

# Funcitions 
1. check out function: insert the order_detail and user_info to the database
2. edit item function: edit the item name, quantity, and price
3. delete item function: delete the whole row of a choosen item from order
4. reset function: delete the whole order
5. orders check function: checking the order so far, user can choose to edit, delete, or reset their order
6. catalog function: user can choose item from catalog or edit the quantity if the item is already in their order
7. manual input function: user can input item that not in our catalog or edit the quantity if the item is already in their order
8. quit function: exit the program
9. main menu function: open a list of task user can choose to do
10. welcome function: welcoming page where user can input their ID which upon submission timestamp collected automatically

every time an item inputted the system will check if there is already item with similar name in the order, if so it would offer to change the quantity instead.
the system will also check if the item inputted manually is actually in the catalog, if so the price will be added automatically.
after having the price and amount the system will check for discount, if there's any it would be calculated automatically.

# Code Flow
1. run welcome() where user can input their id or 'q' to exit the system

![image](https://user-images.githubusercontent.com/128882248/232320716-addbe4f4-72b8-45ec-87a9-e8ce05210019.png)

![image](https://user-images.githubusercontent.com/128882248/232321590-904e6797-c81d-40c0-8b1f-db36f4e3be1c.png)

2. if the user input their id, it take them to main menu

![image](https://user-images.githubusercontent.com/128882248/232320788-bc365f40-3a77-4cf7-8a32-a63e07fb3e23.png)

3. user then can choose which task they want to do
4. if they select the first option, it take them to the catalog where they can choose items or 0 to go back to main menu

![image](https://user-images.githubusercontent.com/128882248/232320867-80e5c74e-8a30-4289-871b-b5f95a038cb7.png)

4a. user can continue input other item

![image](https://user-images.githubusercontent.com/128882248/232320907-99442d40-d945-432e-9e2a-ab31c1249b5e.png)

4b. if the item is already in their order they'll be offered to change the quantity instead

![image](https://user-images.githubusercontent.com/128882248/232320968-c6ba14c1-06d4-48cf-8516-2e9c111c1c01.png)

5. if they select second option, they can manually input their item

![image](https://user-images.githubusercontent.com/128882248/232321091-1b42a657-c781-4ec2-aa2a-00776affeb76.png)

5a. if the item is already in their order they'll be offered to change the quantity instead

![image](https://user-images.githubusercontent.com/128882248/232321152-28a6835b-a005-4a35-a12e-d84120d25384.png)

5b. if the item is in catalog they can't manually input the price

![image](https://user-images.githubusercontent.com/128882248/232321202-39e34c31-c2a7-4a25-8882-8a45d588ad69.png)

6. if they select the third option, it take them to order check

![image](https://user-images.githubusercontent.com/128882248/232321274-e69405bc-5842-42db-8680-b62eb550e49d.png)

6a. to edit an item

![image](https://user-images.githubusercontent.com/128882248/232321351-dc8ab4af-3a1b-42f4-9535-b0652cb05c91.png)

6b. to delete an item

![image](https://user-images.githubusercontent.com/128882248/232321389-58a4bedd-6d2e-4bf3-a912-3bbce3d9670a.png)

![image](https://user-images.githubusercontent.com/128882248/232321527-070597ea-bf2d-427d-ba58-175a8715ec4a.png)

6c. to reset order

![image](https://user-images.githubusercontent.com/128882248/232321446-115a1def-d840-44d5-a7bb-07d57542a3b3.png)

7. if they select the fourth option, it take them to check out and exit the system after check out

![image](https://user-images.githubusercontent.com/128882248/232321561-6f1d45c6-1dfe-462b-b835-ff668aa2c55a.png)

8. if they select the last, it will exit the system

![image](https://user-images.githubusercontent.com/128882248/232321660-aaa2ec0d-e4e3-4a06-b9ff-4905f96d976e.png)

# Conclusion
This is my first project using pyhton, any feedback will be appreciated.
There some improvement I would like to make in the future, for example:
1. having the discount in a dictionary, so it can be easily modified if needed
2. create function for each item, price, discount check as well as to calculate the total and after discount price
3. overall make the code shorter, I still copy-paste a lot in this so there are several repetitions

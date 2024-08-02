
    
# import json
import datetime as datetime
import time as time
# from pprint import pprint

# # Load the JSON data from the file
# with open('data.json') as f:
#     data = json.load(f)
# orders = data["Order"]
    

# filtered_orders = [order for order in orders if   float(order["sell"]) <= 0.5358 ]

# # Remove the filtered orders from the original data
# data["Order"] = [order for order in orders if order not in filtered_orders]

# # Save the updated data back to the file
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4)  # Save with indentation for better readability


import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"Started at {time.strftime('%X')}")

    # Running two coroutines concurrently:
    task1 = asyncio.create_task(say_after(2, 'hello'))
    task2 = asyncio.create_task(say_after(1, 'world'))

    # Wait until both tasks are completed
    await task1
    await task2

    print(f"Finished at {time.strftime('%X')}")

# Running the main coroutine
# asyncio.run(main())


# h = 60
# d = h *24
# y = d*365

# print('Hour : {:,.2f}'.format( y *8))

# qty_ = 20
# tp = 1.1
# closedtrades = 217
# net_perorder = (qty_ / 100 ) * (tp-0.2000)
# clos_value = closedtrades * net_perorder
# net_perorder2 = (qty_ / 100 ) * (tp)
# clos_value2 = closedtrades * net_perorder2
# #  20.22
# print('กำไร ต่อไม้: {:,.4f} | เป็น : {:,.4f}'.format( net_perorder,qty_+net_perorder))
# print('กำไร : {:,.4f}'.format( clos_value))
# print('กำไร TH : {:,.4f}'.format( clos_value*34))

amount_in = '@15'
Type_Order = list(amount_in)[0]
amount_in = float(amount_in[1:])

print(Type_Order)
print(amount_in)
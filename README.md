# Pizza Delivery App

- Backend : FastAPI
- Frontend : Comming Soon

# Architecture
![image](https://github.com/Harshil-Jani/Python-Projects/assets/79367883/df0c1e8b-bd75-4f71-aa1e-3793a9b75863)


## API ROUTES
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
| *POST* | ```/orders/order/``` | _Place an order_|_All users_|
| *PUT* | ```/orders/order/update/{order_id}/``` | _Update an order_|_All users_|
| *PUT* | ```/orders/order/status/{order_id}/``` | _Update order status_|_Superuser_|
| *DELETE* | ```/orders/order/delete/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/orders/user/orders/``` | _Get user's orders_|_All users_|
| *GET* | ```/orders/orders/``` | _List all orders made_|_Superuser_|
| *GET* | ```/orders/orders/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *GET* | ```/orders/user/order/{order_id}/``` | _Get user's specific order_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_|

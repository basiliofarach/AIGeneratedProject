## Prompts Used for generation:
# Tests
I have to create a well structured service for backend. I want to create the tests prior to making any code, here are the requirements: Use Python for the backend service and build the API for this simple & responsive e-commerce app. ● Product List ○ Use fakestoreapi.com for data to populate your database ● Allow sorting by price ○ Price low to high ○ Price high to low ○ Have an add-to-cart button for each product card. ● Shopping Cart ○ List items which are added to the cart. ○ Add the ability to change the quantity of each item. ○ Obtain the total price of the shopping cart ● Payment ○ Add Stripe payment integration

Having this, please, create test for each section using pytests. I will be using Python with OOP not with functional programming, so keep that in mind when creating the tests.

# Endpoints (API)
Perfect. This looks good. Now, please, having those tests, create the needed endpoints and connections to fakestoreapi.com and to stripe to follow the specifications for completion for each test.

- Inline prompts:
Add environ on this file, and make a call to the .env file, add this line to be STRIPE_SECRET_KEY

# Models
In the selected text: This three classes should be sent to a new folder, called models, send them there, and add the imports on this file main.py
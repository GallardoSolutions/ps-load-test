# ps-load-test

A `LocustIO` Project to help `Promotional Industry` Suppliers to test their own `PromoStandards` environments

You should try it first on `staging` and then on `production`.

We hope it helps you, as a Supplier, to find issues before your customers do.

It uses [Jinja2 templates](https://jinja.palletsprojects.com/en/3.1.x/) to generate data for the following `PromoStandards` services:
- [x] Product Data (2.0.0)
- [ ] Media Content
- [ ] Inventory
- [ ] Product Pricing and Configuration
- [ ] Order Shipment Notification
- [ ] Order Status
- [ ] Invoice
- [ ] Purchase Order

Here is the starting point to understand the project: [locustio](https://locust.io/)

Key Configurations are in file config.yml where you need to update the `prod_url` and `staging_url` accordingly.

If you are testing on `stating` you still don't need to update the `prod_url` but you need to update the `staging_url`.

We used `Hit` endpoints as an example, so you can understand how to use it.

You should create an .env file with the following variables:

```shell
PROMO_USERNAME=your_promostandards_username
PROMO_PASSWORD=your_promostandards_password
ENVIRONMENT=staging/production
SUPPLIER_CODE=your_supplier_code
T_SHIRT_PRODUCT_CODE=your_product_code
HARD_GOODS_PRODUCT_CODE=your_product_code
```

You can use several methods to add the values of the `.env` file to your environment but here is one for linux/mac:

```shell
export $(cat .env | xargs)
```

Remember to setup a virtual environment and run `pip install -r requirements.txt`

```shell
locust --host=https://psrestful.com
```

or 

```shell
locust --host=https://psrestful.com --loglevel DEBUG
```

These will run a server by default on port `8089` [http://localhost:8089](http://localhost:8089)

So you can go there and say how many users and Hatch rate (users spawned/second)
to start.


Happy load testing!

Good luck!!!

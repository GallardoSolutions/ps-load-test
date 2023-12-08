# ps-load-test

A `LocustIO` Project to help `Promotional Industry` Suppliers to test their own `PromoStandards` environments

## Our Goal

We want to help `Promotional Industry` Suppliers to improve their `PromoStandards` implementations by load testing
their own environments. Load testing is a type of performance testing that simulates real user load on your system.
It helps you to understand how your system behaves under normal and peak load conditions. It also helps you to identify
the maximum operating capacity of your system and determine which element is causing degradation.

Improving your `PromoStandards` implementation is a key factor to improve your distributor's and end user's experience.
It will help improve third party services like [PSRESTful](https://psrestful.com) and [PSMEDx](https://psmedx.com) as well.

## Notes

You should try it first on `staging` and then on `production`.

We hope it helps you, as a Supplier, to find issues before your customers do.

It uses [Jinja2 templates](https://jinja.palletsprojects.com/en/3.1.x/) to generate data for the following `PromoStandards` requests.

If you are new to `LocustIO` we suggest you visit [locustio](https://locust.io/) to understand the project better.

Key Configurations are in file `config.yml` where you need to update the `prod_url` and `staging_url` accordingly.

If you are testing on `stating` you still don't need to update the `prod_url` but you need to update the `staging_url`.

We used `Hit` endpoints in the configuration as an example, so you can understand how to use it, but you must update it with your own endpoints.


## Supported PromoStandards Requests
- [x] Product Data (2.0.0)
- [x] Media Content (1.1.0)
- [x] Inventory (1.2.1, 2.0.0)
- [x] Product Pricing and Configuration
- [x] Order Shipment Notification (1.0.0)
- [x] Order Status (1.0.0)
- [x] Invoice
- [ ] Purchase Order

## How to run it

1. Create a virtual environment and run `pip install -r requirements.txt`

2. You should create an .env file with the following variables:
    
   ```shell
    PROMO_USERNAME=your_promostandards_username
    PROMO_PASSWORD=your_promostandards_password
    ENVIRONMENT=staging/production
    SUPPLIER_CODE=your_supplier_code
    T_SHIRT_PRODUCT_CODE=your_product_code
    HARD_GOODS_PRODUCT_CODE=your_product_code
    ```

3. You can use several methods to add the values of the `.env` file to your environment but here is one for linux/mac:

    ```shell
    export $(cat .env | xargs)
    ```

4. Modify the `config.yml` file with your own endpoints and data.
5. Run the following command:

    ```shell
    locust --host=https://psrestful.com
    ```
    
    or 
    
    ```shell
    locust --host=https://psrestful.com --loglevel DEBUG
    ```

    This command will run a server by default on port `8089` [http://localhost:8089](http://localhost:8089)


So you can go there and state how many users and hatch rate (users spawned/second)
to start.


Happy load testing!

Good luck!!!

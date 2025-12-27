# 99ACRES-MAGICBRICKS-SCRAPER

In this project, we will scrap data from the most popular real estate sites in india, [99acres.com](https://www.99acres.com/) and [magicbricks.com](https://www.magicbricks.com/)

---

## Data Extracted

Column wise, the following data must be there:
* **PROPERTY_NAME**
* **LOCATION**
* **PRICE**
* **PRICE_PER_UNIT_AREA** (per Sq.Ft.)
* **FACING_DIRECTION** (vastu purposes)
* **DAYS_ON_MARKET**
* **PROPERTY_TYPE**
* **SELLER_TYPE** (owner, agent, builder)
* **POSSESSION_STATUS** (ready to move or under construction)
* **LINK**

---

> This project also makes sure to use appropriate data types for each column to make it easier to analyse

> We will use command line interface input to chose between the two sites and find all the data in a particular area *(That area will be inputed to the website using playwright tools)*
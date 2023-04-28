# Metal-recycling-plant-management-django-software
A website that manages and organizes the operations of an enterprise working on metal recycling, Where it manages and adds changes to the financial budget, including expenses and income, stores management, statistics on production and export operations, manages salaries and affairs of working employees, and creates smart reports.


The software was created to serve  "Hamade recycling company" (Cooperate with my family company), where the site was used for 6 months before moving to a more professional version that was built using most of the technologies in this version with the addition of other technologies.

It comes as a development of the previous version developed in php language:
  https://github.com/eedhamada/Metal-recycling-plant-management-php-software

## used Tools and techniques :
- Django framework.
- Sqlite database.
- HTML.
- JS.
- CSS.
- ChartJS.
- Wkhtmltopdf.
- bootstrap.
- jquery.

## Development period: +3 months.

## The main pages and their functions:

### index "/"
The main page shows the new updates and operations and Reports links.

![التقاط الويب_28-4-2023_2210_127 0 0 1](https://user-images.githubusercontent.com/90055804/235243751-552842a2-8c57-40ff-955d-32a0f6306e96.jpeg)



### money_box "/money_box"
A page displaying financial transactions arranged according to time, containing a column displaying the general balance after the transaction.

### Iron purchases "/iron_purchases" , Iron_ ales "/iron_sales"
On the page responsible for entering iron purchases and sales, the quantity, date, price, and other additional information are added. The amount of the transaction is deducted from the general budget and recorded on the expenses or income page.

![التقاط الويب_28-4-2023_2224_127 0 0 1](https://user-images.githubusercontent.com/90055804/235243891-e6745f32-eae1-4b4b-9894-51e4437083f9.jpeg)



### Income "/income"
The page responsible for managing and displaying financial entries operations.It contains the feature of filtering by date, and preparing for printing.

### Expenses "/expenses"
The page responsible for managing and displaying financial expenditure operations.It contains the feature of filtering by date, and preparing for printing.

### Pistons "/pistons"
The page is responsible for managing and recording the operations of pressing iron and other materials, as it is part of the production process.It contains the feature of filtering by date, and preparing for printing.

### Fuel entering "/fuel_entr" , Fuel disbursing "/fuel"
The pages responsible for managing the operations of entering and disbursing fuel.It contains the feature of filtering by date, and preparing for printing.

### Iron Export "/export"
The page responsible for managing and recording iron export operations.It contains the feature of filtering by date, and preparing for printing.

### Accounts "/accounts"
The page responsible for displaying the accounts that are used to record all other operations, such as the accounts of vehicles that consume fuel, the accounts of customers who are suppliers for purchases, etc. When clicking on one of the accounts, a page appears showing all the transactions that were registered under the name of this account.It contains the feature of filtering by date, and preparing for printing.

![التقاط الويب_28-4-2023_22334_127 0 0 1](https://user-images.githubusercontent.com/90055804/235243847-e3b5ca14-3527-4bfc-90f4-07295df9df8a.jpeg)


## Reports pages :

### Basic financial report :
A report showing all income and expenses from the beginning of the week until now.

### Graphic weekly report :
A report that displays all revenues, expenses, production of presses, and others from the beginning of the week.

### Fund movements report :
A report that displays all input and output transactions in their historical order.

### Fuel consumption report :
A report showing all fuel withdrawal movements and the amount of withdrawal of existing mechanisms.

### Iron purchase report :
A report showing all iron purchase movements since the beginning of the week.

### Production expense report :
A report that displays all the movements of production expenses since the beginning of the week.

## Techniques to mention :
 - ### Filtration technology throughout date :
 Most pages have a section where two dates can be placed to display only the operations that took place between them.
 
 ![التقاط الويب_28-4-2023_221411_127 0 0 1](https://user-images.githubusercontent.com/90055804/235244918-5b193689-40ea-4621-8ed3-1e87fc40ffa0.jpeg)
![التقاط الويب_28-4-2023_221426_127 0 0 1](https://user-images.githubusercontent.com/90055804/235244932-d3b9fe59-6d5a-4580-ada9-2f4ce1d5229b.jpeg)

 
 - ### Determine the beginning of the week automatically and perform operations automatically :
On most pages, the operations of the week are displayed in a table, then the operations of the previous week in a table, then the rest of the operations in a table. The weekly report is also generated automatically without intervention to specify the operations included in the week. All of this happens automatically.

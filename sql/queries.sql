select * from superstore

--finding the total sales
select sum(sales) from superstore

--category wise sales
select category, sum(sales) as Total_sales
from superstore
group by category

--Top 10 products by sale
select product_name, sum(sales) as total_sales
from superstore
group by product_name
order by total_sales desc
limit 10;

--cities with highest profit
select city, sum(profit) as total_profit
from superstore
group by city
order by total_profit desc

-- Average shipping days by ship mode
select ship_mode, avg(shipping_days) as avg_ship_days
from superstore
group by ship_mode
order by avg_ship_days desc

-- Which sub-category has most negative profit
select sub_category, sum(profit) as total_profit
from superstore
group by sub_category 
order by total_profit
limit 1;

-- Monthly sales trend
select date_trunc('month',order_date::date) as month,
		sum(sales) as total_sales
from superstore
group by month
order by month


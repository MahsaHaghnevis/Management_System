-- query 13

SELECT 
    TPL.TP_ID,
    TPL.first_name || ' ' || TPL.last_name AS Name, -- to connect fullname 
    strftime('%w', O.order_date) AS DayOfWeek, -- to get days of the week from timestamp 
    Round(AVG(C.selling_price - C.manufacturing_cost) , 2) AS AvgProfit
FROM 
    Orders O
JOIN 
    OrdersCatalogJoin OCJ ON O.order_ID = OCJ.order_ID
JOIN 
    Catalog C ON OCJ.catalog_ID = C.catalog_ID
JOIN 
    TPL ON O.TP_ID = TPL.TP_ID
GROUP BY 
    TPL.TP_ID, 
    Name, 
    DayOfWeek
ORDER BY 
    TPL.TP_ID, 
    DayOfWeek;



--query 14

SELECT 
    P1.product_name AS Product1,
    P2.product_name AS Product2,
    P3.product_name AS Product3,
    COUNT(*) AS TripletCount
FROM 
    OrdersCatalogJoin OCJ1
JOIN 
    OrdersCatalogJoin OCJ2 ON OCJ1.order_ID = OCJ2.order_ID AND OCJ1.catalog_ID < OCJ2.catalog_ID
JOIN 
    OrdersCatalogJoin OCJ3 ON OCJ1.order_ID = OCJ3.order_ID AND OCJ2.catalog_ID < OCJ3.catalog_ID
JOIN 
    Catalog P1 ON OCJ1.catalog_ID = P1.catalog_ID
JOIN 
    Catalog P2 ON OCJ2.catalog_ID = P2.catalog_ID
JOIN 
    Catalog P3 ON OCJ3.catalog_ID = P3.catalog_ID
GROUP BY 
    P1.product_name, 
    P2.product_name, 
    P3.product_name
ORDER BY 
    TripletCount DESC
LIMIT 3;


--query 15


--in case we mean warehouse country
SELECT 
    W.country,
    SUM(C.selling_price - C.manufacturing_cost) AS TotalProfit
FROM 
    Orders O
JOIN 
    OrdersCatalogJoin OCJ ON O.order_ID = OCJ.order_ID
JOIN 
    Catalog C ON OCJ.catalog_ID = C.catalog_ID
JOIN 
    Warehouse W ON O.warehouse_ID = W.warehouse_ID
GROUP BY 
    W.country
ORDER BY 
    TotalProfit DESC
LIMIT 3;

--in case of country origin
SELECT 
    C.country_origin,
    SUM(C.selling_price - C.manufacturing_cost) AS TotalProfit
FROM 
    Orders O
JOIN 
    OrdersCatalogJoin OCJ ON O.order_ID = OCJ.order_ID
JOIN 
    Catalog C ON OCJ.catalog_ID = C.catalog_ID
GROUP BY 
    C.country_origin
ORDER BY 
    TotalProfit DESC
LIMIT 3;

--query 16


SELECT o.order_user_ID 
		, o.TP_ID
		, Round(Sum(c.selling_price-c.manufacturing_cost),2) aS sum 
from
	Orders o 
join 
	OrdersCatalogJoin ocj on o.order_ID=ocj.order_ID
join 
	catalog c on c.catalog_id=ocj.catalog_ID
GROUP by 
	o.order_user_ID , o.TP_ID
order by sum DESC
LIMIT 3 ;


--query 17


SELECT ocjall.country_origin , COUNT(*) as numbersAvailable from 
(SELECT *
from 
	Catalog C
LEFT join 
	OrdersCatalogJoin ocj on c.catalog_ID=ocj.catalog_ID
LEFT JOIN
	Orders o on o.order_ID=ocj.order_ID) As ocjall
WHERE ocjall.order_ID is NULL
GROUP by ocjall.country_origin 
order by numbersAvailable DESC;


--query 18
SELECT
    TPL.TP_ID,
    TPL.first_name,
    TPL.last_name,
    COUNT(Orders.order_ID) AS total_orders,
    (COUNT(Orders.order_ID) * 100.0 / (SELECT COUNT(*) FROM Orders)) AS activity_percentage
FROM
    TPL
LEFT JOIN
    Orders ON TPL.TP_ID = Orders.TP_ID
GROUP BY
    TPL.TP_ID, TPL.first_name, TPL.last_name
ORDER BY
    activity_percentage DESC;



--not so sure on this one 
--query 19
SELECT
    TPL.TP_ID,
    TPL.first_name,
    TPL.last_name,
    STRFTIME('%Y-%m', Orders.order_date) AS order_month,
    AVG(Catalog.selling_price - Catalog.manufacturing_cost) AS avg_monthly_profit
FROM
    TPL
INNER JOIN
    Orders ON TPL.TP_ID = Orders.TP_ID
INNER JOIN
    OrdersCatalogJoin ON OrdersCatalogJoin.order_ID = Orders.order_ID
join 
	Catalog on Catalog.catalog_ID=OrdersCatalogJoin.catalog_ID
WHERE
    Orders.order_date >= DATE('now', '-1 year')  -- بازه زمانی یک سال قبل تا اکنون
GROUP BY
    TPL.TP_ID, TPL.first_name, TPL.last_name, STRFTIME('%Y-%m', Orders.order_date)
ORDER BY
    TPL.TP_ID, order_month;

--query 20
with orderProfits as (
  select o.order_ID, sum(c.selling_price - c.manufacturing_cost) as profit,
  case 
  	when STRFTIME('%w', o.order_date) in ('5', '6') then 'weekend'
  	else 'week'
  end as dayGroup
  from Orders o
  join OrdersCatalogJoin oc on o.order_ID = oc.catalog_ID
  join Catalog c on c.catalog_ID = oc.catalog_ID
  GROUP by o.order_ID
),
averageProfit as (
  select dayGroup, AVG(profit) as averageProfit
  from orderProfits
  group by dayGroup
)
select ap1.dayGroup, ap1.averageProfit, ap2.dayGroup, ap2.averageProfit, 
	case 
    	when ap1.averageProfit > ap2.averageProfit then ap1.dayGroup || 'is more profitable'
        else ap2.dayGroup || 'is more profitable'
    end as comparison
from averageProfit ap1, averageProfit ap2
where ap1.dayGroup = 'week' and ap2.dayGroup = 'weekend';

--query 21
WITH UserOrderCounts AS (
    SELECT 
        u.user_ID, 
        u.first_name, 
        u.last_name, 
        COUNT(o.order_ID) AS num_purchases
    FROM 
        User u
    JOIN 
        Orders o ON u.user_ID = o.order_user_ID
    GROUP BY 
        u.user_ID, u.first_name, u.last_name
)
SELECT 
    user_ID, 
    first_name, 
    last_name, 
    num_purchases
FROM 
    UserOrderCounts
WHERE num_purchases = (
    SELECT 
        MAX(num_purchases) AS max_purchases
    FROM 
        UserOrderCounts
);


--query 22
SELECT 
    w.country,
    COUNT(o.order_ID) AS total_orders,
    SUM(o.Total_cost) AS total_sales
FROM 
    Orders o
JOIN 
    Warehouse w ON o.warehouse_ID = w.warehouse_ID
GROUP BY 
    w.country
ORDER BY 
    total_sales DESC;


--query 23
WITH OrderProfits AS (
    SELECT 
        o.order_ID,
        u.Age,
        SUM(c.selling_price - c.manufacturing_cost) AS profit
    FROM 
        Orders o
    JOIN 
        User u ON o.order_user_ID = u.user_ID
    JOIN 
        Catalog c ON o.order_user_ID = c.ordered_by_user_ID
    GROUP BY 
        o.order_ID
),
AgeGroups AS (
    SELECT 
        CASE 
            WHEN Age BETWEEN 0 AND 18 THEN '0-18'
            WHEN Age BETWEEN 19 AND 30 THEN '19-30'
            WHEN Age BETWEEN 31 AND 40 THEN '31-40'
            WHEN Age BETWEEN 41 AND 50 THEN '41-50'
            WHEN Age BETWEEN 51 AND 60 THEN '51-60'
            ELSE '60+'
        END AS age_group,
        profit
    FROM 
        OrderProfits
)
SELECT 
    age_group,
    AVG(profit) AS average_profit
FROM 
    AgeGroups
GROUP BY 
    age_group
ORDER BY 
    age_group;


--query 24
WITH CustomerOrderCounts AS (
    SELECT 
        o.order_user_ID AS customer_ID,
        c.TP_ID AS store_ID,
        COUNT(o.order_ID) AS order_count
    FROM 
        Orders o,Catalog c
    WHERE 
        o.order_user_ID = c.ordered_by_user_ID AND o.TP_ID = c.TP_ID
    GROUP BY 
        o.order_user_ID, c.TP_ID
),
RepeatCustomers AS (
    SELECT 
        store_ID,
        COUNT(*) AS repeat_customers
    FROM 
        CustomerOrderCounts
    WHERE 
        order_count > 1
    GROUP BY 
        store_ID
)
SELECT 
    T.first_name,
    T.last_name,
    T.TP_ID,
    rc.repeat_customers
FROM 
    RepeatCustomers rc
JOIN 
    TPL T ON rc.store_ID = T.TP_ID
ORDER BY 
    rc.repeat_customers DESC;


--query 25

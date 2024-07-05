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
    COUNT(*) AS PairCount
FROM 
    OrdersCatalogJoin OCJ1
JOIN 
    OrdersCatalogJoin OCJ2 ON OCJ1.order_ID = OCJ2.order_ID AND OCJ1.catalog_ID < OCJ2.catalog_ID
JOIN 
    Catalog P1 ON OCJ1.catalog_ID = P1.catalog_ID
JOIN 
    Catalog P2 ON OCJ2.catalog_ID = P2.catalog_ID
GROUP BY 
    P1.product_name, 
    P2.product_name
ORDER BY 
    PairCount DESC
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



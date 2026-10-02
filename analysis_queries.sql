-- Retail Sales & Customer Analytics
-- SQL examples use broadly supported SQL syntax. Adjust date functions to your database.

-- 1. Monthly sales, profit, and order count
SELECT
    SUBSTR(order_date, 1, 7) AS month,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM retail_sales
GROUP BY SUBSTR(order_date, 1, 7)
ORDER BY month;

-- 2. Revenue and profit by product category
SELECT
    category,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM retail_sales
GROUP BY category
ORDER BY revenue DESC;

-- 3. Regional performance
SELECT
    region,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM retail_sales
GROUP BY region
ORDER BY revenue DESC;

-- 4. Top customers by total spend
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(sales), 2) AS total_spend
FROM retail_sales
GROUP BY customer_id
ORDER BY total_spend DESC
LIMIT 10;

-- 5. Sales channel comparison
SELECT
    sales_channel,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(AVG(sales), 2) AS average_line_item_value
FROM retail_sales
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 6. Product profitability
SELECT
    product_name,
    category,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM retail_sales
GROUP BY product_name, category
ORDER BY profit_margin_pct ASC;

-- 7. Repeat customers
SELECT
    COUNT(*) AS repeat_customer_count
FROM (
    SELECT customer_id
    FROM retail_sales
    GROUP BY customer_id
    HAVING COUNT(DISTINCT order_id) > 1
) AS repeat_customers;

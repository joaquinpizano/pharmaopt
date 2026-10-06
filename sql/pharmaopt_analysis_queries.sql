USE pharmaopt;
USE pharmaopt;

-- ============================================================
-- PHARMAOPT ANALYSIS QUERIES
-- Core database exploration and business analysis
-- ============================================================


-- 1. TOTAL PRODUCTS
SELECT COUNT(*) AS total_products
FROM drug_product;


-- 2. TOTAL PACKAGES
SELECT COUNT(*) AS total_packages
FROM drug_package;


-- 3. TOTAL SHORTAGE EVENTS
SELECT COUNT(*) AS total_shortage_events
FROM shortage_event;


-- 4. TOTAL RECALL EVENTS
SELECT COUNT(*) AS total_recall_events
FROM recall_event;


-- 5. TOTAL RECALL-PACKAGE LINKS
SELECT COUNT(*) AS total_recall_package_links
FROM recall_package;


-- 6. RECALLS BY CLASSIFICATION
SELECT
    classification,
    COUNT(*) AS recall_count
FROM recall_event
GROUP BY classification
ORDER BY recall_count DESC;


-- 7. FIRMS WITH THE MOST RECALL EVENTS
SELECT
    recalling_firm,
    COUNT(*) AS recall_count
FROM recall_event
GROUP BY recalling_firm
ORDER BY recall_count DESC
LIMIT 20;


-- 8. PRODUCTS WITH THE MOST PACKAGE NDCs
SELECT
    product_id,
    COUNT(*) AS package_count
FROM drug_package
GROUP BY product_id
ORDER BY package_count DESC
LIMIT 20;


-- 9. SHORTAGES BY STATUS
SELECT
    status,
    COUNT(*) AS shortage_count
FROM shortage_event
GROUP BY status
ORDER BY shortage_count DESC;


-- 10. UNMATCHED RECALL PACKAGES
SELECT COUNT(*) AS unmatched_recall_packages
FROM recall_package
WHERE linked_package_ndc IS NULL;


-- 11. MATCHED RECALL PACKAGES
SELECT COUNT(*) AS matched_recall_packages
FROM recall_package
WHERE linked_package_ndc IS NOT NULL;


-- 12. RECALL PACKAGE MATCH RATE
SELECT
    ROUND(
        100.0 * SUM(linked_package_ndc IS NOT NULL) / COUNT(*),
        2
    ) AS recall_package_match_rate_pct
FROM recall_package;




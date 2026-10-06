USE pharmaopt;

-- ============================================================
-- PHARMAOPT DATA VALIDATION
-- Data-quality checks for core FDA tables
-- ============================================================


-- 1. DUPLICATE PRODUCT IDs
SELECT
    product_id,
    COUNT(*) AS duplicate_count
FROM drug_product
GROUP BY product_id
HAVING COUNT(*) > 1;


-- 2. MISSING PRODUCT NDCs
SELECT COUNT(*) AS missing_product_ndcs
FROM drug_product
WHERE product_ndc IS NULL
   OR TRIM(product_ndc) = '';


-- 3. DUPLICATE PACKAGE NDCs
SELECT
    package_ndc,
    COUNT(*) AS duplicate_count
FROM drug_package
GROUP BY package_ndc
HAVING COUNT(*) > 1;


-- 4. MISSING PACKAGE NDCs
SELECT COUNT(*) AS missing_package_ndcs
FROM drug_package
WHERE package_ndc IS NULL
   OR TRIM(package_ndc) = '';


-- 5. UNMATCHED RECALL PACKAGES
SELECT COUNT(*) AS unmatched_recall_packages
FROM recall_package
WHERE linked_package_ndc IS NULL;


-- 6. MATCHED RECALL PACKAGES
SELECT COUNT(*) AS matched_recall_packages
FROM recall_package
WHERE linked_package_ndc IS NOT NULL;


-- 7. RECALL PACKAGE MATCH RATE
SELECT
    ROUND(
        100.0 * SUM(linked_package_ndc IS NOT NULL) / COUNT(*),
        2
    ) AS recall_package_match_rate_pct
FROM recall_package;


-- 8. CORE TABLE ROW COUNTS
SELECT 'drug_product' AS table_name, COUNT(*) AS row_count
FROM drug_product

UNION ALL

SELECT 'drug_package', COUNT(*)
FROM drug_package

UNION ALL

SELECT 'shortage_event', COUNT(*)
FROM shortage_event

UNION ALL

SELECT 'recall_event', COUNT(*)
FROM recall_event

UNION ALL

SELECT 'recall_package', COUNT(*)
FROM recall_package;

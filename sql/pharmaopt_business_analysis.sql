USE pharmaopt;

-- ============================================================
-- PHARMAOPT BUSINESS ANALYSIS
-- Pharmaceutical shortage and recall insights
-- ============================================================

-- 1. Manufacturers with the most recalls
SELECT
    recalling_firm,
    COUNT(*) AS recall_count
FROM recall_event
GROUP BY recalling_firm
ORDER BY recall_count DESC
LIMIT 20;

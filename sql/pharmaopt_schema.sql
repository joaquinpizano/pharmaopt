USE pharmaopt;

-- ============================================================
-- PHARMAOPT DATABASE SCHEMA
-- FDA FOUNDATION TABLES
-- ============================================================

-- Remove the empty development tables in dependency order
DROP TABLE IF EXISTS recall_package;
DROP TABLE IF EXISTS shortage_event;
DROP TABLE IF EXISTS recall_event;
DROP TABLE IF EXISTS drug_package;
DROP TABLE IF EXISTS drug_product;


-- ============================================================
-- 1. DRUG PRODUCT
-- One row per unique FDA product_id
-- ============================================================

CREATE TABLE drug_product (
    product_id VARCHAR(64) PRIMARY KEY,
    product_ndc VARCHAR(20) NOT NULL,
    spl_id VARCHAR(36),
    generic_name VARCHAR(600),
    brand_name VARCHAR(400),
    labeler_name VARCHAR(200),
    dosage_form VARCHAR(100),
    marketing_category VARCHAR(100),

    INDEX idx_product_ndc (product_ndc),
    INDEX idx_generic_name (generic_name),
    INDEX idx_labeler_name (labeler_name)
);


-- ============================================================
-- 2. DRUG PACKAGE
-- One row per unique FDA package_ndc
-- Each package links to its FDA product_id
-- ============================================================

CREATE TABLE drug_package (
    package_ndc VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(64) NOT NULL,
    package_description TEXT,

    INDEX idx_package_product_id (product_id),

    CONSTRAINT fk_package_product
        FOREIGN KEY (product_id)
        REFERENCES drug_product(product_id)
);


-- ============================================================
-- 3. SHORTAGE EVENT
-- Preserve every FDA shortage record.
-- source_package_ndc = value reported by shortage dataset
-- linked_package_ndc = current NDC package match, if available
-- ============================================================

CREATE TABLE shortage_event (
    shortage_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    source_package_ndc VARCHAR(20) NOT NULL,
    linked_package_ndc VARCHAR(20),

    generic_name VARCHAR(600),
    company_name VARCHAR(255),
    status VARCHAR(100),
    availability VARCHAR(100),

    shortage_reason TEXT,
    therapeutic_category TEXT,

    dosage_form VARCHAR(150),
    presentation TEXT,
    update_type VARCHAR(100),

    initial_posting_date DATE,
    update_date DATE,
    change_date DATE,

    resolved_note TEXT,

    INDEX idx_shortage_source_ndc (source_package_ndc),
    INDEX idx_shortage_linked_ndc (linked_package_ndc),
    INDEX idx_shortage_status (status),

    CONSTRAINT fk_shortage_package
        FOREIGN KEY (linked_package_ndc)
        REFERENCES drug_package(package_ndc)
);


-- ============================================================
-- 4. RECALL EVENT
-- One row per unique FDA recall_number
-- ============================================================

CREATE TABLE recall_event (
    recall_number VARCHAR(50) PRIMARY KEY,

    event_id BIGINT,
    recalling_firm VARCHAR(255),
    classification VARCHAR(100),
    status VARCHAR(100),
    product_type VARCHAR(100),

    product_description TEXT,
    product_quantity TEXT,
    reason_for_recall TEXT,
    distribution_pattern TEXT,

    voluntary_mandated VARCHAR(100),
    initial_firm_notification VARCHAR(150),

    recall_initiation_date DATE,
    report_date DATE,
    termination_date DATE,

    INDEX idx_recall_event_id (event_id),
    INDEX idx_recalling_firm (recalling_firm),
    INDEX idx_recall_classification (classification)
);


-- ============================================================
-- 5. RECALL PACKAGE BRIDGE
-- One recall can affect many package NDCs.
-- Original FDA NDC is always preserved.
-- Current-directory match is nullable.
-- ============================================================

CREATE TABLE recall_package (
    recall_package_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    recall_number VARCHAR(50) NOT NULL,
    source_package_ndc VARCHAR(20) NOT NULL,
    linked_package_ndc VARCHAR(20),
drug_product
    INDEX idx_rp_recall_number (recall_number),
    INDEX idx_rp_source_ndc (source_package_ndc),
    INDEX idx_rp_linked_ndc (linked_package_ndc),
drug_product
    CONSTRAINT fk_rp_recall
        FOREIGN KEY (recall_number)
        REFERENCES recall_event(recall_number),

    CONSTRAINT fk_rp_package
        FOREIGN KEY (linked_package_ndc)
        REFERENCES drug_package(package_ndc)
);


-- ============================================================
-- VERIFY
-- ============================================================

SHOW TABLES;
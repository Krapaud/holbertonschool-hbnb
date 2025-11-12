-- Test script to verify CASCADE DELETE functionality
-- This script creates test data and then tests cascade deletion

-- Clean up any existing test data
DELETE FROM reviews WHERE user_id LIKE 'test-%' OR place_id LIKE 'test-%';
DELETE FROM place_amenity WHERE place_id LIKE 'test-%';
DELETE FROM places WHERE id LIKE 'test-%' OR owner_id LIKE 'test-%';
DELETE FROM users WHERE id LIKE 'test-%';

-- Create test users
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES 
    ('test-user-owner-001', 'Test', 'Owner', 'test.owner@example.com', '$2b$12$test', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('test-user-reviewer-002', 'Test', 'Reviewer', 'test.reviewer@example.com', '$2b$12$test', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Create test place owned by test user
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES 
    ('test-place-001', 'Test Place', 'A test place for cascade delete', 100.00, 40.7128, -74.0060, 'test-user-owner-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Create test reviews
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES 
    ('test-review-001', 'Review by owner', 5, 'test-user-owner-001', 'test-place-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('test-review-002', 'Review by reviewer', 4, 'test-user-reviewer-002', 'test-place-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Verify data was inserted
SELECT 'BEFORE DELETE - Users:' AS Test;
SELECT id, first_name, last_name, email FROM users WHERE id LIKE 'test-%';

SELECT 'BEFORE DELETE - Places:' AS Test;
SELECT id, title, owner_id FROM places WHERE id LIKE 'test-%';

SELECT 'BEFORE DELETE - Reviews:' AS Test;
SELECT id, text, user_id, place_id FROM reviews WHERE id LIKE 'test-%';

-- TEST 1: Delete the owner user (should cascade to places and reviews)
SELECT '=== TEST 1: Deleting owner user ===' AS Test;
DELETE FROM users WHERE id = 'test-user-owner-001';

SELECT 'AFTER DELETE OWNER - Users:' AS Test;
SELECT id, first_name, last_name, email FROM users WHERE id LIKE 'test-%';

SELECT 'AFTER DELETE OWNER - Places (should be empty):' AS Test;
SELECT id, title, owner_id FROM places WHERE id LIKE 'test-%';

SELECT 'AFTER DELETE OWNER - Reviews (should be empty):' AS Test;
SELECT id, text, user_id, place_id FROM reviews WHERE id LIKE 'test-%';

-- Clean up remaining test data
DELETE FROM reviews WHERE user_id LIKE 'test-%' OR place_id LIKE 'test-%';
DELETE FROM place_amenity WHERE place_id LIKE 'test-%';
DELETE FROM places WHERE id LIKE 'test-%' OR owner_id LIKE 'test-%';
DELETE FROM users WHERE id LIKE 'test-%';

SELECT '=== CASCADE DELETE TEST COMPLETED ===' AS Test;

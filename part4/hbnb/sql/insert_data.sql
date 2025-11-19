-- Insert initial data into the database

-- Insert Administrator User - Using bcrypt-generator.com for hash bcrypt2 the password
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$6D/A418HGqInNHr.syUNf.HAyxcK6Uz2FB4yuiOQwSpytaoD48TTG',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Test User - password: test_user1234
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Test',
    'User',
    'test_user@example.com',
    '$2b$12$N6HuyLoIbmo0xQgILZdJLeYyYUtLPi9CausIFTzg1krsOKz6h1H6u',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities - Using uuidgenerator.net pour generate UUID4
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES 
    ('2767d121-c1b4-4d16-a816-0f5113ab06d0', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('bcf813cf-1fd0-4a7f-b69d-d4167331aaa1', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('32561383-c728-4ba3-9fd2-cb7ceab79fca', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert Initial Places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES 
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Apartment Cosy Nice', 'Beautiful apartment in Nice with sea view', 90.00, 43.7102, 7.2620, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'Apartment Cosy Fréjus', 'Charming apartment in Fréjus near the beach', 75.00, 43.4332, 6.7369, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c3d4e5f6-a7b8-9012-cdef-123456789012', 'Apartment Cosy Paris', 'Modern apartment in the heart of Paris', 120.00, 48.8566, 2.3522, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('d4e5f6a7-b8c9-0123-def1-234567890123', 'Budget Studio Marseille', 'Affordable studio near the old port', 45.00, 43.2965, 5.3698, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('e5f6a7b8-c9d0-1234-ef12-345678901234', 'Luxury Villa Cannes', 'Exclusive villa with private pool and sea view', 350.00, 43.5528, 7.0174, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('f6a7b8c9-d0e1-2345-f123-456789012345', 'Cozy Room Lyon', 'Small room in city center, perfect for solo travelers', 35.00, 45.7640, 4.8357, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a7b8c9d0-e1f2-3456-1234-567890123456', 'Penthouse Monaco', 'Stunning penthouse with panoramic views', 500.00, 43.7384, 7.4246, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b8c9d0e1-f2a3-4567-2345-678901234567', 'Charming Flat Bordeaux', 'Beautiful flat in historic district', 65.00, 44.8378, -0.5792, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c9d0e1f2-a3b4-5678-3456-789012345678', 'Tiny House Toulouse', 'Eco-friendly tiny house with garden', 55.00, 43.6047, 1.4442, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('d0e1f2a3-b4c5-6789-4567-890123456789', 'Beachfront Apartment Biarritz', 'Direct access to the beach', 95.00, 43.4832, -1.5586, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert Place-Amenity associations
INSERT INTO place_amenity (place_id, amenity_id)
VALUES 
    -- Apartment Cosy Nice (90€): WiFi + Air Conditioning
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', '32561383-c728-4ba3-9fd2-cb7ceab79fca'),
    
    -- Apartment Cosy Fréjus (75€): WiFi only
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    
    -- Apartment Cosy Paris (120€): WiFi + Air Conditioning
    ('c3d4e5f6-a7b8-9012-cdef-123456789012', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    ('c3d4e5f6-a7b8-9012-cdef-123456789012', '32561383-c728-4ba3-9fd2-cb7ceab79fca'),
    
    -- Budget Studio Marseille (45€): NO amenities
    
    -- Luxury Villa Cannes (350€): ALL amenities
    ('e5f6a7b8-c9d0-1234-ef12-345678901234', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    ('e5f6a7b8-c9d0-1234-ef12-345678901234', 'bcf813cf-1fd0-4a7f-b69d-d4167331aaa1'),
    ('e5f6a7b8-c9d0-1234-ef12-345678901234', '32561383-c728-4ba3-9fd2-cb7ceab79fca'),
    
    -- Cozy Room Lyon (35€): NO amenities
    
    -- Penthouse Monaco (500€): ALL amenities
    ('a7b8c9d0-e1f2-3456-1234-567890123456', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    ('a7b8c9d0-e1f2-3456-1234-567890123456', 'bcf813cf-1fd0-4a7f-b69d-d4167331aaa1'),
    ('a7b8c9d0-e1f2-3456-1234-567890123456', '32561383-c728-4ba3-9fd2-cb7ceab79fca'),
    
    -- Charming Flat Bordeaux (65€): WiFi only
    ('b8c9d0e1-f2a3-4567-2345-678901234567', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    
    -- Tiny House Toulouse (55€): WiFi only
    ('c9d0e1f2-a3b4-5678-3456-789012345678', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    
    -- Beachfront Apartment Biarritz (95€): WiFi + Swimming Pool
    ('d0e1f2a3-b4c5-6789-4567-890123456789', '2767d121-c1b4-4d16-a816-0f5113ab06d0'),
    ('d0e1f2a3-b4c5-6789-4567-890123456789', 'bcf813cf-1fd0-4a7f-b69d-d4167331aaa1');

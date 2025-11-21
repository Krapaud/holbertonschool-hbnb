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

-- Insert Maria Garcia - password: test_user1234
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Maria',
    'Garcia',
    'maria.garcia@example.com',
    '$2b$12$N6HuyLoIbmo0xQgILZdJLeYyYUtLPi9CausIFTzg1krsOKz6h1H6u',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Yuki Tanaka - password: yuki_pass2024
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f',
    'Yuki',
    'Tanaka',
    'yuki.tanaka@example.com',
    '$2b$12$8K5BoJ0MfXqN.zTvW1YxHuV3pL9sC2jD4nE6mF7gH8iJ9kL0mN1oP',
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
    -- Admin's properties (luxury & premium)
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Apartment Cosy Nice', 'Beautiful apartment in Nice with sea view', 90.00, 43.7102, 7.2620, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('e5f6a7b8-c9d0-1234-ef12-345678901234', 'Luxury Villa Cannes', 'Exclusive villa with private pool and sea view', 350.00, 43.5528, 7.0174, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a7b8c9d0-e1f2-3456-1234-567890123456', 'Penthouse Monaco', 'Stunning penthouse with panoramic views', 500.00, 43.7384, 7.4246, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c3d4e5f6-a7b8-9012-cdef-123456789012', 'Apartment Cosy Paris', 'Modern apartment in the heart of Paris', 120.00, 48.8566, 2.3522, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Maria Garcia's properties (mid-range)
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'Apartment Cosy Fréjus', 'Charming apartment in Fréjus near the beach', 75.00, 43.4332, 6.7369, '550e8400-e29b-41d4-a716-446655440000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b8c9d0e1-f2a3-4567-2345-678901234567', 'Charming Flat Bordeaux', 'Beautiful flat in historic district', 65.00, 44.8378, -0.5792, '550e8400-e29b-41d4-a716-446655440000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('d0e1f2a3-b4c5-6789-4567-890123456789', 'Beachfront Apartment Biarritz', 'Direct access to the beach', 95.00, 43.4832, -1.5586, '550e8400-e29b-41d4-a716-446655440000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Yuki Tanaka's properties (budget & eco-friendly)
    ('d4e5f6a7-b8c9-0123-def1-234567890123', 'Budget Studio Marseille', 'Affordable studio near the old port', 45.00, 43.2965, 5.3698, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('f6a7b8c9-d0e1-2345-f123-456789012345', 'Cozy Room Lyon', 'Small room in city center, perfect for solo travelers', 35.00, 45.7640, 4.8357, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c9d0e1f2-a3b4-5678-3456-789012345678', 'Tiny House Toulouse', 'Eco-friendly tiny house with garden', 55.00, 43.6047, 1.4442, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

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

-- Insert Reviews (users cannot review their own places)
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES
    -- Maria reviews Admin's places
    ('r1a2b3c4-d5e6-7890-abcd-ef1234567890', 'Amazing apartment with stunning sea views! The location is perfect and the host was very welcoming. Highly recommend!', 5, '550e8400-e29b-41d4-a716-446655440000', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('r2b3c4d5-e6f7-8901-bcde-f12345678901', 'Absolutely luxurious! The villa exceeded all expectations. Private pool was a dream. Worth every penny!', 5, '550e8400-e29b-41d4-a716-446655440000', 'e5f6a7b8-c9d0-1234-ef12-345678901234', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('r3c4d5e6-f7a8-9012-cdef-123456789012', 'Great location in Paris, but a bit noisy at night. Overall good experience though.', 4, '550e8400-e29b-41d4-a716-446655440000', 'c3d4e5f6-a7b8-9012-cdef-123456789012', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Yuki reviews Admin's places
    ('r4d5e6f7-a8b9-0123-def1-234567890123', 'Too expensive for what it offers. Nice place but not worth the price for budget travelers.', 3, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', 'a7b8c9d0-e1f2-3456-1234-567890123456', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('r5e6f7a8-b9c0-1234-ef12-345678901234', 'Beautiful apartment but definitely on the pricey side. Clean and well-maintained.', 4, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Admin reviews Maria's places
    ('r6f7a8b9-c0d1-2345-f123-456789012345', 'Perfect beachside getaway! Clean, comfortable, and great value for money. Maria is an excellent host!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('r7a8b9c0-d1e2-3456-1234-567890123456', 'Charming flat in a historic area. Could use better WiFi but overall very pleasant stay.', 4, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'b8c9d0e1-f2a3-4567-2345-678901234567', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('r8b9c0d1-e2f3-4567-2345-678901234567', 'Direct beach access is amazing! The apartment was spotless and well-equipped. Fantastic experience!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'd0e1f2a3-b4c5-6789-4567-890123456789', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Yuki reviews Maria's places
    ('r9c0d1e2-f3a4-5678-3456-789012345678', 'Good value for the price. Location is convenient and the host responded quickly to questions.', 4, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('rad1e2f3-a4b5-6789-4567-890123456789', 'Nice place but a bit far from the city center. Apartment itself was cozy and clean.', 4, '7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f', 'b8c9d0e1-f2a3-4567-2345-678901234567', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Admin reviews Yuki's places
    ('rbe2f3a4-b5c6-7890-5678-901234567890', 'Great budget option! Perfect for a quick stay. Very clean and Yuki was helpful.', 4, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'd4e5f6a7-b8c9-0123-def1-234567890123', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('rcf3a4b5-c6d7-8901-6789-012345678901', 'Cozy room, exactly as described. Great for solo travelers on a budget. Would stay again!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'f6a7b8c9-d0e1-2345-f123-456789012345', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('rda4b5c6-d7e8-9012-7890-123456789012', 'Loved the eco-friendly concept! The tiny house was charming and comfortable. Unique experience!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'c9d0e1f2-a3b4-5678-3456-789012345678', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Maria reviews Yuki's places
    ('reb5c6d7-e8f9-0123-8901-234567890123', 'Excellent value! The studio was small but had everything needed. Very clean and well-located.', 5, '550e8400-e29b-41d4-a716-446655440000', 'd4e5f6a7-b8c9-0123-def1-234567890123', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('rfc6d7e8-f9a0-1234-9012-345678901234', 'Basic but functional. Good for a night or two. Yuki was responsive and helpful.', 3, '550e8400-e29b-41d4-a716-446655440000', 'f6a7b8c9-d0e1-2345-f123-456789012345', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('r0d7e8f9-a0b1-2345-0123-456789012345', 'The tiny house concept is great! Very peaceful and perfect for a digital detox. Loved it!', 5, '550e8400-e29b-41d4-a716-446655440000', 'c9d0e1f2-a3b4-5678-3456-789012345678', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

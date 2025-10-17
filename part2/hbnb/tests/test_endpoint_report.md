# API Testing Report

## Introduction
This report describes the tests performed on the User, Place, Review, and Amenity endpoints of the Flask-RESTx HBNB API.

**Report date:** October 16, 2025  
**API version:** v1  
**Test framework:** pytest + test automation

## Methodology
- **Tools:** pytest
- **Base URL:** http://127.0.0.1:5000/api/v1/
- **Test type:** Automated unit tests with endpoint validation

## Manual cURL Tests
| # | Method | Endpoint | Data | Expected Result | Actual Result | Status |
|---|----------|-----------|----------|------------------|------------------|--------|
| 1 | POST | /users | `{ "first_name": "John", "last_name": "Doe", "email": "john@example.com" }` | 201 Created | 201 Created | PASS |
| 2 | POST | /users | `{ "first_name": "", "last_name": "Doe", "email": "john@example.com" }` | 400 Bad Request | 400 Bad Request | PASS |
| 3 | GET | /users/invalid-id | — | 404 Not Found | 404 Not Found | PASS |
| 4 | POST | /places | `{ "title": "", "price": 100, "latitude": 25, "longitude": -80, "owner_id": "valid-id" }` | 400 Bad Request | 400 Bad Request | PASS |
| 5 | POST | /reviews | `{ "text": "", "rating": 5, "user_id": "valid", "place_id": "valid" }` | 400 Bad Request | 400 Bad Request | PASS |

## Automated Unit Tests

### Global Results
- **Total tests:** 26
- **Successful tests:** 26
- **Failed tests:** 0
- **Success rate:** 100%

### Tests by Category

#### 1. User Tests (7 tests)
| Test | Description | Status |
|------|-------------|--------|
| `test_create_user_valid_data` | User creation with valid data | PASSED |
| `test_create_user_empty_first_name` | Empty first_name validation | PASSED |
| `test_create_user_empty_last_name` | Empty last_name validation | PASSED |
| `test_create_user_empty_email` | Empty email validation | PASSED |
| `test_create_user_invalid_email_format` | Invalid email format validation | PASSED |
| `test_create_user_missing_required_fields` | Missing required fields | PASSED |
| `test_create_user_whitespace_only_fields` | Whitespace-only fields | PASSED |

**Email formats tested as invalid:**
- `invalid-email` (no @)
- `user@` (missing domain)
- `@domain.com` (missing user)
- `user.domain.com` (missing @)
- `user @domain.com` (invalid space)
- `user@domain` (missing TLD)
- `user@.com` (invalid domain)

#### 2. Place Tests (7 tests)
| Test | Description | Status |
|------|-------------|--------|
| `test_create_place_valid_data` | Place creation with valid data | PASSED |
| `test_create_place_empty_title` | Empty title validation | PASSED |
| `test_create_place_negative_price` | Negative price validation | PASSED |
| `test_create_place_zero_price` | Zero price validation | PASSED |
| `test_create_place_invalid_latitude` | Invalid latitude validation | PASSED |
| `test_create_place_invalid_longitude` | Invalid longitude validation | PASSED |
| `test_create_place_valid_boundary_coordinates` | Valid boundary coordinates | PASSED |

**Geographic validations tested:**
- Latitude: [-90.0, 90.0]
- Longitude: [-180.0, 180.0]
- Boundary values tested: (-90,-180), (90,180), (0,0)

#### 3. Review Tests (6 tests)
| Test | Description | Status |
|------|-------------|--------|
| `test_create_review_valid_data` | Review creation with valid data | PASSED |
| `test_create_review_empty_text` | Empty text validation | PASSED |
| `test_create_review_whitespace_only_text` | Whitespace-only text validation | PASSED |
| `test_create_review_invalid_user_id` | Invalid user_id validation | PASSED |
| `test_create_review_invalid_place_id` | Invalid place_id validation | PASSED |
| `test_create_review_invalid_rating` | Invalid rating validation | PASSED |

**Ratings tested as invalid:** 0, 6, -1, 10 (valid: 1-5)

#### 4. Amenity Tests (6 tests)
| Test | Description | Status |
|------|-------------|--------|
| `test_create_amenity_valid_data` | Amenity creation with valid data | PASSED |
| `test_create_amenity_empty_text` | Empty name validation | PASSED |
| `test_create_amenity_whitespace_only_text` | Whitespace-only name validation | PASSED |
| `test_create_amenity_already_exist` | Duplicate Creation | PASSED |
| `test_create_amenity_missing_name` | Missing required field | PASSED |
| `test_create_amenity_name_too_long` | Name length validation (max 50 chars) | PASSED |

## Swagger Documentation
- Swagger UI accessible on `/api/v1/`
- All endpoints documented with schemas
- Data models correctly defined
- Appropriate HTTP response codes

## Issues Identified and Resolved

### 1. Review Validation Error (Resolved)
**Problem:** Review validations returned 404 instead of 400  
**Cause:** Incorrect exception handling in `reviews.py`  
**Solution:** Distinction between 404 errors (entity not found) and 400 errors (validation failed)

```python
# Before (incorrect)
except ValueError as e:
    return {'error': str(e)}, 404

# After (correct)  
except ValueError as e:
    error_msg = str(e)
    if "not found" in error_msg:
        return {'error': error_msg}, 404
    return {'error': error_msg}, 400
```

### 2. Amenity Validation Error (Resolved)
**Problem:** Amenity validations returned `{'id': None, 'name': None}` instead of proper error messages  
**Cause:** The `@api.marshal_with(amenity_response_model, code=201)` decorator was applied to the POST endpoint, forcing all responses to follow the success response model even for errors  
**Solution:** Remove the decorator from error responses or skip marshalling for error cases

```python
# Before (incorrect)
@api.marshal_with(amenity_response_model, code=201)
def post(self):
    # ...validation code...
    return {'error': 'Name cannot be empty'}, 400  # Gets marshalled to {'id': None, 'name': None}

# After (correct)
@api.marshal_with(amenity_response_model, code=201, skip_none=True)
def post(self):
    # ...validation code...
    return {'error': 'Name cannot be empty'}, 400  # Returns proper error message
```

**Tests affected:**
- `test_create_amenity_empty_text` - Empty name validation | OK
- `test_create_amenity_whitespace_only_text` - Whitespace-only validation | OK
- `test_create_amenity_already_exist` - Duplicate amenity detection | OK
- `test_create_amenity_missing_name` - Missing required field | X
- `test_create_amenity_name_too_long` - Name length validation | OK

### 3. Amenity Missing Name Field Error (Resolved)
**Problem:** Creating amenity without `name` field returns 500 instead of 400  
**Cause:** When `api.payload` is empty or `name` key is missing, accessing `amenity_data['name']` raises a `KeyError` before validation checks, triggering the generic exception handler that returns 500  
**Solution:** Check for missing field before attempting to access it

```python
# Before (incorrect)
def post(self):
    amenity_data = api.payload
    # This line throws KeyError if 'name' is missing
    existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
    if not amenity_data or 'name' not in amenity_data:
        return {'error': 'Name is required'}, 400

# After (correct)
def post(self):
    amenity_data = api.payload
    # Check for missing field FIRST
    if not amenity_data or 'name' not in amenity_data:
        return {'error': 'Name is required'}, 400
    # Now safe to access amenity_data['name']
    existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
```

**Test affected:**
- `test_create_amenity_missing_name` - Returns 500 instead of 400 | OK

### 4. Amenity Duplicate Detection Error (Resolved)
**Problem:** Creating duplicate amenity returns 201 instead of 400  
**Cause:** The duplicate check was performed AFTER accessing `amenity_data['name']`, and the logic order prevented proper duplicate detection  
**Solution:** Reorganize validation order: check field existence → validate format → check duplicates → create

```python
# Before (incorrect order)
def post(self):
    amenity_data = api.payload
    existing_amenity = facade.get_amenity_by_name(amenity_data['name'])  # KeyError risk
    if not amenity_data or 'name' not in amenity_data:
        return {'error': 'Name is required'}, 400
    # ...

# After (correct order)
def post(self):
    amenity_data = api.payload
    # 1. Check field existence
    if not amenity_data or 'name' not in amenity_data:
        return {'error': 'Name is required'}, 400
    # 2. Validate format
    name = amenity_data['name'].strip()
    if not name:
        return {'error': 'Name cannot be empty'}, 400
    # 3. Check for duplicates
    existing_amenity = facade.get_amenity_by_name(name)
    if existing_amenity:
        return {'error': 'Amenity already exist'}, 400
    # 4. Create new amenity
    new_amenity = facade.create_amenity(amenity_data)
```

**Test affected:**
- `test_create_amenity_already_exist` - Returns 201 instead of 400 | OK

### 5. Email Validation
**Implementation:** Regex for valid email format  
**Tests:** 7 invalid formats tested successfully

### 6. Geographic Coordinates Validation
**Implementation:** Latitude [-90, 90] and longitude [-180, 180] controls  
**Tests:** Boundaries and out-of-bounds values tested

### 7. Place Reviews Retrieval Error (Resolved - October 16, 2025)
**Problem:** Unable to retrieve reviews for a specific place via Postman  
**Identified causes:**

1. **Error in `app/services/facade.py`:**
   - The method `get_reviews_by_place(place_id)` was using `self.review_repo.get_by_attribute('place_id', place_id)`
   - Issue: The `ReviewModel` model doesn't have a `place_id` attribute, but a `place` object
   - Result: The search failed and returned `None` or an empty list

2. **Duplicated and misplaced route:**
   - A route `@api.route('/<place_id>/reviews')` existed in the `reviews` namespace (`app/api/v1/reviews.py`)
   - This created the incorrect URL: `/reviews/<place_id>/reviews`
   - The expected logical URL was: `/places/<place_id>/reviews`

**Applied solutions:**

1. **Fix in `app/services/facade.py` (line ~141):**
```python
# BEFORE (incorrect)
def get_reviews_by_place(self, place_id):
    return self.review_repo.get_by_attribute('place_id', place_id)

# AFTER (correct)
def get_reviews_by_place(self, place_id):
    all_reviews = self.review_repo.get_all()
    return [review for review in all_reviews if review.place.id == place_id]
```
   - The method now iterates through all reviews and filters by `review.place.id`
   - Uses the correct object relationship between Review and Place

2. **Removal of duplicated route in `app/api/v1/reviews.py`:**
   - Removed the `PlaceReviews` class and its route `/<place_id>/reviews` (lines 126-141)
   - Eliminates confusion and URL conflict

3. **Addition of correct route in `app/api/v1/places.py`:**
```python
@api.route('/<place_id>/reviews')
class PlaceReviewsList(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                'user_id': review.user.id} for review in reviews], 200
```

**Impact:**
- OK Endpoint works correctly in Postman
- OK Consistent and RESTful URL: `GET /api/v1/places/<place_id>/reviews`
- OK Proper validation with correct HTTP error codes (400, 404)
- OK Verification of place existence before retrieving reviews
- OK Returns empty list if the place has no reviews
- OK No breaking changes for other endpoints

**Modified files:**
- `app/services/facade.py`
- `app/api/v1/reviews.py`
- `app/api/v1/places.py`

### 8. Error 500 Detection Tests (October 17, 2025)

A comprehensive test suite was created to detect potential Internal Server Error (500) responses across all API endpoints. These tests validate that the API handles edge cases and malformed requests gracefully with appropriate error codes instead of crashing.

#### Error 500 Cases Identified and Resolved

| # | Endpoint | Issue | Request Data | Expected | Actual Before Fix | Status |
|---|----------|-------|--------------|----------|-------------------|--------|
| 1 | POST /amenities | Integer as name | `{"name": 123}` | 400 Bad Request | **500 Internal Server Error** | OK FIXED |
| 2 | POST /places | String as price | `{"title": "Test", "price": "100", ...}` | 400 Bad Request | **500 Internal Server Error** | OK FIXED |
| 3 | POST /places | String as coordinates | `{"latitude": "40.7", "longitude": "-74.0", ...}` | 400 Bad Request | **500 Internal Server Error** | OK FIXED |
| 4 | POST /places | Missing title field | `{"price": 100, "latitude": 40.7, ...}` | 400 Bad Request | **500 Internal Server Error** | OK FIXED |
| 5 | POST /places/{id}/amenities | Array instead of single ID | `{"amenity_id": ["id1", "id2"]}` | 400 Bad Request | **500 Internal Server Error** | OK FIXED |
| 6 | POST /reviews | Array as user_id/place_id | `{"user_id": ["id1"], "place_id": ["id2"], ...}` | 400 Bad Request | **500 Internal Server Error** | OK FIXED |

#### Detailed Error Analysis

**1. Amenity - Integer Name (Fixed)**
```python
# Problem: Type validation missing
POST /api/v1/amenities/
{"name": 123}

# Response before fix: 500 Internal Server Error
# Response after fix: 400 Bad Request with proper error message
```

**Fix applied in `app/api/v1/amenities.py`:**
```python
def post(self):
    amenity_data = api.payload
    if not amenity_data or 'name' not in amenity_data:
        return {'error': 'Name is required'}, 400
    
    # Added type validation
    if not isinstance(amenity_data['name'], str):
        return {'error': 'Name must be a string'}, 400
    
    name = amenity_data['name'].strip()
    if not name:
        return {'error': 'Name cannot be empty'}, 400
```

**2. Place - String Price (Fixed)**
```python
# Problem: Type coercion not handled
POST /api/v1/places/
{"title": "House", "price": "100", "latitude": 40.7, "longitude": -74.0, "owner_id": "valid-id"}

# Response before fix: 500 Internal Server Error
# Response after fix: 400 Bad Request
```

**Fix applied in `app/api/v1/places.py`:**
```python
def post(self):
    place_data = api.payload
    
    # Added type validation for numeric fields
    if 'price' in place_data and not isinstance(place_data['price'], (int, float)):
        return {'error': 'Price must be a number'}, 400
```

**3. Place - String Coordinates (Fixed)**
```python
# Problem: Latitude/Longitude type validation missing
POST /api/v1/places/
{"title": "House", "price": 100, "latitude": "40.7", "longitude": "-74.0", "owner_id": "valid-id"}

# Response before fix: 500 Internal Server Error
# Response after fix: 400 Bad Request
```

**Fix applied in `app/api/v1/places.py`:**
```python
def post(self):
    place_data = api.payload
    
    # Added coordinate type validation
    if 'latitude' in place_data and not isinstance(place_data['latitude'], (int, float)):
        return {'error': 'Latitude must be a number'}, 400
    if 'longitude' in place_data and not isinstance(place_data['longitude'], (int, float)):
        return {'error': 'Longitude must be a number'}, 400
```

**4. Place - Missing Required Field (Fixed)**
```python
# Problem: KeyError when accessing missing 'title' field
POST /api/v1/places/
{"price": 100, "latitude": 40.7, "longitude": -74.0, "owner_id": "valid-id"}

# Response before fix: 500 Internal Server Error
# Response after fix: 400 Bad Request
```

**Fix applied in `app/api/v1/places.py`:**
```python
def post(self):
    place_data = api.payload
    
    # Check required fields BEFORE accessing them
    required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
    for field in required_fields:
        if field not in place_data:
            return {'error': f'{field} is required'}, 400
```

**5. Place Add Amenity - Array Instead of String (Fixed)**
```python
# Problem: Array sent instead of single amenity_id
POST /api/v1/places/{place_id}/amenities
{"amenity_id": ["amenity-id-1", "amenity-id-2"]}

# Response before fix: 500 Internal Server Error
# Response after fix: 400 Bad Request
```

**Fix applied in `app/api/v1/places.py`:**
```python
@api.route('/<place_id>/amenities')
class PlaceAmenityList(Resource):
    def post(self, place_id):
        data = api.payload
        
        # Validate amenity_id is a string
        if not isinstance(data.get('amenity_id'), str):
            return {'error': 'amenity_id must be a string'}, 400
```

**6. Review - Array IDs (Fixed)**
```python
# Problem: Arrays sent for user_id and place_id
POST /api/v1/reviews/
{"text": "Great!", "rating": 5, "user_id": ["user1"], "place_id": ["place1"]}

# Response before fix: 500 Internal Server Error
# Response after fix: 400 Bad Request
```

**Fix applied in `app/api/v1/reviews.py`:**
```python
def post(self):
    review_data = api.payload
    
    # Validate ID types
    if not isinstance(review_data.get('user_id'), str):
        return {'error': 'user_id must be a string'}, 400
    if not isinstance(review_data.get('place_id'), str):
        return {'error': 'place_id must be a string'}, 400
```

#### Additional Tests Performed

**Edge Cases Tested (No 500 errors found):**
- OK Empty request bodies
- OK Null JSON bodies
- OK Invalid JSON format
- OK Very large payloads (>1MB)
- OK Unicode and special characters
- OK Extremely long strings (>10000 chars)
- OK Boolean values in string fields
- OK Object values in string fields
- OK Negative prices
- OK Out-of-range coordinates
- OK Duplicate email/name validations
- OK Nonexistent entity updates/deletes
- OK Invalid UUID formats
- OK Wrong HTTP methods on endpoints
- OK Wrong Content-Type headers

#### Files Modified for Error 500 Fixes
- `app/api/v1/amenities.py` - Added type and existence validation
- `app/api/v1/places.py` - Added type validation for numeric fields and required field checks
- `app/api/v1/reviews.py` - Added type validation for ID fields

### 9. Review Deletion - Place Synchronization Error (Resolved - October 17, 2025)

**Problem:** When a review is deleted, it is removed from the review repository but remains in the place's `reviews` list. This causes deleted reviews to still appear when retrieving a place's reviews.

**Identified cause:**
- The `delete_review()` method in `app/services/facade.py` only deleted the review from the repository
- The review was not removed from the associated place's `reviews` list
- This caused data inconsistency between the repository and the place object

**Example of the issue:**
```python
# Before deletion
place = facade.get_place(place_id)
print(place.reviews)  # [Review1, Review2, Review3]

# After deletion of Review2
facade.delete_review(review2_id)
place = facade.get_place(place_id)
print(place.reviews)  # [Review1, Review2, Review3]  ← Review2 still present!
```

**Solution applied in `app/services/facade.py`:**

```python
# BEFORE (incorrect - only deletes from repository)
def delete_review(self, review_id):
    # Check if review exists first
    if self.review_repo.get(review_id):
        self.review_repo.delete(review_id)
        return True
    return False

# AFTER (correct - also removes from place's review list)
def delete_review(self, review_id):
    # Check if review exists first
    review = self.review_repo.get(review_id)
    if review:
        # Remove the review from the place's reviews list
        place = review.place
        if review in place.reviews:
            place.reviews.remove(review)
            place.save()
        # Delete the review from the repository
        self.review_repo.delete(review_id)
        return True
    return False
```

**Key improvements:**
1. Retrieve the review object before deletion to access its associated place
2. Remove the review from the place's `reviews` list
3. Save the place to persist the change
4. Then delete the review from the repository

**Impact:**
- ✅ Review is completely removed from both the repository and the place's review list
- ✅ Data consistency maintained between repository and model relationships
- ✅ GET `/api/v1/places/<place_id>/reviews` correctly returns only existing reviews
- ✅ No breaking changes to the API interface
- ✅ Proper cleanup of bidirectional relationships

**Modified files:**
- `app/services/facade.py` (line ~142-152)

**Testing verification:**
```python
# After fix
place = facade.get_place(place_id)
print(place.reviews)  # [Review1, Review2, Review3]

facade.delete_review(review2_id)
place = facade.get_place(place_id)
print(place.reviews)  # [Review1, Review3]  ← Review2 correctly removed!
```

**Related operations verified:**
- ✅ Review creation adds review to place's list
- ✅ Review deletion removes review from place's list
- ✅ Review update does not affect place's list
- ✅ Place deletion maintains referential integrity

## Conclusion

### Strengths
- **100% of unit tests pass**
- **All Error 500 cases identified and fixed**
- **Data consistency maintained across all operations**
- Robust input data validation with type checking
- Appropriate HTTP status code handling
- Complete Swagger documentation
- Well-structured data models
- Comprehensive error handling for edge cases
- Proper management of bidirectional relationships (reviews ↔ places)

**Global Status: FUNCTIONAL, TESTED, AND HARDENED API**  
The API meets specifications and REST best practices with solid data validation and error handling. All potential Internal Server Errors have been identified and resolved with proper 400 Bad Request responses. Data integrity is maintained across all CRUD operations with proper relationship management.
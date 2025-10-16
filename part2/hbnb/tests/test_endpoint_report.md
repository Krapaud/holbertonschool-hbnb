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
- `test_create_amenity_empty_text` - Empty name validation ✅
- `test_create_amenity_whitespace_only_text` - Whitespace-only validation ✅
- `test_create_amenity_already_exist` - Duplicate amenity detection ✅
- `test_create_amenity_missing_name` - Missing required field ❌
- `test_create_amenity_name_too_long` - Name length validation ✅

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
- `test_create_amenity_missing_name` - Returns 500 instead of 400 ✅

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
- `test_create_amenity_already_exist` - Returns 201 instead of 400 ✅

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
- ✅ Endpoint works correctly in Postman
- ✅ Consistent and RESTful URL: `GET /api/v1/places/<place_id>/reviews`
- ✅ Proper validation with correct HTTP error codes (400, 404)
- ✅ Verification of place existence before retrieving reviews
- ✅ Returns empty list if the place has no reviews
- ✅ No breaking changes for other endpoints

**Modified files:**
- `app/services/facade.py`
- `app/api/v1/reviews.py`
- `app/api/v1/places.py`

## Conclusion

### Strengths
- **100% of unit tests pass**
- Robust input data validation
- Appropriate HTTP status code handling
- Complete Swagger documentation
- Well-structured data models

**Global Status: FUNCTIONAL AND TESTED API**  
The API meets specifications and REST best practices with solid data validation.
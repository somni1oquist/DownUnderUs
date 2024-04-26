from enum import Enum


class Topic(Enum):
    HOUSING = 'Housing'
    NEIGHBOURHOOD = 'Neighbourhood'
    FAMILY = 'Family'
    EVENTS = 'Events'
    SCHOOLS = 'Schools'
    PARKS = 'Parks'
    SAFETY = 'Safety'
    TRANSPORTATION = 'Transportation'
    LOCAL_BUSINESS = 'Local Business'
    ENVIRONMENT = 'Environment'
    HEALTH = 'Health'
    PETS = 'Pets'
    GARDENING = 'Gardening'
    UTILITIES = 'Utilities'
    RECYCLING = 'Recycling'

# Response status
class ResponseStatus(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'


# Reponse messages
class ResponseMessage(str, Enum):
    # Validation
    FORM_ERROR = 'Validation failed'
    # Post
    NOT_FOUND = 'Resource not found'
    UNAUTHORISED = 'Unauthorised'
    CREATED = 'Created successfully'
    EDITED = 'Edited successfully'
    DELETED = 'Deleted successfully'
    REPLY_ADDED = 'Reply added successfully'
    REPLY_ACCEPTED = 'Reply accepted successfully'
    REPLY_EDITED = 'Reply edited successfully'
    REPLY_DELETED = 'Reply deleted successfully'
    VOTED = 'Vote cast successfully'
    VOTE_UPDATED = 'Vote updated successfully'
    VOTE_REVOKED = 'Vote revoked successfully'
    # Topic select
    TOPIC_SELECTED = 'Topic selected successfully'
    TOPIC_RANGE = 'Please select at least 2 topics, but no more than 6.'
    # Sign-in and Sign-up
    INCORRECT_CREDENTIALS = 'Incorrect username or password'
    LOGIN_SUCCESS = 'Login successful'
    USERNAME_REQUIRED = 'Username is required'
    PASSWORD_REQUIRED = 'Password is required'
    EMAIL_REQUIRED = 'Email is required'
    SUBURB_REQUIRED = 'Suburb is required'
    EMAIL_EXISTS = 'An account with this email already exists'
    PASSWORD_MISMATCH = 'Passwords do not match'
    REGISTRATION_SUCCESSFUL = 'Registration successful'
    ACCOUNT_CREATION_FAILED = 'Account could not be created'
    # Profile
    PROFILE_UPDATED_SUCCESS = 'Profile updated successfully'
    PASSWORD_CHANGED_SUCCESS = 'Password changed successfully'
    INCORRECT_CURRENT_PASSWORD = 'Iincorrect current password'
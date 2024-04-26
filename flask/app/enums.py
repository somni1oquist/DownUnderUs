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

# not using now
class Title(Enum):
    #  Register
    NEWCOMER = 'Newcomer'

    #  Answer over 100 questions or posts
    COMMUNITY_PILLAR = 'Community Pillar'

    # Post more than 50 times under a specific topic
    TOPIC_EXPERT = 'Topic Expert'

    # Accumulate over 500 likes on your posts
    INFLUENCER = 'Influencer'


    #  Make over 20 posts during midnight hours
    NIGHT_OWL = 'Night Owl'

    # Help other users solve problems and get marked as the “Best Answer” more than 50 times
    HELPING_HAND = 'Helping Hand'

    # Post every topic at least once in each
    EXPLORER = 'Explorer'

    # Post lenth more than 1000 characters
    CHATTERBOX_KING = 'Chatterbox King'


# Response status
class ResponseStatus(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARN = 'warn'


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
    INCORRECT_CURRENT_PASSWORD = 'Incorrect current password'
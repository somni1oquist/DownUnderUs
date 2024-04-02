from enum import Enum


class Topic(Enum):
    TECHNOLOGY = 'Technology',
    HEALTH = 'Health',
    SCIENCE = 'Science',
    EDUCATION = 'Education',
    ENVIRONMENT = 'Environment',
    POLITICS = 'Politics',
    ECONOMICS = 'Economics',
    CULTURE = 'Culture',
    SPORTS = 'Sports',
    ENTERTAINMENT = 'Entertainment',
    BUSINESS = 'Business',
    TRAVEL = 'Travel',
    FASHION = 'Fashion',
    FOOD = 'Food',
    ART = 'Art'


# Reponse messages
class ResponseMessage(str, Enum):
    NOT_FOUND = 'Resource not found',
    UNAUTHORISED = 'Unauthorised',
    CREATED = 'Created successfully',
    EDITED = 'Edited successfully',
    DELETED = 'Deleted successfully',
    REPLY_ADDED = 'Reply added successfully',
    REPLY_ACCEPTED = 'Reply accepted successfully',
    REPLY_EDITED = 'Reply edited successfully',
    REPLY_DELETED = 'Reply deleted successfully',
    VOTED = 'Vote cast successfully',
    VOTE_UPDATED = 'Vote updated successfully',
    VOTE_REVOKED = 'Vote revoked successfully'
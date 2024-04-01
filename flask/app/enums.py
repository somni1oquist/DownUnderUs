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
class ResponseMessage(Enum):
    NOT_FOUND = {'message': 'Resource not found'}
    UNAUTHORISED = {'message': 'Unauthorised'}
    CREATED = {'message': 'Created successfully'}
    EDITED = {'message': 'Edited successfully'}
    DELETED = {'message': 'Deleted successfully'}
    REPLY_ADDED = {'message': 'Reply added successfully'}
    REPLY_ACCEPTED = {'message': 'Reply accepted successfully'}
    REPLY_EDITED = {'message': 'Reply edited successfully'}
    REPLY_DELETED = {'message': 'Reply deleted successfully'}
    VOTED = {'message': 'Vote cast successfully'}
    VOTE_UPDATED = {'message': 'Vote updated successfully'}
    VOTE_REVOKED = {'message': 'Vote revoked successfully'}
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


# Reponse messages
class ResponseMessage(str, Enum):
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
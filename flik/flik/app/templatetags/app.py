from django import template

register = template.Library()

@register.filter
def tweets_count(user, days):
    return user.tweets_count(days=days)

@register.filter
def retweet_count(user, days):
    return user.retweet_count(days=days)

@register.filter
def total_clicks(user, days):
    return user.total_clicks(days=days)

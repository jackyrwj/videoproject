from datetime import date, datetime
from django.utils.timezone import is_aware, utc

from django import template
register = template.Library()

@register.filter
def time_since(value, default="刚刚"):
    if not isinstance(value, date):  # datetime is a subclass of date
        return value
    now = datetime.now(utc if is_aware(value) else None)
    diff = now - value
    periods = (
        (diff.days / 365, "年"),
        (diff.days / 30, "个月"),
        (diff.days / 7, "周"),
        (diff.days, "天"),
        (diff.seconds / 3600, "小时"),
        (diff.seconds / 60, "分钟"),
        (diff.seconds, "秒"),
    )
    for period, singular in periods:
        if int(period) > 0:
            return "%d%s前" % (period, singular)
    return default

@register.simple_tag
def user_liked_class(video, user):
    liked = video.user_liked(user)
    if liked == 0:
        return "red"
    else:
        return "grey"

@register.simple_tag
def user_collected_class(video, user):
    collected = video.user_collected(user)
    if collected == 0:
        return "red"
    else:
        return "grey"

@register.simple_tag
def video_liker(video, user):
    count = video.count_likers(user)
    return count

@register.simple_tag
def get_ticket(video, user):
    count = video.count_likers(user)
    if count >= 20:
        return "inline"
    else:
        return "none"

@register.simple_tag
def user_coupon_class(video, user):
    coupon_get = video.is_get(user)
    if coupon_get == False:
       return "red"
    else:
        return "grey"

@register.simple_tag
def get_ticket_text(video, user):
    coupon_get = video.is_get(user)
    if coupon_get == False:
       return "(点击领取)"
    else:
        return "(已领取)"

# @register.simple_tag
# def message(video, user):
#     message = video.message(user)
#     return message
#
# @register.simple_tag
# def buy(video, user):
#     video.buy(user)

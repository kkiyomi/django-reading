from django import template
from django.utils import timezone
from datetime import timedelta
from itertools import zip_longest

register = template.Library()


def pairwise(iterable, n=2):
    a = iter(iterable)
    return zip_longest(*[a for i in range(n)], fillvalue=None)


@register.simple_tag
def get_prev_next(value, qset, cond):
    assert value in qset
    qset = list(qset[::-1])
    obj_index = qset.index(value)

    try:
        prev_ch = qset[obj_index - 1]
        if obj_index == 0:
            prev_ch = None
    except IndexError:
        prev_ch = None

    try:
        next_ch = qset[obj_index + 1]
    except IndexError:
        next_ch = None

    if cond == "prev_ch":
        return prev_ch
    if cond == "next_ch":
        return next_ch


@register.filter
def qst_mix(value):

    queryset_qu, queryset_v2 = value

    numbers_qu = [(int(item.number), item) for item in queryset_qu]
    numbers_v2 = [(int(item.number), item) for item in queryset_v2]

    dict_nb_qu = dict(numbers_qu)
    dict_nb_v2 = dict(numbers_v2)

    if len(queryset_v2) == 0:
        ch_nb_max, ch_nb_min = int(queryset_qu[0].number), int(
            queryset_qu[::-1][0].number
        )
    elif len(queryset_qu) == 0:
        ch_nb_max, ch_nb_min = int(queryset_v2[0].number), int(
            queryset_v2[::-1][0].number
        )
    else:
        ch_nb_max = max(int(queryset_qu[0].number), int(queryset_v2[0].number))
        ch_nb_min = min(
            int(queryset_qu[::-1][0].number), int(queryset_v2[::-1][0].number)
        )

    new_queryset = []
    for index, ch_nb in enumerate(range(ch_nb_min, ch_nb_max + 1)):
        if ch_nb in dict_nb_qu.keys():
            new_queryset.append(dict_nb_qu[ch_nb])
        elif ch_nb in dict_nb_v2.keys():
            new_queryset.append(dict_nb_v2[ch_nb])

    return new_queryset[::-1]


@register.filter
def ch_sliced(value):
    queryset = []
    for idx, val in enumerate(pairwise(value, n=100)):
        first = val[0]
        last = val[-1]
        if last is None:
            for i, v in enumerate(val):
                if v is None:
                    last = val[i - 1]
                    break
        queryset.append(((idx, first, last), val))

    return queryset


@register.filter
def chapters_ordereddesc(value):
    """Removes all values of arg from the given string"""
    return (
        value.chapter_set.all()
        .extra(select={"myinteger": "CAST(number AS INTEGER)"})
        .order_by("-myinteger")
    )


@register.filter
def get_chapters(value, novel_title):
    queryset = value.filter(novel__title=novel_title)
    return queryset


@register.filter
def get_chapters_from_id(value, novel_id):
    queryset = value.filter(novel=novel_id)
    return queryset


@register.filter
def ordereddesc(value):
    """Removes all values of arg from the given string"""
    return (
        value.all()
        .extra(select={"myinteger": "CAST(number AS INTEGER)"})
        .order_by("-myinteger")
    )


@register.filter
def shorten_naturaltime(value):
    if "," in value:
        naturaltime = value.split(",")[0]
        return f"{naturaltime} ago"
    else:
        return value


@register.filter
def time_difference(value, hours):
    test = timezone.now() - value
    test = str(test - timedelta(hours=int(hours)))
    if "-" in test:
        return True
    else:
        return False

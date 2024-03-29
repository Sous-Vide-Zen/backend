from django_filters import rest_framework as filters


class FeedFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="author", lookup_expr="username")
    filter = filters.CharFilter(method="filter_by_subscription", label="filter")

    def filter_by_subscription(self, queryset, name, value):
        if value == "subscriptions":
            user = self.request.user
            users_subscribed_to = user.follower.all().values_list(
                "author_id", flat=True
            )
            return queryset.filter(author__in=users_subscribed_to)
        return queryset

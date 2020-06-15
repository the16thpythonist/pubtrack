from django.shortcuts import get_object_or_404


class ThroughModelLookupMixin(object):
    """
    This is a mixin for a detail REST API view for models, which are essentially the "through" model for a many to many
    relationship

    Let me elaborate:
    A many to many relationship between two models is essentially implemented by creating another table, whose rows
    simply contain the two respective primary keys of the models to be connected. An example could be the "Person"
    model. Two persons can be connected by the additional "Friendship" model, which would just contain the names of the
    two people in a friendship.
    In django these "connection models" or "through models" are usually hidden. Which means that django will create
    them in the background, but they will not be explicitly queryable. For a REST Api it is good practice to make these
    through models explicit and also expose them to the outside. Many to many connected objects can than be added
    by first posting both of these objects and then posting their connection, as a separate object.

    Now this creates the problem, that you would have to expose a URL with two primary keys in it like
    "api/friendships/:person1_id/:person2_id". The default API view for django REST only offers the "lookup_field"
    parameter however, which only addresses one of these.

    This is where this mixin comes in. It modifies the behaviour of an APIView in such a way that both these
    keys can be specified in the "lookup_fields" structure and then the correct "through" object is automatically
    found by the queryset...
    """

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = get_object_or_404(queryset)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        # Here we essentially construct the "filter" dict so that it can be used as the keyword arguments for the
        # "filter" function of a django queryset. The filters it will contain will specify as many additional
        # constraints as defined in "lookup_fields"
        filters = {}
        for detail in self.lookup_fields:
            filter_string = '{}__{}__exact'.format(
                detail['related_name'],
                detail['related_field']
            )

            value = self.kwargs[detail['kwarg']]
            filters[filter_string] = value

        return self.queryset.filter(**filters)


class NestedFieldLookupMixin(object):

    def get_queryset(self):
        filter_string = '{related}__{field}__exact'.format(
            related=self.nested_parent_name,
            field=self.nested_parent_field
        )
        filters = {filter_string:  self.kwargs[self.nested_lookup_field]}
        return self.queryset.filter(**filters)

    def get_parent_instance(self):
        filter_string = '{field}__exact'.format(
            field=self.nested_parent_field
        )
        filters = {filter_string: self.kwargs[self.nested_lookup_field]}
        queryset = self.nested_parent_class.objects.filter(**filters)
        return queryset.first()


class MultipleFieldLookupMixin(object):

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filters = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:
                filters[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filters)
        self.check_object_permissions(self.request, obj)
        return obj

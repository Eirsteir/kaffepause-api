import graphene


class AccountNode(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)
        name = "Account"

    uuid = graphene.UUID()
    email = graphene.String()
    archived = graphene.Boolean()
    verified = graphene.Boolean()
    secondary_email = graphene.String()

    def resolve_uuid(parent, info):
        return parent.id

    def resolve_archived(parent, info):
        return parent.status.archived

    def resolve_verified(parent, info):
        return parent.status.verified

    def resolve_secondary_email(parent, info):
        return parent.status.secondary_email

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related("status")

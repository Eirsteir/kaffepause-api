import graphene

from kaffepause.statusupdates.mutations import UpdateStatus


class Mutation(graphene.ObjectType):
    update_status = UpdateStatus.Field()

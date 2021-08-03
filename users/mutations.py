import graphene

from .schema import User
from .models import CustomUser


class Register(graphene.Mutation):
    Output = User

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.avatar = user.gravatar_url()
        user.save()

        return user


class Mutation(graphene.ObjectType):
    register = Register.Field()

from user.models import User


class UserRepository:
    @staticmethod
    def get_username_by_pk(pk: int) -> str:
        return User.objects.filter(pk=pk).values_list('username', flat=True).first()

    @staticmethod
    def get_user_by_username(username: str) -> User:
        return User.objects.filter(username=username).first()

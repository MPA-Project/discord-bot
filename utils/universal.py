def roles_in(user_roles, roles) -> bool:
    if roles in [y.id for y in user_roles]:
        return True
    return False

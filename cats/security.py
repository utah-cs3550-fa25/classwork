
def user_is_staff(user):
    return user.groups.filter(name="Staff").exists()

def can_donate_cat(user):
    return user_is_staff(user)

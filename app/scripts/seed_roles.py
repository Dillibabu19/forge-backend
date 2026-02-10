# from app.db.session import SessionLocal
# from app.models import Roles, RoleType

# db = SessionLocal()

# roles_data = [
#     Roles(name=RoleType.ADMIN),
#     Roles(name=RoleType.USER),
#     Roles(name=RoleType.MANAGER),
# ]

# # add_all accepts a list of objects
# db.add_all(roles_data)
# db.commit()

# db.close()

# from app.db.deps import get_db
# from app.models.roles import Roles, RoleType  # Update with your actual file path

# def create_initial_roles():
#     db_gen = get_db()
#     db = next(db_gen)
#     try:
#         # Create role instances
#         admin_role = Roles(name=RoleType.ADMIN)
#         user_role = Roles(name=RoleType.USER)
#         guest_role = Roles(name=RoleType.GUEST)

#         # Add to session and commit
#         db.add_all([admin_role, user_role, guest_role])
#         db.commit()
#         print("Roles created successfully!")
#     except Exception as e:
#         print(f"Error creating roles: {e}")
#         db.rollback()
#     finally:
#         db.close()

# if __name__ == "__main__":
#     create_initial_roles()
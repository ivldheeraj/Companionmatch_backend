from models.user_models import UserRegisterModel, UserLoginModel
from repositories.implementations.address_repository import AddressRepository
from repositories.implementations.user_repository import UserRepository
from repositories.implementations.student_repository import StudentRepository

class AuthService:
    def __init__(self):
        self.address_repo = AddressRepository()
        self.user_repo = UserRepository()
        self.student_repo = StudentRepository()

    def register_student(self, model: UserRegisterModel):
        address_id = self.address_repo.insert_address(model.address)
        model.address.address_id = address_id

        user_id = self.user_repo.insert_user(model, "student")
        model.user_id = user_id

        self.student_repo.insert_student(user_id, model.student_bio)

        return {"message": "Student account created successfully", "user_id": user_id}

    def authenticate_user(self, model: UserLoginModel):
        user = self.user_repo.get_user_by_email(model.email)
        if not user or user["Password"] != model.password:
            raise Exception("Invalid email or password.")
        return {
            "message": "Login successful",
            "user_type": user["UserType"],
            "user_id": user["UserID"]
        }

from repositories.implementations.questionnaire_repository import QuestionnaireRepository

class QuestionnaireService:
    def __init__(self):
        self.repository = QuestionnaireRepository()

    def get_all_questionnaires(self):
        try:
            return self.repository.fetch_all_questionnaires()
        except Exception as e:
            raise Exception(f"Service Error: {e}")

    def get_questionnaire_list(self):
        try:
            return self.repository.fetch_questionnaire_list()
        except Exception as e:
            raise Exception(f"Service Error: {e}")

    def get_questionnaire_by_id(self, questionnaire_id):
        try:
            return self.repository.fetch_questionnaire_by_id(questionnaire_id)
        except Exception as e:
            raise Exception(f"Service Error: {e}")
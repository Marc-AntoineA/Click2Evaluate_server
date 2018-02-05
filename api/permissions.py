from rest_framework import permissions

class IsAnswerFromStudent(permissions.BasePermission):
    """
    Custom permission for the request "Get or write an answer"
    (only the corresponding student is allow)
    """

    def has_object_permission(self, request, view, qwa):
        # qwa is a QuestionWithAnswer objects
        print(qwa, request)
        print('hello')
        return request.user == qwa.survey.student.user

class IsCourseFromStudent(permissions.BasePermission):
    """
    Custom permission for the request "Get all courses for henri.becquerel@enpc.fr"
    (only the corresponding student is allow)
    """

    def has_object_permission(self, request, view, survey):
        print("hello")
        print(survey)
        return False
        return request.user == survey.student.user

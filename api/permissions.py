from rest_framework import permissions

class IsAnswerFromStudent(permissions.BasePermission):
    """
    Custom permission for the request "Get or write an answer"
    (only the corresponding student is allowed)
    """

    def has_object_permission(self, request, view, qwa):
        # qwa is a QuestionWithAnswer objectsTrue
        return request.user == qwa.survey.student.user

class AreCoursesFromStudent(permissions.BasePermission):
    """
    Custom permission for the request "Get all courses for henri.becquerel@enpc.fr"
    (only the corresponding student is allowed)
    """

    def has_object_permission(self, request, view, surveys):
        print("hello")
        for s in surveys:
            if request.user != s.student.user:
                return False
        return True

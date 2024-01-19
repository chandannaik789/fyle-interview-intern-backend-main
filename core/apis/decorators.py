import json
from flask import request
from core.libs import assertions
from functools import wraps


class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        if request.path.startswith('/student'):
            assertions.assert_true(p.student_id is not None, 'requester should be a student')
        elif request.path.startswith('/teacher'):
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')
        elif request.path.startswith('/principal'):
            assertions.assert_true(p.principal_id is not None, 'requester should be a principal')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper

    def test_grade_assignment_success(self):
        # Create a test assignment
        # Assuming you have a function to create assignments in your app
        assignment_id = create_test_assignment()

        # Mock the principal headers
        headers = {"X-Principal": '{"user_id":3, "teacher_id":1}'}

        # Send a request to grade the assignment
        response = self.client.post(
            f'/teacher/assignments/grade',
            json={"id": assignment_id, "grade": "A"},
            headers=headers
        )

        # Check if the response is successful and contains the graded assignment
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["grade"], "A")
        self.assertEqual(response.json["data"]["state"], "GRADED")

    def test_grade_assignment_invalid_assignment(self):
        # Mock the principal headers
        headers = {"X-Principal": '{"user_id":3, "teacher_id":1}'}

        # Send a request to grade an invalid assignment
        response = self.client.post(
            '/teacher/assignments/grade',
            json={"id": 999, "grade": "A"},
            headers=headers
        )

        # Check if the response indicates failure due to an invalid assignment
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid assignment ID", response.json["error"])


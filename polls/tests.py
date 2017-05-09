from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from .models import Question, Choice

# Create your tests here.


class QuestionModelsTest(TestCase):
    def test_was_published_recently(self):
        q1 = Question(question_text='test 1', pub_date=timezone.now() + timedelta(hours=1))
        q2 = Question(question_text='test 2', pub_date=timezone.now() + timedelta(hours=-1))
        q3 = Question(question_text='test 3', pub_date=timezone.now() + timedelta(days=1))
        q4 = Question(question_text='test 4', pub_date=timezone.now() + timedelta(hours=-23))

        self.assertIs(q1.was_published_recently(), False)
        self.assertIs(q2.was_published_recently(), True)
        self.assertIs(q3.was_published_recently(), False)
        self.assertIs(q4.was_published_recently(), True)


class QuestionViewTest(TestCase):
    def test_index_view_empty(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_index_view_with_past_question(self):
        q1 = Question(question_text='test 1', pub_date=timezone.now() + timedelta(days=-3))
        q1.save()

        response = self.client.get(reverse('polls:index'))
        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context['questions'], ['<Question: test 1>'])

    def test_index_view_with_future_question(self):
        q1 = Question(question_text='test 1', pub_date=timezone.now() + timedelta(days=3))
        q1.save()

        response = self.client.get(reverse('polls:index'))
        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_detail_view_with_future_question(self):
        q1 = Question(question_text='test 1', pub_date=timezone.now() + timedelta(days=10))
        q1.save()

        response = self.client.get(reverse('polls:detail', kwargs={'question_id': q1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_question(self):
        q1 = Question(question_text='test 1', pub_date=timezone.now() - timedelta(days=10))
        q1.save()

        response = self.client.get(reverse('polls:detail', args=[q1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, q1)

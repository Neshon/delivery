from django.test import TestCase

from apps.users.models import User
from apps.customer.models import Customer
from apps.delivery.models import Category, Job


class DeliveryModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.customer = Customer.objects.create(user=self.user)
        self.category = Category.objects.create(name='House item')
        self.job = Job.objects.create(name='New job',
                                      customer=self.customer,
                                      category=self.category
                                      )

    def test_job(self):
        name = 'New job'
        qs = Job.objects.filter(name=name)
        self.assertEqual(self.category, self.job.category)
        self.assertTrue(qs.exists())

    def test_valid_name(self):
        name = 'House item'
        qs = Category.objects.filter(name=name)
        self.assertTrue(qs.exists())

    def test_valid_slug(self):
        slug = 'house-item'
        self.assertEqual(slug, self.category.slug)

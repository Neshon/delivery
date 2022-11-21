import random

from django.db.models import Avg
from django.test import TestCase

from apps.users.models import User
from apps.customer.models import Customer
from apps.ratings.models import Rating, RatingChoices
from apps.delivery.models import Courier, Job


class RatingTestCase(TestCase):
    def create_customer(self):
        items_users = []
        items_customer = []
        self.customer_count = random.randint(10, 100)
        for i in range(0, self.customer_count):
            user = User(username=f'customer_{i}')
            items_users.append(user)
            items_customer.append(Customer(user=user))
        User.objects.bulk_create(items_users)
        Customer.objects.bulk_create(items_customer)
        self.users_customer = User.objects.all()
        self.customer = Customer.objects.all()

    def create_courier(self):
        items_users = []
        items_courier = []
        self.courier_count = random.randint(10, 100)
        for i in range(0, self.courier_count):
            user = User(username=f'courier_{i}')
            items_users.append(user)
            items_courier.append(Courier(user=user))
        User.objects.bulk_create(items_users)
        Courier.objects.bulk_create(items_courier)
        self.users_courier = User.objects.all()
        self.courier = Courier.objects.all()

    def create_job(self):
        items_job = []
        self.job_count = random.randint(10, 100)
        for i in range(0, self.job_count):
            customer = Customer.objects.order_by('?').first()
            courier = Courier.objects.order_by('?').first()
            job = Job(name=f'job_{i}', customer=customer, courier=courier)
            items_job.append(job)
        Job.objects.bulk_create(items_job)
        self.jobs = Job.objects.all()

    def create_rating(self):
        items_rating = []
        self.rating_totals = []
        self.rating_count = 100
        for i in range(0, self.rating_count):
            job_obj = self.jobs.order_by('?').first()
            rating_value = random.choices(RatingChoices.choices)[0][0]
            self.rating_totals.append(rating_value)
            items_rating.append(
                Rating(
                    user=job_obj.customer.user,
                    content_object_user=job_obj.courier.user,
                    content_object_job=job_obj,
                    value=rating_value
                )
            )
        Rating.objects.bulk_create(items_rating)
        self.ratings = Rating.objects.all()

    def setUp(self):
        self.create_customer()
        self.create_courier()
        self.create_job()
        self.create_rating()

    def test_customer_count(self):
        qs = Customer.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.customer_count)
        self.assertEqual(self.customer.count(), self.customer_count)

    def test_courier_count(self):
        qs = Courier.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.courier_count)
        self.assertEqual(self.courier.count(), self.courier_count)

    def test_rating_count(self):
        qs = Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.rating_count)
        self.assertEqual(self.ratings.count(), self.rating_count)

    def test_rating_random_choices(self):
        value_set = set(Rating.objects.values_list('value', flat=True))
        self.assertTrue(len(value_set) > 1)

    def test_rating_agg(self):
        db_avg = Rating.objects.aggregate(average=Avg('value'))['average']
        self.assertIsNotNone(db_avg)
        self.assertTrue(db_avg > 0)
        total_sum = sum(self.rating_totals)
        test_avg = total_sum / self.rating_count
        print(test_avg, db_avg)
        self.assertEqual(test_avg, db_avg)

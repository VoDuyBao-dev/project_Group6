from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from app1.models import Court, BadmintonHall, TimeSlotTemplate, Slot
from django.core.files.uploadedfile import SimpleUploadedFile

class ThemSanViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('them_san')
        # tạo một chi nhánh để thêm sân
        self.badminton_hall = BadmintonHall.objects.create(badminton_hall_id='123', name='Hall 1')
        self.time_slot = TimeSlotTemplate.objects.create(name='Morning Slot')
        self.image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/them_san.html')

    def test_post_request_missing_fields(self):
        response = self.client.post(self.url, {})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Vui lòng nhập đầy đủ thông tin!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

    def test_post_request_duplicate_court(self):
        Court.objects.create(name="Court 1", badminton_hall=self.badminton_hall, status="Active")
        response = self.client.post(self.url, {
            'address': '123',
            'name': 'Court 1',
            'status': 'Active',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Sân này đã tồn tại!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

    def test_successful_court_creation(self):
        response = self.client.post(self.url, {
            'address': '123',
            'name': 'Court 2',
            'status': 'Active',
        }, files={'image': self.image})
        
        self.assertEqual(Court.objects.count(), 1)
        court = Court.objects.get(name='Court 2')
        self.assertEqual(court.badminton_hall, self.badminton_hall)
        self.assertEqual(court.status, 'Active')
        
        self.assertEqual(Slot.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Thêm sân mới thành công!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

    def test_successful_court_creation_with_multiple_time_slots(self):
        TimeSlotTemplate.objects.create(name="Afternoon Slot")
        TimeSlotTemplate.objects.create(name="Evening Slot")
        response = self.client.post(self.url, {
            'address': '123',
            'name': 'Court 3',
            'status': 'Active',
        }, files={'image': self.image})
        self.assertEqual(Court.objects.count(), 1)
        court = Court.objects.get(name='Court 3')
        self.assertEqual(court.badminton_hall, self.badminton_hall)
        self.assertEqual(court.status, 'Active')
        self.assertEqual(Slot.objects.filter(court=court).count(), 3)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Thêm sân mới thành công!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

    def test_court_creation_without_timeslot_templates(self):
        TimeSlotTemplate.objects.all().delete()
        response = self.client.post(self.url, {
            'address': '123',
            'name': 'Court 4',
            'status': 'Active',
        }, files={'image': self.image})
        self.assertEqual(Court.objects.count(), 1)
        court = Court.objects.get(name='Court 4')
        self.assertEqual(Slot.objects.filter(court=court).count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Thêm sân mới thành công!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

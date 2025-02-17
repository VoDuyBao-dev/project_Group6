from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from app1.models import Court, BadmintonHall, TimeSlotTemplate, Slot
from django.core.files.uploadedfile import SimpleUploadedFile

class ThemSanMoiViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('them_san_moi')

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/them_san_moi.html')

    def test_post_request_missing_fields(self):
        response = self.client.post(self.url, {})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Vui lòng nhập đầy đủ thông tin!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

    def test_post_request_duplicate_address(self):
        BadmintonHall.objects.create(name="Hall 1", address="123 Main St")
        response = self.client.post(self.url, {
            'name': 'Hall 2',
            'address': '123 Main St',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Địa điểm này đã có chi nhánh khác!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)

    def test_successful_badminton_hall_creation(self):
        response = self.client.post(self.url, {
            'name': 'New Hall',
            'address': '456 Another St',
        })
        self.assertEqual(BadmintonHall.objects.count(), 1)
        hall = BadmintonHall.objects.get(name='New Hall')
        self.assertEqual(hall.address, '456 Another St')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Thêm sân mới thành công!" in str(msg) for msg in messages))
        self.assertEqual(response.status_code, 302)


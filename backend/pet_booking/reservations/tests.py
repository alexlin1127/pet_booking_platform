import uuid
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from unittest.mock import patch, MagicMock

from .models import GroomingSchedules
from .views import ReservationCustomerViewSet
from .serializers import ReservationGroomingSerializer, ReservationBoardingSerializer
from customers.models import CustomersProfile
from services.models import GroomingService, GroomingServicePricing
from stores.models import Store


class ReservationCustomerViewSetTestCase(APITestCase):
    
    def setUp(self):
        """測試前的準備工作"""
        # 創建測試用戶
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 創建認證 token
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # 創建測試店家
        self.store = Store.objects.create(
            store_name='Test Pet Store',
            address='Test Address',
            phone='1234567890'
        )
        
        # 創建測試客戶資料
        self.customer_profile = CustomersProfile.objects.create(
            user_id=self.user.id,
            full_name='Test Customer',
            phone='0987654321'
        )
        
        # 創建測試美容服務
        self.grooming_service = GroomingService.objects.create(
            store_id=self.store,
            service_title='洗澡',
            introduction='基本洗澡服務',
            notice='請準時到達'
        )
        
        # 創建測試美容服務定價
        self.grooming_pricing = GroomingServicePricing.objects.create(
            grooming_service_id=self.grooming_service,
            fur_amount='short',
            pet_size='medium',
            grooming_duration=60
        )
        
        # 測試資料
        self.valid_grooming_data = {
            'store_name': 'Test Pet Store',
            'pet_name': 'Buddy',
            'pet_type': 'dog',
            'pet_breed': 'Golden Retriever',
            'pick_up_service': False,
            'reservation_time': '10:00',
            'customer_note': 'Please be gentle',
            'grooming_services_name': ['洗澡'],
            'fur_amount': 'short',
            'pet_size': 'medium'
        }
        
        self.url = reverse('reservation-list')  # 假設你有設定 URL name

    def test_create_grooming_reservation_success(self):
        """測試成功創建美容預約"""
        url = f"{self.url}?role=customer&user_id={self.user.id}&service_type=grooming&store_id={self.store.id}"
        
        response = self.client.post(url, self.valid_grooming_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('reservation_id', response.data)
        self.assertEqual(response.data['store_name'], 'Test Pet Store')
        self.assertEqual(response.data['user_name'], 'Test Customer')

    def test_create_reservation_invalid_role(self):
        """測試無效角色"""
        url = f"{self.url}?role=invalid&user_id={self.user.id}&service_type=grooming&store_id={self.store.id}"
        
        response = self.client.post(url, self.valid_grooming_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid role', response.data['error'])

    def test_create_reservation_missing_user_id(self):
        """測試缺少 user_id"""
        url = f"{self.url}?role=customer&service_type=grooming&store_id={self.store.id}"
        
        response = self.client.post(url, self.valid_grooming_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_id parameter is required', response.data['error'])

    def test_create_reservation_missing_store_id(self):
        """測試缺少 store_id"""
        url = f"{self.url}?role=customer&user_id={self.user.id}&service_type=grooming"
        
        response = self.client.post(url, self.valid_grooming_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('store_id parameter is required', response.data['error'])

    def test_create_reservation_invalid_service_type(self):
        """測試無效服務類型"""
        url = f"{self.url}?role=customer&user_id={self.user.id}&service_type=invalid&store_id={self.store.id}"
        
        response = self.client.post(url, self.valid_grooming_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service_type parameter is required', response.data['error'])

    def test_create_reservation_user_not_found(self):
        """測試用戶不存在"""
        url = f"{self.url}?role=customer&user_id=999999&service_type=grooming&store_id={self.store.id}"
        
        response = self.client.post(url, self.valid_grooming_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User not found', response.data['error'])

    def test_create_reservation_missing_service_names(self):
        """測試缺少服務名稱"""
        data = self.valid_grooming_data.copy()
        data['grooming_services_name'] = []
        
        url = f"{self.url}?role=customer&user_id={self.user.id}&service_type=grooming&store_id={self.store.id}"
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service_name is required', response.data['error'])

    def test_generate_reservation_id_grooming(self):
        """測試生成美容預約ID"""
        viewset = ReservationCustomerViewSet()
        reservation_id = viewset.generate_reservation_id('grooming')
        
        self.assertTrue(reservation_id.startswith('GRM'))
        self.assertEqual(len(reservation_id), 21)  # GRM + 14位時間戳 + 4位UUID

    def test_generate_reservation_id_boarding(self):
        """測試生成寄宿預約ID"""
        viewset = ReservationCustomerViewSet()
        reservation_id = viewset.generate_reservation_id('boarding')
        
        self.assertTrue(reservation_id.startswith('BRD'))
        self.assertEqual(len(reservation_id), 21)  # BRD + 14位時間戳 + 4位UUID

    def test_generate_reservation_id_invalid_service(self):
        """測試無效服務類型生成預約ID"""
        viewset = ReservationCustomerViewSet()
        
        with self.assertRaises(ValueError):
            viewset.generate_reservation_id('invalid')

    def test_generate_time_duration_valid_time(self):
        """測試生成時間段 - 有效時間"""
        viewset = ReservationCustomerViewSet()
        duration_list = [60, 30]  # 總計90分鐘
        
        time_slots = viewset.generate_time_duration('10:00', duration_list)
        
        expected_slots = ['10:00', '10:15', '10:30', '10:45', '11:00', '11:15']
        self.assertEqual(time_slots, expected_slots)

    def test_generate_time_duration_invalid_time_format(self):
        """測試生成時間段 - 無效時間格式"""
        viewset = ReservationCustomerViewSet()
        duration_list = [60]
        
        result = viewset.generate_time_duration('25:00', duration_list)
        
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_time_duration_missing_time(self):
        """測試生成時間段 - 缺少時間"""
        viewset = ReservationCustomerViewSet()
        duration_list = [60]
        
        result = viewset.generate_time_duration(None, duration_list)
        
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('reservations.models.GroomingSchedules.objects.bulk_create')
    def test_create_grooming_schedule_success(self, mock_bulk_create):
        """測試創建美容時間表 - 成功"""
        viewset = ReservationCustomerViewSet()
        reservation = MagicMock()
        reservation.id = 1
        time_slots = ['10:00', '10:15', '10:30']
        
        viewset.create_grooming_schedule(reservation, time_slots)
        
        mock_bulk_create.assert_called_once()
        args = mock_bulk_create.call_args[0][0]
        self.assertEqual(len(args), 3)

    def test_create_grooming_schedule_exception(self):
        """測試創建美容時間表 - 異常處理"""
        viewset = ReservationCustomerViewSet()
        reservation = None  # 故意傳入None引發異常
        time_slots = ['10:00']
        
        with self.assertRaises(Exception):
            viewset.create_grooming_schedule(reservation, time_slots)

    def test_get_serializer_class_grooming(self):
        """測試獲取序列化器類別 - 美容"""
        viewset = ReservationCustomerViewSet()
        request = MagicMock()
        request.query_params.get.return_value = 'grooming'
        viewset.request = request
        
        serializer_class = viewset.get_serializer_class()
        
        self.assertEqual(serializer_class, ReservationGroomingSerializer)

    def test_get_serializer_class_boarding(self):
        """測試獲取序列化器類別 - 寄宿"""
        viewset = ReservationCustomerViewSet()
        request = MagicMock()
        request.query_params.get.return_value = 'boarding'
        viewset.request = request
        
        serializer_class = viewset.get_serializer_class()
        
        self.assertEqual(serializer_class, ReservationBoardingSerializer)

    def test_get_serializer_class_default(self):
        """測試獲取序列化器類別 - 預設"""
        viewset = ReservationCustomerViewSet()
        request = MagicMock()
        request.query_params.get.return_value = None
        viewset.request = request
        
        serializer_class = viewset.get_serializer_class()
        
        self.assertEqual(serializer_class, ReservationGroomingSerializer)

    def tearDown(self):
        """測試後清理"""
        User.objects.all().delete()
        Store.objects.all().delete()
        CustomersProfile.objects.all().delete()
        GroomingService.objects.all().delete()
        GroomingServicePricing.objects.all().delete()
        GroomingSchedules.objects.all().delete()


class ReservationIntegrationTestCase(APITestCase):
    """整合測試"""
    
    def setUp(self):
        """設置整合測試環境"""
        self.user = User.objects.create_user(
            username='integrationuser',
            email='integration@example.com',
            password='testpass123'
        )
        
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.store = Store.objects.create(
            store_name='Integration Test Store',
            address='Integration Address',
            phone='1234567890'
        )
        
        self.customer_profile = CustomersProfile.objects.create(
            user_id=self.user.id,
            full_name='Integration Customer',
            phone='0987654321'
        )
        
        self.grooming_service = GroomingService.objects.create(
            store_id=self.store,
            service_title='完整美容',
            introduction='完整美容服務',
            notice='請準時到達'
        )
        
        self.grooming_pricing = GroomingServicePricing.objects.create(
            grooming_service_id=self.grooming_service,
            fur_amount='long',
            pet_size='large',
            grooming_duration=120
        )

    def test_full_grooming_reservation_flow(self):
        """測試完整美容預約流程"""
        url = f"/api/reservations/?role=customer&user_id={self.user.id}&service_type=grooming&store_id={self.store.id}"
        
        data = {
            'store_name': 'Integration Test Store',
            'pet_name': 'Max',
            'pet_type': 'dog',
            'pet_breed': 'Husky',
            'pick_up_service': True,
            'reservation_time': '14:00',
            'customer_note': 'Very fluffy dog',
            'grooming_services_name': ['完整美容'],
            'fur_amount': 'long',
            'pet_size': 'large'
        }
        
        response = self.client.post(url, data, format='json')
        
        # 驗證預約創建成功
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 驗證時間表記錄被創建
        schedules = GroomingSchedules.objects.all()
        self.assertTrue(schedules.exists())
        
        # 驗證時間段數量正確 (120分鐘 = 8個15分鐘段)
        expected_count = 8
        self.assertEqual(schedules.count(), expected_count)
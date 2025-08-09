# origin
import uuid
from datetime import datetime, timedelta
import re

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# app
from .models import GroomingSchedules
from services.models import GroomingService, GroomingServicePricing
from .serializers import ReservationBoardingSerializer, ReservationGroomingSerializer
from customers.models import CustomersProfile


class ReservationCustomerViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        service_type = self.request.query_params.get('service_type')
        if service_type == 'grooming':
            return ReservationGroomingSerializer
        elif service_type == 'boarding':
            return ReservationBoardingSerializer
        return ReservationGroomingSerializer
    
   
    
    def create(self, request, *args, **kwargs):
        """
        處理customer預約請求
        URL參數：role=customer, user_id, service_type
        """
        role = request.query_params.get('role')

        # 驗證 URL 參數
        if role == 'customer':
            user_id = request.query_params.get('user_id')
            service_type = request.query_params.get('service_type')
            store_id = request.query_params.get('store_id')
        else:
            return Response(
                {'error': 'Invalid role. Must be "customer"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not store_id:
            return Response(
                {'error': 'store_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if service_type not in ['grooming', 'boarding']:
            return Response(
                {'error': 'service_type parameter is required and must be "grooming" or "boarding"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = CustomersProfile.objects.filter(user_id=user_id).values('full_name', 'phone').first()

        if not user:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user_name = user['full_name']
        user_phone = user['phone']
        form_data = request.data
        reservation_id = self.generate_reservation_id(service_type)
        
        reservation_data = {
            'reservation_id': reservation_id,
            'store_name': form_data.get('store_name'),
            'user_name': user_name,
            'user_phone': user_phone,
            'pet_name': form_data.get('pet_name'),
            'pet_type': form_data.get('pet_type'),
            'pet_breed': form_data.get('pet_breed'),
            'pick_up_service': form_data.get('pick_up_service', False),
            'reservation_time': form_data.get('reservation_time'),
            'customer_note': form_data.get('customer_note', ''),
            'status': 'pending'
        }
        
        if service_type == 'grooming':
            reservation_data['grooming_services_name'] = form_data.get('grooming_services_name', [])
            serializer = ReservationGroomingSerializer(data=reservation_data)

            if serializer.is_valid():
                reservation = serializer.save()

            duration_list = []
            service_names = reservation_data['grooming_services_name']
            
            if service_names:
                grooming_services = GroomingService.objects.filter(
                    store_id=store_id,
                    service_title__in=service_names
                )
                
                for service in grooming_services:
                    grooming_durations = GroomingServicePricing.objects.filter(
                        grooming_service_id=service.id,
                        fur_amount=form_data.get('fur_amount'),
                        pet_size=form_data.get('pet_size')
                    ).values_list('grooming_duration', flat=True)
                    
                    duration_list.extend(list(grooming_durations))
                
                
                try:
                    # 取得特定店家被預約的美容服務時段
                    time_slots = self.generate_time_duration(form_data.get('reservation_time'), duration_list)
                    
                    # 批量存入GroomingSchedule table
                    self.create_grooming_schedule(reservation, time_slots)
                    
                    return Response(reservation_data, status=status.HTTP_201_CREATED)
                    
                except ValidationError as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'error': 'service_name is required'}, status=status.HTTP_400_BAD_REQUEST)         
        
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    

    def create_grooming_schedule(self, reservation_data, time_slots):
        """創建美容時間表記錄"""
        try:
            today_date = datetime.today().date()
            schedule_records = []
            reservation_id = reservation_data['reservation_id']
            
            for time_slot in time_slots:
                time_obj = datetime.strptime(time_slot, '%H:%M').time()
                
                schedule_data = {
                    'reservation_grooming_id': reservation_id,
                    'date': today_date,
                    'unavailable_time': time_obj
                }
                
                schedule_records.append(GroomingSchedules(**schedule_data))
                            
            GroomingSchedules.objects.bulk_create(schedule_records)
            
        except Exception as e:
            print(f"Failed to create grooming schedules: {e}")
            raise ValidationError(f"Failed to create grooming schedules: {e}")

    def generate_reservation_id(self, service_type):
        """生成預約ID"""
        if service_type == 'grooming':
            prefix = 'GRM'
        elif service_type == 'boarding':
            prefix = 'BRD'
        else:
            raise ValueError(f'Invalid service_type: {service_type}. Must be "grooming" or "boarding"')
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_suffix = str(uuid.uuid4())[:4].upper()
        return f"{prefix}{timestamp}{unique_suffix}"
    
    def generate_time_duration(self, reservation_time_str, duration_list):
        total_spend_time = 0
        for time in duration_list:
            total_spend_time += int(time)
        
        total_count = round(total_spend_time / 15 - 1, 0)

        time_slots = []
        # 驗證時間格式 (HH:MM)
        if reservation_time_str:
            time_pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
            if re.match(time_pattern, reservation_time_str):
                try:
                    start_time = datetime.strptime(reservation_time_str, '%H:%M').time()
                    current_datetime = datetime.combine(datetime.today(), start_time)
                    
                    for i in range(int(total_count) + 1):  # +1 包含起始時間
                        time_slot = current_datetime.strftime('%H:%M')
                        time_slots.append(time_slot)
                        current_datetime += timedelta(minutes=15)
                        
                    return time_slots
                
                except ValueError:
                    return Response(
                        {'error': 'Invalid time format. Expected HH:MM'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Invalid time format. Expected HH:MM (e.g., 10:00)'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'reservation_time is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
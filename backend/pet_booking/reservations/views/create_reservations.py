# origin
from datetime import datetime, timedelta, date, time
from typing import Dict, List, Optional, Tuple
import math

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import QuerySet

# app
from ..models import GroomingSchedules, BoardingSchedules, ReservationBoarding
from pet_booking.services.models import GroomingService, GroomingServicePricing, BoardingService, BoardingServicePricing
from pet_booking.stores.models import Store
from pet_booking.coupon.models import Coupon, CouponStatus
from ..serializers import ReservationGroomingSerializer, ReservationBoardingSerializer
from pet_booking.customers.serializers import PetSerializer
from pet_booking.customers.models import CustomersProfile, Pet


def create_reservation_id(service_type: str) -> str:
    """創建預約ID"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    microsecond_part = f"{now.microsecond:06d}"[-4:]
    
    if service_type == 'grooming':
        return f"GR{timestamp}{microsecond_part}"
    elif service_type == 'boarding':
        return f"BD{timestamp}{microsecond_part}"
    else:
        raise ValueError(f"Invalid service_type: {service_type}")

class StoreInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """店家資訊管理ViewSet"""
    permission_classes = [IsAuthenticated]

    def get_store_queryset(self, store_id: str) -> QuerySet:
        """獲取店家 QuerySet"""
        return Store.objects.filter(user_id__user_id=store_id)

    def get_user_pets_queryset(self, user_id: int) -> QuerySet:
        """獲取用戶寵物 QuerySet"""
        return Pet.objects.filter(user_id=user_id)

    def get_grooming_services_queryset(self, store_id: str) -> QuerySet:
        """獲取美容服務 QuerySet"""
        return GroomingService.objects.filter(store_id=store_id)

    def get_boarding_services_queryset(self, store_id: str) -> QuerySet:
        """獲取住宿服務 QuerySet"""
        return BoardingService.objects.filter(store_id=store_id)

    def create_pet_info_dict(self, pet: Pet) -> Dict:
        """創建寵物資訊字典"""
        return {
            'name': pet.name,
            'species': pet.species,
            'gender': pet.gender,
            'breed': pet.breed,
            'age': pet.age,
            'fur_amount': pet.fur_amount,
            'size': pet.size,
            'weight': pet.weight,
            'spayed_or_neutered': pet.spayed_or_neutered,
            'microchip': pet.microchip,
            'notes': pet.notes,
        }

    def create_store_info_dict(self, store: Store) -> Dict:
        """創建店家資訊字典"""
        return {
            'id': store.id,
            'store_name': store.store_name,
            'store_phone': store.phone,
            'daily_opening_time': store.daily_opening_time,
            'daily_closing_hours': store.daily_closing_hours,
        }

    def create_user_pets_list(self, pets_queryset: QuerySet) -> Dict[str, Dict]:
        """創建用戶寵物列表"""
        user_pets = {}
        for index, pet in enumerate(pets_queryset):
            user_pets[index] = self.create_pet_info_dict(pet)
        return user_pets

    def create_grooming_services_list(self, grooming_services_queryset: QuerySet) -> List[str]:
        """創建美容服務標題列表"""
        return [service.service_title for service in grooming_services_queryset]

    def create_boarding_pricing_info(self, room_type: BoardingService) -> Optional[Dict]:
        """創建住宿定價資訊"""
        try:
            boarding_pricing = BoardingServicePricing.objects.get(room_type=room_type)
            return {
                'duration': boarding_pricing.duration,
                'duration_unit': boarding_pricing.duration_unit,
                'pricing': boarding_pricing.pricing,
                'overtime_price': boarding_pricing.overtime_rate,
                'overtime_charging': boarding_pricing.overtime_charging
            }
        except BoardingServicePricing.DoesNotExist:
            return None

    def create_boarding_room_type_data(self, boarding_service: BoardingService) -> Optional[Dict]:
        """創建住宿房間類型資料"""
        try:
            boarding_room_type = BoardingService.objects.get(boarding_service=boarding_service)
            pricing_info = self.create_boarding_pricing_info(boarding_room_type)
            
            return {
                'id': boarding_room_type.id,
                'species': boarding_room_type.species,
                'room_type': boarding_room_type.room_type,
                'room_count': boarding_room_type.room_count,
                'pet_available_amount': boarding_room_type.pet_available_amount,
                'pricing_info': pricing_info
            }
        except BoardingService.DoesNotExist:
            return None

    def create_boarding_services_list(self, boarding_services_queryset: QuerySet) -> List[Dict]:
        """創建住宿服務列表"""
        boarding_data = []
        
        for boarding_service in boarding_services_queryset:
            room_type_data = self.create_boarding_room_type_data(boarding_service)
            
            boarding_data.append({
                'id': boarding_service.id,
                'cleaning_frequency': boarding_service.cleaning_frequency,
                'introduction': boarding_service.introduction,
                'created_at': boarding_service.created_at,
                'updated_at': boarding_service.updated_at,
                'room_type_info': room_type_data
            })
        
        return boarding_data

    def create_grooming_response_data(self, store: Store, service_titles: List[str], user_pets: Dict, user_id: int) -> Dict:
        """創建美容服務回應資料"""
        return {
            'store': self.create_store_info_dict(store),
            'service_titles': service_titles,
            'user_pets': user_pets,
            'user_id': user_id,
        }

    def create_boarding_response_data(self, store: Store, boarding_data: List[Dict], user_pets: Dict = None) -> Dict:
        """創建住宿服務回應資料"""
        response_data = {
            'store': {
                'store_name': store.store_name,
                'daily_opening_time': store.daily_opening_time,
                'daily_closing_hours': store.daily_closing_hours,
            },
            'boarding_services': boarding_data
        }
        
        if user_pets is not None:
            response_data['user_pets'] = user_pets
            
        return response_data

    @action(detail=False, methods=['get'], url_path='storedata2')
    def get_store_data_userside(self, request):
        """獲取店家資訊和服務選項(客戶端)"""
        store_id = request.query_params.get('store_id')
        service_type = request.query_params.get('service_type')
        user_id = request.user.user_id
        if not store_id:
            return Response({
                'error': '缺少店家ID參數'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            store_queryset = self.get_store_queryset(store_id)
            store = store_queryset.first()
            
            if not store:
                return Response({
                    'error': '店家不存在或已停用'
                }, status=status.HTTP_404_NOT_FOUND)

            # 獲取用戶寵物資訊
            pets_queryset = self.get_user_pets_queryset(user_id)
            user_pets = self.create_user_pets_list(pets_queryset)
            
            if service_type == 'grooming':
                grooming_services_queryset = self.get_grooming_services_queryset(store_id)
                service_titles = self.create_grooming_services_list(grooming_services_queryset)
                response_data = self.create_grooming_response_data(store, service_titles, user_pets, user_id)
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            elif service_type == 'boarding':
                boarding_services_queryset = self.get_boarding_services_queryset(store_id)
                boarding_data = self.create_boarding_services_list(boarding_services_queryset)
                response_data = self.create_boarding_response_data(store, boarding_data, user_pets)
                
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response({
                    'error': '服務項目非美容或住宿'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': f'獲取店家資訊失敗: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='storedata1')
    def get_store_info_storeside(self, request):
        """獲取店家資訊和服務選項(店家端)"""
        store_id = request.query_params.get('store_id')
        service_type = request.query_params.get('service_type')

        if not store_id:
            return Response({
                'error': '缺少店家ID參數'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            store_queryset = self.get_store_queryset(store_id)
            store = store_queryset.first()
            
            if not store:
                return Response({
                    'error': '店家不存在或已停用'
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                store_id = store.id
                
            if service_type == 'grooming':
                grooming_services_queryset = self.get_grooming_services_queryset(store_id)
                
                service_titles = self.create_grooming_services_list(grooming_services_queryset)
                response_data = {
                    'store': self.create_store_info_dict(store),
                    'service_titles': service_titles                
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            elif service_type == 'boarding':
                boarding_services_queryset = self.get_boarding_services_queryset(store_id)
                boarding_data = self.create_boarding_services_list(boarding_services_queryset)
                response_data = self.create_boarding_response_data(store, boarding_data)
                
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response({
                    'error': '服務項目非美容或住宿'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': f'獲取店家資訊失敗: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PetInfoViewSet(viewsets.ModelViewSet):
    """寵物資訊管理ViewSet"""
    permission_classes = [IsAuthenticated]

    def get_pet_queryset(self, user_id: int, pet_name: str) -> QuerySet:
        """獲取寵物 QuerySet"""
        return Pet.objects.filter(user_id=user_id, name=pet_name)

    def create_pet_info_dict(self, pet: Pet) -> Dict:
        """創建寵物資訊字典"""
        return {
            'name': pet.name,
            'species': pet.species,
            'gender': pet.gender,
            'breed': pet.breed,
            'age': pet.age,
            'fur_amount': pet.fur_amount,
            'size': pet.size,
            'weight': pet.weight,
            'spayed_or_neutered': pet.spayed_or_neutered,
            'microchip': pet.microchip,
            'notes': pet.notes,
        }

    def create_pet_response_data(self, pet: Pet) -> Dict:
        """創建寵物回應資料"""
        return {
            'success': True,
            'pet_info': self.create_pet_info_dict(pet)
        }

    def create_success_response(self, message: str, action: str, pet_info: Dict, status_code: int) -> Response:
        """創建成功回應"""
        return Response({
            'success': True,
            'message': message,
            'action': action,
            'pet_info': pet_info
        }, status=status_code)

    def create_error_response(self, error_message: str, status_code: int) -> Response:
        """創建錯誤回應"""
        return Response({'error': error_message}, status=status_code)

    def create_validation_error_response(self, error_message: str, details: Dict) -> Response:
        """創建驗證錯誤回應"""
        return Response({
            'error': error_message,
            'details': details
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='get_petinfo')
    def get_pet_info(self, request):
        """獲取寵物資訊"""
        
        try:
            if not request.user.is_authenticated:
                return self.create_error_response(
                    '用戶未認證', 
                    status.HTTP_401_UNAUTHORIZED
                )
            pet_name = request.query_params.get('pet_name')

            user_id = request.user.user_id
            if not pet_name:
                return self.create_error_response(
                    '缺少寵物姓名參數', 
                    status.HTTP_400_BAD_REQUEST
                )
            
            pet_queryset = self.get_pet_queryset(user_id, pet_name)
            pet = pet_queryset.first()
            if pet:
                response_data = self.create_pet_response_data(pet)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return self.create_error_response(
                    f'找不到用戶ID {user_id} 名為 "{pet_name}" 的寵物', 
                    status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return self.create_error_response(
                f'獲取寵物資訊時出現錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'], url_path='save_petinfo')
    def save_pet_info(self, request):
        """保存寵物資訊"""
        
        try:
            if not request.user.is_authenticated:
                return self.create_error_response(
                    '用戶未認證',
                    status.HTTP_401_UNAUTHORIZED
                )

            user_id = request.user
            pet_data = request.data
            pet_name = pet_data.get('name')

            if not pet_name:
                return self.create_error_response(
                    '寵物姓名為必填欄位',
                    status.HTTP_400_BAD_REQUEST
                )

            # 檢查寵物是否已存在
            pet_queryset = Pet.objects.filter(user_id=user_id, name=pet_name)
            existing_pet = pet_queryset.first()

            if existing_pet:
                # 更新現有寵物
                serializer = PetSerializer(existing_pet, data=pet_data, partial=True)
                if serializer.is_valid():
                    serializer.save(user_id=user_id)
                    return self.create_success_response(
                        f'寵物 "{pet_name}" 資訊覆寫更新成功',
                        'updated',
                        serializer.data,
                        status.HTTP_204_NO_CONTENT
                    )
                else:
                    return self.create_validation_error_response(
                        '寵物資料驗證失敗',
                        serializer.errors
                    )
                
            else:
                # 創建新寵物
                serializer = PetSerializer(data=pet_data)
                
                if serializer.is_valid():
                    serializer.save()
                    
                    return self.create_success_response(
                        f'寵物 "{pet_name}" 新增成功',
                        'created',
                        serializer.data,
                        status.HTTP_201_CREATED
                    )
                else:
                    return self.create_validation_error_response(
                        '寵物資料驗證失敗',
                        serializer.errors
                    )
        
        except Exception as e:
            return self.create_error_response(
                f'保存寵物資訊時出現錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GroomingCalculationViewSet(viewsets.ModelViewSet):
    """美容費用計算ViewSet"""
    permission_classes = [IsAuthenticated]

    def get_store_queryset(self, store_id: str) -> QuerySet:
        """獲取店家 QuerySet"""
        return Store.objects.filter(user_id__user_id=store_id)
    def get_grooming_service_queryset(self, service_title: str, store_id: str) -> QuerySet:
        """獲取美容服務 QuerySet"""
        store = Store.objects.filter(user_id__user_id=store_id).first()
        return GroomingService.objects.filter(
            service_title=service_title, 
            store_id=store.id
        )

    def get_grooming_pricing_queryset(self, grooming_service: GroomingService, pet_size: str, pet_fur_amount: str) -> QuerySet:
        """獲取美容服務定價 QuerySet"""
        return GroomingServicePricing.objects.filter(
            grooming_service_id=grooming_service,
            pet_size=pet_size,
            fur_amount=pet_fur_amount
        )

    def create_pet_data_dict(self, pet_data: Dict) -> Dict:
        """創建寵物資料字典，提取必要欄位"""
        return {
            'name': pet_data.get('name'),
            'species': pet_data.get('species'),
            'fur_amount': pet_data.get('fur_amount'),
            'size': pet_data.get('size')
        }

    def create_calculation_response_data(self, store_id: str, store_name: str, total_price: int) -> Dict:
        """創建計算結果回應資料"""
        return {
            'store_id': store_id,
            'store_name': store_name,
            'total_price': total_price,
        }

    def create_error_response(self, error_message: str, status_code: int) -> Response:
        """創建錯誤回應"""
        return Response({'error': error_message}, status=status_code)

    def validate_request_parameters(self, store_id: str, pet_data: Dict, selected_services: List) -> Optional[Response]:
        """驗證請求參數"""
        if not store_id:
            return self.create_error_response(
                '缺少店家ID參數', 
                status.HTTP_400_BAD_REQUEST
            )
        
        if not pet_data:
            return self.create_error_response(
                '缺少寵物資料', 
                status.HTTP_400_BAD_REQUEST
            )
        
        if not selected_services:
            return self.create_error_response(
                '請選擇至少一項服務', 
                status.HTTP_400_BAD_REQUEST
            )
        
        return None

    def validate_pet_data(self, pet_data_dict: Dict) -> Optional[Response]:
        """驗證寵物資料完整性"""
        required_fields = ['name', 'species', 'fur_amount', 'size']
        if not all(pet_data_dict.get(field) for field in required_fields):
            return self.create_error_response(
                '寵物資料不完整，需要提供: name, species, fur_amount, size', 
                status.HTTP_400_BAD_REQUEST
            )
        return None

    def calculate_service_price(self, service_title: str, store_id: str, pet_size: str, pet_fur_amount: str) -> Tuple[int, Optional[Response]]:
        """計算單項服務價格"""
        grooming_service_queryset = self.get_grooming_service_queryset(service_title, store_id)
        grooming_service = grooming_service_queryset.first()
        
        if not grooming_service:
            error_response = self.create_error_response(
                f'服務項目 "{service_title}" 不存在或不屬於此店家', 
                status.HTTP_404_NOT_FOUND
            )
            return 0, error_response

        pricing_queryset = self.get_grooming_pricing_queryset(grooming_service, pet_size, pet_fur_amount)
        pricing_result = pricing_queryset.first()

        if pricing_result:
            return int(pricing_result.pricing), None
        else:
            error_response = self.create_error_response(
                f'找不到服務 "{service_title}" 對應此寵物類型的定價資訊', 
                status.HTTP_404_NOT_FOUND
            )
            return 0, error_response

    def calculate_total_price(self, selected_services: List[str], store_id: str, pet_size: str, pet_fur_amount: str) -> Tuple[int, Optional[Response]]:
        """計算所有服務的總價格"""
        total_price = 0
        for service_title in selected_services:
            service_price, error_response = self.calculate_service_price(
                service_title, store_id, pet_size, pet_fur_amount
            )
            
            if error_response:
                return 0, error_response
            
            total_price += service_price
        
        return total_price, None

    @action(detail=False, methods=['post'], url_path='calculate')
    def calculate_grooming_cost(self, request):
        """計算美容服務的總時間和總價格"""
        
        try:
            store_id = request.query_params.get('store_id')
            pet_data = request.data.get('pet_data', {})
            selected_services = request.data.get('selected_services', [])
            # 驗證請求參數
            validation_error = self.validate_request_parameters(store_id, pet_data, selected_services)
            if validation_error:
                return validation_error
            # 獲取店家資訊
            store_queryset = self.get_store_queryset(store_id)
            store = store_queryset.first()
            if not store:
                return self.create_error_response(
                    '店家不存在', 
                    status.HTTP_404_NOT_FOUND
                )

            # 驗證寵物資料
            pet_data_dict = self.create_pet_data_dict(pet_data)
            pet_validation_error = self.validate_pet_data(pet_data_dict)
            if pet_validation_error:
                return pet_validation_error
            # 計算總價格
            total_price, calculation_error = self.calculate_total_price(
                selected_services, 
                store_id, 
                pet_data_dict['size'], 
                pet_data_dict['fur_amount']
            )
            if calculation_error:
                return calculation_error

            # 創建回應資料
            response_data = self.create_calculation_response_data(store_id, store.store_name, total_price)
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return self.create_error_response(
                f'顧客總花費計算出現錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GroomingReservationViewSet(viewsets.ModelViewSet):
    """美容預約管理ViewSet"""
    permission_classes = [IsAuthenticated]

    def get_customer_profile_queryset(self, user_id: int) -> QuerySet:
        """獲取客戶檔案 QuerySet"""
        return CustomersProfile.objects.filter(user_id=user_id)

    def get_store_by_name_queryset(self, store_name: str) -> QuerySet:
        """根據店名獲取店家 QuerySet"""
        return Store.objects.filter(store_name=store_name)

    def get_store_by_id_queryset(self, store_id: str) -> QuerySet:
        """根據店家ID獲取店家 QuerySet"""
        return Store.objects.filter(user_id__user_id=store_id)

    def get_pet_queryset(self, user_id: int, pet_name: str) -> QuerySet:
        """獲取寵物 QuerySet"""
        return Pet.objects.filter(user_id=user_id, name=pet_name)

    def get_grooming_service_queryset(self, service_title: str, store_id: str) -> QuerySet:
        """獲取美容服務 QuerySet"""
        store = Store.objects.filter(user_id__user_id=store_id).first()
        return GroomingService.objects.filter(
            service_title=service_title,
            store_id=store.id
        )

    def get_grooming_pricing_queryset(self, grooming_service: GroomingService, pet_size: str, pet_fur_amount: str) -> QuerySet:
        """獲取美容服務定價 QuerySet"""
        return GroomingServicePricing.objects.filter(
            grooming_service_id=grooming_service,
            pet_size=pet_size,
            fur_amount=pet_fur_amount
        )

    def get_grooming_schedules_queryset(self, store_name: str, date: date, time_slot: time) -> QuerySet:
        """獲取美容時間表 QuerySet"""
        return GroomingSchedules.objects.filter(
            store_name=store_name,
            date=date,
            unavailable_time=time_slot
        )

    def get_user_coupon_queryset(self, user_id: int) -> QuerySet:
        """獲取用戶優惠券 QuerySet"""
        return Coupon.objects.filter(user_id=user_id)

    def create_customer_info_dict(self, customer_profile: CustomersProfile) -> Dict:
        """創建客戶資訊字典"""
        return {
            'user_name': customer_profile.full_name,
            'user_phone': customer_profile.phone or ''
        }

    def create_store_info_dict(self, store: Store) -> Dict:
        """創建店家資訊字典"""
        return {
            'store_name': store.store_name,
            'store_phone': store.phone
        }

    def create_pet_info_dict(self, pet: Pet) -> Dict:
        """創建寵物資訊字典"""
        return {
            'pet_type': pet.species,
            'pet_size': pet.size,
            'pet_fur_amount': pet.fur_amount,
            'pet_breed': pet.breed
        }

    def create_reservation_data_dict(self, reservation_id: str, store_name: str, user_name: str, user_phone: str, 
                                   selected_services: List[str], pet: Pet, pet_size: str, pick_up_service: bool,
                                   reservation_datetime: datetime, customer_note: str, store_note: str,
                                   total_price: int, total_grooming_duration: int) -> Dict:
        
        """創建預約資料字典"""
        return {
            'reservation_id': reservation_id,
            'store_name': store_name,
            'user_name': user_name,
            'user_phone': user_phone,
            'grooming_services_name': selected_services,
            'pet_name': pet.name,
            'pet_type': pet.species,
            'pet_breed': pet.breed,
            'pet_size': pet_size,
            'pick_up_service': pick_up_service,
            'reservation_time': reservation_datetime,
            'customer_note': customer_note,
            'store_note': store_note,
            'total_price': total_price,
            'grooming_period': total_grooming_duration,
            'status': 'pending'
        }

    def create_success_response_data(self, reservation_id: str, user_name: str, reservation_date: str,
                                   reservation_time: str, selected_services: List[str], pet_name: str,
                                   species: str,  store_id: str, store_phone: str,
                                   coupon_number: Optional[str] = None) -> Dict:
        """創建成功回應資料"""
        response_data = {
            'success': True,
            'message': '預約建立成功',
            'reservation_id': reservation_id,
            'store_id': store_id,
            'customer_name': user_name,
            'reservation_date': reservation_date,
            'reservation_time': reservation_time,
            'selected_service': selected_services,
            'pet_name': pet_name,
            'species': species,
            'store_phone': store_phone
        }

        if coupon_number:
            response_data['coupon_number'] = coupon_number
        
        else:
            response_data['coupon_number'] = '用戶未取得優惠券代碼'

        return response_data

    def create_error_response(self, error_message: str, status_code: int) -> Response:
        """創建錯誤回應"""
        return Response({'error': error_message}, status=status_code)

    def create_validation_error_response(self, error_message: str, details: Dict) -> Response:
        """創建驗證錯誤回應"""
        return Response({
            'error': error_message,
            'details': details
        }, status=status.HTTP_400_BAD_REQUEST)

    def validate_required_fields(self, required_data: List) -> Optional[Response]:
        """驗證必要欄位"""
        if not all(required_data):
            return self.create_error_response(
                '缺少必要的預約資訊', 
                status.HTTP_400_BAD_REQUEST
            )
        return None

    def parse_datetime(self, reservation_date: str, reservation_time: str) -> Tuple[Optional[datetime], Optional[Response]]:
        """解析日期時間"""
        try:
            reservation_date_obj = datetime.strptime(reservation_date, "%Y-%m-%d").date()
            reservation_time_obj = datetime.strptime(reservation_time, "%H:%M").time()
            reservation_datetime = datetime.combine(reservation_date_obj, reservation_time_obj)
            return reservation_datetime, None
        except ValueError:
            error_response = self.create_error_response(
                '日期時間格式錯誤', 
                status.HTTP_400_BAD_REQUEST
            )
            return None, error_response

    def calculate_service_duration_and_price(self, selected_services: List[str], store_id: str, 
                                           pet_size: str, pet_fur_amount: str) -> Tuple[int, int, Optional[Response]]:
        """計算服務持續時間和價格"""
        total_grooming_duration = 0
        total_price = 0

        for service_title in selected_services:
            grooming_service_queryset = self.get_grooming_service_queryset(service_title, store_id)
            grooming_service = grooming_service_queryset.first()

            if not grooming_service:
                error_response = self.create_error_response(
                    f'服務項目 "{service_title}" 不存在或不屬於此店家', 
                    status.HTTP_404_NOT_FOUND
                )
                return 0, 0, error_response

            pricing_queryset = self.get_grooming_pricing_queryset(grooming_service, pet_size, pet_fur_amount)
            grooming_result = pricing_queryset.first()

            if grooming_result:
                total_grooming_duration += int(grooming_result.grooming_duration)
                total_price += int(grooming_result.pricing)
            else:
                error_response = self.create_error_response(
                    f'找不到服務 "{service_title}" 對應此寵物類型的定價資訊', 
                    status.HTTP_404_NOT_FOUND
                )
                return 0, 0, error_response

        return total_grooming_duration, total_price, None

    def create_unavailable_time_slots(self, reservation_datetime: datetime, total_grooming_duration: int) -> List[time]:
        """創建不可用時間段列表"""
        total_grooming_duration_count = int(round(total_grooming_duration / 15 - 1, 0))
        grooming_unavailable_time = []
        current_time = reservation_datetime
        
        for i in range(total_grooming_duration_count + 1):
            grooming_unavailable_time.append(current_time.time())
            current_time += timedelta(minutes=15)
        
        return grooming_unavailable_time

    def check_time_slot_availability(self, unavailable_times: List[time], store_name: str, 
                                   reservation_date: date) -> Optional[Response]:
        """檢查時間段可用性"""
        for time_slot in unavailable_times:
            schedule_queryset = self.get_grooming_schedules_queryset(store_name, reservation_date, time_slot)
            if schedule_queryset.exists():
                return self.create_error_response(
                    '您預約的服務時段與其他客人重複，請先與店家確認後再進行預約', 
                    status.HTTP_409_CONFLICT
                )
        return None

    def check_and_process_user_coupon(self, user_id: int, reservation_id: str, store_id: str) -> Tuple[Optional[str], Optional[Response]]:
        """檢查並處理用戶優惠券"""
        try:
            # 查詢用戶的優惠券
            coupon_queryset = self.get_user_coupon_queryset(user_id)
            coupon = coupon_queryset.first()
            
            if not coupon:
                # 用戶沒有優惠券，返回None但不算錯誤
                return None, None
            
            # 檢查優惠券狀態
            if coupon.status == CouponStatus.NOT_USED:
                # 將預約ID存入優惠券的reservation_id欄位
                coupon.reservation_id = reservation_id
                coupon.store_id = store_id
                coupon.save()
                # 返回優惠券號碼
                return coupon.coupon_number, None
            else:
                # 優惠券已使用，不返回優惠券號碼
                return '您之前預約已經使用過優惠券囉!', None
                
        except Exception as e:
            error_response = self.create_error_response(
                f'處理優惠券時發生錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return None, error_response

    @action(detail=False, methods=['post'], url_path='user_create')
    def create_reservation(self, request):
        """建立美容預約(客戶端)"""
        
        try:
            if not request.user.is_authenticated:
                return self.create_error_response(
                    '用戶未認證', 
                    status.HTTP_401_UNAUTHORIZED
                )

            store_id = request.query_params.get('store_id')
            service_type = request.query_params.get('service_type')
            user_id = request.user.user_id
            store_name = request.data.get('store_name')
            pet_name = request.data.get('pet_name')                     
            selected_services = request.data.get('selected_services', [])
            pick_up_service = request.data.get('pick_up_service', False)
            reservation_date = request.data.get('reservation_date')
            reservation_time = request.data.get('reservation_time')
            customer_note = request.data.get('customer_note', '')

            # 驗證必要欄位
            validation_error = self.validate_required_fields([
                store_name, store_id, pet_name, selected_services, reservation_date, reservation_time
            ])
            if validation_error:
                return validation_error

            # 獲取客戶資訊
            customer_queryset = self.get_customer_profile_queryset(user_id)
            customer_profile = customer_queryset.first()
            if not customer_profile:
                return self.create_error_response(
                    '用戶不存在', 
                    status.HTTP_404_NOT_FOUND
                )

            customer_info = self.create_customer_info_dict(customer_profile)
            # 獲取店家資訊
            store_queryset = self.get_store_by_name_queryset(store_name)
            store = store_queryset.first()
            if not store:
                return self.create_error_response(
                    '店家不存在', 
                    status.HTTP_404_NOT_FOUND
                )

            store_info = self.create_store_info_dict(store)

            # 獲取寵物資訊
            pet_queryset = self.get_pet_queryset(user_id, pet_name)
            pet = pet_queryset.first()
            
            if not pet:
                return self.create_error_response(
                    f'找不到名為 "{pet_name}" 的寵物', 
                    status.HTTP_404_NOT_FOUND
                )

            pet_info = self.create_pet_info_dict(pet)

            # 計算服務持續時間和價格
            total_grooming_duration, total_price, calculation_error = self.calculate_service_duration_and_price(
                selected_services, store_id, pet_info['pet_size'], pet_info['pet_fur_amount']
            )

            if calculation_error:
                return calculation_error

            # 解析日期時間
            reservation_datetime, datetime_error = self.parse_datetime(reservation_date, reservation_time)
            if datetime_error:
                return datetime_error

            # 創建不可用時間段
            unavailable_times = self.create_unavailable_time_slots(reservation_datetime, total_grooming_duration)
            
            # 檢查時間段可用性
            availability_error = self.check_time_slot_availability(
                unavailable_times, store_name, reservation_datetime.date()
            )
            if availability_error:
                return availability_error
            
            reservation_id = create_reservation_id(service_type)
            reservation_data = self.create_reservation_data_dict(
                reservation_id, store_name, customer_info['user_name'], customer_info['user_phone'],
                selected_services, pet, pet_info['pet_size'], pick_up_service,
                reservation_datetime, customer_note, '', total_price, total_grooming_duration
            )

            serializer = ReservationGroomingSerializer(data=reservation_data)

            if serializer.is_valid():
                serializer.save()

                coupon_number, coupon_error = self.check_and_process_user_coupon(user_id, reservation_id, store_id)
                if coupon_error:
                    return coupon_error

                print(store_info)
                response_data = self.create_success_response_data(
                    reservation_id, customer_info['user_name'], reservation_date, reservation_time,
                    selected_services, pet.name, pet.species, store_id, store_info['store_phone'], coupon_number,
                    
                )

                return Response(response_data, status=status.HTTP_201_CREATED)
            
            else:
                return self.create_validation_error_response(
                    '預約資料驗證失敗',
                    serializer.errors
                )

        except Exception as e:
            return self.create_error_response(
                f'建立預約時發生錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'], url_path='store_create')
    def create_reservation_storeside(self, request):
        """建立美容預約(店家端)"""
        
        try:
            # 提取請求參數
            store_id = request.query_params.get('store_id')
            service_type = request.query_params.get('service_type')
            user_name = request.data.get('user_name')
            user_phone = request.data.get('user_phone')
            pet_name = request.data.get('pet_name')
            pet_type = request.data.get('pet_type')
            pet_breed = request.data.get('pet_breed')
            pet_size = request.data.get('pet_size')
            pet_fur_amount = request.data.get('fur_amount')
            selected_services = request.data.get('selected_services', [])
            pick_up_service = request.data.get('pick_up_service', False)
            reservation_date = request.data.get('reservation_date')
            reservation_time = request.data.get('reservation_time')
            store_note = request.data.get('store_note', '')

            # 驗證必要欄位
            validation_error = self.validate_required_fields([
                store_id, service_type, user_name, user_phone, pet_name, 
                pet_type, pet_breed, selected_services, pick_up_service,
                reservation_date, reservation_time, store_note
            ])
            if validation_error:
                return validation_error

            # 獲取店家資訊
            store_queryset = self.get_store_by_id_queryset(store_id)
            store = store_queryset.first()

            if not store:
                return self.create_error_response(
                    '店家不存在', 
                    status.HTTP_404_NOT_FOUND
                )

            store_info = self.create_store_info_dict(store)

            # 計算服務持續時間
            total_grooming_duration, total_price, calculation_error = self.calculate_service_duration_and_price(
                selected_services, store_id, pet_size, pet_fur_amount
            )
            if calculation_error:
                return calculation_error

            # 解析日期時間
            reservation_datetime, datetime_error = self.parse_datetime(reservation_date, reservation_time)
            if datetime_error:
                return datetime_error
            
            # 創建不可用時間段（店家端計算方式略有不同）
            total_grooming_duration_count = math.ceil(total_grooming_duration / 15) - 1
            grooming_unavailable_time = []
            current_time = reservation_datetime

            for i in range(total_grooming_duration_count + 1):
                grooming_unavailable_time.append(current_time.time())
                current_time += timedelta(minutes=15)

            # 檢查時間段可用性
            availability_error = self.check_time_slot_availability(
                grooming_unavailable_time, store_info['store_name'], reservation_datetime.date()
            )

            if availability_error:
                return availability_error

            # 創建預約資料（店家端不計算價格）
            reservation_id = create_reservation_id(service_type)
            reservation_data = {
                'reservation_id': reservation_id,
                'store_name': store_info['store_name'],
                'user_name': user_name,
                'user_phone': user_phone,
                'grooming_services_name': selected_services,
                'pet_name': pet_name,
                'pet_type': pet_type,
                'pet_breed': pet_breed,
                'pet_size': pet_size,
                'pick_up_service': pick_up_service,
                'reservation_time': reservation_datetime,
                'total_price': total_price,
                'grooming_period': total_grooming_duration,
                'customer_note': '',
                'store_note': store_note,
                'status': 'pending'
            }

            # 序列化和保存
            serializer = ReservationGroomingSerializer(data=reservation_data)

            if serializer.is_valid():
                serializer.save()
                response_data = self.create_success_response_data(
                    reservation_id, user_name, reservation_date, reservation_time,
                    selected_services, pet_name, pet_type, store_id, store_info['store_phone']
                )

                return Response(response_data, status=status.HTTP_201_CREATED)
            
            else:
                return self.create_validation_error_response(
                    '預約資料驗證失敗',
                    serializer.errors
                )

        except Exception as e:
            return self.create_error_response(
                f'建立預約時發生錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 


class BoardingRoomInfoViewSet(viewsets.ModelViewSet):
    """住宿房間資訊ViewSet"""
    permission_classes = [IsAuthenticated]

    def get_store_queryset(self, store_id: str) -> QuerySet:
        """獲取店家 QuerySet"""
        return Store.objects.filter(user_id__user_id=store_id)

    def get_boarding_services_queryset(self, store_id: str) -> QuerySet:
        """獲取住宿服務 QuerySet"""
        store = Store.objects.filter(user_id__user_id=store_id).first()
        return BoardingService.objects.filter(store_id=store.id)

    def get_room_type_queryset(self, boarding_service: BoardingService, pet_species: str) -> QuerySet:
        """獲取房間類型 QuerySet"""
        return BoardingService.objects.filter(
            species=pet_species
        )

    def get_room_pricing_queryset(self, room_type: BoardingService) -> QuerySet:
        """獲取房間定價 QuerySet"""
        return BoardingServicePricing.objects.filter(boarding_service_id=room_type)

    def create_pricing_info_dict(self, room_pricing: BoardingServicePricing) -> Dict:
        """創建定價資訊字典"""
        return {
            'duration': room_pricing.duration,
            'duration_unit': room_pricing.duration_unit,
            'pricing': room_pricing.pricing,
            'overtime_rate': room_pricing.overtime_rate,
            'overtime_charging': room_pricing.overtime_charging
        }

    def create_response_data_dict(self, store_id: str, store_name: str, room_types_data: Dict) -> Dict:
        """創建回應資料字典"""
        return {
            'success': True,
            'store_id': store_id,
            'store_name': store_name,
            'room_types': room_types_data
        }

    def create_error_response(self, error_message: str, status_code: int) -> Response:
        """創建錯誤回應"""
        return Response({'error': error_message}, status=status_code)

    def validate_request_parameters(self, store_id: str, pet_species: str) -> Optional[Response]:
        """驗證請求參數"""
        if not store_id:
            return self.create_error_response(
                '缺少店家ID參數', 
                status.HTTP_400_BAD_REQUEST
            )
        
        if not pet_species:
            return self.create_error_response(
                '缺少寵物類別參數', 
                status.HTTP_400_BAD_REQUEST
            )
        
        return None

    def process_room_types(self, boarding_services_queryset: QuerySet, pet_species: str) -> List[Dict]:
        """處理房間類型資料"""
        room_types_data = {}

        for boarding_service in boarding_services_queryset:
            room_id = boarding_service.id
            room_type = boarding_service.room_type
            if room_id:
                # 獲取定價資訊
                pricing_queryset = self.get_room_pricing_queryset(room_id)

                room = []
                for room_pricing in pricing_queryset:
                    pricing_info = self.create_pricing_info_dict(room_pricing)

                    room.append(pricing_info)
                
                room_types_data[room_type] = room
        
        return room_types_data

    @action(detail=False, methods=['get'], url_path='info')
    def get_room_types(self, request):
        """獲取房間類型資訊"""
        try:
            store_id = request.query_params.get('store_id')
            pet_species = request.query_params.get('pet_species')
            
            # 驗證請求參數
            validation_error = self.validate_request_parameters(store_id, pet_species)
            if validation_error:
                return validation_error
            
            # 獲取店家資訊
            store_queryset = self.get_store_queryset(store_id)
            store = store_queryset.first()

            if not store:
                return self.create_error_response(
                    '店家不存在', 
                    status.HTTP_404_NOT_FOUND
                )
            
            # 獲取住宿服務
            boarding_services_queryset = self.get_boarding_services_queryset(store_id)
            if not boarding_services_queryset.exists():
                return self.create_error_response(
                    '該店家沒有提供住宿服務', 
                    status.HTTP_404_NOT_FOUND
                )
            
            # 處理房間類型資料
            room_types_data = self.process_room_types(boarding_services_queryset, pet_species)
            
            if not room_types_data:
                return self.create_error_response(
                    f'該店家沒有提供給 {pet_species} 的住宿房間', 
                    status.HTTP_404_NOT_FOUND
                )
            
            # 創建回應資料
            response_data = self.create_response_data_dict(store_id, store.store_name, room_types_data)
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return self.create_error_response(
                f'獲取房間類型資訊時發生錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BoardingCalculationViewSet(viewsets.ModelViewSet):
    """住宿費用計算ViewSet"""
    permission_classes = [IsAuthenticated]

    def get_store_queryset(self, store_id: str) -> QuerySet:
        """獲取店家 QuerySet"""
        return Store.objects.filter(user_id__user_id=store_id)

    def get_boarding_services_queryset(self, store_id: str) -> QuerySet:
        """獲取住宿服務 QuerySet"""
        store = Store.objects.filter(user_id__user_id=store_id).first()
        return BoardingService.objects.filter(store_id=store.id)

    def get_boarding_service_by_filters_queryset(self, filters: Dict) -> QuerySet:
        """根據過濾條件獲取住宿服務 QuerySet"""
        return BoardingService.objects.filter(**filters)

    def get_room_pricing_queryset(self, boarding_service: BoardingService) -> QuerySet:
        """獲取房間定價 QuerySet"""
        return BoardingServicePricing.objects.filter(room_id=boarding_service)

    def create_date_validation_error_response(self, error_message: str) -> Response:
        """創建日期驗證錯誤回應"""
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

    def create_missing_parameter_error_response(self, parameter_name: str) -> Response:
        """創建缺少參數錯誤回應"""
        return Response({
            'error': f'缺少{parameter_name}參數'
        }, status=status.HTTP_400_BAD_REQUEST)

    def create_error_response(self, error_message: str, status_code: int) -> Response:
        """創建錯誤回應"""
        return Response({'error': error_message}, status=status_code)

    def create_service_detail_dict(self, room_pricing: BoardingServicePricing, duration_in_days: int) -> Dict:
        """創建服務詳細資訊字典"""
        service_detail = {
            'pricing_id': room_pricing.id,
            'original_duration': room_pricing.duration,
            'duration_unit': room_pricing.duration_unit,
            'duration_in_days': duration_in_days,
            'pricing': room_pricing.pricing
        }

        if room_pricing.overtime_charging:
            service_detail['overtime_price'] = room_pricing.overtime_rate
        
        return service_detail

    def create_service_detail_with_warning_dict(self, room_pricing: BoardingServicePricing, duration_in_days: int, warning: str) -> Dict:
        """創建包含警告的服務詳細資訊字典"""
        return {
            'original_duration': room_pricing.duration,
            'duration_unit': room_pricing.duration_unit,
            'duration_in_days': duration_in_days,
            'pricing': room_pricing.pricing,
            'overtime_rate': room_pricing.overtime_rate,
            'overtime_charging': room_pricing.overtime_charging,
            'warning': warning
        }

    def create_store_info_dict(self, store: Store) -> Dict:
        """創建店家資訊字典"""
        return {
            'store_id': store.id,
            'store_name': store.store_name
        }

    def create_pricing_option_dict(self, best_pricing_option: Dict) -> Dict:
        """創建定價選項字典"""
        return {
            'original_duration': best_pricing_option['original_duration'],
            'duration_unit': best_pricing_option['duration_unit'],
        }

    def create_cost_result_dict(self, boarding_duration: int, price_per_day: int, total_cost: int) -> Dict:
        """創建費用結果字典"""
        return {
            'boarding_duration_days': boarding_duration,
            'price_per_day': price_per_day,
            'total_boarding_cost': total_cost,
        }

    def create_response_data_dict(self, store_info: Dict, pricing_option: Dict, cost_result: Dict) -> Dict:
        """創建回應資料字典"""
        return {
            'success': True,
            'store_info': store_info,
            'selected_pricing_option': pricing_option,
            'total_boarding_cost_result': cost_result,
        }

    def validate_required_data(self, check_in_date: str, check_in_time: str, check_out_date: str, check_out_time: str) -> Optional[Response]:
        """驗證必要資料"""
        if not all([check_in_date, check_in_time, check_out_date, check_out_time]):
            return self.create_date_validation_error_response(
                '日期資料不完整，請輸入完整到店和離店日期'
            )
        return None

    def validate_parameters(self, store_id: str, room_type: str) -> Optional[Response]:
        """驗證參數"""
        if not store_id:
            return self.create_missing_parameter_error_response('店家ID')
        
        if not room_type:
            return self.create_missing_parameter_error_response('房型資訊')
        
        return None

    def parse_dates_and_calculate_duration(self, check_in_date: str, check_out_date: str) -> Tuple[int, Optional[Response]]:
        """解析日期並計算住宿天數"""
        try:
            check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()
            
            # 計算住宿晚數
            boarding_duration = (check_out_date_obj - check_in_date_obj).days

            # 如果當天入住當天退房，至少算1晚
            if boarding_duration <= 0:
                boarding_duration = 1
                
            return boarding_duration, None
            
        except ValueError:
            error_response = self.create_date_validation_error_response(
                '日期格式錯誤，請使用 YYYY-MM-DD 格式'
            )
            return 0, error_response

    def calculate_duration_in_days(self, room_pricing: BoardingServicePricing) -> int:
        """計算以天為單位的持續時間"""
        duration_in_days = room_pricing.duration
        if room_pricing.duration_unit == 'week':
            duration_in_days = room_pricing.duration * 7
        elif room_pricing.duration_unit == 'month':
            duration_in_days = room_pricing.duration * 30
        return duration_in_days


    def process_multiple_boarding_services(self, boarding_services_queryset: QuerySet, room_type: any) -> List[Dict]:
        """處理多個住宿服務"""
        service_details = []
        
        for boarding_service in boarding_services_queryset:
            try:
                if boarding_service.room_type == room_type:
                    pricing_queryset = BoardingServicePricing.objects.filter(boarding_service_id=boarding_service.id)
                    
                    for pricing in pricing_queryset:
                        if pricing.duration_unit == 'week':
                            pricing.duration = int(pricing.duration) * 7

                        elif pricing.duration_unit == 'month':
                            pricing.duration = int(pricing.duration) * 30

                        elif pricing.duration_unit == 'day':
                            pass

                        service_details.append({
                            "duration_in_days": int(pricing.duration),
                            "duration_unit": 'day',
                            "pricing": pricing.pricing,
                            "overtime_charging": pricing.overtime_charging,
                            "overtime_rate": pricing.overtime_rate
                            })

            except BoardingService.DoesNotExist:
                continue

        return service_details

    def select_best_pricing_option(self, service_details: List[Dict], boarding_duration: int) -> Tuple[Dict, int, Optional[Response]]:
        """選擇最佳定價選項"""
        # 驗證價格選項
        valid_pricing_options = [detail for detail in service_details if 'pricing' in detail]

        if not valid_pricing_options:
            error_response = self.create_error_response(
                '沒有找到有效的價格資訊', 
                status.HTTP_404_NOT_FOUND
            )
            return {}, 0, error_response
        
        # 選擇最適合的價格選項
        suitable_options = [
            option for option in valid_pricing_options 
            if option['duration_in_days'] <= boarding_duration
        ]
        
        if suitable_options:
            best_pricing_option = max(suitable_options, key=lambda x: x['duration_in_days'])
        else:
            best_pricing_option = min(valid_pricing_options, key=lambda x: x['duration_in_days'])
        
        total_cost = boarding_duration * best_pricing_option['pricing']
        return best_pricing_option, total_cost, None
    
    @action(detail=False, methods=['post'], url_path='calculate')
    def calculate_boarding_cost(self, request):
        """計算住宿服務的總晚數和總價格"""
        
        try:
            store_id = request.query_params.get('store_id')
            pet_species = request.query_params.get('pet_species')

            room_type = request.data.get('room_type')
            check_in_date = request.data.get('check_in_date')
            check_in_time = request.data.get('check_in_time')
            check_out_date = request.data.get('check_out_date')
            check_out_time = request.data.get('check_out_time')

            # 驗證必要資料
            data_validation_error = self.validate_required_data(check_in_date, check_in_time, check_out_date, check_out_time)
            if data_validation_error:
                return data_validation_error

            # 驗證參數
            parameter_validation_error = self.validate_parameters(store_id, room_type)
            if parameter_validation_error:
                return parameter_validation_error
            
            # 解析日期並計算住宿天數
            boarding_duration, date_error = self.parse_dates_and_calculate_duration(check_in_date, check_out_date)
            if date_error:
                return date_error

            # 獲取店家資訊
            store_queryset = self.get_store_queryset(store_id)
            store = store_queryset.first()

            if not store:
                return self.create_error_response(
                    '店家不存在', 
                    status.HTTP_404_NOT_FOUND
                )

            # 獲取住宿服務
            boarding_services_queryset = self.get_boarding_services_queryset(store_id)
            # 建立過濾條件
            room_type_filters = {
                'room_type': room_type
            }
            
            if pet_species:
                room_type_filters['species'] = pet_species
            
            # 處理住宿服務
            service_details = self.process_multiple_boarding_services(boarding_services_queryset, room_type)
            if not service_details:
                return self.create_error_response(
                    f'該店家沒有提供 "{room_type}" 房型的住宿服務', 
                    status.HTTP_404_NOT_FOUND
                )
    
            # 選擇最佳定價選項
            best_pricing_option, total_cost, pricing_error = self.select_best_pricing_option(service_details, boarding_duration)
            if pricing_error:
                return pricing_error

            # 創建回應資料
            response_data = {
                'success': True,
                'store_id': store.id,
                'store_name': store.store_name,
                'pricing_option': best_pricing_option,
                'boarding_duration_days': boarding_duration,
                'duration_unit': 'day',
                'total_boarding_cost': total_cost,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return self.create_error_response(
                f'數值格式錯誤: {str(e)}', 
                status.HTTP_400_BAD_REQUEST
            )
        except Store.DoesNotExist:
            return self.create_error_response(
                '店家不存在', 
                status.HTTP_404_NOT_FOUND
            )
        except BoardingService.DoesNotExist:
            return self.create_error_response(
                '住宿服務不存在', 
                status.HTTP_404_NOT_FOUND
            )
        except BoardingServicePricing.DoesNotExist:
            return self.create_error_response(
                '房間價格資訊不存在', 
                status.HTTP_404_NOT_FOUND
            )
        except KeyError as e:
            return self.create_error_response(
                f'缺少必要的資料欄位: {str(e)}', 
                status.HTTP_400_BAD_REQUEST
            )
        except TypeError as e:
            return self.create_error_response(
                f'資料類型錯誤: {str(e)}', 
                status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.create_error_response(
                f'計算住宿費用時發生未預期錯誤: {str(e)}', 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BoardingReservationManager:
    """住宿預約管理器"""
    
    def __init__(self):
        self.reservation_data = {}
        self.time_slots = []
        
    def get_customer_profile_queryset(self, user_id: int) -> QuerySet:
        """獲取客戶檔案 QuerySet"""
        return CustomersProfile.objects.filter(user_id=user_id)
    
    def get_customer_by_name_phone_queryset(self, user_name: str, user_phone: str) -> QuerySet:
        """根據姓名和電話獲取客戶 QuerySet"""
        return CustomersProfile.objects.filter(full_name=user_name, phone=user_phone)
    
    def get_store_by_name_queryset(self, store_name: str) -> QuerySet:
        """根據店名獲取店家 QuerySet"""
        return Store.objects.filter(store_name=store_name)
    
    def get_store_by_id_queryset(self, store_id: str) -> QuerySet:
        """根據店家ID獲取店家 QuerySet"""
        return Store.objects.filter(user_id__user_id=store_id)
    
    def get_boarding_services_queryset(self, store_id: str) -> QuerySet:
        """獲取住宿服務 QuerySet"""
        store = Store.objects.filter(user_id__user_id=store_id).first()
        return BoardingService.objects.filter(store_id=store.id)
    
    def get_room_type_queryset(self, boarding_service: BoardingService, room_type: str) -> QuerySet:
        """獲取房間類型 QuerySet"""
        return BoardingService.objects.filter(
            boarding_service=boarding_service,
            room_type=room_type
        )
    
    def get_boarding_schedules_queryset(self, store_name: str, room_type: str, time_slot: datetime) -> QuerySet:
        """獲取住宿時間表 QuerySet"""
        return BoardingSchedules.objects.filter(
            store_name=store_name,
            room_type=room_type,
            unavailable_time=time_slot
        )
    
    def create_reservation_data_dict(self, reservation_id: str, store_name: str, user_name: str, 
                                   user_phone: str, pet_name: str, room_type: str,
                                   checkin_datetime: datetime, checkout_datetime: datetime,
                                   total_price, customer_note: str = '', store_note: str = '') -> Dict:
        """創建預約資料字典"""
        return {
            'reservation_id': reservation_id,
            'store_name': store_name,
            'user_name': user_name,
            'user_phone': user_phone,
            'pet_name': pet_name,
            'room_type': room_type,
            'checkin_date': checkin_datetime,
            'checkout_date': checkout_datetime,
            'boarding_durations': (checkout_datetime.date() - checkin_datetime.date()).days,
            'customer_note': customer_note,
            'store_note': store_note,
            'status': 'pending',
            'total_price': total_price
        }
    
    def create_success_response_data(self, user_name: str, checkin_datetime: datetime,
                                   checkout_datetime: datetime, boarding_duration: int,
                                   room_type: str, store_phone: str, coupon_number: Optional[str] = None) -> Dict:
        """創建成功回應資料"""
        response_data = {
            'success': True,
            'message': '住宿預約建立成功',
            'user_name': user_name,
            'checkin_datetime': checkin_datetime.strftime("%Y-%m-%d %H:%M"),
            'checkout_datetime': checkout_datetime.strftime("%Y-%m-%d %H:%M"),
            'boarding_duration': boarding_duration,
            'room_type': room_type,
            'store_phone': store_phone,
        }
        
        # 如果有優惠券，加入回應資料
        if coupon_number:
            response_data['coupon_number'] = coupon_number
        else:
            response_data['coupon_number'] = '用戶未取得優惠券代碼'
        
        return response_data
    
    def parse_datetime_from_strings(self, check_in_date: str, check_in_time: str,
                                  check_out_date: str, check_out_time: str) -> Tuple[datetime, datetime, int, Optional[str]]:
        """解析日期時間字串"""
        try:
            check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_in_time_obj = datetime.strptime(check_in_time, "%H:%M").time()
            checkin_datetime = datetime.combine(check_in_date_obj, check_in_time_obj)
            
            check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()
            check_out_time_obj = datetime.strptime(check_out_time, "%H:%M").time()
            checkout_datetime = datetime.combine(check_out_date_obj, check_out_time_obj)
            
            if checkout_datetime <= checkin_datetime:
                return None, None, 0, '退房時間必須晚於入住時間'
                
            boarding_duration = (check_out_date_obj - check_in_date_obj).days
            
            return checkin_datetime, checkout_datetime, boarding_duration, None
            
        except ValueError:
            return None, None, 0, '日期或時間格式錯誤，請使用 YYYY-MM-DD 和 HH:MM 格式'
    
    def generate_time_slots(self, checkin_datetime: datetime, checkout_datetime: datetime) -> List[datetime]:
        """生成時間段列表（每30分鐘一個時間段）"""
        time_slots = []
        current_datetime = checkin_datetime
        
        while current_datetime < checkout_datetime:
            time_slots.append(current_datetime)
            current_datetime += timedelta(minutes=30)
        
        return time_slots
    
    def validate_room_availability(self, store_name: str, room_type: str, 
                                 time_slots: List[datetime], room_count: int) -> Optional[str]:
        """驗證房間可用性"""
        for time_slot in time_slots:
            occupied_rooms_queryset = self.get_boarding_schedules_queryset(store_name, room_type, time_slot)
            occupied_rooms = occupied_rooms_queryset.count()
            
            if occupied_rooms >= room_count:
                return f'房型 "{room_type}" 在 {time_slot.strftime("%Y-%m-%d %H:%M")} 時段已額滿'
        
        return None
    
    def find_room_type_info(self, boarding_services_queryset: QuerySet, room_type: str) -> Tuple[Optional[BoardingService], Optional[str]]:
        """查找房間類型資訊"""
        room_type_obj = {}
        for boarding_service in boarding_services_queryset:
            if boarding_service.room_type == room_type:
                room_type_obj["room_count"] = boarding_service.room_count
                room_type_obj["species"] = boarding_service.species
                return room_type_obj, None
        
        return None, f'找不到房型 "{room_type}"'
    
    def get_user_coupon_queryset(self, user_id: int) -> QuerySet:
        """獲取用戶優惠券 QuerySet"""
        return Coupon.objects.filter(user_id=user_id)
    
    def check_and_process_user_coupon(self, user_id: int, reservation_id: str, store_id: str) -> Tuple[Optional[str], Optional[str]]:
        """檢查並處理用戶優惠券"""
        try:
            # 查找用戶的優惠券
            coupon_queryset = self.get_user_coupon_queryset(user_id)
            coupon = coupon_queryset.first()
            
            if coupon and coupon.status == CouponStatus.NOT_USED:
                # 更新預約ID和店家ID
                coupon.reservation_id = reservation_id
                coupon.store_id = store_id
                coupon.save()
                
                return coupon.coupon_number, None
            else:
                # 沒有可用優惠券或已使用
                return None, None
                
        except Exception as e:
            return None, f'處理優惠券時發生錯誤: {str(e)}'

class BoardingReservationViewSet(viewsets.ModelViewSet):
    """住宿預約管理ViewSet"""
    permission_classes = [IsAuthenticated]
    queryset = ReservationBoarding.objects.all()
    serializer_class = ReservationBoardingSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = BoardingReservationManager()
    
    def calculate_boarding_total_price(self, store_id: str, room_type: str, pet_species: str, boarding_duration: int) -> Optional[int]:
        """計算住宿總價格 - 複用 BoardingCalculationViewSet 的邏輯"""
        try:
            boarding_services_queryset = self.manager.get_boarding_services_queryset(store_id)
            service_details = []
            
            for boarding_service in boarding_services_queryset:
                if boarding_service.room_type == room_type and boarding_service.species == pet_species:
                    try:
                        from pet_booking.services.models import BoardingServicePricing

                        pricing_queryset = BoardingServicePricing.objects.filter(boarding_service_id=boarding_service.id)
                        
                        for pricing in pricing_queryset:
                            duration_in_days = pricing.duration
                            
                            # 轉換時間單位為天數
                            if pricing.duration_unit == 'week':
                                duration_in_days = int(pricing.duration) * 7
                            elif pricing.duration_unit == 'month':
                                duration_in_days = int(pricing.duration) * 30
                            elif pricing.duration_unit == 'day':
                                duration_in_days = int(pricing.duration)
                                
                            service_details.append({
                                "duration_in_days": duration_in_days,
                                "duration_unit": 'day',
                                "pricing": pricing.pricing,
                                "overtime_charging": pricing.overtime_charging,
                                "overtime_rate": pricing.overtime_rate
                            })
                    except Exception:
                        continue
            
            if not service_details:
                return None
            
            # 選擇最佳定價選項 - 複用 BoardingCalculationViewSet 的邏輯
            valid_pricing_options = [detail for detail in service_details if 'pricing' in detail]

            if not valid_pricing_options:
                return None
            
            # 選擇最適合的價格選項
            suitable_options = [
                option for option in valid_pricing_options 
                if option['duration_in_days'] <= boarding_duration
            ]
            
            if suitable_options:
                best_pricing_option = max(suitable_options, key=lambda x: x['duration_in_days'])
            else:
                best_pricing_option = min(valid_pricing_options, key=lambda x: x['duration_in_days'])
            
            # 計算總價格
            total_cost = boarding_duration * best_pricing_option['pricing']
            return total_cost
            
        except Exception as e:
            print(f"計算住宿費用時發生錯誤: {str(e)}")
            return None
    
    def create_error_response(self, error_message: str, status_code: int) -> Response:
        """創建錯誤回應"""
        return Response({'error': error_message}, status=status_code)
    
    def validate_user_side_parameters(self, request) -> Tuple[Dict, Optional[Response]]:
        """驗證客戶端參數"""
        store_id = request.query_params.get('store_id')
        user_id = request.user.user_id
        service_type = request.query_params.get('service_type')
        
        required_fields = ['store_name', 'pet_name', 'room_type', 'check_in_date', 
                          'check_in_time', 'check_out_date', 'check_out_time']
        
        request_data = {
            'store_id': store_id,
            'user_id': user_id,
            'service_type': service_type,
            'store_name': request.data.get('store_name'),
            'pet_name': request.data.get('pet_name'),
            'room_type': request.data.get('room_type'),
            'pick_up_service': request.data.get('pick_up_service', False),
            'check_in_date': request.data.get('check_in_date'),
            'check_in_time': request.data.get('check_in_time'),
            'check_out_date': request.data.get('check_out_date'),
            'check_out_time': request.data.get('check_out_time'),
            'customer_note': request.data.get('customer_note', '')
        }
        
        # 檢查必要欄位
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        if missing_fields or not all([store_id, service_type]):
            return {}, self.create_error_response('缺少必要的預約資訊', status.HTTP_400_BAD_REQUEST)
        
        return request_data, None
    
    def validate_store_side_parameters(self, request) -> Tuple[Dict, Optional[Response]]:
        """驗證店家端參數"""
        store_id = request.query_params.get('store_id')
        
        required_fields = ['service_type', 'user_name', 'user_phone', 'pet_name', 
                          'pet_type', 'pet_breed', 'room_type', 'check_in_date',
                          'check_in_time', 'check_out_date', 'check_out_time']
        
        request_data = {
            'store_id': store_id,
            'service_type': request.data.get('service_type'),
            'user_name': request.data.get('user_name'),
            'user_phone': request.data.get('user_phone'),
            'pet_name': request.data.get('pet_name'),
            'pet_type': request.data.get('pet_type'),
            'pet_breed': request.data.get('pet_breed'),
            'room_type': request.data.get('room_type'),
            'pick_up_service': request.data.get('pick_up_service', False),
            'check_in_date': request.data.get('check_in_date'),
            'check_in_time': request.data.get('check_in_time'),
            'check_out_date': request.data.get('check_out_date'),
            'check_out_time': request.data.get('check_out_time'),
            'store_note': request.data.get('store_note', '')
        }
        
        # 檢查必要欄位
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        if missing_fields or not store_id:
            return {}, self.create_error_response('缺少必要的預約資訊', status.HTTP_400_BAD_REQUEST)
        
        return request_data, None
    
    @action(detail=False, methods=['post'], url_path='user')
    def create_reservation_usersides(self, request):
        """建立住宿預約(客戶端)"""
        try:
            if not request.user.is_authenticated:
                return self.create_error_response('用戶未認證', status.HTTP_401_UNAUTHORIZED)
            
            # 驗證參數
            request_data, error_response = self.validate_user_side_parameters(request)
            if error_response:
                return error_response

            # 獲取客戶資訊
            customer_queryset = self.manager.get_customer_profile_queryset(request_data['user_id'])
            customer_profile = customer_queryset.first()

            if not customer_profile:
                return self.create_error_response('用戶不存在', status.HTTP_404_NOT_FOUND)
            
            # 獲取店家資訊
            store_queryset = self.manager.get_store_by_name_queryset(request_data['store_name'])
            store = store_queryset.first()

            if not store:
                return self.create_error_response('店家不存在', status.HTTP_404_NOT_FOUND)

            # 獲取寵物資訊
            pet = Pet.objects.filter(user_id=request_data['user_id'], name=request_data['pet_name']).first()
            if not pet:
                return self.create_error_response('找不到對應的寵物資訊', status.HTTP_404_NOT_FOUND)
            
            # 獲取住宿服務
            boarding_services_queryset = self.manager.get_boarding_services_queryset(request_data['store_id'])
            if not boarding_services_queryset.exists():
                return self.create_error_response('該店家沒有提供住宿服務', status.HTTP_404_NOT_FOUND)

            # 查找房間類型
            room_type_obj, room_error = self.manager.find_room_type_info(
                boarding_services_queryset, request_data['room_type']
            )
            
            if room_error:
                return self.create_error_response(room_error, status.HTTP_404_NOT_FOUND)

            # 驗證寵物類型與房型的物種是否一致
            if pet.species != room_type_obj['species']:
                return self.create_error_response(
                    f"寵物類型 ({pet.species}) 與房型的物種 ({room_type_obj['species']}) 不一致，無法預約。",
                    status.HTTP_400_BAD_REQUEST
                )
            
            # 解析日期時間
            checkin_datetime, checkout_datetime, boarding_duration, datetime_error = \
                self.manager.parse_datetime_from_strings(
                    request_data['check_in_date'], request_data['check_in_time'],
                    request_data['check_out_date'], request_data['check_out_time']
                )
            
            if datetime_error:
                return self.create_error_response(datetime_error, status.HTTP_400_BAD_REQUEST)

            # 生成時間段
            time_slots = self.manager.generate_time_slots(checkin_datetime, checkout_datetime)
            
            # 驗證房間可用性
            availability_error = self.manager.validate_room_availability(
                request_data['store_name'], request_data['room_type'], 
                time_slots, room_type_obj['room_count']
            )


            if availability_error:
                return self.create_error_response(availability_error, status.HTTP_400_BAD_REQUEST)
            # 計算住宿費用 - 使用 BoardingCalculationViewSet 的邏輯
            total_price = self.calculate_boarding_total_price(
                request_data['store_id'], request_data['room_type'], 
                pet.species, boarding_duration
            )
            if total_price is None:
                return self.create_error_response(
                    '無法計算住宿費用，請聯繫店家', 
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 創建預約ID
            reservation_id = create_reservation_id(request_data['service_type'])
            
            # 創建預約資料
            reservation_data = self.manager.create_reservation_data_dict(
                reservation_id, request_data['store_name'], customer_profile.full_name,
                customer_profile.phone or '', request_data['pet_name'], request_data['room_type'],
                checkin_datetime, checkout_datetime, total_price, request_data['customer_note']
            )
            
            # 檢查並處理用戶優惠券
            coupon_number, coupon_error = self.manager.check_and_process_user_coupon(
                request_data['user_id'], reservation_id, request_data['store_id']
            )
            
            if coupon_error:
                print(f"優惠券處理警告: {coupon_error}")
            
            # 創建成功回應
            response_data = self.manager.create_success_response_data(
                customer_profile.full_name, checkin_datetime, checkout_datetime,
                boarding_duration, request_data['room_type'], store.phone, coupon_number
            )
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return self.create_error_response(f'建立預約時發生錯誤: {str(e)}', status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'], url_path='store')
    def create_reservation_storesides(self, request):
        """建立住宿預約(店家端)"""
        try:
            # 驗證參數
            request_data, error_response = self.validate_store_side_parameters(request)
            if error_response:
                return error_response
            
            # 獲取客戶資訊
            customer_queryset = self.manager.get_customer_by_name_phone_queryset(
                request_data['user_name'], request_data['user_phone']
            )
            
            try:
                customer_profile = customer_queryset.get()
            except CustomersProfile.DoesNotExist:
                return self.create_error_response('找不到對應的用戶', status.HTTP_404_NOT_FOUND)
            except CustomersProfile.MultipleObjectsReturned:
                return self.create_error_response('找到多個相同的用戶記錄', status.HTTP_400_BAD_REQUEST)
            
            # 獲取店家資訊
            store_queryset = self.manager.get_store_by_id_queryset(request_data['store_id'])
            store = store_queryset.first()
            
            if not store:
                return self.create_error_response('店家不存在', status.HTTP_404_NOT_FOUND)
            
            # 解析日期時間
            checkin_datetime, checkout_datetime, boarding_duration, datetime_error = \
                self.manager.parse_datetime_from_strings(
                    request_data['check_in_date'], request_data['check_in_time'],
                    request_data['check_out_date'], request_data['check_out_time']
                )
            
            if datetime_error:
                return self.create_error_response(datetime_error, status.HTTP_400_BAD_REQUEST)
            
            # 生成時間段
            time_slots = self.manager.generate_time_slots(checkin_datetime, checkout_datetime)
            
            # 獲取住宿服務
            boarding_services_queryset = self.manager.get_boarding_services_queryset(request_data['store_id'])
            
            if not boarding_services_queryset.exists():
                return self.create_error_response('該店家沒有提供住宿服務', status.HTTP_404_NOT_FOUND)
            
            # 查找房間類型
            room_type_obj, room_error = self.manager.find_room_type_info(
                boarding_services_queryset, request_data['room_type']
            )
            
            if room_error:
                return self.create_error_response(room_error, status.HTTP_404_NOT_FOUND)
            
            # 驗證房間可用性
            availability_error = self.manager.validate_room_availability(
                store.store_name, request_data['room_type'], 
                time_slots, room_type_obj.room_count
            )
            
            if availability_error:
                return self.create_error_response(availability_error, status.HTTP_400_BAD_REQUEST)
            
            # 創建預約ID
            reservation_id = create_reservation_id(request_data['service_type'])
            
            # 創建預約資料
            reservation_data = self.manager.create_reservation_data_dict(
                reservation_id, store.store_name, request_data['user_name'],
                request_data['user_phone'], request_data['pet_name'], request_data['room_type'],
                checkin_datetime, checkout_datetime, '', request_data['store_note']
            )
            
            
            # 創建成功回應
            response_data = self.manager.create_success_response_data(
                request_data['user_name'], checkin_datetime, checkout_datetime,
                f'{boarding_duration}天', request_data['room_type'], store.phone
            )
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return self.create_error_response(f'建立預約時發生錯誤: {str(e)}', status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
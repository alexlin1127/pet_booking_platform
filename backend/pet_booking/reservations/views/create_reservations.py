# origin
from datetime import datetime, timedelta, date

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# app
from ..models import GroomingSchedules, BoardingSchedules, ReservationBoarding
from pet_booking.services.models import GroomingService, GroomingServicePricing, BoardingService, BoardingServicePricing
from pet_booking.stores.models import Store
from ..serializers import ReservationGroomingSerializer
from pet_booking.customers.serializers import PetSerializer
from pet_booking.customers.models import CustomersProfile, Pet


class StoreInfoViewSet(viewsets.ModelViewSet):
    """店家資訊管理ViewSet"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='storedata2')
    def get_store_data_userside(self, request):
        """獲取店家資訊和服務選項(客戶端)"""

        store_id = request.query_params.get('store_id')
        user_id = request.query_params.get('user_id')
        service_type = request.query_params.get('service_type')

        if not store_id:
            return Response(
                {'error': '缺少店家ID參數'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_pets = {}
        if user_id:
            pets = Pet.objects.filter(user_id=user_id)
            for pet in pets:
                user_pets[pet.name] = {
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

        try:
            store = get_object_or_404(Store, id=store_id)
            
            if service_type == 'grooming':
                grooming_services = GroomingService.objects.filter(store_id=store_id)
                service_titles = [service.service_title for service in grooming_services]

                response_data = {
                    'store': {
                        'id': store.id,
                        'store_name': store.store_name,
                        'store_phone': store.phone,
                        'daily_opening_time': store.daily_opening_time,
                        'daily_closing_hours': store.daily_closing_hours,
                    },
                    'service_titles': service_titles,
                    'user_pets': user_pets,
                    'user_id': user_id,
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            elif service_type == 'boarding':
                boarding_services = BoardingService.objects.filter(store_id=store_id)
                boarding_data = []
                
                for boarding_service in boarding_services:
                    try:
                        boarding_room_type = BoardingService.objects.get(boarding_service=boarding_service)
                        
                        try:
                            boarding_pricing = BoardingServicePricing.objects.get(room_type=boarding_room_type)
                            
                            pricing_info = {
                                'duration': boarding_pricing.duration,
                                'duration_unit': boarding_pricing.duration_unit,
                                'pricing': boarding_pricing.pricing,
                                'overtime_price': boarding_pricing.overtime_rate,
                                'overtime_charging': boarding_pricing.overtime_charging
                            }

                        except BoardingServicePricing.DoesNotExist:
                            pricing_info = None
                        
                        room_type_data = {
                            'id': boarding_room_type.id,
                            'species': boarding_room_type.species,
                            'room_type': boarding_room_type.room_type,
                            'room_count': boarding_room_type.room_count,
                            'pet_available_amount': boarding_room_type.pet_available_amount,
                            'pricing_info': pricing_info
                        }
                        
                    except BoardingService.DoesNotExist:
                        room_type_data = None
                    
                    boarding_data.append({
                        'id': boarding_service.id,
                        'cleaning_frequency': boarding_service.cleaning_frequency,
                        'introduction': boarding_service.introduction,
                        'created_at': boarding_service.created_at,
                        'updated_at': boarding_service.updated_at,
                        'room_type_info': room_type_data
                    })
                
                response_data = {
                    'store': {
                        'store_name': store.store_name,
                        'daily_opening_time': store.daily_opening_time,
                        'daily_closing_hours': store.daily_closing_hours,
                    },
                    'boarding_services': boarding_data,
                    'user_pets': user_pets
                }
                
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response(
                    {'error': '服務項目非美容或住宿'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Store.DoesNotExist:
            return Response(
                {'error': '店家不存在或已停用'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'獲取店家資訊失敗: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='storedata1')
    def get_store_info_storeside(self, request):
        """獲取店家資訊和服務選項(店家端)"""
        
        store_id = request.query_params.get('store_id')
        service_type = request.query_params.get('service_type')

        if not store_id:
            return Response(
                {'error': '缺少店家ID參數'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            store = get_object_or_404(Store, id=store_id)

            if service_type == 'grooming':
                grooming_services = GroomingService.objects.filter(store_id=store_id)
                service_titles = [service.service_title for service in grooming_services]

                '''
                    get unavailable booking time for specific store
                    default unavailable time => today
                '''
               
                response_data = {
                    'store': {
                        'id': store.id,
                        'store_name': store.store_name,
                        'store_phone': store.phone,
                        'daily_opening_time': store.daily_opening_time,
                        'daily_closing_hours': store.daily_closing_hours,
                    },
                    'service_titles': service_titles                
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            elif service_type == 'boarding':
                boarding_services = BoardingService.objects.filter(store_id=store_id)
                boarding_data = []
                
                for boarding_service in boarding_services:
                    try:
                        boarding_room_type = BoardingService.objects.get(boarding_service=boarding_service)
                        
                        try:
                            boarding_pricing = BoardingServicePricing.objects.get(room_type=boarding_room_type)

                            pricing_info = {
                                'duration': boarding_pricing.duration,
                                'duration_unit': boarding_pricing.duration_unit,
                                'pricing': boarding_pricing.pricing,
                                'overtime_price': boarding_pricing.overtime_rate,
                                'overtime_charging': boarding_pricing.overtime_charging
                            }

                        except BoardingServicePricing.DoesNotExist:
                            pricing_info = None
                        
                        room_type_data = {
                            'id': boarding_room_type.id,
                            'species': boarding_room_type.species,
                            'room_type': boarding_room_type.room_type,
                            'room_count': boarding_room_type.room_count,
                            'pet_available_amount': boarding_room_type.pet_available_amount,
                            'pricing_info': pricing_info
                        }

                    except BoardingService.DoesNotExist:
                        room_type_data = None
                    
                    boarding_data.append({
                        'id': boarding_service.id,
                        'cleaning_frequency': boarding_service.cleaning_frequency,
                        'introduction': boarding_service.introduction,
                        'created_at': boarding_service.created_at,
                        'updated_at': boarding_service.updated_at,
                        'room_type_info': room_type_data
                    })
                
                response_data = {
                    'store': {
                        'store_name': store.store_name,
                        'daily_opening_time': store.daily_opening_time,
                        'daily_closing_hours': store.daily_closing_hours,
                    },
                    'boarding_services': boarding_data
                }
                
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response(
                    {'error': '服務項目非美容或住宿'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Store.DoesNotExist:
            return Response(
                {'error': '店家不存在或已停用'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'獲取店家資訊失敗: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PetInfoViewSet(viewsets.ModelViewSet):
    """寵物資訊管理ViewSet"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get_petinfo')
    def get_pet_info(self, request):
        """獲取寵物資訊"""
        
        try:
            user_id = request.query_params.get('user_id')
            pet_name = request.data.get('pet_name')

            if not user_id:
                return Response(
                    {'error': '缺少顧客ID參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not pet_name:
                return Response(
                    {'error': '缺少寵物姓名參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                pet = Pet.objects.get(user_id=user_id, name=pet_name)

                pet_info = {
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

                return Response({
                    'success': True,
                    'pet_info': pet_info
                }, status=status.HTTP_200_OK)
            
            except Pet.DoesNotExist:
                return Response(
                    {'error': f'找不到用戶ID {user_id} 名為 "{pet_name}" 的寵物'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return Response(
                {'error': f'獲取寵物資訊時出現錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'], url_path='save_petinfo')
    def save_pet_info(self, request):
        """保存寵物資訊"""
        
        try:
            user_id = request.query_params.get('user_id')

            if not user_id:
                return Response(
                    {'error': '缺少顧客ID參數'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            pet_data = request.data.copy()
            pet_name = pet_data.get('name')

            if not pet_name:
                return Response(
                    {'error': '寵物姓名為必填欄位'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            pet_data['user_id'] = user_id

            try:
                pet = Pet.objects.get(user_id=user_id, name=pet_name)
                
                serializer = PetSerializer(pet, data=pet_data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    
                    return Response({
                        'success': True,
                        'message': f'寵物 "{pet_name}" 資訊覆寫更新成功',
                        'action': 'updated',
                        'pet_info': serializer.data
                    }, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({
                        'error': '寵物資料驗證失敗',
                        'details': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except Pet.DoesNotExist:
                # if pet not exist, then create pet data.
                serializer = PetSerializer(data=pet_data)
                
                if serializer.is_valid():
                    serializer.save()
                    
                    return Response({
                        'success': True,
                        'message': f'寵物 "{pet_name}" 新增成功',
                        'action': 'created',
                        'pet_info': serializer.data
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'error': '寵物資料驗證失敗',
                        'details': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {'error': f'保存寵物資訊時出現錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GroomingCalculationViewSet(viewsets.ModelViewSet):
    """美容費用計算ViewSet"""
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='calculate')
    def calculate_grooming_cost(self, request):
        """計算美容服務的總時間和總價格"""
        
        try:
            store_id = request.query_params.get('store_id')
            pet_data = request.data.get('pet_data', {})
            selected_services = request.data.get('selected_services', [])

            if not store_id:
                return Response(
                    {'error': '缺少店家ID參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not pet_data:
                return Response(
                    {'error': '缺少寵物資料'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not selected_services:
                return Response(
                    {'error': '請選擇至少一項服務'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            store = get_object_or_404(Store, id=store_id)

            pet_name = pet_data.get('name')
            pet_species = pet_data.get('species')
            pet_fur_amount = pet_data.get('fur_amount')
            pet_size = pet_data.get('size')

            if not all([pet_name, pet_species, pet_fur_amount, pet_size]):
                return Response(
                    {'error': '寵物資料不完整，需要提供: name, species, fur_amount, size'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_price = 0

            for service_title in selected_services:
                try:
                    grooming_service = GroomingService.objects.get(
                        service_title=service_title, 
                        store_id=store_id
                    )

                    # find the only one price result.
                    result = GroomingServicePricing.objects.filter(
                        grooming_service_id=grooming_service,
                        pet_size=pet_size,
                        fur_amount=pet_fur_amount
                    ).first()

                    if result:
                        total_price += int(result.pricing)
                    else:
                        return Response(
                            {'error': f'找不到服務 "{service_title}" 對應此寵物類型的定價資訊'}, 
                            status=status.HTTP_404_NOT_FOUND
                        )

                except GroomingService.DoesNotExist:
                    return Response(
                        {'error': f'服務項目 "{service_title}" 不存在或不屬於此店家'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

            response_data = {
                'store_id': store_id,
                'store_name': store.store_name,
                'total_price': total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'顧客總花費計算出現錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GroomingReservationViewSet(viewsets.ModelViewSet):
    """美容預約管理ViewSet"""
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='user_create')
    def create_reservation(self, request):
        """建立美容預約(客戶端)"""
        
        try:
            store_id = request.query_params.get('store_id')
            user_id = request.query_params.get('user_id')
            service_type = request.query_params.get('service_type')
            store_name = request.data.get('store_name')
            pet_name = request.data.get('pet_name')                     
            selected_services = request.data.get('selected_services', [])
            pick_up_service = request.data.get('pick_up_service', False)
            reservation_date = request.data.get('reservation_date')
            reservation_time = request.data.get('reservation_time')
            customer_note = request.data.get('customer_note', '')

            if not all([store_name, store_id, user_id, pet_name, selected_services, reservation_date, reservation_time]):
                return Response(
                    {'error': '缺少必要的預約資訊'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # customer info
            try:
                customer_profile = CustomersProfile.objects.get(user_id=user_id)
                user_name = customer_profile.full_name
                user_phone = customer_profile.phone or ''
            except CustomersProfile.DoesNotExist:
                return Response(
                    {'error': '用戶不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # store info
            try:
                store = Store.objects.get(store_name=store_name)
                store_phone = store.phone
            except Store.DoesNotExist:
                return Response(
                    {'error': '店家不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # pet info
            try:
                pet = Pet.objects.get(user_id=user_id, name=pet_name)
                pet_type = pet.species
                pet_size = pet.size
                pet_fur_amount = pet.fur_amount
            except Pet.DoesNotExist:
                return Response(
                    {'error': f'找不到名為 "{pet_name}" 的寵物'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # calculate grooming service duration
            total_grooming_duration = 0
            total_price = 0

            for service_title in selected_services:
                try:
                    grooming_service = GroomingService.objects.get(
                        service_title=service_title,
                        store_id=store_id
                    )

                    grooming_result = GroomingServicePricing.objects.filter(
                        grooming_service_id=grooming_service,
                        pet_size=pet_size,
                        fur_amount=pet_fur_amount
                    ).first()

                    if grooming_result:
                        total_grooming_duration += int(grooming_result.grooming_duration)
                        total_price += int(grooming_result.pricing)
                    else:
                        return Response(
                            {'error': f'找不到服務 "{service_title}" 對應此寵物類型的定價資訊'}, 
                            status=status.HTTP_404_NOT_FOUND
                        )

                except GroomingService.DoesNotExist:
                    return Response(
                        {'error': f'服務項目 "{service_title}" 不存在或不屬於此店家'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

            total_grooming_duration_count = int(round(total_grooming_duration / 15 - 1, 0))
            
            try:
                reservation_date_obj = datetime.strptime(reservation_date, "%Y-%m-%d").date()
                reservation_time_obj = datetime.strptime(reservation_time, "%H:%M").time()
                reservation_datetime = datetime.combine(reservation_date_obj, reservation_time_obj)

            except ValueError:
                return Response(
                    {'error': '日期時間格式錯誤'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # calculate unavailable time for grooming service
            grooming_unavailable_time = []
            current_time = reservation_datetime
            
            # go through total_grooming_duration_count + 1 times
            for i in range(total_grooming_duration_count + 1):
                grooming_unavailable_time.append(current_time.time())
                current_time += timedelta(minutes=15)
            
            for time_slot in grooming_unavailable_time:
                existing_schedule = GroomingSchedules.objects.filter(
                    store_name=store_name,
                    date=reservation_date_obj,
                    unavailable_time=time_slot
                ).exists()
                
                if existing_schedule:
                    return Response(
                        {'error': '您預約的服務時段與其他客人重複，請先與店家確認後再進行預約'}, 
                        status=status.HTTP_409_CONFLICT
                    )

            reservation_id = create_reservation_id(service_type)
            reservation_data = {
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
                'store_note': '',
                'total_price': total_price,
                'grooming_period': total_grooming_duration,
                'status': 'pending'
            }

            serializer = ReservationGroomingSerializer(data=reservation_data)
            
            if serializer.is_valid():
                serializer.save()

                return Response({
                    'success': True,
                    'message': '預約建立成功',
                    'reservation_id': reservation_id,
                    'customer_name': user_name,
                    'reservation_date': reservation_date,
                    'reservation_time': reservation_time,
                    'selected_service': selected_services,
                    'pet_name': pet.name,
                    'species': pet.species,
                    'store_phone': store_phone
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'error': '預約資料驗證失敗',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': f'建立預約時發生錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
        
    @action(detail=False, methods=['post'], url_path='store_create')
    def create_reservation_storeside(self, request):
        """建立美容預約(店家端)"""
        
        try:
            store_id = request.query_params.get('store_id')
            service_type = request.query_params.get('service_type')
            user_name = request.data.get('user_name')
            user_phone = request.data.get('user_phone')
            pet_name = request.data.get('pet_name')
            pet_type = request.data.get('pet_type')
            pet_breed = request.data.get('pet_breed')
            pet_size = request.data.get('pet_size')
            pet_fur_amount = request.data.get('fur_amount')
            selected_services = request.data.get('selected_services', {})
            pick_up_service = request.data.get('pick_up_service', False)
            reservation_date = request.data.get('reservation_date')
            reservation_time = request.data.get('reservation_time')
            store_note = request.data.get('store_note', '')

            if not all([store_id, service_type, user_name, user_phone, pet_name, 
                        pet_type, pet_breed, selected_services, pick_up_service,
                        reservation_date, reservation_time, store_note]):
                return Response(
                    {'error': '缺少必要的預約資訊'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # user = CustomersProfile.objects.filter(phone=user_phone)
            # user_id = user.id

            store = get_object_or_404(Store, id=store_id)
            store_phone = store.phone
            store_name = store.store_name

            # calculate grooming service duration
            total_grooming_duration = 0

            for service_title in selected_services:
                try:
                    grooming_service = GroomingService.objects.get(
                        service_title=service_title,
                        store_id=store_id
                    )

                    grooming_result = GroomingServicePricing.objects.filter(
                        grooming_service_id=grooming_service,
                        pet_size=pet_size,
                        fur_amount=pet_fur_amount
                    ).first()

                    if grooming_result:
                        total_grooming_duration += int(grooming_result.grooming_duration)
                    else:
                        return Response(
                            {'error': f'找不到服務 "{service_title}" 對應此寵物類型的定價資訊'}, 
                            status=status.HTTP_404_NOT_FOUND
                        )

                except GroomingService.DoesNotExist:
                    return Response(
                        {'error': f'服務項目 "{service_title}" 不存在或不屬於此店家'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            total_grooming_duration_count = int(round(total_grooming_duration) / 15 - 1, 0)

            try:
                reservation_date_obj = datetime.strptime(reservation_date, "%Y-%m-%d").date()
                reservation_time_obj = datetime.strptime(reservation_time, "%H:%M").time()
                reservation_datetime = datetime.combine(reservation_date_obj, reservation_time_obj)

            except ValueError:
                return Response(
                    {'error': '日期時間格式錯誤'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
             # calculate unavailable time for grooming service
            grooming_unavailable_time = []
            current_time = reservation_datetime
            
            # go through total_grooming_duration_count + 1 times
            for i in range(total_grooming_duration_count + 1):
                grooming_unavailable_time.append(current_time.time())
                current_time += timedelta(minutes=15)
            
            for time_slot in grooming_unavailable_time:
                existing_schedule = GroomingSchedules.objects.filter(
                    store_name=store_name,
                    date=reservation_date_obj,
                    unavailable_time=time_slot
                ).exists()
                
                if existing_schedule:
                    return Response(
                        {'error': '您預約的服務時段與其他客人重複，請先與店家確認後再進行預約'}, 
                        status=status.HTTP_409_CONFLICT
                    )

            reservation_id = create_reservation_id(service_type)
            reservation_data = {
                'reservation_id': reservation_id,
                'store_name': store_name,
                'user_name': user_name,
                'user_phone': user_phone,
                'grooming_services_name': selected_services,
                'pet_name': pet_name,
                'pet_type': pet_type,
                'pet_breed': pet_breed,
                'pick_up_service': pick_up_service,
                'reservation_time': reservation_datetime,
                'customer_note': '',
                'store_note': store_note,
                'status': 'pending'
            }

            serializer = ReservationGroomingSerializer(data=reservation_data)
            
            if serializer.is_valid():
                serializer.save()

                return Response({
                    'success': True,
                    'message': '預約建立成功',
                    'reservation_id': reservation_id,
                    'customer_name': user_name,
                    'reservation_date': reservation_date,
                    'reservation_time': reservation_time,
                    'selected_service': selected_services,
                    'pet_name': pet_name,
                    'species': pet_type,
                    'store_phone': store_phone
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'error': '預約資料驗證失敗',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': f'建立預約時發生錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 


class BoardingRoomInfoViewSet(viewsets.ModelViewSet):
    """住宿房間資訊ViewSet"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='info')
    def get_room_types(self, request):
        """獲取房間類型資訊"""
        
        try:
            store_id = request.query_params.get('store_id')
            
            pet_species = request.query_params.get('pet_species')
            
            if not store_id:
                return Response(
                    {'error': '缺少店家ID參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not pet_species:
                return Response(
                    {'error': '缺少寵物類別參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                store = Store.objects.get(id=store_id)
                boarding_services = BoardingService.objects.filter(store_id=store_id)

            except Store.DoesNotExist:
                return Response(
                    {'error': '店家不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            except BoardingService.DoesNotExist:
                return Response(
                    {'error': '該店家沒有提供住宿服務'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            room_types_data = []
            
            for boarding_service in boarding_services:
                try:
                    room_type = BoardingService.objects.get(
                        boarding_service=boarding_service,
                        species=pet_species
                    )
                    
                    try:
                        room_pricing = BoardingServicePricing.objects.get(room_type=room_type)
                        pricing_info = {
                            'duration': room_pricing.duration,
                            'duration_unit': room_pricing.duration_unit,
                            'pricing': room_pricing.pricing,
                            'overtime_rate': room_pricing.overtime_rate,
                            'overtime_charging': room_pricing.overtime_charging
                        }
                    except BoardingServicePricing.DoesNotExist:
                        pricing_info = None
                    
                    # combine room type data
                    room_type_data = {
                        'id': room_type.id,
                        'species': room_type.species,
                        'room_type': room_type.room_type,
                        'room_count': room_type.room_count,
                        'pet_available_amount': room_type.pet_available_amount,
                        'pricing_info': pricing_info
                    }
                    room_types_data.append(room_type_data)

                except BoardingService.DoesNotExist:
                    continue
            
            if not room_types_data:
                return Response(
                    {'error': f'該店家沒有提供給 {pet_species} 的住宿房間'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            response_data = {
                'success': True,
                'store_id': store_id,
                'store_name': store.store_name,
                'room_types': room_types_data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'獲取房間類型資訊時發生錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BoardingCalculationViewSet(viewsets.ModelViewSet):
    """住宿費用計算ViewSet"""
    permission_classes = [IsAuthenticated]
    
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

            if not all([check_in_date, check_in_time, check_out_date, check_out_time]):
                return Response(
                    {'error': '日期資料不完整，請輸入完整到店和離店日期'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not store_id:
                return Response(
                    {'error': '缺少店家ID參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not room_type:
                return Response(
                    {'error': '缺少房型資訊參數'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()
                
                # 計算住宿晚數
                boarding_duration = (check_out_date_obj - check_in_date_obj).days
                
                # 如果當天入住當天退房，至少算1晚
                if boarding_duration <= 0:
                    boarding_duration = 1
                    
            except ValueError:
                return Response(
                    {'error': '日期格式錯誤，請使用 YYYY-MM-DD 格式'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            store = Store.objects.get(id=store_id)
            boarding_services = BoardingService.objects.filter(store_id=store_id)
            
            service_details = []
            
            for boarding_service in boarding_services:
                room_type_filters = {
                    'boarding_service': boarding_service,
                    'room_type': room_type
                }
                
                if pet_species:
                    room_type_filters['species'] = pet_species
                
                try:
                    boarding_service = BoardingService.objects.get(**room_type_filters)
                    room_pricings = BoardingServicePricing.objects.filter(room_type=boarding_service)
                    
                    if not room_pricings.exists():
                        return Response(
                           {'error': '找不到房型對應價格'},
                           status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    for room_pricing in room_pricings:
                        # 將 duration_unit 轉換為天數
                        duration_in_days = room_pricing.duration
                        if room_pricing.duration_unit == 'week':
                            duration_in_days = room_pricing.duration * 7
                        elif room_pricing.duration_unit == 'month':
                            duration_in_days = room_pricing.duration * 30
                        
                        service_detail = {
                            'pricing_id': room_pricing.id,
                            'original_duration': room_pricing.duration,
                            'duration_unit': room_pricing.duration_unit,
                            'duration_in_days': duration_in_days,
                            'pricing': room_pricing.pricing
                        }

                        if room_pricing.overtime_charging:
                            service_detail['overtime_price'] = room_pricing.overtime_rate
                        
                        service_details.append(service_detail)

                except BoardingService.DoesNotExist:
                    continue

                except BoardingService.MultipleObjectsReturned:
                    # 如果找到多筆資料，表示資料設計有問題，但仍然處理第一筆
                    boarding_service = BoardingService.objects.filter(**room_type_filters).first()
                    room_pricings = BoardingServicePricing.objects.filter(room_type=boarding_service)

                    if room_pricings.exists():
                        for room_pricing in room_pricings:
                            duration_in_days = room_pricing.duration
                            if room_pricing.duration_unit == 'week':
                                duration_in_days = room_pricing.duration * 7
                            elif room_pricing.duration_unit == 'month':
                                duration_in_days = room_pricing.duration * 30
                            
                            service_detail = {
                                'original_duration': room_pricing.duration,
                                'duration_unit': room_pricing.duration_unit,
                                'duration_in_days': duration_in_days,
                                'pricing': room_pricing.pricing,
                                'overtime_rate': room_pricing.overtime_rate,
                                'overtime_charging': room_pricing.overtime_charging,
                                'warning': '發現多筆房型資料，但只處理第一筆房型的所有價格選項'
                            }
                            
                            service_details.append(service_detail)
                    else:
                        service_detail = {
                            'warning': '發現多筆相同房型資料且該房型尚未設定價格資訊'
                        }
                        service_details.append(service_detail)
            
            if not service_details:
                return Response(
                    {'error': f'該店家沒有提供 "{room_type}" 房型的住宿服務'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # calculate total boarding spend
            best_pricing_option = None
            total_cost = 0
            
            # verify price options
            valid_pricing_options = [detail for detail in service_details if 'pricing' in detail]
            
            if not valid_pricing_options:
                return Response(
                    {'error': '沒有找到有效的價格資訊'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # choose the one with duration_in_days <= boarding_duration 
            suitable_options = [
                option for option in valid_pricing_options 
                if option['duration_in_days'] <= boarding_duration
            ]
            
            if suitable_options:
                best_pricing_option = max(suitable_options, key=lambda x: x['duration_in_days'])
            else:
                best_pricing_option = min(valid_pricing_options, key=lambda x: x['duration_in_days'])
            
            total_cost = boarding_duration * best_pricing_option['pricing']
            
            response_data = {
                'success': True,
                'store_info': {
                    'store_id': store.id,
                    'store_name': store.store_name
                    },
                'selected_pricing_option': {
                        'original_duration': best_pricing_option['original_duration'],
                        'duration_unit': best_pricing_option['duration_unit'],
                    },
                'total_boarding_cost_result': {
                    'boarding_duration_days': boarding_duration,
                    'price_per_day': best_pricing_option['pricing'],
                    'total_boarding_cost': total_cost,
                    },
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': f'數值格式錯誤: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Store.DoesNotExist:
            return Response(
                {'error': '店家不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except BoardingService.DoesNotExist:
            return Response(
                {'error': '住宿服務不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except BoardingService.DoesNotExist:
            return Response(
                {'error': '房間類型不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except BoardingServicePricing.DoesNotExist:
            return Response(
                {'error': '房間價格資訊不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except KeyError as e:
            return Response(
                {'error': f'缺少必要的資料欄位: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError as e:
            return Response(
                {'error': f'資料類型錯誤: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'計算住宿費用時發生未預期錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BoardingReservationViewSet(viewsets.ModelViewSet):
    """住宿預約管理ViewSet"""
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='user')
    def create_reservation_usersides(self, request):
        """建立住宿預約(客戶端)"""
        
        try:
            store_id = request.query_params.get('store_id')
            user_id = request.query_params.get('user_id')
            service_type = request.query_params.get('service_type')
            store_name = request.data.get('store_name')
            pet_name = request.data.get('pet_name')                     
            room_type = request.data.get('room_type')
            pick_up_service = request.data.get('pick_up_service', False)
            check_in_date = request.data.get('check_in_date')
            check_in_time = request.data.get('check_in_time')
            check_out_date = request.data.get('check_out_date')
            check_out_time = request.data.get('check_out_time')
            customer_note = request.data.get('customer_note', '')

            # verify input data
            if not all([store_name, store_id, user_id, pet_name, pick_up_service, room_type, check_in_date, check_in_time, check_out_date, check_out_time]):
                return Response(
                    {'error': '缺少必要的預約資訊'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # customer info
            try:
                customer_profile = CustomersProfile.objects.get(user_id=user_id)
                user_name = customer_profile.full_name
                user_phone = customer_profile.phone or ''
            except CustomersProfile.DoesNotExist:
                return Response(
                    {'error': '用戶不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # store info
            try:
                store = Store.objects.get(store_name=store_name)
                store_phone = store.phone
            except Store.DoesNotExist:
                return Response(
                    {'error': '店家不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            reservation_id = create_reservation_id(service_type)
            
            # combine check-in and check-out datetime
            try:
                check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                check_in_time_obj = datetime.strptime(check_in_time, "%H:%M").time()
                checkin_datetime = datetime.combine(check_in_date_obj, check_in_time_obj)
                
                check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()
                check_out_time_obj = datetime.strptime(check_out_time, "%H:%M").time()
                checkout_datetime = datetime.combine(check_out_date_obj, check_out_time_obj)
                
                # verify check-out time that must smaller than check-in time
                if checkout_datetime <= checkin_datetime:
                    return Response(
                        {'error': '退房時間必須晚於入住時間'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                boarding_duration = (check_out_date_obj - check_in_date_obj).days

            except ValueError:
                return Response(
                    {'error': '日期或時間格式錯誤，請使用 YYYY-MM-DD 和 HH:MM 格式'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # create time slots (every 30 minutes)
            boarding_time_slots = []
            current_datetime = checkin_datetime
            
            while current_datetime < checkout_datetime:
                boarding_time_slots.append(current_datetime)
                current_datetime += timedelta(minutes=30)
            
            # get room type from BoardingService model by store_id
            try:
                boarding_services = BoardingService.objects.filter(store_id=store_id)
                if not boarding_services.exists():
                    return Response(
                        {'error': '該店家沒有提供住宿服務'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # get room info according to room type
                room_type_obj = None
                for boarding_service in boarding_services:
                    try:
                        room_type_obj = BoardingService.objects.get(
                            boarding_service=boarding_service,
                            room_type=room_type
                        )
                        break
                    except BoardingService.DoesNotExist:
                        continue
                
                if not room_type_obj:
                    return Response(
                        {'error': f'找不到房型 "{room_type}"'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                room_count = room_type_obj.room_count
                
            except Exception as e:
                return Response(
                    {'error': f'查詢房型資訊時發生錯誤: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # check last room count
            for time_slot in boarding_time_slots:
                occupied_rooms = BoardingSchedules.objects.filter(
                    store_name=store_name,
                    room_type=room_type,
                    unavailable_time=time_slot
                ).count()
                
                if occupied_rooms >= room_count:
                    return Response(
                        {'error': f'房型 "{room_type}" 在 {time_slot.strftime("%Y-%m-%d %H:%M")} 時段已額滿'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            reservation_data = {
                'reservation_id': reservation_id,
                'store_name': store_name,
                'user_name': user_name,
                'user_phone': user_phone,
                'pet_name': pet_name,
                'room_type': room_type,
                'checkin_date': checkin_datetime,
                'checkout_date': checkout_datetime,
                'customer_note': customer_note,
                'store_note': '',
                'status': 'pending'
            }
            
            # create boarding revservation record
            ReservationBoarding.objects.create(**reservation_data)
            
            return Response({
                'success': True,
                'message': '住宿預約建立成功',
                'user_name': user_name,
                'checkin_datetime': checkin_datetime.strftime("%Y-%m-%d %H:%M"),
                'checkout_datetime': checkout_datetime.strftime("%Y-%m-%d %H:%M"),
                'boarding_duration': boarding_duration,
                'room_type': room_type,
                'store_phone': store_phone,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'建立預約時發生錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'], url_path='store')
    def create_reservation_storesides(self, request):
        """建立住宿預約(店家端)"""
        
        try:
            store_id = request.query_params.get('store_id')
            service_type = request.data.get('service_type')
            user_name = request.data.get('user_name')
            user_phone = request.data.get('user_phone')
            pet_name = request.data.get('pet_name')           
            pet_type = request.data.get('pet_type')  
            pet_breed = request.data.get('pet_breed')        
            room_type = request.data.get('room_type')
            pick_up_service = request.data.get('pick_up_service', False)
            check_in_date = request.data.get('check_in_date')
            check_in_time = request.data.get('check_in_time')
            check_out_date = request.data.get('check_out_date')
            check_out_time = request.data.get('check_out_time')
            store_note = request.data.get('store_note', '')

            # verify input data
            if not all([store_id, user_id, service_type, user_name, user_phone, 
                        pet_name, pet_type, pet_breed, pick_up_service,
                        room_type, check_in_date, check_in_time, check_out_date, check_out_time,
                        store_note]):
                
                return Response(
                    {'error': '缺少必要的預約資訊'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # customer info
            user = CustomersProfile.objects.filter(full_name=user_name, phone=user_phone)
            user_id = user.id

            # store info
            store = get_object_or_404(Store, id=store_id)
            store_name = store.store_name
            store_phone = store.phone

            # create reservation_id
            reservation_id = create_reservation_id(service_type)
            
            # combine check-in and check-out datetime
            try:
                check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                check_in_time_obj = datetime.strptime(check_in_time, "%H:%M").time()
                checkin_datetime = datetime.combine(check_in_date_obj, check_in_time_obj)
                
                check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()
                check_out_time_obj = datetime.strptime(check_out_time, "%H:%M").time()
                checkout_datetime = datetime.combine(check_out_date_obj, check_out_time_obj)
                
                # verify check-out time that must smaller than check-in time
                if checkout_datetime <= checkin_datetime:
                    return Response(
                        {'error': '退房時間必須晚於入住時間'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                boarding_duration = (check_out_date_obj - check_in_date_obj).days

            except ValueError:
                return Response(
                    {'error': '日期或時間格式錯誤，請使用 YYYY-MM-DD 和 HH:MM 格式'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # create time slots (every 30 minutes)
            boarding_time_slots = []
            current_datetime = checkin_datetime
            
            while current_datetime < checkout_datetime:
                boarding_time_slots.append(current_datetime)
                current_datetime += timedelta(minutes=30)
            
            # get room type from BoardingService model by store_id
            try:
                boarding_services = BoardingService.objects.filter(store_id=store_id)
                if not boarding_services.exists():
                    return Response(
                        {'error': '該店家沒有提供住宿服務'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # get room info according to room type
                room_type_obj = None
                for boarding_service in boarding_services:
                    try:
                        room_type_obj = BoardingService.objects.get(
                            boarding_service=boarding_service,
                            room_type=room_type
                        )
                        break
                    except BoardingService.DoesNotExist:
                        continue
                
                if not room_type_obj:
                    return Response(
                        {'error': f'找不到房型 "{room_type}"'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                room_count = room_type_obj.room_count
                
            except Exception as e:
                return Response(
                    {'error': f'查詢房型資訊時發生錯誤: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # check last room count
            for time_slot in boarding_time_slots:
                occupied_rooms = BoardingSchedules.objects.filter(
                    store_name=store_name,
                    room_type=room_type,
                    unavailable_time=time_slot
                ).count()
                
                if occupied_rooms >= room_count:
                    return Response(
                        {'error': f'房型 "{room_type}" 在 {time_slot.strftime("%Y-%m-%d %H:%M")} 時段已額滿'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            reservation_data = {
                'reservation_id': reservation_id,
                'store_name': store_name,
                'user_name': user_name,
                'user_phone': user_phone,
                'pet_name': pet_name,
                'room_type': room_type,
                'checkin_date': checkin_datetime,
                'checkout_date': checkout_datetime,
                'customer_note': '',
                'store_note': store_note,
                'status': 'pending'
            }
            
            # create boarding revservation record
            ReservationBoarding.objects.create(**reservation_data)
            
            return Response({
                'success': True,
                'message': '住宿預約建立成功',
                'user_name': user_name,
                'checkin_datetime': checkin_datetime.strftime("%Y-%m-%d %H:%M"),
                'checkout_datetime': checkout_datetime.strftime("%Y-%m-%d %H:%M"),
                'boarding_duration': f'{boarding_duration}天',
                'room_type': room_type,
                'store_phone': store_phone,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'建立預約時發生錯誤: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
        
def create_reservation_id(service_type):
    if service_type == 'grooming':
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        microsecond_part = f"{now.microsecond:06d}"[-4:]  
        
        return f"GR{timestamp}{microsecond_part}"
    
    elif service_type == 'boarding':
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        microsecond_part = f"{now.microsecond:06d}"[-4:]  
        
        return f"BD{timestamp}{microsecond_part}"
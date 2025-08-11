# origin
from datetime import datetime, timedelta, date

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# app
from .models import GroomingSchedules, BoardingSchedules
from pet_booking.services.models import GroomingService, GroomingServicePricing, BoardingService, BoardingRoomType, BoardingRoomPricing
from pet_booking.stores.models import Store
from .serializers import ReservationGroomingSerializer
from pet_booking.customers.serializers import PetSerializer
from pet_booking.customers.models import CustomersProfile, Pet


class StoreInfoViewSet(viewsets.ModelViewSet):
    """
    ViewSet 1: 根據URL參數獲取店家基本資訊和服務選項
    GET /api/store-info/get_store_data/?store_id=1&user_id=5
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get_store_data')
    def get_store_data(self, request):
        """
        獲取店家資訊和服務選項
        GET /api/store-info/get_store_data/?store_id=1&user_id=5
        """

        store_id = request.query_params.get('store_id')
        user_id = request.query_params.get('user_id')
        service_type = request.query_params.get('service_type')

        # 驗證必要參數
        if not store_id:
            return Response(
                {'error': '缺少店家ID參數'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 獲取用戶的寵物資訊（如果有user_id）
        user_pets = {}
        if user_id:
            pets = Pet.objects.filter(user_id=user_id)
            for pet in pets:
                user_pets[pet.id] = {
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
            # 獲取店家資訊
            store = get_object_or_404(Store, id=store_id)
            
            if service_type == 'grooming':
                # 獲取店家美容服務標題陣列
                grooming_services = GroomingService.objects.filter(store_id=store_id)
                service_titles = [service.service_title for service in grooming_services]
                
                # 取得該店當天不可預約的時間
                today = date.today()
                grooming_schedules = GroomingSchedules.objects.filter(
                    store_name = store.store_name,
                    date=today
                )

                unavailable_times_grooming = []
                for schedule in grooming_schedules:
                    if schedule.unavailable_time:
                        unavailable_times_grooming.append(schedule.unavailable_time)

                response_data = {
                    'store': {
                        'id': store.id,
                        'store_name': store.store_name,
                        'daily_opening_time': store.daily_opening_time,
                        'daily_closing_hours': store.daily_closing_hours,
                    },
                    'service_titles': service_titles,
                    'user_pets': user_pets,
                    'user_id': user_id,
                    'unavailable_times': unavailable_times_grooming
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            elif service_type == 'boarding':
                # 根據 store_id 獲取所有住宿服務
                boarding_services = BoardingService.objects.filter(store_id=store_id)
                boarding_data = []
                
                for boarding_service in boarding_services:
                    try:
                        boarding_room_type = BoardingRoomType.objects.get(boarding_service=boarding_service)
                        
                        try:
                            boarding_pricing = BoardingRoomPricing.objects.get(room_type=boarding_room_type)
                            
                            pricing_info = {
                                'duration': boarding_pricing.duration,
                                'duration_unit': boarding_pricing.duration_unit,
                                'pricing': boarding_pricing.pricing,
                                'overtime_rate': boarding_pricing.overtime_rate,
                                'overtime_charging': boarding_pricing.overtime_charging
                            }
                            
                        except BoardingRoomPricing.DoesNotExist:
                            pricing_info = None
                        
                        room_type_data = {
                            'id': boarding_room_type.id,
                            'species': boarding_room_type.species,
                            'room_type': boarding_room_type.room_type,
                            'room_count': boarding_room_type.room_count,
                            'pet_available_amount': boarding_room_type.pet_available_amount,
                            'pricing_info': pricing_info
                        }
                        
                    except BoardingRoomType.DoesNotExist:
                        room_type_data = None
                    
                    boarding_data.append({
                        'id': boarding_service.id,
                        'cleaning_frequency': boarding_service.cleaning_frequency,
                        'introduction': boarding_service.introduction,
                        'created_at': boarding_service.created_at,
                        'updated_at': boarding_service.updated_at,
                        'room_type_info': room_type_data
                    })
                
                # 取得該店當天不可預約的時間
                today = date.today()
                boarding_schedules = BoardingSchedules.objects.filter(
                    store_name = store.store_name,
                    date=today
                )

                unavailable_times_boarding = []
                for schedule in boarding_schedules:
                    if schedule.unavailable_time:
                        unavailable_times_boarding.append(schedule.unavailable_time)
                        
                response_data = {
                    'store': {
                        'store_name': store.store_name,
                        'daily_opening_time': store.daily_opening_time,
                        'daily_closing_hours': store.daily_closing_hours,
                        'unavailable_times': unavailable_times_boarding
                    },
                    'boarding_services': boarding_data,
                    'user_pets': user_pets,
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
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get_pet_info')
    def get_pet_info(self, request):
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
        
    @action(detail=False, methods=['post'], url_path='save_pet_info')
    def save_pet_info(self, request):
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
                # 如果寵物已存在，進行更新
                pet = Pet.objects.get(user_id=user_id, name=pet_name)
                
                # 使用PetSerializer進行驗證和更新
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
                # 如果寵物不存在，建立新的寵物資料
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
    """
    ViewSet 2: 根據寵物資料和選擇的服務項目計算總時間和總價格
    POST /api/grooming-calculation/calculate_grooming_cost/?store_id=1&user_id=5
    """
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='calculate_grooming_cost')
    def calculate_grooming_cost(self, request):
        """
        計算美容服務的總時間和總價格
        POST /api/grooming-calculation/calculate_grooming_cost/?store_id=1&user_id=5
        
        Request Body:
        {
            "pet_data": {
                "name": "小白",
                "species": "dog",
                "fur_amount": "long",
                "size": "medium"
            },
            "selected_services": ['剪毛', '洗澡']  
        }
        """
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

            # 驗證店家是否存在
            store = get_object_or_404(Store, id=store_id)

            # 獲取寵物資料
            pet_name = pet_data.get('name')
            pet_species = pet_data.get('species')
            pet_fur_amount = pet_data.get('fur_amount')
            pet_size = pet_data.get('size')

            # 驗證寵物必要資料
            if not all([pet_name, pet_species, pet_fur_amount, pet_size]):
                return Response(
                    {'error': '寵物資料不完整，需要提供: name, species, fur_amount, size'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 初始化計算變數
            total_price = 0

            # 逐一處理選擇的服務
            for service_title in selected_services:
                try:
                    # 獲取美容服務
                    grooming_service = GroomingService.objects.get(
                        service_title=service_title, 
                        store_id=store_id
                    )

                    # 根據寵物資料找到對應的定價
                    result = GroomingServicePricing.objects.filter(
                        grooming_service_id=grooming_service,
                        species=pet_species,
                        pet_size=pet_size,
                        fur_amount=pet_fur_amount
                    ).first()

                    if result:
                        total_price += int(result.pricing)

                    else:
                        Response({'error': f'找不到對應店家的服務'}, status=status.HTTP_404_NOT_FOUND)

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
    """
    ViewSet: 處理美容預約表單提交
    POST /api/reservation/grooming/?user_id=<user_id>
    """
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='create_reservation')
    def create_reservation(self, request):
        """
        建立美容預約
        POST /api/reservation/grooming/?user_id=<user_id>
        
        Request Body:
        {
            "store_name": "店家名稱",
            "pet_name": "小白",
            "selected_services": ["剪毛", "洗澡"],
            "pick_up_service": true,
            "reservation_date": "2025-08-15",
            "reservation_time": "14:30",
            "customer_note": "客戶備註"
        }
        
        URL Parameters:
        - user_id: 用戶ID
        - store_id: 店家ID (可選，如果未提供會從store_name查找)
        """
        try:
            # 取得請求資料
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

            # 驗證必要欄位
            if not all([store_name, store_id, user_id, pet_name, selected_services, reservation_date, reservation_time]):
                return Response(
                    {'error': '缺少必要的預約資訊'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # customer info
            customer_profile = get_customer_profile(user_id, "用戶不存在")
            user_name = customer_profile.full_name
            user_phone = customer_profile.phone or ''

            # store info
            store = get_store(store_name, "店家不存在")
            store_phone = store.phone

            # pet info
            pet = get_pet(user_id, pet_name)
            pet_type = pet.species
            pet_size = pet.size
            pet_fur_amount = pet.fur_amount

            # 計算總美容時間
            total_grooming_duration = 0

            for service_title in selected_services:
                try:
                    # 獲取美容服務
                    grooming_service = GroomingService.objects.get(
                        service_title=service_title,
                        store_id=store_id
                    )

                    # 根據寵物資料找到對應的定價和時間
                    grooming_result = GroomingServicePricing.objects.filter(
                        grooming_service_id=grooming_service,
                        species=pet_type,
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

            total_grooming_duration_count = int(round(total_grooming_duration / 15 - 1, 0))
            
            # 組合預約日期時間
            try:
                reservation_date_obj = datetime.strptime(reservation_date, "%Y-%m-%d").date()
                reservation_time_obj = datetime.strptime(reservation_time, "%H:%M").time()
                reservation_datetime = datetime.combine(reservation_date_obj, reservation_time_obj)

            except ValueError:
                return Response(
                    {'error': '日期時間格式錯誤'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 計算服務所佔據的時間段
            grooming_unavailable_time = []
            current_time = reservation_datetime
            
            # 遍歷 total_grooming_duration_count + 1 次
            for i in range(total_grooming_duration_count + 1):
                grooming_unavailable_time.append(current_time.time())
                current_time += timedelta(minutes=15)
            
            # 檢查時段衝突
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

            # 生成預約ID
            reservation_id = create_reservation_id(service_type)


            # 準備預約資料
            reservation_data = {
                'reservation_id': reservation_id,
                'store_name': store_name,
                'user_name': user_name,
                'user_phone': user_phone,
                'grooming_services_name': selected_services,
                'pet_name': pet.name,
                'pet_type': pet.species,
                'pet_breed': pet.breed,
                'pick_up_service': pick_up_service,
                'reservation_time': reservation_datetime,
                'customer_note': customer_note,
                'store_note': '',
                'status': 'pending'
            }

            # 使用序列化器進行驗證
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
        

class BoardingRoomInfoViewSet(viewsets.ModelViewSet):
    """
    ViewSet: 根據店家ID和寵物類別獲取住宿房間類型資訊
    POST /api/boarding-room-info/get_room_types/?store_id=1&pet_species=cat
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='get_room_types')
    def get_room_types(self, request):
        """
        根據店家ID和寵物類別獲取對應的房間類型
        POST /api/boarding-room-info/get_room_types/?store_id=1
        
        Request Body:
        {
            "pet_species": "dog"  # 從 save_pet_info 傳來的寵物類別
        }
        """
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
            except Store.DoesNotExist:
                return Response(
                    {'error': '店家不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            boarding_services = BoardingService.objects.filter(store_id=store_id)
            
            if not boarding_services.exists():
                return Response(
                    {'error': '該店家沒有提供住宿服務'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            room_types_data = []
            
            for boarding_service in boarding_services:
                try:
                    room_type = BoardingRoomType.objects.get(
                        boarding_service=boarding_service,
                        species=pet_species
                    )
                    
                    # 獲取房間價格資訊
                    try:
                        room_pricing = BoardingRoomPricing.objects.get(room_type=room_type)
                        pricing_info = {
                            'duration': room_pricing.duration,
                            'duration_unit': room_pricing.duration_unit,
                            'pricing': room_pricing.pricing,
                            'overtime_rate': room_pricing.overtime_rate,
                            'overtime_charging': room_pricing.overtime_charging
                        }
                    except BoardingRoomPricing.DoesNotExist:
                        pricing_info = None
                    
                    # 組合房間類型資料
                    room_type_data = {
                        'id': room_type.id,
                        'species': room_type.species,
                        'room_type': room_type.room_type,
                        'room_count': room_type.room_count,
                        'pet_available_amount': room_type.pet_available_amount,
                        'pricing_info': pricing_info
                    }
                    room_types_data.append(room_type_data)
                    
                except BoardingRoomType.DoesNotExist:
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
    """
    ViewSet: 根據到店離店時間和房型計算住宿費用
    POST /api/boarding-calculation/calculate_boarding_cost/?store_id=1
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='calculate_boarding_cost')
    def calculate_boarding_cost(self, request):
        """
        計算住宿服務的總晚數和總價格
        POST /api/boarding-calculation/calculate_boarding_cost/?store_id=1&pet_species=cat
        
        Request Body:
        {   
            "room_type": "精緻房",
            "check_in_date": "2025-07-18",
            "check_in_time": "09:30",
            "check_out_date": "2025-07-20",
            "check_out_time": "18:00",
        }

        URL 參數:
        store_id, pet_species
        """
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
                    boarding_room_type = BoardingRoomType.objects.get(**room_type_filters)
                    room_pricings = BoardingRoomPricing.objects.filter(room_type=boarding_room_type)
                    
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
                        
                except BoardingRoomType.DoesNotExist:
                    continue

                except BoardingRoomType.MultipleObjectsReturned:
                    # 如果找到多筆資料，表示資料設計有問題，但仍然處理第一筆
                    boarding_room_type = BoardingRoomType.objects.filter(**room_type_filters).first()
                    room_pricings = BoardingRoomPricing.objects.filter(room_type=boarding_room_type)
                    
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
            
            # 計算最終住宿金額
            # 根據 boarding_duration 找出合適的價格方案
            best_pricing_option = None
            total_cost = 0
            
            # 篩選有效的價格選項（排除沒有價格資訊的項目）
            valid_pricing_options = [detail for detail in service_details if 'pricing' in detail]
            
            if not valid_pricing_options:
                return Response(
                    {'error': '沒有找到有效的價格資訊'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 優先選擇 duration_in_days <= boarding_duration 且最接近的方案
            suitable_options = [
                option for option in valid_pricing_options 
                if option['duration_in_days'] <= boarding_duration
            ]
            
            if suitable_options:
                # 選擇最大的 duration_in_days（最接近但不超過 boarding_duration）
                best_pricing_option = max(suitable_options, key=lambda x: x['duration_in_days'])
            else:
                # 如果沒有合適的選項，選擇最小的 duration_in_days
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
        except BoardingRoomType.DoesNotExist:
            return Response(
                {'error': '房間類型不存在'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except BoardingRoomPricing.DoesNotExist:
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
    """
    ViewSet: 處理住宿預約表單提交
    POST /api/reservation/boarding/?user_id=123
    """
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='boarding')
    def create_reservation(self, request):
        """
        建立美容預約
        POST /api/reservation/boarding/?user_id=123&store_id=12
        
        Request Body:
        {
            "store_name": "店家名稱",
            "pet_name": "小白",
            "pick_up_service": true,
            "room_type": '小型犬',
            "check_in_date": "2025-08-15",
            "check_in_time": "09:30",
            "check_out_date": "2025-08-17"
            "check_out_time": "14:30",
            "customer_note": "客戶備註"
        }
        
        URL Parameters:
        - user_id: 用戶ID
        - store_id: 店家ID 
        """
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
            if not all([store_name, store_id, user_id, room_type, pick_up_service, check_in_date, check_in_time, check_out_date, check_out_time]):
                return Response(
                    {'error': '缺少必要的預約資訊'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # customer info
            customer_profile = get_customer_profile(user_id, "用戶不存在")
            user_name = customer_profile.full_name
            user_phone = customer_profile.phone or ''

            # store info
            store = get_store(store_name, "店家不存在")
            store_phone = store.phone

            # 生成預約ID
            reservation_id = create_reservation_id(service_type)
            
            # 組合 check-in 和 check-out 日期時間
            try:
                check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                check_in_time_obj = datetime.strptime(check_in_time, "%H:%M").time()
                checkin_datetime = datetime.combine(check_in_date_obj, check_in_time_obj)
                
                check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()
                check_out_time_obj = datetime.strptime(check_out_time, "%H:%M").time()
                checkout_datetime = datetime.combine(check_out_date_obj, check_out_time_obj)
                
                # 驗證 check-out 時間必須晚於 check-in 時間
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
            
            # 生成時間間隔陣列（每半小時一筆）
            boarding_time_slots = []
            current_datetime = checkin_datetime
            
            while current_datetime < checkout_datetime:
                boarding_time_slots.append(current_datetime)
                current_datetime += timedelta(minutes=30)
            
            # 透過 store_id 取得 BoardingService 中的房型資訊
            try:
                boarding_services = BoardingService.objects.filter(store_id=store_id)
                if not boarding_services.exists():
                    return Response(
                        {'error': '該店家沒有提供住宿服務'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # 根據 room_type 找到對應的房型資訊
                room_type_obj = None
                for boarding_service in boarding_services:
                    try:
                        room_type_obj = BoardingRoomType.objects.get(
                            boarding_service=boarding_service,
                            room_type=room_type
                        )
                        break
                    except BoardingRoomType.DoesNotExist:
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
            
            # 檢查每個時間段的房間可用性
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
            
            # 建立住宿預約記錄
            from .models import ReservationBoarding
            
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
            
            # 建立預約記錄
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
        
def get_customer_profile(user_id, message):
    try:
        return CustomersProfile.objects.get(user_id=user_id)
    except CustomersProfile.DoesNotExist:
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)


def get_store(store_name, message):
    try:
        return Store.objects.get(store_name=store_name)
    except Store.DoesNotExist:
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

def get_pet(user_id, pet_name):
    try:
        return Pet.objects.get(user_id=user_id, name=pet_name)
    except Pet.DoesNotExist:
        return Response({'error': f'找不到名為 "{pet_name}" 的寵物'}, status=status.HTTP_404_NOT_FOUND)

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
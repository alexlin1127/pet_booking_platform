# origin
from datetime import datetime, timedelta, date

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# app
from .models import GroomingSchedules
from services.models import GroomingService, GroomingServicePricing
from stores.models import Store
from .serializers import ReservationGroomingSerializer
from customers.serializers import PetSerializer
from customers.models import CustomersProfile, Pet


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

        # 驗證必要參數
        if not store_id:
            return Response(
                {'error': '缺少店家ID參數'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 獲取店家資訊
            store = get_object_or_404(Store, id=store_id)
            
            # 獲取店家美容服務標題陣列
            grooming_services = GroomingService.objects.filter(store_id=store_id)
            service_titles = [service.service_title for service in grooming_services]
            
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
            
            # 取得該店當天不可預約的時間
            today = date.today()
            grooming_schedules = GroomingSchedules.objects.filter(
                store_name = store.store_name,
                date=today
            )

            unavailable_times = []
            for schedule in grooming_schedules:
                if schedule.unavailable_time:
                    unavailable_times.append(schedule.unavailable_time)

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
                'unavailable_times': unavailable_times
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
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
    ViewSet 3: 處理美容預約表單提交
    POST /api/grooming-reservation/create_reservation/?user_id=<user_id>
    """
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='create_reservation')
    def create_reservation(self, request):
        """
        建立美容預約
        POST /api/grooming-reservation/create_reservation/?user_id=<user_id>
        
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
            store_name = request.data.get('store_name')
            store_id = request.query_params.get('store_id')
            user_id = request.query_params.get('user_id')
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
                
            try:
                customer_profile = CustomersProfile.objects.get(user_id=user_id)
                user_name = customer_profile.full_name
                user_phone = customer_profile.phone or ''

            except CustomersProfile.DoesNotExist:
                return Response(
                    {'error': '用戶不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )                

            try:
                store = Store.objects.get(store_name=store_name)
                store_phone = store.phone

            except Store.DoesNotExist:
                return Response(
                    {'error': '店家不存在'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # 根據 pet_name 和 user_id 獲取寵物資訊
            try:
                pet = Pet.objects.get(name=pet_name, user_id=user_id)
                pet_type = pet.species
                pet_size = pet.size
                pet_fur_amount = pet.fur_amount

            except Pet.DoesNotExist:
                return Response(
                    {'error': f'找不到名為 "{pet_name}" 的寵物'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

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
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            microsecond_part = f"{now.microsecond:06d}"[-4:]  
            reservation_id = f"GR{timestamp}{microsecond_part}"

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
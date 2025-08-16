# origin 
from datetime import timedelta

# third-party
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# app
from ..models import ReservationGrooming, ReservationBoarding, Orders
from ..serializers import ReservationGroomingSerializer, ReservationBoardingSerializer
from ...stores.models import Store
from ...customers.models import Pet, CustomersProfile



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class GroomingHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationGroomingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ReservationGrooming.objects.filter(status='finished')
        
        store_id = self.request.user.user_id
        if store_id is not None:
            store = Store.objects.get(user_id=store_id)
            store_name = store.store_name
            queryset = queryset.filter(store_name=store_name)
        
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):     

        store_id = request.user.user_id
        if not store_id:
            return Response(
                {'error': 'store_id parameter is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            history_data = []
            for reservation in page:
                history_data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': reservation.pet_breed,
                    'reservation_date': reservation.reservation_time.date(),
                    'service_type': 'grooming',
                    'status': reservation.status
                })
            
            return self.get_paginated_response({
                'service_type': 'grooming',
                'store_id': store_id,
                'results': history_data
            })
        
class BoardingHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationBoardingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ReservationBoarding.objects.filter(status='finished')
        
        store_id = self.request.user.user_id
        if store_id is not None:
            store = Store.objects.get(user_id=store_id)
            store_name = store.store_name
            queryset = queryset.filter(store_name=store_name)
        
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        store_id = request.user.user_id
        if not store_id:
            return Response(
                {'error': 'store_id parameter is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            history_data = []
            for reservation in page:
                user_id = CustomersProfile.objects.get(full_name=reservation.user_name, phone=reservation.user_phone).user_id
                pet_breed = Pet.objects.get(user_id=user_id, name=reservation.pet_name).breed
                history_data.append({
                     'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': pet_breed,  
                    'reservation_date': reservation.checkin_date.date(),
                    'service_type': 'boarding',
                    'status': reservation.status
                })
            
            # Return paginated response
            return self.get_paginated_response({
                'service_type': 'boarding',
                'store_id': store_id,
                'results': history_data
            })

class StoreNoteUpdateSerializer(serializers.Serializer):
    reservation_id = serializers.CharField(max_length=20, required=True)
    store_note = serializers.CharField(max_length=1000, required=True, allow_blank=True)

    def validate_reservation_id(self, value):
        """驗證 reservation_id 是否存在"""
        try:
            ReservationGrooming.objects.get(reservation_id=value)
        except ReservationGrooming.DoesNotExist:
            raise serializers.ValidationError("Reservation not found")
        return value
    
class StoreNoteUpdateViewSet(viewsets.ViewSet):
    '''更新店家備註'''
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        '''更新預約的店家備註'''
        serializer = StoreNoteUpdateSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = serializer.validated_data['reservation_id']
        store_note = serializer.validated_data['store_note']

        # 更新美容店家備註
        if reservation_id[:2] == 'GR':
            try:
                reservation = ReservationGrooming.objects.get(reservation_id=reservation_id)
                reservation.store_note = store_note
                reservation.save()

                return Response({
                    'message': 'Store note updated successfully',
                    'reservation_id': reservation_id,
                    'store_note': store_note
                }, status=status.HTTP_200_OK)

            except ReservationGrooming.DoesNotExist:
                return Response({
                    'error': 'Reservation not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        # 更新住宿店家備註
        elif reservation_id[:2] == 'BD':
            try:
                reservation = ReservationBoarding.objects.get(reservation_id=reservation_id)
                reservation.store_note = store_note
                reservation.save()

                return Response({
                    'message': 'Store note updated successfully',
                    'reservation_id': reservation_id,
                    'store_note': store_note
                }, status=status.HTTP_200_OK)

            except ReservationBoarding.DoesNotExist:
                return Response({
                    'error': 'Reservation not found'
                }, status=status.HTTP_404_NOT_FOUND)

# class ReservationDetailsViewSet(viewsets.ViewSet):
#     """預約詳情"""
#     permission_classes = [IsAuthenticated]
    
#     def list(self, request, *args, **kwargs):
#         '''取得預約詳情：根據 reservation_id 取得 confirmed 預約 + 該客戶在該店家的所有 finished 預約'''
#         reservation_id = request.query_params.get('reservation_id')

        
#         if not reservation_id:
#             return Response({
#                 'error': 'reservation_id is required'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         if reservation_id[:2] == 'GR':
#             try:
#                 # 取得指定的 confirmed 預約資料
#                 current_reservation = ReservationGrooming.objects.get(
#                     reservation_id=reservation_id,
#                     status='finished'
#                 )
#                 reservation_datetime = current_reservation.reservation_time
#                 reservation_date = reservation_datetime.date()
#                 reservation_start_time = reservation_datetime.time()
#                 end_datetime = reservation_datetime + timedelta(minutes=current_reservation.grooming_period)
#                 reservation_end_time = end_datetime.time() 

#                 current_reservation_data = {
#                     'reservation_id': current_reservation.reservation_id,
#                     'user_name': current_reservation.user_name,
#                     'user_phone': current_reservation.user_phone,
#                     'grooming_services_name': current_reservation.grooming_services_name,
#                     'pet_name': current_reservation.pet_name,
#                     'pet_breed': current_reservation.pet_breed,
#                     'pet_size': current_reservation.pet_size,
#                     'pick_up_service': current_reservation.pick_up_service,
#                     'reservation_date': reservation_date,
#                     'start_time': reservation_start_time,
#                     'end_time': reservation_end_time,
#                     'customer_note': current_reservation.customer_note,
#                     'store_note': current_reservation.store_note,
#                     'total_price': current_reservation.total_price,
#                     'grooming_duration': current_reservation.grooming_period
#                 }
#                 return Response(current_reservation_data, status=status.HTTP_200_OK)

#             except ReservationGrooming.DoesNotExist:
#                 return Response({
#                     'error': 'finished reservation not found',
#                     'details': f'No finished reservation found with ID: {reservation_id}'
#                 }, status=status.HTTP_404_NOT_FOUND)

#         elif reservation_id[:2] == 'BD':
#             try:
#                 current_reservation = ReservationBoarding.objects.get(
#                     reservation_id=reservation_id,
#                     status='finished'
#                 )

#                 # 透過 Orders 模型來取得 user_id
#                 order = Orders.objects.filter(reservation_boarding=current_reservation).first()
#                 user_id = order.user_id
                
#                 # 取得寵物品種和尺寸資訊
#                 pet = None
#                 pet_breed = None
#                 pet_size = None
#                 if user_id:
#                     pet = Pet.objects.filter(user_id=user_id, name=current_reservation.pet_name).values('breed', 'size').first()
#                     pet_breed = pet['breed'] if pet else None
#                     pet_size = pet['size'] if pet else None
                
#                 checkin_date = current_reservation.checkin_date.date()
#                 checkout_date = current_reservation.checkout_date.date()

#                 current_reservation_data = {
#                     'reservation_id': current_reservation.reservation_id,
#                     'user_name': current_reservation.user_name,
#                     'user_phone': current_reservation.user_phone,
#                     'pet_name': current_reservation.pet_name,
#                     'pet_breed': pet_breed,
#                     'pet_size': pet_size,
#                     'checkin_date': checkin_date,
#                     'checkout_date': checkout_date,
#                     'boarding_duration': current_reservation.boarding_durations,
#                     'pick_up_service': current_reservation.pick_up_service,
#                     'customer_note': current_reservation.customer_note,
#                     'store_note': current_reservation.store_note,
#                     'total_price': current_reservation.total_price,
#                     'service_type': '住宿'
#                 }

#                 return Response(current_reservation_data, status=status.HTTP_200_OK)

#             except ReservationBoarding.DoesNotExist:
#                 return Response({
#                     'error': 'finished reservation not found',
#                     'details': f'No finished reservation found with ID: {reservation_id}'
#                 }, status=status.HTTP_404_NOT_FOUND)
            
#         else:
#             return Response({
#                 'error': 'Invalid reservation ID format',
#                 'details': 'Reservation ID must start with "GR" for grooming or "BD" for boarding'
#             }, status=status.HTTP_400_BAD_REQUEST)


class CustomerObservationViewSet(viewsets.ViewSet):
    """
    顧客觀察名單管理
    - GET: 取得顧客預約資訊
    - POST: 將顧客加入黑名單
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def get_customer_info(self, request):
        """
        取得顧客預約資訊 (使用 query parameter)
        GET /api/reservations/customer-observation/get_customer_info/?reservation_id=GR001
        """
        reservation_id = request.query_params.get('reservation_id')
        print(reservation_id)

        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 處理美容預約
        if reservation_id[:2] == 'GR':
            try:
                reservation = ReservationGrooming.objects.get(reservation_id=reservation_id).first()
                
                customer_info = {
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': reservation.pet_breed,
                    'pet_size': reservation.pet_size,
                    'store_note': reservation.store_note or ''
                }
                
                return Response(customer_info, status=status.HTTP_200_OK)

            except ReservationGrooming.DoesNotExist:
                return Response({
                    'error': 'Reservation not found',
                    'details': f'No reservation found with ID: {reservation_id}'
                }, status=status.HTTP_404_NOT_FOUND)

        # 處理寄宿預約
        elif reservation_id[:2] == 'BD':
            try:
                reservation = ReservationBoarding.objects.get(reservation_id=reservation_id)
                order = Orders.objects.filter(reservation_boarding_id=reservation.reservation_id).first()
                user_id = order.user_id if order else None
                
                pet_breed = None
                pet_size = None
                if user_id:
                    pet = Pet.objects.filter(user_id=user_id, name=reservation.pet_name).values('breed', 'size').first()
                    pet_breed = pet['breed'] if pet else None
                    pet_size = pet['size'] if pet else None
                
                customer_info = {
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': pet_breed,
                    'pet_size': pet_size,
                    'store_note': reservation.store_note or ''
                }
                
                return Response(customer_info, status=status.HTTP_200_OK)

            except ReservationBoarding.DoesNotExist:
                return Response({
                    'error': 'Reservation not found',
                    'details': f'No reservation found with ID: {reservation_id}'
                }, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({
                'error': 'Invalid reservation ID format',
                'details': 'Reservation ID must start with "GR" for grooming or "BD" for boarding'
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        取得顧客預約資訊
        根據 reservation_id 取得顧客詳細資訊用於確認是否加入觀察名單
        """
        reservation_id = pk or request.query_params.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 處理美容預約
        if reservation_id[:2] == 'GR':
            try:
                reservation = ReservationGrooming.objects.get(reservation_id=reservation_id)
                
                customer_info = {
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': reservation.pet_breed,
                    'pet_size': reservation.pet_size,
                    'store_note': reservation.store_note or ''
                }
                
                return Response(customer_info, status=status.HTTP_200_OK)

            except ReservationGrooming.DoesNotExist:
                return Response({
                    'error': 'Reservation not found',
                    'details': f'No reservation found with ID: {reservation_id}'
                }, status=status.HTTP_404_NOT_FOUND)

        # 處理寄宿預約
        elif reservation_id[:2] == 'BD':
            try:
                reservation = ReservationBoarding.objects.get(reservation_id=reservation_id)
                order = Orders.objects.filter(reservation_boarding_id=reservation.reservation_id).first()
                user_id = order.user_id if order else None
                
                pet_breed = None
                pet_size = None
                if user_id:
                    pet = Pet.objects.filter(user_id=user_id, name=reservation.pet_name).values('breed', 'size').first()
                    pet_breed = pet['breed'] if pet else None
                    pet_size = pet['size'] if pet else None
                
                customer_info = {
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': pet_breed,
                    'pet_size': pet_size,
                    'store_note': reservation.store_note or ''
                }
                
                return Response(customer_info, status=status.HTTP_200_OK)

            except ReservationBoarding.DoesNotExist:
                return Response({
                    'error': 'Reservation not found',
                    'details': f'No reservation found with ID: {reservation_id}'
                }, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({
                'error': 'Invalid reservation ID format',
                'details': 'Reservation ID must start with "GR" for grooming or "BD" for boarding'
            }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        將顧客加入黑名單
        根據 reservation_id 找到對應的 Order 並將 blacklist 設為 True
        """
        reservation_id = request.data.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = None
            
            # 處理美容預約
            if reservation_id[:2] == 'GR':
                reservation = ReservationGrooming.objects.get(reservation_id=reservation_id)
                order = Orders.objects.filter(reservation_grooming_id=reservation.reservation_id).first()
            
            # 處理寄宿預約
            elif reservation_id[:2] == 'BD':
                reservation = ReservationBoarding.objects.get(reservation_id=reservation_id)
                order = Orders.objects.filter(reservation_boarding_id=reservation.reservation_id).first()
            
            else:
                return Response({
                    'error': 'Invalid reservation ID format',
                    'details': 'Reservation ID must start with "GR" for grooming or "BD" for boarding'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not order:
                return Response({
                    'error': 'Order not found',
                    'details': f'No order found for reservation ID: {reservation_id}'
                }, status=status.HTTP_404_NOT_FOUND)

            # 將顧客加入黑名單
            order.blacklist = True
            order.save()

            return Response({
                'message': 'Customer successfully added to blacklist',
                'reservation_id': reservation_id,
                'blacklist_status': True
            }, status=status.HTTP_200_OK)

        except (ReservationGrooming.DoesNotExist, ReservationBoarding.DoesNotExist):
            return Response({
                'error': 'Reservation not found',
                'details': f'No reservation found with ID: {reservation_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'error': 'Failed to add customer to blacklist',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['patch'], url_path='remove_blacklist')
    def remove_blacklist(self, request):
        """
        移除顧客黑名單
        根據 reservation_id 找到對應的 Order 並將 blacklist 設為 False
        """
        reservation_id = request.data.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = None
            
            # 處理美容預約
            if reservation_id[:2] == 'GR':
                reservation = ReservationGrooming.objects.get(reservation_id=reservation_id)
                order = Orders.objects.filter(reservation_grooming_id=reservation.reservation_id).first()
            
            # 處理寄宿預約
            elif reservation_id[:2] == 'BD':
                reservation = ReservationBoarding.objects.get(reservation_id=reservation_id)
                order = Orders.objects.filter(reservation_boarding_id=reservation.reservation_id).first()
            
            else:
                return Response({
                    'error': 'Invalid reservation ID format',
                    'details': 'Reservation ID must start with "GR" for grooming or "BD" for boarding'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not order:
                return Response({
                    'error': 'Order not found',
                    'details': f'No order found for reservation ID: {reservation_id}'
                }, status=status.HTTP_404_NOT_FOUND)

            # 移除顧客黑名單
            order.blacklist = False
            order.save()

            return Response({
                'message': 'Customer successfully removed from blacklist',
                'reservation_id': reservation_id,
                'blacklist_status': False
            }, status=status.HTTP_200_OK)

        except (ReservationGrooming.DoesNotExist, ReservationBoarding.DoesNotExist):
            return Response({
                'error': 'Reservation not found',
                'details': f'No reservation found with ID: {reservation_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'error': 'Failed to remove customer from blacklist',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
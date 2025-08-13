# origin 
from datetime import datetime, timedelta

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone

# app
from pet_booking.reservations.models import ReservationGrooming, Orders
from pet_booking.reservations.serializers import StoreNoteUpdateSerializer, OrdersSerializer
from pet_booking.stores.models import Store
from pet_booking.customers.models import CustomersProfile  


class ReservationPagination(PageNumberPagination):
    """自定義分頁類別"""
    page_size = 5  # 每頁顯示5筆資料
    page_size_query_param = 'page_size'  # 允許前端設定每頁筆數
    max_page_size = 50  # 最大每頁筆數限制


class GroomingReservationInfoViewSet(viewsets.ModelViewSet):
    '''顧客當日美容預約資訊'''
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='')
    def get_reservation_info_grooming(self, request):
        '''取得顧客當日美容預約資訊'''
        current_date = timezone.now().date()
        store_id = request.query_params.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # get customer booking with confirmed status
        confirmed_reservations = ReservationGrooming.objects.filter(
            store_name=store_name,
            reservation_time__date=current_date,
            status='confirmed'
        )

        # count customer booking with confirmed status
        confirmed_reservations_count = ReservationGrooming.objects.filter(
            store_name=store_name,
            status='confirmed'
        ).count()

        # count customer booking with pennding status
        pending_reservations_count = ReservationGrooming.objects.filter(
            store_name=store_name,
            reservation_time__date=current_date,
            status='pending'
        ).count()

        return Response({
            'store_name': store_name,
            'confirmed_reservations': confirmed_reservations.values(
                'reservation_id',
                'user_name',
                'user_phone',
                'grooming_services_name',
                'pet_name',
                'pet_type',
                'pet_breed',
                'pet_size',
                'pick_up_service',
                'reservation_time',
                'customer_note',
                'store_note',
                'total_price',
                'grooming_duration',
            ),
            'pending_reservations_count': pending_reservations_count,
            'confirmed_reservations_count': confirmed_reservations_count
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='update-store-note')
    def update_store_note(self, request):
        '''更新美容預約的店家備註'''
        serializer = StoreNoteUpdateSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = serializer.validated_data['reservation_id']
        store_note = serializer.validated_data['store_note']

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

class GroomingReservationManagementViewSet(viewsets.ModelViewSet):
    '''預約管理：處理待審核和近期預約'''
    permission_classes = [IsAuthenticated]
    pagination_class = ReservationPagination

    @action(detail=False, methods=['get'], url_path='all-reservations')
    def get_all_reservations_grooming(self, request):
        '''取得所有美容預約資料（待審核 + 近期預約）'''
        store_id = request.query_params.get('store_id')

        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # get grooming reservation with pending status
        pending_reservations = ReservationGrooming.objects.filter(
            store_name=store_name,
            status='pending'
        ).order_by('-created_at')

        # get grooming reservation with confirmed status
        confirmed_reservations = ReservationGrooming.objects.filter(
            store_name=store_name,
            status='confirmed'
        ).order_by('reservation_time')

        # 計算筆數
        pending_count = pending_reservations.count()
        confirmed_count = confirmed_reservations.count()

        # 處理 confirmed_reservations 的時間資料
        confirmed_reservations_data = []
        for reservation in confirmed_reservations:
            reservation_datetime = reservation.reservation_time
            reservation_date = reservation_datetime.date()
            reservation_start_time = reservation_datetime.time()
            
            # 計算預約結束時間
            start_datetime = reservation_datetime
            end_datetime = start_datetime + timedelta(minutes=reservation.grooming_period)
            reservation_end_time = end_datetime.time()
            
            confirmed_reservations_data.append({
                'reservation_id': reservation.reservation_id,
                'user_name': reservation.user_name,
                'user_phone': reservation.user_phone,
                'grooming_services_name': reservation.grooming_services_name,
                'pet_name': reservation.pet_name,
                'pet_type': reservation.pet_type,
                'pet_breed': reservation.pet_breed,
                'pet_size': reservation.pet_size,
                'pick_up_service': reservation.pick_up_service,
                'reservation_date': reservation_date,
                'reservation_start_time': reservation_start_time,
                'reservation_end_time': reservation_end_time,
                'customer_note': reservation.customer_note,
                'store_note': reservation.store_note,
                'total_price': reservation.total_price,
                'grooming_duration': reservation.grooming_period,
                'status': reservation.status,
            })

        return Response({
            'store_name': store_name,
            'pending_reservations': pending_reservations.values(
                'reservation_id',
                'user_name',
                'user_phone',
                'grooming_services_name',
                'pet_name',
                'pet_type',
                'pet_breed',
                'pet_size',
                'pick_up_service',
                'reservation_time',
                'customer_note',
                'store_note',
                'total_price',
                'grooming_duration',
                'status',
                'created_at'
            ),
            'confirmed_reservations': confirmed_reservations_data,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='pending-reservations')
    def get_pending_reservations(self, request):
        '''取得待審核預約資料（支援分頁）'''
        store_id = request.query_params.get('store_id')

        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # 取得待審核預約資料
        pending_reservations = ReservationGrooming.objects.filter(
            store_name=store_name,
            status='pending'
        ).order_by('-created_at')

        # 使用分頁
        page = self.paginate_queryset(pending_reservations)
        if page is not None:
            # 序列化分頁資料
            serialized_data = []
            for reservation in page:
                serialized_data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'grooming_services_name': reservation.grooming_services_name,
                    'pet_name': reservation.pet_name,
                    'pet_type': reservation.pet_type,
                    'pet_breed': reservation.pet_breed,
                    'pet_size': reservation.pet_size,
                    'pick_up_service': reservation.pick_up_service,
                    'reservation_time': reservation.reservation_time,
                    'customer_note': reservation.customer_note,
                    'store_note': reservation.store_note,
                    'total_price': reservation.total_price,
                    'grooming_duration': reservation.grooming_period,
                    'status': reservation.status,
                    'created_at': reservation.created_at
                })
            
            return self.get_paginated_response({
                'store_name': store_name,
                'reservations': serialized_data,
                'total_count': pending_reservations.count()
            })

        # 如果沒有分頁，回傳所有資料
        return Response({
            'store_name': store_name,
            'reservations': list(pending_reservations.values()),
            'total_count': pending_reservations.count()
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='confirmed-reservations')
    def get_confirmed_reservations(self, request):
        '''取得近期預約資料（支援分頁）'''
        store_id = request.query_params.get('store_id')

        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # 取得已確認預約資料
        confirmed_reservations = ReservationGrooming.objects.filter(
            store_name=store_name,
            status='confirmed'
        ).order_by('reservation_time')

        # 使用分頁
        page = self.paginate_queryset(confirmed_reservations)
        if page is not None:
            # 處理時間資料並序列化
            serialized_data = []
            for reservation in page:
                reservation_datetime = reservation.reservation_time
                reservation_date = reservation_datetime.date()
                reservation_start_time = reservation_datetime.time()
                
                # 計算預約結束時間
                start_datetime = reservation_datetime
                end_datetime = start_datetime + timedelta(minutes=reservation.grooming_period)
                reservation_end_time = end_datetime.time()
                
                serialized_data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'grooming_services_name': reservation.grooming_services_name,
                    'pet_name': reservation.pet_name,
                    'pet_type': reservation.pet_type,
                    'pet_breed': reservation.pet_breed,
                    'pet_size': reservation.pet_size,
                    'pick_up_service': reservation.pick_up_service,
                    'reservation_date': reservation_date,
                    'reservation_start_time': reservation_start_time,
                    'reservation_end_time': reservation_end_time,
                    'customer_note': reservation.customer_note,
                    'store_note': reservation.store_note,
                    'total_price': reservation.total_price,
                    'grooming_duration': reservation.grooming_period,
                    'status': reservation.status,
                })
            
            return self.get_paginated_response({
                'store_name': store_name,
                'reservations': serialized_data,
                'total_count': confirmed_reservations.count()
            })

        # 如果沒有分頁，回傳所有資料
        return Response({
            'store_name': store_name,
            'reservations': [],
            'total_count': confirmed_reservations.count()
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='confirm-reservation')
    def confirm_reservation(self, request):
        '''確認預約：將 pending 狀態改為 confirmed'''
        reservation_id = request.data.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = ReservationGrooming.objects.get(
                reservation_id=reservation_id,
                status='pending'
            )
            
            reservation.status = 'confirmed'
            reservation.save()

            return Response({
                'message': 'Reservation confirmed successfully',
                'reservation_id': reservation_id,
                'old_status': 'pending',
                'new_status': 'confirmed'
            }, status=status.HTTP_200_OK)

        except ReservationGrooming.DoesNotExist:
            return Response({
                'error': 'Pending reservation not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], url_path='cancel-reservation')
    def cancel_reservation(self, request):
        '''取消預約：將 pending 狀態改為 cancelled'''
        reservation_id = request.data.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = ReservationGrooming.objects.get(
                reservation_id=reservation_id,
                status='pending'
            )
            
            reservation.status = 'cancelled'
            reservation.save()

            return Response({
                'message': 'Reservation cancelled successfully',
                'reservation_id': reservation_id,
                'old_status': 'pending',
                'new_status': 'cancelled'
            }, status=status.HTTP_200_OK)

        except ReservationGrooming.DoesNotExist:
            return Response({
                'error': 'Pending reservation not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], url_path='cancel-confirmed-reservation')
    def cancel_confirmed_reservation(self, request):
        '''取消已確認預約：將 confirmed 狀態改為 cancelled'''
        reservation_id = request.data.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = ReservationGrooming.objects.get(
                reservation_id=reservation_id,
                status='confirmed'
            )
            
            reservation.status = 'cancelled'
            reservation.save()

            return Response({
                'message': 'Confirmed reservation cancelled successfully',
                'reservation_id': reservation_id,
                'old_status': 'confirmed',
                'new_status': 'cancelled'
            }, status=status.HTTP_200_OK)

        except ReservationGrooming.DoesNotExist:
            return Response({
                'error': 'Confirmed reservation not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], url_path='finish-reservation')
    def finish_reservation(self, request):
        '''完成預約：將 confirmed 狀態改為 finished 並創建訂單記錄'''
        reservation_id = request.data.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = ReservationGrooming.objects.get(
                reservation_id=reservation_id,
                status='confirmed'
            )
            
            # 根據 user_name 和 user_phone 查找 user_id
            try:
                customer_profile = CustomersProfile.objects.get(
                    full_name=reservation.user_name,
                    phone=reservation.user_phone
                )
                user_id = customer_profile.user_id

            except CustomersProfile.DoesNotExist:
                return Response({
                    'error': 'Customer profile not found',
                    'details': f'No customer found with name: {reservation.user_name} and phone: {reservation.user_phone}'
                }, status=status.HTTP_404_NOT_FOUND)
            
            except CustomersProfile.MultipleObjectsReturned:
                return Response({
                    'error': 'Multiple customer profiles found',
                    'details': f'Multiple customers found with name: {reservation.user_name} and phone: {reservation.user_phone}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            order_data = {
                'reservation_grooming': reservation.id,
                'user_id': user_id,
                'total_price': reservation.total_price,
                'status': 'completed',
                'blacklist': False
            }
            
            order_serializer = OrdersSerializer(data=order_data)
            
            if not order_serializer.is_valid():
                return Response({
                    'error': 'Order validation failed',
                    'details': order_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            reservation.status = 'finished'
            reservation.save()
            
            order = order_serializer.save()

            return Response({
                'message': 'Reservation finished successfully and order created',
                'reservation_id': reservation_id,
                'old_status': 'confirmed',
                'new_status': 'finished',
                'order_id': order.id,
                'order_total_price': order.total_price,
                'customer_name': reservation.user_name,
                'customer_phone': reservation.user_phone,
            }, status=status.HTTP_200_OK)

        except ReservationGrooming.DoesNotExist:
            return Response({
                'error': 'Confirmed reservation not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Failed to finish reservation',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='reservation-details')
    def get_reservation_details(self, request):
        '''取得預約詳情：根據 reservation_id 取得 confirmed 預約 + 該客戶在該店家的所有 finished 預約'''
        reservation_id = request.query_params.get('reservation_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 取得指定的 confirmed 預約資料
            current_reservation = ReservationGrooming.objects.get(
                reservation_id=reservation_id,
                status='confirmed'
            )

            reservation_date = current_reservation.reservation_time.date()
            reservation_start_time = current_reservation.reservation_time.time()
            reservation_duratuion = current_reservation.grooming_period
            reservation_end_time = reservation_start_time + timedelta(minutes=reservation_duratuion)

            finished_reservations = ReservationGrooming.objects.filter(
                store_name=current_reservation.store_name,
                user_name=current_reservation.user_name,
                user_phone=current_reservation.user_phone,
                status='finished'
            ).order_by('-updated_at')  

            current_reservation_data = {
                'reservation_id': current_reservation.reservation_id,
                'user_name': current_reservation.user_name,
                'user_phone': current_reservation.user_phone,
                'grooming_services_name': current_reservation.grooming_services_name,
                'pet_name': current_reservation.pet_name,
                'pet_breed': current_reservation.pet_breed,
                'pet_size': current_reservation.pet_size,
                'pick_up_service': current_reservation.pick_up_service,
                'reservation_date': reservation_date,
                'start_time': reservation_start_time,
                'end_time': reservation_end_time,
                'customer_note': current_reservation.customer_note,
                'store_note': current_reservation.store_note,
                'total_price': current_reservation.total_price,
                'grooming_period': current_reservation.grooming_period,
            }

            finished_reservations_data = finished_reservations.values(
                'reservation_id',
                'grooming_services_name',
                'pet_name',
                'pet_type',
                'pet_breed',
                'pet_size',
                'reservation_time',
                'store_note',
                'total_price',
            )

            return Response({
                'current_reservation': current_reservation_data,
                'finished_reservations': list(finished_reservations_data),
                'finished_count': finished_reservations.count(),
                'customer_info': {
                    'name': current_reservation.user_name,
                    'phone': current_reservation.user_phone,
                    'store_name': current_reservation.store_name
                }
            }, status=status.HTTP_200_OK)

        except ReservationGrooming.DoesNotExist:
            return Response({
                'error': 'Confirmed reservation not found',
                'details': f'No confirmed reservation found with ID: {reservation_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Failed to get reservation details',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
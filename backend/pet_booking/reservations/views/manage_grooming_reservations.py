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
from pet_booking.coupon.models import Coupon, CouponStatus

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class GroomingReservationInfoViewSet(viewsets.ReadOnlyModelViewSet):
    '''顧客當日美容預約資訊'''
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        current_date = timezone.now().date()
        store_id = self.request.query_params.get('store_id')
        if not store_id:
            return ReservationGrooming.objects.none()
        
        try:
            store = Store.objects.get(id=store_id)
            return ReservationGrooming.objects.filter(
                store_name=store.store_name,
                reservation_time__date=current_date,
                status='confirmed'
            )
        except Store.DoesNotExist:
            return ReservationGrooming.objects.none()
    
    def list(self, request, *args, **kwargs):
        '''取得顧客當日美容預約資訊'''
        current_date = timezone.now().date()
        store_id = request.query_params.get('store_id')
        
        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # get customer booking with confirmed status
        confirmed_reservations = ReservationGrooming.objects.filter(
            store_name=store_name,
            reservation_time__date=current_date,
            status='confirmed'
        )

        confirmed_reservations_count = confirmed_reservations.count()

        # count customer booking with pending status
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
                'grooming_period',
            ),
            'pending_reservations_count': pending_reservations_count,
            'confirmed_reservations_count': confirmed_reservations_count
        }, status=status.HTTP_200_OK)

class StoreNoteUpdateViewSet(viewsets.ViewSet):
    '''更新店家備註'''
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
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

class GroomingReservationManagementViewSet(viewsets.ViewSet):
    '''預約管理：處理待審核和近期預約'''
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['patch'], url_path='confirm')
    def confirm_reservation(self, request):
        '''確認預約：將 pending 狀態改為 confirmed，並可同時更新 store_note'''
        reservation_id = request.data.get('reservation_id')
        store_note = request.data.get('store_note', '') 
        
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
            reservation.store_note = store_note
            reservation.save()

            response_data = {
                'message': 'Reservation confirmed successfully',
                'reservation_id': reservation_id,
                'store_note': store_note,
                'old_status': 'pending',
                'new_status': 'confirmed'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ReservationGrooming.DoesNotExist:
            return Response({
                'error': 'Pending reservation not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], url_path='cancel')
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

    @action(detail=False, methods=['patch'], url_path='cancel-confirmed')
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

    @action(detail=False, methods=['patch'], url_path='complete')
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
                'reservation_grooming': reservation_id,
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

            # 處理優惠券：根據 reservation_id 找到對應的優惠券並更新狀態
            try:
                coupon = Coupon.objects.get(reservation_id=reservation_id)
                coupon.status = CouponStatus.USED
                coupon.order_id = str(order.id)
                coupon.save()
            except Coupon.DoesNotExist:
                pass
            except Exception as coupon_error:
                print(f"優惠券處理錯誤: {coupon_error}")

            try:
                store = Store.objects.get(store_name=reservation.store_name)
                used_coupons_count = Coupon.objects.filter(
                    store_id=store.id,
                    status=CouponStatus.USED
                ).count()
                used_coupons_total_revenue = 50 * int(used_coupons_count)
            except Store.DoesNotExist:
                used_coupons_count = 0

            reservation_datetime = reservation.reservation_time
            reservation_date = reservation_datetime.date()
            reservation_start_time = reservation_datetime.time()
            end_datetime = reservation_datetime + timedelta(minutes=reservation.grooming_period)
            reservation_end_time = end_datetime.time()

            return Response({
                'message': 'Reservation finished successfully and order created',
                'reservation_id': reservation_id,
                'old_status': 'confirmed',
                'new_status': 'finished',
                'order_id': order.id,
                'order_total_price': order.total_price,
                'customer_name': reservation.user_name,
                'customer_phone': reservation.user_phone,
                'reservation_date': reservation_date,
                'reservation_start_time': reservation_start_time,
                'reservation_end_time': reservation_end_time,
                'grooming_services_name': reservation.grooming_services_name,
                'pet_name': reservation.pet_name,
                'pet_type': reservation.pet_type,
                'pet_breed': reservation.pet_breed,
                'total_price': reservation.total_price,
                'pick_up_service': reservation.pick_up_service,
                'used_coupons_count': used_coupons_count,
                'used_coupons_total_revenue': used_coupons_total_revenue
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


class AllReservationsViewSet(viewsets.ViewSet):
    """所有預約資料（待審核 + 近期預約）"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
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
            end_datetime = reservation_datetime + timedelta(minutes=reservation.grooming_period)
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
                'grooming_period',
                'status',
                'created_at'
            ),
            'confirmed_reservations': confirmed_reservations_data,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
        }, status=status.HTTP_200_OK)


class ReservationDetailsViewSet(viewsets.ViewSet):
    """預約詳情"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
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
            reservation_datetime = current_reservation.reservation_time
            reservation_date = reservation_datetime.date()
            reservation_start_time = reservation_datetime.time()
            end_datetime = reservation_datetime + timedelta(minutes=current_reservation.grooming_period)
            reservation_end_time = end_datetime.time()
           
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
                'grooming_duration': current_reservation.grooming_period,
            }

            finished_reservations_data = finished_reservations.values(
                'reservation_id',
                'grooming_services_name',
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


class PendingReservationViewSet(viewsets.ReadOnlyModelViewSet):
    """待審核預約"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        store_id = self.request.query_params.get('store_id')
        if not store_id:
            return ReservationGrooming.objects.none()
        
        try:
            store = Store.objects.get(id=store_id)
            return ReservationGrooming.objects.filter(
                store_name=store.store_name,
                status='pending'
            ).order_by('-created_at')
        except Store.DoesNotExist:
            return ReservationGrooming.objects.none()
    
    def list(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serialized_data = []
            for reservation in page:
                reservation_datetime = reservation.reservation_time
                reservation_date = reservation_datetime.date()
                reservation_start_time = reservation_datetime.time()
                
                # 計算預約結束時間
                end_datetime = reservation_datetime + timedelta(minutes=reservation.grooming_period)
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
                    'created_at': reservation.created_at
                })
            
            return self.get_paginated_response({
                'store_name': store_name,
                'reservations': serialized_data,
                'total_count': queryset.count()
            })
        
        return Response({
            'store_name': store_name,
            'reservations': [],
            'total_count': queryset.count()
        }, status=status.HTTP_200_OK)


class UpcomingReservationViewSet(viewsets.ReadOnlyModelViewSet):
    """近期預約"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        store_id = self.request.query_params.get('store_id')
        if not store_id:
            return ReservationGrooming.objects.none()
        
        try:
            store = Store.objects.get(id=store_id)
            return ReservationGrooming.objects.filter(
                store_name=store.store_name,
                status='confirmed'
            ).order_by('reservation_time')
        except Store.DoesNotExist:
            return ReservationGrooming.objects.none()
    
    def list(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name
        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serialized_data = []
            for reservation in page:
                reservation_datetime = reservation.reservation_time
                reservation_date = reservation_datetime.date()
                reservation_start_time = reservation_datetime.time()
                
                # 計算預約結束時間
                end_datetime = reservation_datetime + timedelta(minutes=reservation.grooming_period)
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
                'total_count': queryset.count()
            })
        
        return Response({
            'store_name': store_name,
            'reservations': [],
            'total_count': queryset.count()
        }, status=status.HTTP_200_OK)
    
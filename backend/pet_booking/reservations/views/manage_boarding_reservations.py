# origin 
from collections import defaultdict
from datetime import timedelta

# third-party
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count

from pet_booking.stores.models import Store
from pet_booking.services.models import BoardingService
from pet_booking.reservations.models import ReservationBoarding
from pet_booking.reservations.serializers import StoreNoteUpdateSerializer, OrdersSerializer
from pet_booking.customers.models import CustomersProfile  
from pet_booking.customers.models import Pet
from pet_booking.coupon.models import Coupon, CouponStatus



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class BoardingRoomAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    取得貓狗個房型的房間數統計、待審核預約及近期預約數量
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        today = timezone.now().date()
        store_id = self.request.query_params.get('store_id')
        if not store_id:
            return ReservationBoarding.objects.none()
        
        try:
            store = Store.objects.get(id=store_id)
            return ReservationBoarding.objects.filter(
                store_name=store.store_name,
                status='confirmed',
                checkin_date__date__lte=today,
                checkout_date__date__gte=today
            )
        except Store.DoesNotExist:
            return ReservationBoarding.objects.none()
    
    def list(self, request, *args, **kwargs):
        today = timezone.now().date()
        store_id = request.query_params.get('store_id')

        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # 1. 根據 store_name 取得 BoardingService 資料
        boarding_services = BoardingService.objects.filter(
            store_id__store_name=store_name
        ).values('species', 'room_type', 'room_count', 'pet_available_amount')

        if not boarding_services.exists():
            return Response({
                'error': 'No boarding services found for this store'
            }, status=status.HTTP_404_NOT_FOUND)

        # 2. 取得 status=confirmed 且今日在 checkin_date 和 checkout_date 之間的預訂
        confirmed_reservations = ReservationBoarding.objects.filter(
            store_name=store_name,
            status='confirmed',
            checkin_date__date__lte=today,
            checkout_date__date__gte=today
        ).values('room_type').annotate(count=Count('id'))

        # 3. 取得 pending 和 confirmed 的總統計
        pending_count = ReservationBoarding.objects.filter(
            store_name=store_name,
            status='pending'
        ).count()

        confirmed_total_count = ReservationBoarding.objects.filter(
            store_name=store_name,
            status='confirmed'
        ).count()

        # 4. 組織資料結構
        # 先建立房型使用數量的字典
        room_usage = {}
        for reservation in confirmed_reservations:
            room_usage[reservation['room_type']] = reservation['count']

        # 5. 按 pet_type (species) 組織結果
        result_by_species = defaultdict(lambda: {
            'room_types': [],
        })

        for service in boarding_services:
            species = service['species']
            room_type = service['room_type']
            total_rooms = service['room_count']
            pet_available_count = service['pet_available_amount']

            # 計算該房型目前被使用的數量
            used_rooms = room_usage.get(room_type, 0)

            if species == 'cat':
                # 計算剩餘空位數量
                total_pet_slots = total_rooms * pet_available_count
                remaining_pet_slots = max(0, total_pet_slots - used_rooms)
                result_by_species[species]['room_types'].append({
                    'room_type': room_type,
                    'total_count': total_rooms,
                    'pet_available_count': pet_available_count,
                    'total_slots': total_pet_slots,
                    'used_slots': used_rooms,
                    'remaining_pet_slots': remaining_pet_slots
                })
            elif species == 'dog':
                # 計算剩餘房間數量
                remaining_rooms = max(0, total_rooms - used_rooms)
                result_by_species[species]['room_types'].append({
                    'room_type': room_type,
                    'total_count': total_rooms,
                    'used_count': used_rooms,
                    'remaining_count': remaining_rooms,
                })

        # 6. 格式化最終回傳資料
        return Response({
            'store_id': store_id,
            'store_name': store_name,
            'date': today.isoformat(),
            'species_data': dict(result_by_species),
            'pending_count': pending_count,
            'confirmed_count': confirmed_total_count
        }, status=status.HTTP_200_OK)


class BoardingStoreNoteUpdateViewSet(viewsets.ViewSet):
    '''更新住宿預約的店家備註'''
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = StoreNoteUpdateSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = serializer.validated_data['reservation_id']
        store_note = serializer.validated_data['store_note']

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


class BoardingReservationManagementViewSet(viewsets.ViewSet):
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
            reservation = ReservationBoarding.objects.get(
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

        except ReservationBoarding.DoesNotExist:
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
            reservation = ReservationBoarding.objects.get(
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

        except ReservationBoarding.DoesNotExist:
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
            reservation = ReservationBoarding.objects.get(
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

        except ReservationBoarding.DoesNotExist:
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
            reservation = ReservationBoarding.objects.get(
                reservation_id=reservation_id,
                status='confirmed'
            )
            
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
                'reservation_boarding': reservation_id,
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

            checkin_date = reservation.checkin_date
            checkout_date = reservation.checkout_date
            boarding_durations = (checkout_date.date() - checkin_date.date()).days

            return Response({
                'message': 'Reservation finished successfully and order created',
                'reservation_id': reservation_id,
                'old_status': 'confirmed',
                'new_status': 'finished',
                'customer_name': reservation.user_name,
                'customer_phone': reservation.user_phone,
                'checkin_date': checkin_date,
                'checkout_date': checkout_date,
                'boarding_duration': boarding_durations,
                'room_type': reservation.room_type,
                'pet_name': reservation.pet_name,
                'pick_up_service': reservation.pick_up_service,
                'total_price': reservation.total_price,
                'used_coupons_count': used_coupons_count,
                'used_coupons_total_revenue': used_coupons_total_revenue
            }, status=status.HTTP_200_OK)

        except ReservationBoarding.DoesNotExist:
            return Response({
                'error': 'Confirmed reservation not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Failed to finish reservation',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BoardingAllReservationsViewSet(viewsets.ViewSet):
    """所有預約資料（待審核 + 近期預約）"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        '''取得所有住宿預約資料（待審核 + 近期預約）'''
        store_id = request.query_params.get('store_id')
        user_id = request.query_params.get('user_id')

        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        # get boarding reservation with pending status
        pending_reservations = ReservationBoarding.objects.filter(
            store_name=store_name,
            status='pending'
        ).order_by('-created_at')

        # get boarding reservation with confirmed status
        confirmed_reservations = ReservationBoarding.objects.filter(
            store_name=store_name,
            status='confirmed'
        ).order_by('checkin_date')

        pending_count = pending_reservations.count()
        confirmed_count = confirmed_reservations.count()

        confirmed_reservations_data = []

        for reservation in confirmed_reservations:
            pet = Pet.objects.filter(user_id=user_id, name=reservation.pet_name).values('breed', 'size').first()
            pet_breed = pet['breed'] if pet else None

            confirmed_reservations_data.append({
                'reservation_id': reservation.reservation_id,
                'user_name': reservation.user_name,
                'user_phone': reservation.user_phone,
                'pet_name': reservation.pet_name,
                'pet_breed': pet_breed,
                'pick_up_service': reservation.pick_up_service,
                'checkin_date': reservation.checkin_date.date(),
                'status': reservation.status,
            })

        pending_reservations_data = []

        for reservation in pending_reservations:
            pet = Pet.objects.filter(user_id=user_id, name=reservation.pet_name).values('breed', 'size').first()
            pet_breed = pet['breed'] if pet else None

            pending_reservations_data.append({
                'reservation_id': reservation.reservation_id,
                'user_name': reservation.user_name,
                'user_phone': reservation.user_phone,
                'pet_name': reservation.pet_name,
                'pet_breed': pet_breed,
                'pick_up_service': reservation.pick_up_service,
                'checkin_date': reservation.checkin_date.date(),
                'status': reservation.status,
            })

        return Response({
            'store_name': store_name,
            'pending_reservations': pending_reservations_data,
            'confirmed_reservations': confirmed_reservations_data,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
        }, status=status.HTTP_200_OK)


class BoardingReservationDetailsViewSet(viewsets.ViewSet):
    """預約詳情"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        '''取得預約詳情：根據 reservation_id 取得 confirmed 預約 + 該客戶在該店家的所有 finished 預約'''
        reservation_id = request.query_params.get('reservation_id')
        user_id = request.query_params.get('user_id')
        
        if not reservation_id:
            return Response({
                'error': 'reservation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_reservation = ReservationBoarding.objects.get(
                reservation_id=reservation_id,
                status='confirmed'
            )
           
            finished_reservations = ReservationBoarding.objects.filter(
                store_name=current_reservation.store_name,
                user_name=current_reservation.user_name,
                user_phone=current_reservation.user_phone,
                status='finished'
            ).order_by('-updated_at')  

            pet = Pet.objects.filter(user_id=user_id, name=current_reservation.pet_name).values('breed', 'size').first()
            pet_breed = pet['breed'] if pet else None
            pet_size = pet['size'] if pet else None
            checkin_date = current_reservation.checkin_date.date()
            checkout_date = current_reservation.checkout_date.date()

            current_reservation_data = {
                'reservation_id': current_reservation.reservation_id,
                'user_name': current_reservation.user_name,
                'user_phone': current_reservation.user_phone,
                'pet_name': current_reservation.pet_name,
                'pet_breed': pet_breed,
                'pet_size': pet_size,
                'checkin_date': checkin_date,
                'checkout_date': checkout_date,
                'boarding_duration': current_reservation.boarding_durations,
                'pick_up_service': current_reservation.pick_up_service,
                'customer_note': current_reservation.customer_note,
                'store_note': current_reservation.store_note,
                'total_price': current_reservation.total_price,
                'service_type': '住宿'
            }

            finished_reservations_data = finished_reservations.values(
                'reservation_id',
                'checkin_date',
                'room_type',
                'boarding_duration',
                'total_price',
                'store_note'
            )

            return Response({
                'current_reservation': current_reservation_data,
                'finished_reservations': list(finished_reservations_data),
                'finished_count': finished_reservations.count()
            }, status=status.HTTP_200_OK)

        except ReservationBoarding.DoesNotExist:
            return Response({
                'error': 'Confirmed reservation not found',
                'details': f'No confirmed reservation found with ID: {reservation_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Failed to get reservation details',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BoardingPendingReservationViewSet(viewsets.ReadOnlyModelViewSet):
    """待審核預約"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def list(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        queryset = ReservationBoarding.objects.filter(
            store_name=store_name,
            status='pending'
        ).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serialized_data = []
            for reservation in page:
                
                serialized_data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': reservation.pet_breed,
                    'checkin_date': reservation.checkin_date,
                    'room_type': reservation.room_type,
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


class BoardingUpcomingReservationViewSet(viewsets.ReadOnlyModelViewSet):
    """近期預約"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def list(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({
                'error': 'store_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        store = get_object_or_404(Store, id=store_id)
        store_name = store.store_name

        queryset = ReservationBoarding.objects.filter(
                store_name=store_name,
                status='confirmed'
            ).order_by('checkin_date')
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serialized_data = []
            for reservation in page:
                 serialized_data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'pet_name': reservation.pet_name,
                    'pet_breed': reservation.pet_breed,
                    'checkin_date': reservation.checkin_date,
                    'room_type': reservation.room_type,
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


class BoardingPendingReservationDetailViewSet(viewsets.ViewSet):
    """待審核預約詳情 - 用於審核 Modal 視窗"""
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request):
        '''根據 reservation_id 取得待審核預約的詳細資訊'''
        try:
            user_id = request.query_params.get('user_id')
            reservation_id = request.query_params.get('reservation_id')
            reservation = ReservationBoarding.objects.get(
                reservation_id=reservation_id,
                status='pending'
            )
            
            # 取得寵物品種資訊
            pet = Pet.objects.filter(user_id=user_id, name=reservation.pet_name).values('breed', 'size').first()
            pet_breed = pet['breed']
            pet_size = pet['size']
            
            # 計算住宿天數
            checkin_date = reservation.checkin_date.date()
            checkout_date = reservation.checkout_date.date()
            boarding_durations = (checkout_date - checkin_date).days
            
            reservation_data = {
                'reservation_id': reservation.reservation_id,
                'user_name': reservation.user_name,
                'user_phone': reservation.user_phone,
                'pet_name': reservation.pet_name,
                'pet_breed': pet_breed,
                'pet_size': pet_size,
                'service_type': "住宿",
                'checkin_time': checkin_date.strftime("%Y/%m/%d"),
                'checkout_time': checkout_date.strftime("%Y/%m/%d"),
                'booking_duration': boarding_durations,
                'room_type': reservation.room_type,
                'total_amount': f"NT${reservation.total_price}",
                'pickup_service': '是' if reservation.pick_up_service else '否',
                'total_price': reservation.total_price,
                'customer_note': reservation.customer_note,
                'store_note': reservation.store_note
            }
            
            return Response(reservation_data, status=status.HTTP_200_OK)
            
        except ReservationBoarding.DoesNotExist:
            return Response({
                'error': 'Pending reservation not found',
                'details': f'No pending reservation found with ID: {reservation_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Failed to get reservation details',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
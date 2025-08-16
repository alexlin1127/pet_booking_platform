# origin 
from datetime import timedelta

# third-party
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

# app
from ..models import ReservationGrooming, ReservationBoarding
from ..serializers import ReservationGroomingSerializer, ReservationBoardingSerializer
from ...stores.models import Store
from ...customers.models import Pet


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RiskGroomingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing risk grooming reservation history.
    Returns finished grooming reservations for blacklist management.
    
    Query Parameters:
    - store_id: Required. The store ID to filter reservations
    - service_type: Optional. Should be "grooming" for this endpoint
    """
    serializer_class = ReservationGroomingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Filter grooming reservations by store_id and status=finished
        """
        queryset = ReservationGrooming.objects.filter(status='finished')
        
        store_id = self.request.query_params.get('store_id', None)
        if store_id is not None:
            store = get_object_or_404(Store, id=store_id)
            store_name = store.store_name
            queryset = queryset.filter(store_name=store_name)
        
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        Return list of finished grooming reservations with specified fields
        """
        service_type = request.query_params.get('service_type', None)
        if service_type and service_type != 'grooming':
            return Response(
                {'error': 'Invalid service_type. Expected "grooming".'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        store_id = request.query_params.get('store_id', None)
        if not store_id:
            return Response(
                {'error': 'store_id parameter is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = []
            for reservation in page:
                data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'service_type': 'grooming',
                    'reservation_date': reservation.reservation_time.date(),
                    'blacklist_status': True
                })
            
            return self.get_paginated_response({
                'service_type': 'grooming',
                'store_id': store_id,
                'results': data
            })
        

class RiskBoardingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing risk boarding reservation history.
    Returns finished boarding reservations for blacklist management.
    
    Query Parameters:
    - store_id: Required. The store ID to filter reservations
    - service_type: Optional. Should be "boarding" for this endpoint
    """
    serializer_class = ReservationBoardingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Filter boarding reservations by store_id and status=finished
        """
        queryset = ReservationBoarding.objects.filter(status='finished')
        
        store_id = self.request.query_params.get('store_id', None)
        if store_id is not None:
            # Get store_name from Store model using store_id
            store = get_object_or_404(Store, id=store_id)
            store_name = store.store_name
            queryset = queryset.filter(store_name=store_name)
        
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        Return list of finished boarding reservations with specified fields
        """
        service_type = request.query_params.get('service_type', None)
        if service_type and service_type != 'boarding':
            return Response(
                {'error': 'Invalid service_type. Expected "boarding".'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        store_id = request.query_params.get('store_id', None)
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
                    'reservation_date': reservation.checkin_date.date(),
                    'service_type': 'boarding',
                    'blacklist_status': True
                })
            
            return self.get_paginated_response({
                'service_type': 'boarding',
                'store_id': store_id,
                'results': history_data
            })
        

class RiskStoreNoteUpdateSerializer(serializers.Serializer):
    reservation_id = serializers.CharField(max_length=20, required=True)
    store_note = serializers.CharField(max_length=1000, required=True, allow_blank=True)

    def validate_reservation_id(self, value):
        """驗證 reservation_id 是否存在"""
        try:
            ReservationGrooming.objects.get(reservation_id=value)
        except ReservationGrooming.DoesNotExist:
            raise serializers.ValidationError("Reservation not found")
        return value
    

class RiskStoreNoteUpdateViewSet(viewsets.ViewSet):
    '''更新風險客戶店家備註'''
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        '''更新預約的店家備註'''
        serializer = RiskStoreNoteUpdateSerializer(data=request.data, partial=True)
        
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

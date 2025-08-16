# third-party
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# app
from ..models import ReservationGrooming, ReservationBoarding
from ..serializers import ReservationGroomingSerializer, ReservationBoardingSerializer
from ..models import Orders


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RiskGroomingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationGroomingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        orders = Orders.objects.filter(blacklist=True).exclude(reservation_grooming_id__isnull=True)
        grooming_reservation_ids = orders.values_list('reservation_grooming_id', flat=True)
        queryset = ReservationGrooming.objects.filter(reservation_id__in=grooming_reservation_ids)
        return queryset

    def list(self, request, *args, **kwargs):
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
                'results': data
            })
        

class RiskBoardingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationBoardingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        orders = Orders.objects.filter(blacklist=True).exclude(reservation_boarding_id__isnull=True)
        boarding_reservation_ids = orders.values_list('reservation_boarding_id', flat=True)
        queryset = ReservationBoarding.objects.filter(reservation_id__in=boarding_reservation_ids)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = []
            for reservation in page:
                data.append({
                    'reservation_id': reservation.reservation_id,
                    'user_name': reservation.user_name,
                    'user_phone': reservation.user_phone,
                    'service_type': 'boarding',
                    'checkin_date': reservation.checkin_date.date(),
                    'blacklist_status': True
                })

            return self.get_paginated_response({
                'service_type': 'boarding',
                'results': data
            })
        

class RiskStoreNoteUpdateViewSet(viewsets.ViewSet):
    '''更新風險客戶店家備註'''
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        reservation_id = request.data.get('reservation_id')
        store_note = request.data.get('store_note')
        
        if reservation_id[:2] == 'GR':
            try:
                reservation = ReservationGrooming.objects.get(reservation_id=reservation_id)
                reservation.store_note = store_note
                reservation.save()

            except ReservationGrooming.DoesNotExist:
                return Response({
                    'error': 'Reservation not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        elif reservation_id[:2] == 'BD':
            try:
                reservation = ReservationBoarding.objects.get(reservation_id=reservation_id)
                reservation.store_note = store_note
                reservation.save()

            except ReservationBoarding.DoesNotExist:
                return Response({
                    'error': 'Reservation not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
                'message': 'Store note updated successfully',
                'reservation_id': reservation_id,
                'store_note': store_note
            }, status=status.HTTP_200_OK)

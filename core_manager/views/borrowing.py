from core_manager.models.borrowing import Borrowing
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Book
from ..serializers.borrowing import BorrowingBulkReturnSerializer, BorrowingCreateSerializer, BorrowingSerializer
from ..services.borrowing import BorrowingService

class BorrowingViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'book', 'user']

    def get_queryset(self):
        """Filter queryset based on user role"""
        if self.request.user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='bulk-borrow')
    def bulk_borrow(self, request):
        """Borrow multiple books in one transaction"""
        try:
            book_ids = request.data.get('book_ids', [])
            days = int(request.data.get('days', BorrowingService.DEFAULT_MAX_BORROWING_DAYS))
            data = {
                'book_ids': book_ids,
                'days': days
            }
            serializer = BorrowingCreateSerializer(data=data, context={'request': request})
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            books = Book.objects.filter(id__in=book_ids, available_copies__gt=0)
            BorrowingService.create_bulk_borrowings(
                user=request.user,
                books=books,
                days=days
            )
            return Response({'message': 'Books borrowed successfully'}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='bulk-return')
    def bulk_return(self, request):
        """Return multiple books in one transaction"""
        try:
            serializer = BorrowingBulkReturnSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            borrowings = Borrowing.objects.filter(id__in=serializer.validated_data['borrowing_ids'], user=request.user)
            BorrowingService.return_bulk_books(borrowings)
            return Response({'message': 'Books returned successfully'}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=['get'], url_path='my-borrowings')
    def my_borrowings(self, request):
        """Get current user's borrowings"""
        borrowings = BorrowingService.get_user_borrowings(request.user)
        serializer = self.get_serializer(borrowings, many=True)
        return Response(serializer.data)

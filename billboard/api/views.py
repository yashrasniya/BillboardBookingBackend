import razorpay
import django
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from razorpay_app.models import Create_payment_link, razorpay_gateway_detail
from .serializers import cities, Address_serializers, BillBoard_serializers, BookingHistorySerializer
from ..models import Address, BillBoard, bookingHistory

try:
    RGD = razorpay_gateway_detail.objects.all()[0]
    callBackUrl = RGD.call_back_url
    # client = razorpay.Client(auth=("rzp_test_u01RD7HTlF1ysu", "oJclH13vmmj5evdT5HeKXrOG"))pxcGYJTKy2rc2fSIoLTlvrJA
    client = razorpay.Client(auth=(RGD.razorpay_id, RGD.razorpay_SECRET))
except (django.db.utils.ProgrammingError, razorpay_gateway_detail.DoesNotExist, django.db.utils.OperationalError,
        IndexError) as e:
    callBackUrl = ''

    print(e)


class cities_list(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(cities(Address.objects.all(), many=True).data)


class address_list(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.GET.get('city'):
            return Response(Address_serializers(Address.objects.filter(city=request.GET.get('city')), many=True).data)
        return Response(Address_serializers(Address.objects.filter(), many=True).data)


class billBoard(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        if id:
            if BillBoard.objects.filter(id=id):
                billBoard_obj = BillBoard.objects.get(id=id)
                return Response(BillBoard_serializers(billBoard_obj, context={'request': request}).data)
            else:
                return Response({'message': 'Bill Board id not found'}, status=404)
        else:
            billBoard_obj = BillBoard.objects.filter()
            if request.GET.get('city', '') and request.GET.get('address', ''):
                print(request.GET.get('city', ''), request.GET.get('address', ''), billBoard_obj)
                billBoard_obj = billBoard_obj.filter(address__city=request.GET.get('city'),
                                                     address__address=request.GET.get('address'))
                print(billBoard_obj)
            if request.GET.get('banner_type', ''):
                billBoard_obj = billBoard_obj.filter(banner_type=request.GET.get('banner_type', ''))
            if request.GET.get('location_type', ''):
                billBoard_obj = billBoard_obj.filter(location_type=request.GET.get('location_type'))
            if request.GET.get('lessTprice', ''):
                billBoard_obj = billBoard_obj.filter(price__lte=request.GET.get('lessTprice'))
            if request.GET.get('higherTprice', ''):
                billBoard_obj = billBoard_obj.filter(price__hte=request.GET.get('higherTprice'))

            return Response(BillBoard_serializers(billBoard_obj, many=True, context={'request': request}).data)


class BillBoardHistoryViewSet(ListAPIView):
    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated]

    def error_message(self, message, status=400):
        return Response({'error': message}, status=status)

    def get_queryset(self):
        return bookingHistory.objects.filter(user=self.request.user).order_by('-start_date')

    def post(self, request, format=None):
        print(request.data, request.GET, request.POST)
        if request.data.get('start_date', '') and request.data.get('billboard', ''):

            if not bookingHistory.objects.filter(end_date__gte=request.data.get('start_date'),
                                                 billboard=request.data.get('billboard'),
                                                 payment__status='0'
                                                 ):
                serializer = BookingHistorySerializer(data=request.data)
                if serializer.is_valid() and BillBoard.objects.get(id=request.data.get('billboard')):
                    obj = serializer.save(user=self.request.user,
                                          billboard=BillBoard.objects.get(id=request.data.get('billboard')),
                                          )
                    obj.fetching_link(callBackUrl=request.data.get('callBackUrl'))

                    return Response(serializer.data, status=200)
                else:
                    return self.error_message(serializer.errors)
            else:
                return self.error_message('Bill Board already booked', status=400)
        else:
            return self.error_message('data is missing', status=400)


class BillBoardHistoryCartViewSet(ListAPIView):
    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated]

    def error_message(self, message, status=400):
        return Response({'error': message}, status=status)

    def get_queryset(self):
        return bookingHistory.objects.filter(user=self.request.user).order_by('-start_date')


    def post(self, request, format=None):
        import json
        if request.data.get('billboard', ''):
            callBackUrl = request.data.get('callBackUrl', RGD.call_back_url)

            payment = Create_payment_link.objects.create(amount='0',
                                                         user=request.user,

                                                         callBackUrl=callBackUrl
                                                         )
            for i in json.loads(request.data.get('billboard', '')):
                print(not i.get('start_date',''),not i.get("billboard",''))
                if not i.get('start_date','') or  not i.get("billboard",''):
                    return Response({'error': 'Data is not filled'}, status=400)
                if not bookingHistory.objects.filter(end_date__gte=i.get('start_date'),
                                                     billboard=i.get("billboard"),
                                                     payment__status='0'
                                                     ):
                    serializer = BookingHistorySerializer(data=i)
                    if serializer.is_valid() and BillBoard.objects.get(id=i.get("billboard")):

                        obj = bookingHistory.objects.create(**serializer.validated_data,
                                                            user=self.request.user,
                                                            billboard=BillBoard.objects.get(id=i.get("billboard")),
                                                            payment=payment
                                                            )
                        payment.amount = int(payment.amount)+((obj.end_date - obj.start_date).days / 30) * int(obj.billboard.price)
                        payment.save()


                    else:
                        return self.error_message(serializer.errors)
                else:

                    return self.error_message(f'{BillBoard.objects.get(id=i.get("billboard"))}, Bill Board already booked', status=400)
            print(payment.amount)
            return Response(payment.fetching_link(price=payment.amount,callBackUrl=callBackUrl))
        else:
            return self.error_message('data is missing', status=400)

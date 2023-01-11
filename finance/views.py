import datetime
import requests
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status
from finance.models import Bill, Coupon
from finance.serializers import CouponSerializer

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
description = 'رزرو صندلی در فضای کار اشتراکی مکین'
CallbackURL = 'http://127.0.0.1:8000/finance/verify/'


class PayOrderAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, order_id):
        bill = Bill.objects.get(id=order_id)
        # request.session['order_pay'] = {
        #     'order_id': bill.id,
        # }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": bill.price,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number, "email": "a@b.com"}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyAPI(APIView):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Bill.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_payed = True
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse('Transaction failed or canceled by user')


class CouponApplyAPI(APIView):
    serializer_class = CouponSerializer

    def post(self, request, order_id):
        now = datetime.datetime.now()
        srz_data = CouponSerializer(instance=request.POST)
        if srz_data.is_valid():
            code = srz_data.data['code']
            try:
                coupon = Coupon.objects.get(code=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
            except Coupon.DoesNotExist:
                return Response({'msg': 'coupon does not exist'})
            order = Bill.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return Response({'msg': 'coupon applied'})
        return Response(srz_data.errors)


class GetThisMonthIncome(APIView):
    def post(self, request):
        pass


class GetSpecificMonthIncome(APIView):
    def post(self, request):
        pass

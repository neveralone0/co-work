from rest_framework.views import APIView, Response, status
from .serializers import *
from .models import *


class GetAllImage(APIView):
    serializer_class = ImageSerializer

    def get(self, request):
        images = Images.objects.all()
        srz_data = self.serializer_class(instance=images, many=True)
        return Response(srz_data.data)


class UploadImage(APIView):
    serializer_class = ImageSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'msg': 'image uploaded'}, status=status.HTTP_201_CREATED)
        return Response({srz_data.errors})


class DeleteImage(APIView):
    def delete(self, request):
        id = request.data['id']
        img = Images.objects.filter(id=id)
        img.delete()
        return Response({'msg': 'deleted'})


class ListDeleteImages(APIView):
    def delete(self, request):
        ids = request.data['ids']
        imgs = Images.objects.filter(id=ids)
        for img in imgs:
            img.delete()
        return Response({'msg': 'deleted'})


class ContactUsGet(APIView):
    serializer_class = ContactUsSerializer

    def get(self, request):
        info = ContactUs.objects.get(pk=1)
        srz_data = self.serializer_class(instance=info)
        return Response(srz_data.data)


class ContactUsUpdate(APIView):
    def post(self, request):
        info = ContactUs.objects.get(pk=1)
        srz_data = self.serializer_class(data=request.data, instance=info)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'msg': 'information updated'})


class CardAPI(APIView):
    serializer_class = CardSerializer

    def get(self, request):
        cards = Cards.objects.all()
        srz_data = self.serializer_class(instance=cards, many=True)
        return Response(srz_data.data)

    def post(self, request):
        for card in request.data:
            obj = Cards.objects.get(id=card['id'])
            srz_data = self.serializer_class(data=card, instance=obj)
            if srz_data.is_valid():
                srz_data.save()
            return Response({'msg': 'cards updated'})


# class AddLi(APIView):
#     serializer_class = LiSerializer
#
#     def post(self, request):
#         srz_data = self.serializer_class(data=request.data)
#         if srz_data.is_valid():
#             srz_data.save()
#             return Response({'msg': 'li added'})

#
# class UpdateLi(APIView):
#     serializer_class = LiSerializer
#
#     def put(self, request, pk):
#         lis = Li.objects.get(pk=pk)
#         srz_data = self.serializer_class(instance=lis, data=request.data, many=True)
#         if srz_data.is_valid():
#             srz_data.save()
#             return Response({'msg': 'li updated'})
#
#
# class DeleteLi(APIView):
#     def delete(self, request, pk):
#         li = Li.objects.get(pk=pk)
#         li.delete()
#         return Response({'msg': 'li deleted'})


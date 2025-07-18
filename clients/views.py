from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, Branch
from .serializers import ClientSerializerDetails, ClientBranchCreateSerializer, ClientBranchListSerializer, ClientSerializerList, ClientBranchUpdateSerializer, ClientOptionSerializer, ClientBranchOptionSerializer

# Create your views here.
class ClientViewSet(generics.ListCreateAPIView):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializerList
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'name',]
    search_fields = ['id', 'name',]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved clients list',
            'data': response.data
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client created successfully',
            'data': response.data
        })

   

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializerDetails
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client details retrieved successfully',
            'data': response.data
        })
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client updated successfully',
            'data': response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client updated successfully',
            'data': response.data
        })
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client deleted successfully'
        })

class ClientBranchList(generics.ListAPIView):
    queryset = Branch.objects.all().order_by('id')
    serializer_class = ClientBranchListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client']
    search_fields = ['id', 'name',]

    def get(self, request, *args, **kwargs):
        print("query_params:", request.query_params)

        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved branches list',
            'data': response.data
        })
    
class ClientBranchCreate(generics.CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch created successfully',
            'data': response.data
        })

class ClientBranchSDetail(generics.RetrieveDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch details retrieved successfully',
            'data': response.data
        })
class ClientBranchUpdate(generics.UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchUpdateSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch updated successfully',
            'data': response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch updated successfully',
            'data': response.data
        })
    
class ClientOptionsView(generics.ListAPIView):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientOptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]



    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Clients options retrieved successfully',
            'data': response.data
        })

class ClientBranchOptionsView(generics.ListAPIView):
    serializer_class = ClientBranchOptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client']
    search_fields = ['id', 'name']

    def get_queryset(self):
        queryset = Branch.objects.all().order_by('id')

        # دعم client_id في حال الفرونت يرسله بهذا الشكل
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)

        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branches options retrieved successfully',
            'data': response.data
        })


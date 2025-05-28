from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Cart, CartItem
from rest_framework.generics import DestroyAPIView
from .serializers import (
    CategorySerializer, ProductSerializer,
    CartSerializer, CartItemSerializer,
    AddCartItemSerializer
)
from .serializers import ProductSerializer

# Catégories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {'request': self.request}

# Produits
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

# Voir le panier
class CurrentCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_validated=False)
        return cart

    def get_serializer_context(self):
        return {'request': self.request}

# Ajouter un produit au panier
class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Produit non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user, is_validated=False)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = cart_item.quantity + quantity if not created else quantity
        cart_item.save()

        return Response({"Success": "Produit ajouté au panier"}, status=status.HTTP_200_OK)

# Valider le panier
class CartValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user, is_validated=False)
        except Cart.DoesNotExist:
            return Response({"detail": "Aucun panier à valider."}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({"detail": "Le panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

        cart.is_validated = True
        cart.save()
        return Response({"detail": "Panier validé avec succès."})
    
    

# Supprimer un produit (admin ou vendeur)
class DeleteProductView(DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        return super().delete(request, *args, **kwargs)

# Supprimer un produit du panier
class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            cart = Cart.objects.get(user=request.user, is_validated=False)
        except Cart.DoesNotExist:
            return Response({"detail": "Panier introuvable."}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({"detail": "Produit supprimé du panier."}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Ce produit n'est pas dans votre panier."}, status=status.HTTP_404_NOT_FOUND)
        
        
class ProductListSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('search')
        category_id = self.request.query_params.get('category')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | # type: ignore
                Q(description__icontains=search_query) # type: ignore
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from client.api.serializers import (
    AccountSerializer,
    CardSerializer,
    TransactionSerializer,
)
from client.models import Client
from transactions.models import Transaction


class SessionAuthMixing:
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AccountListView(generics.ListAPIView, SessionAuthMixing):
    serializer_class = AccountSerializer

    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        return client.accounts.all()


class AccountDetailView(generics.RetrieveAPIView, SessionAuthMixing):
    serializer_class = AccountSerializer

    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        return client.accounts.all()


class TransactionListView(generics.ListAPIView, SessionAuthMixing):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        return Transaction.objects.filter(account__user=client)


class TransactionDetailView(generics.RetrieveAPIView, SessionAuthMixing):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        return Transaction.objects.filter(account__user=client)


class CardListView(generics.ListAPIView, SessionAuthMixing):
    serializer_class = CardSerializer

    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        return client.cards.all()


class CardDetailView(generics.RetrieveAPIView, SessionAuthMixing):
    serializer_class = CardSerializer

    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        return client.cards.all()

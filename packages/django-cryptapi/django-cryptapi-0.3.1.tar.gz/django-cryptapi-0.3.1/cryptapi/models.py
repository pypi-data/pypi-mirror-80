from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from .choices import COINS, STATUS, TOKEN_DICT


class Provider(models.Model):
    coin = models.CharField(_('Coin'), max_length=16, choices=COINS, unique=True)
    cold_wallet = models.CharField(_('Cold Wallet'), max_length=128)
    active = models.BooleanField(_('Active'), default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.get_coin_display())


class Request(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(_('Order ID'), default='', max_length=128)
    nonce = models.CharField(_('Nonce'), max_length=32, default='')
    address_in = models.CharField(_('Payment Address'), max_length=128, default='', null=True)
    address_out = models.CharField(_('Receiving Address'), max_length=128, default='', null=True)
    value_requested = models.DecimalField(_('Value Requested'), default=0, max_digits=65, decimal_places=0)
    status = models.CharField(_('Status'), choices=STATUS, max_length=16, default='', null=True)
    raw_request_url = models.CharField(_('Request URL'), max_length=8192, default='', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        qs = self.payment_set.all()

        if qs.exists():
            return qs.aggregate(sum=Sum('value_paid')).get('sum', 0)

        return 0

    @property
    def total_pending(self):
        qs = self.payment_set.filter(pending=True)

        if qs.exists():
            return qs.aggregate(sum=Sum('value_paid')).get('sum', 0)

        return 0

    @property
    def total_confirmed(self):
        qs = self.payment_set.filter(pending=False)

        if qs.exists():
            return qs.aggregate(sum=Sum('value_paid')).get('sum', 0)

        return 0

    def set_value(self, value, commit=False):
        _coin = self.provider.coin.lower()
        _token = TOKEN_DICT.get(_coin)

        if _token:
            value = value / (10 ** _token[4])

        self.value_requested = value

        if commit:
            self.save()

    def __str__(self):
        return "#{}, {}#{}, {} ({})".format(self.id, _('Order'), self.order_id, self.get_status_display(), self.timestamp.strftime('%x %X'))

    class Meta:
        unique_together = (('provider', 'order_id'),)


class Payment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    value_paid = models.DecimalField(_('Value Paid'), default=0, max_digits=65, decimal_places=0)
    value_received = models.DecimalField(_('Value Received'), default=0, max_digits=65, decimal_places=0)
    value_paid_coin = models.DecimalField(_('Value Paid Coin'), default=0, max_digits=65, decimal_places=18)
    value_received_coin = models.DecimalField(_('Value Received Coin'), default=0, max_digits=65, decimal_places=18)
    txid_in = models.CharField(_('TXID in'), max_length=256, default='')
    txid_out = models.CharField(_('TXID out'), max_length=256, default='')
    pending = models.BooleanField(default=True)
    confirmations = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def coin(self):
        return self.request.provider.coin

    def __str__(self):
        return "#{}, {}, {} ({})".format(self.request.id, self.value_paid, self.request.provider.get_coin_display(), self.timestamp.strftime('%x %X'))


class RequestLog(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    raw_data = models.CharField(max_length=8192)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{} ({})".format(self.request_id, self.timestamp.strftime('%x %X'))


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    raw_data = models.CharField(max_length=8192)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{} ({})".format(self.payment_id, self.timestamp.strftime('%x %X'))

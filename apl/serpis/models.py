from django.db import models
from django.contrib.auth.models import User



def foto_orderan(instance, filename):
	return '/'.join(['foto', str(instance.orderan.pk), filename])


class Orang(models.Model):
	user 			= models.OneToOneField(
			User, on_delete=models.CASCADE, related_name='orang'
		)
	pendapatan 		= models.IntegerField(default=0)

class Orderan(models.Model):
	keluhan 		= models.TextField(blank=False, null=False)
	penanganan 		= models.TextField(blank=True, null=True, default="")
	STATUS			= (
			('1', "Tertunda"),
			('2', "Dikerjakan"),
			('3', "Selesai"),
		)
	status 			= models.CharField(max_length=1, choices=STATUS, default="1")
	pelanggan 		= models.CharField(max_length=125, blank=False, null=False)
	alamat 			= models.TextField(blank=False, null=False)
	telp 			= models.CharField(max_length=30, blank=False, null=False)
	tgl_masuk		= models.DateField(auto_now_add=True, auto_now=False)
	tgl_keluar 		= models.DateField(blank=True, null=True)
	biaya_total		= models.IntegerField(default=0)


class Rincian(models.Model):
	orderan 		= models.ForeignKey(Orderan, on_delete=models.CASCADE, related_name='rincian_orderan')
	ket 			= models.CharField(max_length=125, blank=False, null=False)
	biaya 			= models.IntegerField(default=0)


class Gambar(models.Model):
	orderan 		= models.ForeignKey(Orderan, on_delete=models.CASCADE, related_name='gambar_orderan')
	gambar 			= models.ImageField(
			upload_to=foto_orderan,
		)

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import datetime
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from django.contrib import messages




def masuk(request):
	if request.method == 'POST':
		username		= request.POST.get('username')
		password		= request.POST.get('password')
		user 			= authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'Login Berhasil !!!')
			return redirect('serpis:beranda')
		else:
			messages.error(request, 'Login Gagal !!!')
			return redirect('serpis:masuk')
	return render(request, 'dalem/masuk.html', {'title': 'Login'})


@login_required
def beranda(request):
	user 		= User.objects.get(pk=request.user.pk)
	duit 		= Orderan.objects.filter(status=3)
	tod 		= 0
	for i in duit:
		tod += i.biaya_total
	context 	= {
		'user'			: user,
		'titleHead'		: 'Dashboard',
		'titleDesc'		: 'Selamat Datang, No Party No Life',
		'beranda' 		: True,
		'title'			: 'Home',
		'orderanAll'	: len(Orderan.objects.all()),
		'orderanPend'	: len(Orderan.objects.filter(status=1)),
		'orderanProc'	: len(Orderan.objects.filter(status=2)),
		'orderanDone'	: len(Orderan.objects.filter(status=3)),
		#'pendapatan'	: user.orang.pendapatan,
		'pendapatan'	: tod,
		'titleLink'		: 'serpis:beranda',
	}
	return render(request, 'dalem/beranda.html', context)


@login_required
def orderan(request, pk=None):
	user 		= User.objects.get(pk=request.user.pk)
	if pk:
		instance = get_object_or_404(Orderan, pk=pk)
		context  = {
			'instance'	: instance,
			'user'		: user,
			'titleHead'	: 'Orderan',
			'titleDesc'	: 'Update Orderan',
			'title'		: 'Update',
			'titleLink'	: 'serpis:orderan',
			#'rincianOrder' 	: 
		}
	else:
		query 		= request.GET.get('q')
		page 		= request.GET.get('page')
		data 		= Orderan.objects.all().order_by('-pk')
		if query:
			data = data.filter(
				Q(keluhan__icontains=query) | Q(penanganan__icontains=query) | Q(pelanggan__icontains=query)
			).distinct()
		paginator 	= Paginator(data, 20)
		data 		= paginator.get_page(page)
		context 	= {
			'user'			: user,
			'titleHead'		: 'Orderan',
			'titleDesc'		: 'Daftar Orderan',
			'orderan'		: True,
			'title'			: 'Order',
			'data'			: data,
			'query'			: query,
			'titleLink'		: 'serpis:orderan',
		}

	if request.method == 'POST':
		aksi = request.POST.get('aksi')
		if aksi == 'tambah':
			gambar		= request.FILES.getlist('gambar')
			instance	= Orderan.objects.create(
				keluhan 	= request.POST.get('keluhan'),
				penanganan 	= request.POST.get('penanganan'),
				pelanggan 	= request.POST.get('pelanggan'),
				alamat 		= request.POST.get('alamat'),
				telp 		= request.POST.get('telp'),
			)
			try:
				for i in gambar:
					Gambar.objects.create(
						gambar 	= i,
						orderan = instance,
					)
			except:
				pass
			messages.success(request, 'Berhasil Tambah Data !!!')
			return redirect('serpis:orderan')
		elif aksi == 'hapus':
			instance = get_object_or_404(Orderan, pk=request.POST.get('pk_order'))
			instance.delete()
			messages.success(request, 'Berhasil Hapus Data !!!')
			return redirect('serpis:orderan')
		else:
			context['instance'].keluhan 	= request.POST.get('keluhan')
			context['instance'].penanganan 	= request.POST.get('penanganan')
			context['instance'].pelanggan 	= request.POST.get('pelanggan')
			context['instance'].alamat 		= request.POST.get('alamat')
			context['instance'].telp 		= request.POST.get('telp')
			context['instance'].status 		= request.POST.get('status')


			tgl							 	= request.POST.get('tgl_keluar')
			if tgl:
				#tgl 							= datetime.strptime(tgl, '%d %B %Y')
				#context['instance'].tgl_keluar  = datetime.strftime(tgl, '%d%m%Y')
				context['instance'].tgl_keluar  = datetime.strptime(tgl, '%d %B %Y')
			else:
				context['instance'].tgl_keluar  = None

			gambar_old 						= request.POST.getlist('gambar_old')
			gambar_new 						= request.FILES.getlist('gambar')
			
			#pkRincOld						= request.POST.getlist('pkRincOld')
			#ketRincOld						= request.POST.getlist('ketRincOld')
			#biayaRincOld					= request.POST.getlist('biayaRincOld')

			rincKet							= request.POST.getlist('ketRincian')
			rincBiy							= request.POST.getlist('biayaRincian')

			# process gambar old
			for i in context['instance'].gambar_orderan.all():
				if str(i.pk) in gambar_old:
					continue
				else:
					i.delete()

			# proses gambar new
			if '' not in gambar_new:
				for i in gambar_new:
					Gambar.objects.create(
						gambar 	= i,
						orderan = context['instance'],
					)

			# Rincian nih
			for i in context['instance'].rincian_orderan.all():
				context['instance'].biaya_total -= i.biaya
				context['instance'].save()
				i.delete()

			if '' not in rincKet:
				tai = 0
				for i in range(len(rincKet)):
					fak = Rincian.objects.create(
						orderan 	= context['instance'],
						ket 		= rincKet[i],
						biaya 		= int(rincBiy[i]),
					)
					tai += int(rincBiy[i])
				context['instance'].biaya_total += tai
			context['instance'].save()

			# proses rincian old
			#try:
			#	for i in context['instance'].rincian_orderan.all():
			#		context['instance'].biaya_total -= i.biaya
			#		i.delete()
			#except:
			#	print('No Data Rincian Old')


			# proses rincian masuk
			#try:
			#	tai = 0
			#	for i in range(len(rincKet)):
			#		fak = Rincian.objects.create(
			#			orderan 	= context['instance'],
			#			ket 		= rincKet[i],
			#			biaya 		= rincBiy[i],
			#		)
			#		tai += fak.biaya
			#	context['instance'].biaya_total += tai
			#except:
			#	print('Tidak Ada Rincian Masuk')
			#context['instance'].save()


			messages.success(request, 'Berhasil Update Data !!!')
			return redirect('serpis:orderan')
	
	return render(request, 'dalem/order.html', context)


@login_required
def orderan_detail(request, pk=None):
	user 		= User.objects.get(pk=request.user.pk)
	instance 	= get_object_or_404(Orderan, pk=pk)

	return render(request, 'dalem/order_detail.html', {'user': user, 'instance': instance, 'titleLink': 'serpis:orderan'})
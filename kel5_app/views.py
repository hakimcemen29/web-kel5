from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import requests


from .models import (
    Project, Projek, Meaningful, Experience, Implementasi,
    Batasan, Relasi, Perencanaan,ToExperience,Management
)
from .serializers import (
    ProyekEngineeringSerializer, ProjekSerializer
)
from .forms import (
    RegisterForm, LoginForm, ProjekForm, MeaningfulForm,
    ExperienceForm, ImplementasiForm, BatasanForm,
    RelasiForm, PerencanaanForm, ProfileUpdateForm
)

def integrasi_view(request):
    proyek_list = Project.objects.all().order_by('-id')
    return render(request, 'integrasi.html', {'proyek_list': proyek_list})

@api_view(['POST'])
def terima_proyek_engineering(request):
    data = request.data
    aktivitas = data.get('aktivitas', [])

    aktivitas1 = aktivitas[0] if len(aktivitas) > 0 else ''
    aktivitas2 = aktivitas[1] if len(aktivitas) > 1 else ''
    aktivitas3 = aktivitas[2] if len(aktivitas) > 2 else ''

    proyek = Project.objects.create(
        nama=data.get('nama'),
        deskripsi=data.get('deskripsi'),
        mulai=data.get('mulai'),
        selesai=data.get('selesai'),
        penanggungjawab=data.get('penanggungjawab'),
        jumlah=data.get('jumlah'),
        pendanaan=data.get('pendanaan'),
        aktivitas1=aktivitas1,
        aktivitas2=aktivitas2,
        aktivitas3=aktivitas3
    )

    serializer = ProyekEngineeringSerializer(proyek)
    return Response({'status': 'berhasil disimpan', 'data': serializer.data})

class ProjekAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProjekSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Projek.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response({'error': 'Semua field wajib diisi'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username sudah digunakan'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key})

def landing(request):
    return render(request, 'landing.html')

def registerPage(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Registrasi berhasil. Silakan login.")
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def projek_view(request):
    form = ProjekForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        projek = form.save(commit=False)
        projek.user = request.user
        projek.save()
        messages.success(request, "Projek berhasil ditambahkan.")
        return redirect('projek')

    projek_list = Projek.objects.filter(user=request.user)
    
    search_query = request.GET.get('q')
    if search_query:
        projek_list = projek_list.filter(nama__icontains=search_query)
        
    context = {
        'form': form, 
        'projek_list': projek_list.order_by('-id')
    }
    return render(request, 'projek.html', context)

@login_required
def delete_projek(request, id):
    projek = get_object_or_404(Projek, id=id, user=request.user)
    projek.delete()
    messages.success(request, "Projek berhasil dihapus.")
    return redirect('projek')

@login_required
def get_projek_or_redirect(request):
    projek_id = request.GET.get('projek_id') or request.POST.get('projek_id')
    if not projek_id:
        return None, redirect('projek')
    projek = get_object_or_404(Projek, id=projek_id, user=request.user)
    return projek, None

@login_required
def meaningful_input(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Meaningful.objects.get_or_create(projek=projek)
    form = MeaningfulForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/experience/?projek_id={projek.id}')

    return render(request, 'meaningful.html', {'form': form, 'projek_terpilih': projek})

@login_required
def experience_input(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Experience.objects.get_or_create(projek=projek)
    form = ExperienceForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/implementasi/?projek_id={projek.id}')

    return render(request, 'experience.html', {'form': form, 'projek_terpilih': projek})

@login_required
def implementasi_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Implementasi.objects.get_or_create(projek=projek)
    form = ImplementasiForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/batasan/?projek_id={projek.id}')

    return render(request, 'implementasi.html', {'form': form, 'projek_terpilih': projek})

@login_required
def batasan_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Batasan.objects.get_or_create(projek=projek)
    form = BatasanForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/status/?projek_id={projek.id}')

    return render(request, 'batasan.html', {'form': form, 'projek_terpilih': projek})

@login_required
def statusRelasi_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Relasi.objects.get_or_create(projek=projek)
    form = RelasiForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/perencanaan/?projek_id={projek.id}')

    return render(request, 'status.html', {'form': form, 'projek_terpilih': projek})

@login_required
def perencanaan_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Perencanaan.objects.get_or_create(projek=projek)
    form = PerencanaanForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('projek')

    return render(request, 'perencanaan.html', {'form': form, 'projek_terpilih': projek})

@login_required
def view_projek_detail(request, projek_id):
    projek = get_object_or_404(Projek, id=projek_id, user=request.user)
    context = {
        'projek': projek,
        'meaningful_list': Meaningful.objects.filter(projek=projek),
        'experience_list': Experience.objects.filter(projek=projek),
        'implementasi_list': Implementasi.objects.filter(projek=projek),
        'batasan_list': Batasan.objects.filter(projek=projek),
        'relasi_list': Relasi.objects.filter(projek=projek),
        'perencanaan_list': Perencanaan.objects.filter(projek=projek),
    }
    return render(request, 'viewProjek.html', context)

def home_view(request):
    return render(request, 'home.html')

# def view_tess(request):
#     proyek = Project.objects.all().order_by('-id')
#     return render(request, 'integrasi.html', {'proyek': proyek})

@login_required
def projek_chart_data(request):
    projek_list = Projek.objects.filter(user=request.user).order_by('created_at')
    data = [
        {
            'tanggal': p.created_at.strftime('%Y-%m-%d'),
            'nama': p.nama,
        } for p in projek_list
    ]
    return JsonResponse(data, safe=False)

@login_required
def profil_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Foto profil berhasil diperbarui!')
            return redirect('profil')

    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': form
    }
    return render(request, 'profil.html', context)



def delete_integrasi_proyek(request, id):
    if request.method == 'POST':
        proyek_dihapus = get_object_or_404(Project, id=id)
        
        proyek_dihapus.delete()
        
        # Kirim pesan sukses
        messages.success(request, f"Proyek '{proyek_dihapus.nama}' berhasil dihapus.")
    
    return redirect('integrasi')




from .serializers import ToExperienceSerializer

class ToExperienceViewSet(viewsets.ModelViewSet):
    queryset = ToExperience.objects.all()
    serializer_class = ToExperienceSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def kirim_ke_teman(request):
    if request.method == 'POST':
        namaProjek = request.POST.get('namaProjek')
        meaningful = request.FILES.get('meaningful')
        experience = request.FILES.get('experience')
        implementasi = request.FILES.get('implementasi')
        batasan = request.FILES.get('batasan')
        perencanaan = request.FILES.get('perencanaan')

        files = {}

        try:
            # Validasi: pastikan semua file ada
            if not all([namaProjek, meaningful, experience, implementasi, batasan, perencanaan]):
                error_msg = "Semua field dan file wajib diisi."
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'error': error_msg}, status=400)
                return render(request, 'kirim_form.html', {'error': error_msg})

            # Simpan file lokal ke database
            instance = ToExperience.objects.create(
                namaProjek=namaProjek,
                meaningful=meaningful,
                experience=experience,
                implementasi=implementasi,
                batasan=batasan,
                perencanaan=perencanaan
            )

            # Siapkan file untuk dikirim ke server teman
            files = {
                'meaningful': open(instance.meaningful.path, 'rb'),
                'experience': open(instance.experience.path, 'rb'),
                'implementasi': open(instance.implementasi.path, 'rb'),
                'batasan': open(instance.batasan.path, 'rb'),
                'perencanaan': open(instance.perencanaan.path, 'rb'),
            }

            data = {
                'namaProjek': namaProjek,
            }

            # Kirim ke server teman
            response = requests.post(
                'http://10.24.64.23:8000/api/engineering/',
                data=data,
                files=files
            )

            print("Kirim berhasil:", response.status_code)

            if request.headers.get('Accept') == 'application/json':
                
                return JsonResponse({'message': 'Berhasil dikirim ke teman'}, status=201)
            
            else:
                
                messages.success(request, "Proyek berhasil dikirim ke teman.")
                return render(request, 'kirim_form.html')  # atau redirect jika memang dari browser


        except Exception as e:
            print("Gagal kirim ke teman:", e)
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': str(e)}, status=500)
            else:
                messages.error(request, f"Gagal kirim proyek: {e}")
                return redirect('/creation/')

        finally:
            for f in files.values():
                f.close()

    # Jika GET (akses dari browser)
    return render(request, 'kirim_form.html')



import requests
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Management





import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Management

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
import requests, json
from .models import Management

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import requests
import json
from .models import Management  # pastikan model diimpor

import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Management


import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Management

import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Management

import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def kirim_management_ke_teman(request):
    if request.method == 'POST':
        # Ambil data dari form
        nama_kelompok = "Inteligen Engineering"  # HARUS ADA, WAJIB SESUAI FORMAT SERVER TEMAN
        deskripsi = request.POST.get('deskripsi')
        status = request.POST.get('status')

        # Validasi: Semua field wajib diisi
        if not all([nama_kelompok, deskripsi, status]):
            messages.error(request, "Semua data wajib diisi.")
            return redirect('/api/kirimmanagement/')

        if status not in ['selesai', 'belum selesai']:
            messages.error(request, "Status harus 'selesai' atau 'belum selesai'.")
            return redirect('/api/kirimmanagement/')

        try:
            # Simpan ke database lokal
            Management.objects.create(
                namaKelompok=nama_kelompok,
                deskripsi=deskripsi,
                status=1 if status == "selesai" else 0
            )

            # Siapkan payload JSON untuk server teman
            payload = {
                "namaKelompok": nama_kelompok,
                "deskripsi": deskripsi,
                "status": status
            }

            headers = {
                "Content-Type": "application/json"
            }

            # Kirim ke server teman (harus HTTPS dan endpoint benar)
            response = requests.post(
                'https://rezasugiarto.pythonanywhere.com/api/terima-management/',
                data=json.dumps(payload),
                headers=headers
            )

            # Cek respon server teman
            if response.status_code == 201:
                messages.success(request, "Data berhasil dikirim ke server teman.")
            else:
                try:
                    pesan_error = response.json().get('error', 'Gagal kirim proyek ke teman.')
                except:
                    pesan_error = response.text
                messages.error(request, f"Gagal kirim proyek ke teman: {pesan_error}")

        except Exception as e:
            messages.error(request, f"Gagal kirim proyek: {str(e)}")

        return redirect('/api/kirimmanagement/')

    return render(request, 'kirimManagemen_form.html')












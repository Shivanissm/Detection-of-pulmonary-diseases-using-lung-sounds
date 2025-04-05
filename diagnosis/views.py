# diagnosis/views.py
from django.shortcuts import render
from .ml import predict_disease  # 🔸 Import ML function
import os
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')

def patient_record(request):
    if request.method == "POST" and 'name' in request.POST:
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        symptoms = request.POST.get('symptoms')
        weight = request.POST.get('weight')
        bp = request.POST.get('bp')
        diseases = request.POST.get('existing_diseases')
        audio = request.FILES.get('audio_file')

        # 🔸 Save uploaded audio to disk
        audio_path = os.path.join(settings.MEDIA_ROOT, audio.name)
        with open(audio_path, 'wb+') as destination:
            for chunk in audio.chunks():
                destination.write(chunk)
            destination.flush()                       # ✅ Ensure all data is flushed
            os.fsync(destination.fileno())            # ✅ Force write to disk (fixes FileNotFoundError)
        print(f"Saved audio at: {audio_path}")

        # 🔸 Run prediction
        predicted_disease = predict_disease(audio_path)

        # 🔸 Prepare context to show result
        context = {
            'name': name,
            'age': age,
            'address': address,
            'symptoms': symptoms,
            'weight': weight,
            'bp': bp,
            'diseases': diseases,
            'predicted_disease': predicted_disease,
        }
        return render(request, 'result.html', context)

    return render(request, 'patient_record.html')

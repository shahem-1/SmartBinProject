# smartbin/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout

import json
from django.shortcuts     import render, redirect
from django.contrib              import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms    import UserCreationForm, AuthenticationForm
from django.contrib.auth.models   import User
from django.views.decorators.csrf import csrf_exempt
from django.http   import JsonResponse, HttpResponseBadRequest
from django.db.models       import Max
from .models          import SensorReading

# ─── Authentication Views ─────────────────────────────────────────────────────

def signup_view(request):
    """Allow new user sign‑up (max 5 users)."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if User.objects.count() >= 5:
                form.add_error(None, "User limit reached (5).")
            else:
                form.save()
                messages.success(request, "User created successfully!")
                return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def mainP(request):
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib import messages

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            from django.contrib.auth import login as auth_login
            auth_login(request, form.get_user())
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'MainPage.html', {'form': form})



def logout_view(request):
    """Log user out and redirect to login."""
    logout(request)
    return redirect('login')


# Protected Dashboard 

@login_required
def dashboard(request):
    """Render the main dashboard (map, live-fill, table)."""
    return render(request, 'dashboard.html')


#  Sensor API Views 

@csrf_exempt
def sensor_data(request):
    """
    
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            distance = float(payload.get('distance'))
            bin_id   = payload.get('bin_id', 'BIN001')
            SensorReading.objects.create(distance=distance, bin_id=bin_id)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    if request.method == 'GET':
        try:
            latest = SensorReading.objects.latest('timestamp')
            return JsonResponse({'distance': latest.distance})
        except SensorReading.DoesNotExist:
            return JsonResponse({'distance': None})
        except Exception as e:
            return JsonResponse({'distance': None, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_sensor_data(request):
    """
    Alias for GET the most recent sensor reading.
    """
    try:
        latest = SensorReading.objects.latest('timestamp')
        return JsonResponse({'distance': latest.distance})
    except SensorReading.DoesNotExist:
        return JsonResponse({'distance': None})
    except Exception as e:
        return JsonResponse({'distance': None, 'error': str(e)}, status=500)


# ─── Bin List API ─────────────────────────────────────────────────────────────

def bin_list_api(request):
    """
    Return a list of all bins with their latest reading, latitude & longitude.
    """
    # find latest timestamp for each bin_id
    latest_per_bin = (
        SensorReading.objects
        .values('bin_id')
        .annotate(latest_time=Max('timestamp'))
    )

    data = []
    for entry in latest_per_bin:
        reading = SensorReading.objects.get(
            bin_id=entry['bin_id'],
            timestamp=entry['latest_time']
        )
        data.append({
            'bin_id':   reading.bin_id,
            'distance': reading.distance,
            'timestamp': reading.timestamp.strftime('%Y-%m-%d %H:%M'),
            'lat':      getattr(reading, 'latitude', 0),
            'lon':      getattr(reading, 'longitude', 0),
        })

    return JsonResponse(data, safe=False)




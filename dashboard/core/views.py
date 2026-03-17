import json
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


# ── Load artifacts once at startup ──────────────────────────────────────────
_MODEL       = None
_ENCODER     = None
_FEAT_META   = None
_HOTSPOT_DF  = None
_CLEAN_DF    = None

def _load_model():
    global _MODEL, _ENCODER, _FEAT_META
    if _MODEL is None:
        _MODEL   = joblib.load(settings.MODELS_DIR / 'rf_model.pkl')
        _ENCODER = joblib.load(settings.MODELS_DIR / 'label_encoder.pkl')
        with open(settings.MODELS_DIR / 'feature_meta.json') as f:
            _FEAT_META = json.load(f)
    return _MODEL, _ENCODER, _FEAT_META


def _load_hotspots():
    global _HOTSPOT_DF
    if _HOTSPOT_DF is None:
        path = settings.DATA_DIR / 'hotspot_summary.csv'
        _HOTSPOT_DF = pd.read_csv(path)
    return _HOTSPOT_DF


def _load_clean():
    global _CLEAN_DF
    if _CLEAN_DF is None:
        path = settings.DATA_DIR / 'accidents_clean.parquet'
        _CLEAN_DF = pd.read_parquet(
            path,
            columns=['Severity','Hour','DayOfWeek','MonthName',
                     'WeatherGroup','Season','State','City']
        )
    return _CLEAN_DF


# ── Helper: build input vector (mirrors notebook 03) ────────────────────────
def _build_input_vector(lat, lon, hour, month,
                        temperature_f=65.0, humidity_pct=50.0,
                        visibility_mi=10.0, wind_speed_mph=5.0,
                        precipitation_in=0.0, weather_group='Clear',
                        junction=False, traffic_signal=False, crossing=False):

    _, _, meta = _load_model()
    features   = meta['features']

    def get_season(m):
        if m in [12,1,2]: return 'Winter'
        if m in [3,4,5]:  return 'Spring'
        if m in [6,7,8]:  return 'Summer'
        return 'Fall'

    def get_tod(h):
        if 5  <= h < 12: return 'Morning'
        if 12 <= h < 17: return 'Afternoon'
        if 17 <= h < 21: return 'Evening'
        return 'Night'

    row = {
        'Start_Lat':          lat,
        'Start_Lng':          lon,
        'Temperature(F)':     temperature_f,
        'Humidity(%)':        humidity_pct,
        'Visibility(mi)':     visibility_mi,
        'Wind_Speed(mph)':    wind_speed_mph,
        'Precipitation(in)':  precipitation_in,
        'Junction':           int(junction),
        'Traffic_Signal':     int(traffic_signal),
        'Crossing':           int(crossing),
        'IsWeekend':          0,
        'Hour_sin':           np.sin(2 * np.pi * hour  / 24),
        'Hour_cos':           np.cos(2 * np.pi * hour  / 24),
        'Month_sin':          np.sin(2 * np.pi * month / 12),
        'Month_cos':          np.cos(2 * np.pi * month / 12),
    }

    sunrise = 'Day' if 6 <= hour < 20 else 'Night'
    season  = get_season(month)
    tod     = get_tod(hour)

    for wg in meta['weather_groups']:
        row[f'WeatherGroup_{wg}'] = int(weather_group == wg)
    for ss in meta['sunrise_sunset']:
        row[f'Sunrise_Sunset_{ss}'] = int(sunrise == ss)
    for s in meta['seasons']:
        row[f'Season_{s}'] = int(season == s)
    for t in meta['time_of_day']:
        row[f'TimeOfDay_{t}'] = int(tod == t)

    df = pd.DataFrame([row])
    for col in features:
        if col not in df.columns:
            df[col] = 0
    return df[features].fillna(0).astype(np.float32)


# ── Views ────────────────────────────────────────────────────────────────────
def home(request):
    return render(request, 'home.html')


def map_view(request):
    df       = _load_hotspots()
    city_sel = request.GET.get('city', 'All')
    cities   = sorted(df['City'].unique().tolist())

    if city_sel != 'All':
        df = df[df['City'] == city_sel]

    hotspots = df.to_dict(orient='records')

    # Stats for the info bar
    stats = {
        'total_hotspots': len(df),
        'high_risk':      int((df['Risk'] == 'High').sum()),
        'medium_risk':    int((df['Risk'] == 'Medium').sum()),
        'low_risk':       int((df['Risk'] == 'Low').sum()),
    }
    return render(request, 'map.html', {
        'hotspots':     json.dumps(hotspots),
        'cities':       cities,
        'city_sel':     city_sel,
        'stats':        stats,
    })


def insights_view(request):
    df = _load_clean()

    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    # Accidents by hour
    by_hour = df.groupby('Hour').size().reset_index(name='count')
    # Accidents by day
    by_day  = df['DayOfWeek'].value_counts().reindex(day_order).fillna(0).reset_index()
    by_day.columns = ['day', 'count']
    # Severity distribution
    by_sev  = df['Severity'].value_counts().sort_index().reset_index()
    by_sev.columns = ['severity', 'count']
    # Weather group
    by_wx   = df['WeatherGroup'].value_counts().head(7).reset_index()
    by_wx.columns = ['weather', 'count']
    # Top states
    by_state = df['State'].value_counts().head(10).reset_index()
    by_state.columns = ['state', 'count']

    context = {
        'by_hour':  json.dumps(by_hour.to_dict(orient='records')),
        'by_day':   json.dumps(by_day.to_dict(orient='records')),
        'by_sev':   json.dumps(by_sev.to_dict(orient='records')),
        'by_wx':    json.dumps(by_wx.to_dict(orient='records')),
        'by_state': json.dumps(by_state.to_dict(orient='records')),
        'total':    f'{len(df):,}',
    }
    return render(request, 'insights.html', context)


def risk_view(request):
    model, _, meta = _load_model()
    weather_options = sorted(meta['weather_groups'])
    return render(request, 'risk.html', {'weather_options': weather_options})


@csrf_exempt
@require_POST
def predict_api(request):
    try:
        data = json.loads(request.body)

        lat            = float(data.get('lat', 34.05))
        lon            = float(data.get('lon', -118.24))
        hour           = int(data.get('hour', 8))
        month          = int(data.get('month', 6))
        temperature_f  = float(data.get('temperature_f', 65))
        humidity_pct   = float(data.get('humidity_pct', 50))
        visibility_mi  = float(data.get('visibility_mi', 10))
        wind_speed_mph = float(data.get('wind_speed_mph', 5))
        precipitation  = float(data.get('precipitation_in', 0))
        weather_group  = data.get('weather_group', 'Clear')
        junction       = bool(data.get('junction', False))
        traffic_signal = bool(data.get('traffic_signal', False))
        crossing       = bool(data.get('crossing', False))

        model, encoder, _ = _load_model()

        vec       = _build_input_vector(
            lat, lon, hour, month,
            temperature_f, humidity_pct, visibility_mi,
            wind_speed_mph, precipitation, weather_group,
            junction, traffic_signal, crossing
        )
        pred_enc  = model.predict(vec)[0]
        proba     = model.predict_proba(vec)[0]
        risk      = encoder.inverse_transform([pred_enc])[0]

        return JsonResponse({
            'risk_label':    risk,
            'confidence':    round(float(proba.max()) * 100, 1),
            'probabilities': {
                cls: round(float(p) * 100, 1)
                for cls, p in zip(encoder.classes_, proba)
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

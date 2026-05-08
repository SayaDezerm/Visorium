import json
import requests
import traceback
import urllib3
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.catalog.models import Movie

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def get_movies_context():
    movies = Movie.objects.all().values('title', 'genre', 'release_year', 'description', 'duration')
    return "\n".join([
        f"- {m['title']} ({m['release_year']}, {m['genre']}, {m['duration']} min): {m['description'][:100]}"
        for m in movies
    ])

@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Mesaj gol.'}, status=400)

        movies_context = get_movies_context()

        system_prompt = f"""Ești un asistent AI specializat în filme, integrat într-un catalog de filme.
                        Cataloagul conține următoarele filme:
                        {movies_context}

                        Răspunde DOAR la întrebări despre filme — din catalog sau în general.
                        Dacă ți se pun întrebări care nu sunt despre filme, redirecționează politicos conversația spre filme.
                        Răspunsurile să fie concise, maxim 3-4 propoziții.
                        Răspunde în limba în care ți se pune întrebarea."""

        # construiește conversația
        contents = []
        for msg in history[-10:]:
            contents.append({
                'role': msg['role'],
                'parts': [{'text': msg['content']}]
            })

        # adaugă mesajul curent
        contents.append({
            'role': 'user',
            'parts': [{'text': f"{system_prompt}\n\nÎntrebare: {user_message}"}]
        })

        payload = {
            'contents': contents,
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 512,
            }
        }

        response = requests.post(
            GEMINI_URL,
            params={'key': settings.GEMINI_API_KEY},
            json=payload,
            verify=False,
            timeout=30
        )

        result = response.json()

        if 'candidates' in result:
            text = result['candidates'][0]['content']['parts'][0]['text']
            return JsonResponse({'response': text, 'status': 'ok'})
        else:
            print("Gemini error:", result)
            return JsonResponse({'error': 'Răspuns invalid de la Gemini.'}, status=500)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
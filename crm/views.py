from django.shortcuts import render

# Create your views here.
import logging
logger = logging.getLogger('django')

def test_view(request):
    logger.warning("Bu bir uyarı mesajıdır.")
    logger.error("Bu bir hata mesajıdır.")
    return HttpResponse("Log test edildi.")




def main_view(request):
    return render(request, 'main.html')
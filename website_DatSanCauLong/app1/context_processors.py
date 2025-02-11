from .models import BadmintonHall
from .forms import SearchForm

# Hiển thị các cơ sở ở footer qua toàn bộ template
def badminton_halls_context(request):
    # Lấy tất cả các cơ sở từ database
    badminton_halls = BadmintonHall.objects.all()
    return {'Badminton_Halls': badminton_halls}

def search_form_processor(request):
    search_court = SearchForm()
    return {'searchCourt': search_court,}
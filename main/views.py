from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.



def randomchat_enterance(request):
    if not request.user.is_authenticated:
        return redirect("login") 

    return render(request,"main/randomchat_enter.html")

def index(request):
    if not request.user.is_authenticated:
        return redirect("login") 

    return render(request,"main/index.html")


def home(request):
    if not request.user.is_authenticated:
        return redirect("login") 
    
    if request.method == "POST":
        search_query = request.POST["search_query"].strip()
        if search_query:
            search_query = request.POST["search_query"]
            search_profile = User.objects.filter(username__icontains = search_query)
            context = {'search_profile':search_profile}
            return render(request,"main/profiles.html",context)
        else:
            return redirect("home")

    else:
        all_profiles = User.objects.all()

        num_profiles_to_display = 1

        random_profiles = random.sample(list(all_profiles), num_profiles_to_display)

        context = {
            'random_profiles': random_profiles
        }

        return render(request,"main/profiles.html",context)



from django.views.decorators.cache import never_cache
from django.db.models import Q

@never_cache
def mychats(request):
    if not request.user.is_authenticated:
        return redirect("login") 
    
    if request.method == "POST":
        search_query = request.POST.get("search_query", "").strip()
        if search_query:
            search_results = Message.objects.filter(
                Q(sender__username__icontains=search_query) | Q(receiver__username__icontains=search_query),
                receiver=request.user
            ).order_by('-timestamp')
            last_messages = {}
            for message in search_results:
                if message.sender.id not in last_messages:
                    last_messages[message.sender.id] = message
            context = {'messages': last_messages.values()}
            return render(request, "main/mychats.html", context)
        else:
                
        # Tüm mesajları al
            all_messages = Message.objects.filter(receiver=request.user).order_by('timestamp')
            all_messages = reversed(all_messages)

            # Her bir kişi için son mesajları al
            last_messages = {}
            for message in all_messages:
                if message.sender.id not in last_messages:
                    last_messages[message.sender.id] = message

            return render(request, "main/mychats.html", {'messages': last_messages.values()})

    else:
    # Tüm mesajları al
        all_messages = Message.objects.filter(receiver=request.user).order_by('timestamp')
        all_messages = reversed(all_messages)

        # Her bir kişi için son mesajları al
        last_messages = {}
        for message in all_messages:
            if message.sender.id not in last_messages:
                last_messages[message.sender.id] = message

        return render(request, "main/mychats.html", {'messages': last_messages.values()})


def get_room_name(user1, user2):
    
    user_ids = sorted([user1.id, user2.id])
    room_name = f"user_{user_ids[0]}_{user_ids[1]}"
    return room_name

from .models import Message


def private_chat_view(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login") 
    target_user = get_object_or_404(User, id=user_id)
    room_name = get_room_name(request.user, target_user)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=target_user) | Q(sender=target_user, receiver=request.user)
        ).order_by('-timestamp')[:20]
    messages = reversed(messages)
    
    context = {
        'target_user': target_user,
        'room_name': room_name,
        'target_username': target_user.username,
        'messages': messages  
    }


    # Görünümdeki şablonu render et
    return render(request, 'main/privatechat.html', context)



"""  
    float yapma öncesi kullanılan mesaj yükleme kısmı
    sent_messages = Message.objects.filter(sender=request.user, receiver=target_user)
    received_messages = Message.objects.filter(sender=target_user, receiver=request.user)
    messages = (sent_messages | received_messages).order_by('-timestamp')[:20] """


"""     messages = Message.objects.filter(
        Q(sender=request.user, receiver=target_user) | Q(sender=target_user, receiver=request.user)
    ).order_by('timestamp')[:20] """

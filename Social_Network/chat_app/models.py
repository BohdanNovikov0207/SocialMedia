from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()

class Chat(models.Model):
    # 
    admin = models.ForeignKey(user, on_delete= models.CASCADE, blank= True, null= True)
    # 
    users = models.ManyToManyField(user, related_name= 'chats')
    # 
    name = models.CharField(max_length= 30, blank= True, null= True)
    is_group = models.BooleanField(default= False)
    avatar  = models.ImageField(upload_to= 'chat_avatars/', blank= True, null= True)
    
    def __str__(self):
        return self.name or f"Chat {self.id}"
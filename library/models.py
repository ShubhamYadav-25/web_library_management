from django.db import models  

class books(models.Model):  
    book_id = models.AutoField(primary_key=True)   
    book_name = models.CharField(max_length=50)   
    author_name = models.CharField(max_length=50)  
    edition = models.IntegerField()               
    genre = models.CharField(max_length=50)  

    class Meta:  
        db_table = 'books'  
        managed = True    
    
class users(models.Model):
    User_ID = models.AutoField(primary_key=True)
    User_Name = models.CharField(max_length=20)
    Pass_word = models.CharField(max_length=20)
    contact_details = models.CharField(max_length=50)
    user_birthday = models.DateField(blank=True, null=True)

    class Meta:  
        db_table = 'users' 
        managed = True    

class issued_books(models.Model):
    book_id = models.AutoField(primary_key=True) 
    book_name = models.CharField(max_length=50) 
    author_name = models.CharField(max_length=50)  
    edition = models.IntegerField()               
    genre = models.CharField(max_length=50)
    issued_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'issued_books'
        managed = True

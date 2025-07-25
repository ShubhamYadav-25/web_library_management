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



# from django.db import models

# # Create your models here.
# from django.db import models

# class User(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15)
#     address = models.TextField()
#     membership_date = models.DateField()

# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     genre = models.CharField(max_length=100)
#     publication_year = models.PositiveIntegerField()
#     isbn = models.CharField(max_length=13, unique=True)
#     copies_available = models.IntegerField()

# class BorrowingRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     borrow_date = models.DateField()
#     return_date = models.DateField(null=True, blank=True)
#     status = models.CharField(max_length=10, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned'), ('overdue', 'Overdue')])
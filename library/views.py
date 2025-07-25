from django.db import connection
from django.shortcuts import render, redirect  
from django.http import HttpResponse 
from django.template import loader
from .models import books, users, issued_books
from django.views.decorators.http import require_POST 
from django.db.models import Q  
from datetime import date  
from django.shortcuts import get_object_or_404  

def create_triggers_and_procedures():
    with connection.cursor() as cursor:
        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER update_copies_on_borrow
        AFTER INSERT ON BorrowingRecords
        FOR EACH ROW
        BEGIN
            UPDATE Books
            SET copies_available = copies_available - 1
            WHERE book_id = NEW.book_id;
        END;//
        DELIMITER ;
        """)
        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER update_copies_on_return
        AFTER UPDATE ON BorrowingRecords
        FOR EACH ROW
        BEGIN
            IF NEW.status = 'returned' THEN
                UPDATE Books
                SET copies_available = copies_available + 1
                WHERE book_id = NEW.book_id;
            END IF;
        END;//
        DELIMITER ;
        """)

# Create your views here.

@require_POST   
def submit_page(request):  
    form_type = request.POST.get('form_type')  
        
    if form_type == 'searchbook_form':    
        Bookname = request.POST.get('Bookname')    #store the input bookname in  a variable.
        x=str(Bookname)                            # convert the input bookname to string.
        Author = request.POST.get('Author')        #store the input Authur in  a variable.
        y=str(Author)                              # convert the input bookname to string.
        mybook = books.objects.filter(book_name__icontains=x,author_name__icontains=y).values()   #retrive the  book details from the database using the input bookname and authorname
        template=loader.get_template('newapp/searchbook.html')    #using template to render is good for projects.
        content = {                                               #specifing the values of placeholder.
            'mybook': mybook,
        }  
        return HttpResponse(template.render(content, request))

    elif form_type == 'viewbooks_form':
        Genre = request.POST.get('Category')         #Stores the input Category  in a variable.
        Bookname = request.POST.get('Bookname')      #Stores the input  Bookname  in a variable.
        genstr=str(Genre)                            #covert input into string.
        x=str(Bookname)
        if x=='' and genstr != '':                               #if bookname is empty and category is not empty then filter the books based on category.

            if genstr == 'Other':
                mybook=books.objects.filter(genre__isnull=True).values() | books.objects.filter(genre='').values()   #check for NULL feild or empty string in the genre attribute.

            else:
                mybook=books.objects.filter(genre__icontains=genstr).values()

            return render(request, 'newapp/viewbooks.html', {'mybook': mybook})
        
        elif x!='' and genstr == '':                            # if category  is empty and bookname is not empty then filter the books based on bookname
           
            mybook=books.objects.filter(book_name__icontains=x).values()
            return render(request, 'newapp/viewbooks.html', {'mybook': mybook})
        
        elif x=='' and genstr =='':                             # if both bookname and category are empty then show all the books in the database
            return render(request, 'newapp/viewbooks.html')
        
        else:
            if genstr == 'Other':
                mybook=books.objects.filter(Q(genre__isnull=True) | Q(genre='')).values()     #check for NULL feild or empty string in the genre attribute

            else:
                mybook = books.objects.filter(book_name__icontains=x,genre__icontains=genstr).values()   #check for bookname with category in the database
            return render(request, 'newapp/viewbooks.html', {'mybook': mybook})
        
    elif form_type == 'issuebook_form':
        Bookname = request.POST.get('Bookname')     #stores the input bookname in  a variable.
        BookID = request.POST.get('BookID')         #stores the input bookid in  a variable.
        current_date = date.today()                 #extract the  current date from the system.

        Bookname1=str(Bookname)
        z=int(BookID)
        mybook = books.objects.filter(book_name__icontains=Bookname1,book_id=z).first()   #retrive the data from  the database using the input bookname and bookid.

        content = {
            'current_date':current_date,
        }
        if mybook:                                        #if  the book is found in the database then proceed with the issue process.

            mybook_dict = {                               #stores the value to display in place of placeholder.
                'book_id': mybook.book_id,  
                'book_name': mybook.book_name,  
                'author_name': mybook.author_name,  
                'edition': mybook.edition,  
            }  
            book = get_object_or_404(books,book_id=z)     #load the object(book) from the database using the bookid. Here object is the book from database books.

            add_book=issued_books(book_id=book.book_id,book_name=book.book_name,author_name=book.author_name,edition=book.edition,genre=book.genre,issued_date=current_date)
            #Create a new object(add_book) in the issued_books table with the bookid,bookname,authorname,edition
            add_book.save()              #save the object(add_book) in the database issued_books.
            book.delete()                #delete the object(book) from the database books.

            content['mybook'] = [mybook_dict]         #for passing the data to the template/html page.
        else:  
            content['mybook'] = []                    #for passing the data to the template/html page.

        return render(request, 'newapp/issuebook.html', content) 

    elif form_type == 'login_form':
        Username = request.POST.get('username')         #store  the input username in a variable
        Pass_wd = request.POST.get('password')          #store   the input password in a variable.
        US = str(Username)
        PS=str(Pass_wd)
        myuser = users.objects.filter(User_Name=US,Pass_word=PS).first()    #retrive the data  from the database using the input username and password.

        if myuser:
            return redirect('Home')                      #if the user is found in the database then redirect to the home page
        else:
            return render(request,'newapp/login.html')   #if  the user is not found in the database then render the login page
        
    elif form_type == 'register_form':
        Username=request.POST.get('username')
        Pass_wd=request.POST.get('password')
        BirthD=request.POST.get('Birthday')
        Contact=request.POST.get('contact')
        Cont = str(Contact)               
        add_user=users(User_Name=Username,Pass_word=Pass_wd,contact_details=Cont,user_birthday=BirthD) 
        #create the  object(add_user) in the users table with the input username,password,birthday,contactdetails.

        add_user.save()                               #save the  object(add_user) in the database users.
        return redirect('login')                      #after saving the user in the database then redirect to the login page

    elif form_type == 'returnbook_form':              
        BOOKid = request.POST.get('BookID')            #store  the input bookid in a variable
        action = request.POST.get('submit_action')     #store the action of the button(i.e which button have been selected 'Return/check') in a variable.
        Bid=int(BOOKid)
        mybook = issued_books.objects.filter(book_id=Bid).first()     #retrive the data  from the database 'issued_book' using the input bookid.

        if mybook:              #if  the book is found in the database then proceed with the written process.

            context = {}
            if action == 'Check':                    #logic for calculating the  fine for the book.
                issueddate = mybook.issued_date
                current_date = date.today()
                penalty = 0
                difference = (current_date - issueddate).days
                if difference > 7:
                    penalty_days = 7 
                    penalty= difference*penalty_days

                context["penalty"] =penalty
                book1 = issued_books.objects.all()
                context['mybook']=book1
                
            if action == 'Return':                #logic to return  the book and update the database.
                book = get_object_or_404(issued_books,book_id=Bid)      
                add_book=books(book_id=book.book_id,book_name=book.book_name,author_name=book.author_name,edition=book.edition,genre=book.genre)
                add_book.save()  
                book.delete()
                book1 = issued_books.objects.all()  
                context['mybook']=book1
                context['book']=mybook

            return render(request, 'newapp/returnbook.html', context)

        return render(request, 'newapp/returnbook.html')
        

    else:               #if some other form/page is submitted then return the error message
        return HttpResponse("Invalid form type.")    

def Home(request):             #used due to menu button.probabily.
    return render(request,'newapp/Home.html')

def returnbook(request):             #when user opens the returnbook page then list of issued books should be in the result section.
    book = issued_books.objects.all()  
    context = {  
        "mybook": book  
    }  
    return render(request, 'newapp/returnbook.html', context) 


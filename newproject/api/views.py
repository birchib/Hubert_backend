from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializer import BookSerializer, PersonSerializer
from mongoengine.queryset.visitor import Q
from pymongo import MongoClient
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .mongo_models import Person
import re
from dotenv import load_dotenv
import os
from api.azure_llm import get_llm_answer

from django.urls import path
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World")


load_dotenv()
conection_string = os.getenv('mongo_connection_string')
hubert_mongo_db = os.getenv('hubert_mongo_db')
hubert_mongo_db_table = os.getenv('hubert_mongo_db_table')



class PersonListView(APIView):
    def get(self, request):
        # Connect to MongoDB
        client = MongoClient(conection_string)
        db = client[hubert_mongo_db]
        collection = db[hubert_mongo_db_table]

        # Get the search query from request parameters
        search_query = request.query_params.get('search', '').strip()
        if search_query:
            # Decode the query in case it contains encoded characters like '%20'
            search_query = search_query.replace('%20', ' ').replace('%2C', ',')
            
            # Split the search query by commas and spaces
            search_terms = re.split(r'[\s,]+', search_query)
            search_terms = [term for term in search_terms if term]  # Filter out empty strings

            # Build regex patterns for each term (case-insensitive search)
            regex_patterns = [{"name": {"$regex": re.escape(term), "$options": "i"}} for term in search_terms]

            # Create the MongoDB query with the $or operator
            query = {"$or": regex_patterns}
            persons = collection.find(query)
        else:
            # If no search query, return all documents
            persons = collection.find()

        # Convert MongoDB cursor to a list of dictionaries
        persons_list = list(persons)
        # Convert ObjectId to string for JSON serialization
        for person in persons_list:
            person['_id'] = str(person['_id'])
        return Response(persons_list, status=status.HTTP_200_OK)
    
def get(self, request):
    # Connect to MongoDB
    client = MongoClient(conection_string)
    db = client[hubert_mongo_db]
    collection = db[hubert_mongo_db_table]

    # Get the search query from request parameters
    search_query = request.query_params.get('search', '').strip()
    print(f"Raw search query: '{search_query}'", flush=True)

    if search_query:
        # Split the search query by commas and spaces
        search_terms = re.split(r'[\s,]+', search_query)
        search_terms = [term for term in search_terms if term]  # Filter out empty strings

        # Build regex patterns for each term (case-insensitive search)
        regex_patterns = [{"name": {"$regex": re.escape(term), "$options": "i"}} for term in search_terms]

        # Create the MongoDB query with the $or operator
        query = {"$or": regex_patterns}
        persons = collection.find(query)
    else:
        # If no search query, return all documents
        persons = collection.find()

    # Convert MongoDB cursor to a list of dictionaries
    persons_list = list(persons)
    # Convert ObjectId to string for JSON serialization
    for person in persons_list:
        person['_id'] = str(person['_id'])

    return Response(persons_list, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_dbset(request):
    client = MongoClient(conection_string)  # Connect to MongoDB
    db = client[hubert_mongo_db]  # Replace with your actual database name
    collection = db[hubert_mongo_db_table]  # Replace with your collection name
    
    search_query = request.query_params.get('search', '').strip()
    search_terms = re.split(r'[\s,]+', search_query)
    search_terms = [term for term in search_terms if term]

    if search_terms:
        regex_patterns = [{"name": {"$regex": re.escape(term), "$options": "i"}} for term in search_terms]
        query = {"$or": regex_patterns}
        persons = collection.find(query)
    else:
        persons = collection.find()

    # Convert MongoDB documents to a list and format the ObjectId to strings for JSON serialization
    persons_list = []
    for person in persons:
        person['_id'] = str(person['_id'])
        persons_list.append(person)
    if persons_list:
        formatted_documents = [str(person) for person in persons_list]
        try: 
            answer = get_llm_answer(search_query, formatted_documents)
        except Exception as e:
            answer = {"error": "Error processing LLM request"}
                      
    else:
        answer ={"error": "No matching documents found."}
    
    response_data = [{'id':1,
                      'name':search_query,
                      'age':answer}]
    return JsonResponse(response_data, safe=False)




# @api_view(['POST'])
# def create_dbset(request):
#     data=request.data
#     seriliser = BookSerializer(data=data)
#     if seriliser.is_valid():
#         seriliser.save()
#         return Response(seriliser.data, status = status.HTTP_201_CREATED)
#     return Response(seriliser.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', 'DELETE'])
# def dbset_detail(request, pk):
#     try:
#         book = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'DELETE':
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         data = request.data
#         serialiser = BookSerializer(book, data=data)
#         if serialiser.is_valid():
#             serialiser.save()
#             return Response(serialiser.data)
#         return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Create your views here.

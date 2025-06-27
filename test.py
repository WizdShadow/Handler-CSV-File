import pytest
import argparse
import csv
import os
from main import where, agg


@pytest.fixture(autouse=True)
def create_cvs():
    with open("data_test.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iphone 15 pro", "apple", "999", "4.9"])
        writer.writerow(["galaxy s23 ultra", "samsung", "1199", "4.8"])
        writer.writerow(["redmi note 12", "xiaomi", "199", "4.6"])
        writer.writerow(["poco x5 pro", "xiaomi", "299", "4.4"])
        writer.writerow(["poco x5 pro", "xiaomi", "299", "4.5"])
    with open("pust.csv", "w") as f:
        writer = csv.writer(f)  
        writer.writerow("")
    yield 
    os.remove("data_test.csv")
    os.remove("pust.csv")
        

def test_agg_max():
    colums = ['name', 'brand', 'price', 'rating']
    data = [
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '500', 'rating': '4.4'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.5'}   
    ]
    assert agg("price=max", data, colums) == ("500", "max")
    

def test_agg_min():
    colums = ['name', 'brand', 'price', 'rating']
    data = [
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '500', 'rating': '4.4'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.5'}   
    ]
    assert agg("price=min", data, colums) == ("299", "min")
    
    
def test_agg_avg():
    colums = ['name', 'brand', 'price', 'rating']
    data = [
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '999', 'rating': '4.2'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '1199', 'rating': '4.3'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '199', 'rating': '4.4'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.6'}   ,
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.7'}   
    ]
    assert agg("price=avg", data, colums) == ("599", "avg")
    

def test_agg_error_1():
    colums = ['name', 'brand', 'price', 'rating']
    data = [
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '500', 'rating': '4.4'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.5'}   
    ]
    assert agg("price=let", data, colums) == (None, "No operator")
    

def test_agg_error_2():
    colums = ['name', 'brand', 'price', 'rating']
    data = [
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '500', 'rating': '4.4'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.5'}   
    ]
    assert agg("lest=max", data, colums) == (None, "No column")
    

def test_where_error_1():
    mock_argument = argparse.Namespace(file=None, where=None, aggregate=None)
    assert where(mock_argument) == (None, "No file or incorrect file path")
    

def test_where_error_2():
    mock_argument = argparse.Namespace(file="pust.csv")
    assert where(mock_argument) == (None, "No data")
    

def test_where_error_3():
    mock_argument = argparse.Namespace(file="data_test.csv", where="test=1")
    assert where(mock_argument) == (None, "No column")
    
    
def test_where_error_4():
    mock_argument = argparse.Namespace(file="data_test.csv", where="test/1")
    assert where(mock_argument) == (None, "No operator")
    

def test_where_more():
    mock_argument = argparse.Namespace(file="data_test.csv", where="rating>4.7", aggregate=None)
    assert where(mock_argument) == ([['name', 'brand', 'price', 'rating'],
                                     ['iphone 15 pro', 'apple', '999', '4.9'],
                                     ['galaxy s23 ultra', 'samsung', '1199', '4.8']], None)


def test_where_more():
    mock_argument = argparse.Namespace(file="data_test.csv", where="rating>4.7", aggregate=None)
    assert where(mock_argument) == ([['name', 'brand', 'price', 'rating'],
                                     ['iphone 15 pro', 'apple', '999', '4.9'],
                                     ['galaxy s23 ultra', 'samsung', '1199', '4.8']], None)
    
    
def test_where_less():
    mock_argument = argparse.Namespace(file="data_test.csv", where="rating<4.7", aggregate=None)
    assert where(mock_argument) == ([['name', 'brand', 'price', 'rating'],
                                     ['redmi note 12', 'xiaomi', '199', '4.6'],
                                     ['poco x5 pro', 'xiaomi', '299', '4.4'],
                                     ['poco x5 pro', 'xiaomi', '299', '4.5']], None)
    
    
def test_where_equal():
    mock_argument = argparse.Namespace(file="data_test.csv", where="rating=4.8", aggregate=None)
    assert where(mock_argument) == ([['name', 'brand', 'price', 'rating'],
                                     ['galaxy s23 ultra', 'samsung', '1199', '4.8']], None)
    

def test_where():
    mock_argument = argparse.Namespace(file="data_test.csv", where=None, aggregate=None)
    assert where(mock_argument) == ([['name', 'brand', 'price', 'rating'],
                                     ['iphone 15 pro', 'apple', '999', '4.9'],
                                     ['galaxy s23 ultra', 'samsung', '1199', '4.8'],
                                     ['redmi note 12', 'xiaomi', '199', '4.6'],
                                     ['poco x5 pro', 'xiaomi', '299', '4.4'],
                                     ['poco x5 pro', 'xiaomi', '299', '4.5']], None)



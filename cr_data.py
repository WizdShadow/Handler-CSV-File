import csv

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'brand', 'price', 'rating'])
    writer.writerow(['iphone 15 pro', 'apple', '999', '4.9'])
    writer.writerow(['galaxy s23 ultra', 'samsung', '1199', '4.8'])
    writer.writerow(['redmi note 12', 'xiaomi', '199', '4.6'])
    writer.writerow(['poco x5 pro', 'xiaomi', '299', '4.4'])
    writer.writerow(['poco x5 pro', 'xiaomi', '299', '4.5'])
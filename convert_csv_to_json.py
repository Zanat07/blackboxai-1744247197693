import csv
import json

data = {}
filenames = {
    'financial': 'financial_data.csv',
    'geographic': 'geographic_data.csv', 
    'demographic': 'demographic_data.csv',
    'product_segments': 'product_segments.csv'
}

for name, filename in filenames.items():
    with open(filename) as f:
        data[name] = list(csv.DictReader(f))

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

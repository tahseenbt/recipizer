from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/results', methods=['POST'])
def results():
    data = request.form
    query = ','.join([data[key] for key in data])
    dishes = get_dishes(query)
    return render_template('results.html', images=dishes)

def get_dishes(query):
    
    app_id = ""
    app_key = ""
    req = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}'
    x = requests.get(req)
    content = x.content
    dict_data = json.loads(content.decode('utf-8'))
    # get name, image, calories, proteins, carbs, fats, ingredients of the top 3 dishes
    
    dishes = []
    for i in range(len(dict_data["hits"])):
        if i < 3:
            dish = {
                "name": dict_data["hits"][i]["recipe"]["label"],
                "src": dict_data["hits"][i]["recipe"]["image"],
                "calories": round(dict_data["hits"][i]["recipe"]["calories"]),
                "proteins": round(dict_data["hits"][i]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]),
                "carbs": round(dict_data["hits"][i]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]),
                "fats": round(dict_data["hits"][i]["recipe"]["totalNutrients"]["FAT"]["quantity"]),
                "ingredients": ", ".join(dict_data["hits"][i]["recipe"]["ingredientLines"])
            }
            dishes.append(dish)
        else:
            break

    return dishes


if __name__ == '__main__':
    app.run(debug=False)


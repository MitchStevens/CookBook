from flask import Flask, url_for, Markup, render_template
import json

app = Flask(__name__)

f = open('recipes.json', 'r')
json_file = json.load(f)

all_recipes = json_file.get('recipes')
for i in range(0, len(all_recipes)):
  all_recipes[i]['index'] = i

all_meats = {}
group_by_meat = {}

for r in all_recipes:
  if r.get('meat_type') == 'Meatless':
    group_by_meat.setdefault('Meatless', [])
    group_by_meat['Meatless'].append(r)
  else:
    meat = r.get('meat_type').split()
    group_by_meat.setdefault(meat[0], {})
    group_by_meat[meat[0]].setdefault(meat[1], [])
    group_by_meat[meat[0]][meat[1]].append(r)
    all_meats.setdefault(meat[0] , set())
    all_meats[meat[0]].add(meat[1])

@app.route('/')
def index():
  recipes = group_by_meat
  return render_template('index.html', recipes=generate_recipe_HTML(recipes), num_recipes=count_recipes(recipes), meats=all_meats)

@app.route('/group/<meat>')
def by_meat(meat):
  recipes = { meat: group_by_meat[meat] }
  return render_template('index.html', recipes=generate_recipe_HTML(recipes), num_recipes=count_recipes(recipes), meats=all_meats)

@app.route('/group/<meat>/<submeat>')
def by_submeat(meat, submeat):
  recipes = { meat: { submeat: group_by_meat[meat][submeat] } }
  return render_template('index.html', recipes=generate_recipe_HTML(recipes), num_recipes=count_recipes(recipes), meats=all_meats)

@app.route("/recipe/<int:n>")
def recipe(n):
  return render_template('recipe.html', recipe=all_recipes[int(n)])

def generate_recipe_HTML(recipes):
  def font_size(text, depth):
    if depth is 0:
      return '<h2>%s</h2>' % text
    else:
      return text

  def generate_rec(obj, depth):
    if isinstance(obj, dict):
      if obj.get('name') is not None and obj['index'] is not None:
        return '<a href="/recipe/{i}">{name}</a>'.format(i=obj['index'], name=obj['name'])
      else:
        s = '<ul>'
        for k in obj:
          s += '<li>' + font_size(str(k), depth)
          s += generate_rec(obj[k], depth+1) + '</li>'
        return s + "</ul>"
    elif isinstance(obj, set) or isinstance(obj, list):
      s = '<ul>'
      for x in obj:
        s += '<li>' + generate_rec(x, depth+1) + '</li>'
      return s + '</ul>'

  return generate_rec(recipes, 0)




def count_recipes(obj):
  if isinstance(obj, dict):
    if obj.get('name') is not None and obj['index'] is not None:
      return 1
    else:
      return sum(map(count_recipes, obj.values()))
  elif isinstance(obj, set) or isinstance(obj, list):
    return sum(map(count_recipes, obj))
  return 0

import os


# app = Flask(__name__)
app.run(host='192.168.1.19')
# app.run(host='localhost:5000')

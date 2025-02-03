from flask import Flask, render_template, json


app = Flask(__name__)

data = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'},
    # More blog posts can go here...
]

# Function to create a json file with the given data
def initiate_json_file():
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

# Function to load posts from JSON file
def load_posts():
    with open("data.json", "r") as file:
        return json.load(file)  # Load JSON into a Python list


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
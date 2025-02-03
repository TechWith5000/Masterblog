from flask import Flask, render_template, json, request, redirect, url_for


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

def save_posts(posts):
    with open("data.json", "w") as file:
        json.dump(posts, file, indent=4)

# Get the next available ID
def get_next_id():
    posts = load_posts()
    if posts:
        return max(post["id"] for post in posts) + 1
    return 1

def fetch_post_by_id(post_id):
    posts = load_posts()  # Load all posts from JSON
    for post in posts:
        if post["id"] == post_id:  # Check if the ID matches
            return post
    return None  # Return None if post is not found


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        # Load existing posts
        posts = load_posts()

        # Create new post dictionary
        new_post = {
            "id": get_next_id(),
            "title": title,
            "author": author,
            "content": content,
        }

        # Add the new post and save
        posts.append(new_post)
        save_posts(posts)

        # Redirect to home page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    posts = load_posts()  # Load existing posts

    # Filter out the post with the given ID
    new_posts = []
    for post in posts:  # Loop through each post
        if post["id"] != post_id:  # Check if post should be kept
            new_posts.append(post)  # Append it to the new list
    posts = new_posts  # Replace old list with the new one

    save_posts(posts)  # Save updated posts back to JSON

    return redirect(url_for("index"))  # Redirect back to homepage


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Load all posts
    posts = load_posts()
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Get updated data from the form
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]

        post["author"] = author
        post["title"] = title
        post["content"] = content


    # Save updated post back to JSON
    for i, p in enumerate(posts):
        if p["id"] == post_id:
            posts[i] = post  # Update the post in the list
            break

    save_posts(posts)  # Save changes to file

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
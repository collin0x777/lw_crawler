from bs4 import BeautifulSoup
import requests
import csv
import time
import functools

crawl_delay = 0.5
post_ids_file = "post_ids.txt"
output_file = "posts.csv"

def form_post_url(post_id):
    return f"https://www.lesswrong.com/posts/{post_id}"

def form_user_url(user_id):
    return f"https://www.lesswrong.com/users/{user_id}"

def get_page(url):
    time.sleep(crawl_delay)
    response = requests.get(url, headers={"User-Agent": "XY"})
    return response.text

@functools.cache
def parse_author_karma(author_id):
    text = get_page(form_user_url(author_id))
    soup = BeautifulSoup(text, "html.parser")
    return soup.find("span", class_="UsersProfile-userMetaInfo").find("span").text

def parse_post(text, post_id):
    soup = BeautifulSoup(text, "html.parser")

    authorElement = soup.find("span", class_="PostsAuthors-authorName").find("span").find("span").find("span").find("a")
    author = authorElement.text
    author_id = authorElement["href"].split("/")[2]

    author_karma = parse_author_karma(author_id)

    title = soup.find("a", class_="PostsPageTitle-link").text

    length = soup.find("span", class_="PostsPagePostHeader-wordCount").text.split(" ")[0]

    date = soup.find("span", class_="PostsPageDate-date").text

    comments = soup.find("a", class_="PostsPagePostHeader-secondaryInfoLink").text.split(" ")[0]

    scoreElement = soup.find("div", class_="PostsVote-voteScores")
    votes = scoreElement.find("div")["title"].split(" ")[0]
    score = scoreElement.find("div").find("h1").text

    return {
        "post_id": post_id,
        "author": author,
        "author_id": author_id,
        "author_karma": author_karma,
        "title": title,
        "length": length,
        "date": date,
        "comments": comments,
        "votes": votes,
        "score": score
    }


def read_post_ids():
    with open(post_ids_file, "r") as f:
        return f.read().split("\n")

def read_posts(post_ids):
    posts = []

    for (idx, post_id) in enumerate(post_ids):
        print(f"Processing post {idx+1} of {len(post_ids)}")
        try:
            url = form_post_url(post_id)
            post_text = get_page(url)
            post = parse_post(post_text, post_id)
            posts.append(post)
        except:
            pass

    return posts

def write_data(data):
    fieldnames = data[0].keys()

    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    print("Reading posts...")
    post_ids = read_post_ids()
    posts = read_posts(post_ids)
    write_data(posts)

if __name__ == "__main__":
    main()
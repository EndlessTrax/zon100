import csv
import requests
from bs4 import BeautifulSoup


URLS = [
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Dystopian-Science-Fiction/zgbs/digital-text/6361470011/ref=zg_bs_nav_kstore_4_158591011",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Dystopian-Science-Fiction/zgbs/digital-text/6361470011/ref=zg_bs_pg_2?_encoding=UTF8&pg=2",
]

for url in URLS:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    items = soup.find_all(class_="a-list-item")

    with open("results.csv", "a", encoding="utf-8") as csv_file:
        fieldnames = [
            "Rank",
            "Book Title",
            "Author",
            "Price",
            "Book Link",
            "Author Link",
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for item in items:
            rank = item.find(class_="zg-badge-text").text
            title = item.find(class_="p13n-sc-truncate-desktop-type2").text.strip()
            rel_link = item.find(class_="a-link-normal")["href"]

            author_anchor = item.find(class_="a-row a-size-small").a
            author_name = author_anchor.text
            author_link = author_anchor["href"]

            price = item.find(class_="p13n-sc-price").text

            csv_writer.writerow(
                {
                    "Rank": rank,
                    "Book Title": title,
                    "Author": author_name,
                    "Price": price,
                    "Book Link": f"https://www.amazon.com{rel_link}",
                    "Author Link": f"https://www.amazon.com{author_link}",
                }
            )

            print(f"Added: {title}")

print("Done!")

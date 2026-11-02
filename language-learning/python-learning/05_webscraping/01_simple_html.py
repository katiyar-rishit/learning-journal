from bs4 import BeautifulSoup

SIMPLE_HTML = """
    <html>
        <head></head>
        <body>
        <h1>This is a title</h1>
        <p class="subtitle">67</p>
        <p>When knee surgery is tomorrow.</p>
        <ul>
            <li>Rishit</li>
            <li>Ayush</li>
            <li>Harsh</li>
            <li>Mayank</li>
        </ul>
        </body>
    </html>
"""

simple_soup = BeautifulSoup(SIMPLE_HTML, "html.parser")

print(simple_soup.find("h1"))
header = simple_soup.find("h1")

assert header is not None
print(header.string)


def find_list_members_tags():
    names = BeautifulSoup(SIMPLE_HTML, "html.parser")
    print(names.find_all("li"))


def find_list_members():
    agent = BeautifulSoup(SIMPLE_HTML, "html.parser")
    names = [name.string for name in agent.find_all("li")]  # list-comprehension
    print(names)


find_list_members_tags()
find_list_members()

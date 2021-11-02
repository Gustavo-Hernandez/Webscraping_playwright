from playwright.sync_api import sync_playwright

companies = []


def handle_company_request():
    company_name = input("Company name: ").lower().replace(" ", "_")
    url_tail = company_name + "&page=1"
    url = "https://www.importyeti.com/search?q=" + url_tail
    print("[Fetching]", url)
    return url


def block_selected_resources(route):
    excluded_resources = ["stylesheet", "image", "font"]

    if route.request.resource_type in excluded_resources:
        route.abort()
    else:
        route.continue_()


def modify_data(data):
    global companies
    companies.append(data)


with sync_playwright() as p:

    url = handle_company_request()
    browser = p.firefox.launch()
    page = browser.new_page()

    def handle_response(response):
        if "https://api.importyeti.com/api/search?q=" in response.url:
            try:
                print(response.headers)
                modify_data(response.json())
            except:
                print("<<", response.status, response.url)

    page.on("response", handle_response)

    page.goto(url, wait_until="networkidle", timeout=120000)
    page.context.close()
    browser.close()

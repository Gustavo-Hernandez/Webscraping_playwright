from playwright.sync_api import sync_playwright

url = "https://www.auction.com/residential/ca/"

excluded_resources = ["stylesheet", "image", "font"]


def block_selected_resources(route):
    if route.request.resource_type in excluded_resources:
        route.abort()
    else:
        route.continue_()


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # page.route("**/*", block_selected_resources) # For blocked resource types

    def handle_response(response):
        if "v1/search/assets?" in response.url:
            print(response.json()["result"]["assets"]["asset"])

    page.on("response", handle_response)

    page.goto(url, wait_until="networkidle", timeout=120000)
    page.wait_for_selector("h4[data-elm-id]", timeout=120000)
    # print(page.content())
    page.context.close()
    browser.close()

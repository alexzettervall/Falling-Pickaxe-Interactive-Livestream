import time
from numpy import append
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chat_messages: list[tuple[str, str]] = []

def init(url: str):
    # Optional: run in headless mode
    options = Options()
    #options.add_argument("--headless")

    # Path to your chromedriver (omit Service() if chromedriver is in PATH)
    #service = Service("/path/to/chromedriver")

    driver = webdriver.Chrome()
    driver.get(url)

    wait = WebDriverWait(driver, 30)

    # Wait for chat iframe and switch to it
    chat_iframe = wait.until(
        EC.presence_of_element_located((By.ID, "chatframe"))
    )
    driver.switch_to.frame(chat_iframe)

    # Inject MutationObserver to capture chat messages
    driver.execute_script("""
        window.collectedMessages = [];

        const target = document.querySelector("yt-live-chat-item-list-renderer #items");

        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const author = node.querySelector("#author-name");
                        const message = node.querySelector("#message");

                        if (author && message) {
                            window.collectedMessages.push({
                                author: author.innerText,
                                message: message.innerText
                            });
                        }
                    }
                });
            });
        });

        observer.observe(target, { childList: true });
    """)

    print("Listening for live chat messages...\n")

    try:
        while True:
            messages = driver.execute_script("""
                const msgs = window.collectedMessages.slice();
                window.collectedMessages.length = 0;
                return msgs;
            """)

            for msg in messages:
                author: str = msg['author']
                message: str = msg['message']
                chat_messages.append((author, message))

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        driver.quit()
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

google_play_books_url = r"https://play.google.com/store/books"
library_url = r"https://play.google.com/books"
book_reader_url = r"https://play.google.com/books/reader"

account_button = r"/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[1]/button"
login_button = r"/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[2]/div/ul/li[@data-href='https://accounts.google.com/ServiceLogin?service=googleplay&passive=86400']"

iframe_tag = r"/html/body/iframe"

display_setting_button = r"/html/body/reader-app/reader-app-bar/div[last()]/button[3]"
reading_dropdown = r"/html/body/div[3]/div/div/mat-dialog-container/div/div/reader-display-options/mat-dialog-content/label[@for='reading-mode-select']/following-sibling::mat-form-field"
zoom_dropdown = r"/html/body/div[3]/div/div/mat-dialog-container/div/div/reader-display-options/mat-dialog-content/label[@for='zoom-select']/following-sibling::mat-form-field"
option_first_button = r"/html/body/div[3]/div[3]/div/div/mat-option[1]"
option_last_button = r"/html/body/div[3]/div[3]/div/div/mat-option[last()]"
scroll_toggle = r"/html/body/div[3]/div/div/mat-dialog-container/div/div/reader-display-options/mat-dialog-content/mat-slide-toggle[2]/div/button[@aria-checked='true']"
layout_checkbox = r"/html/body/div[3]/div/div/mat-dialog-container/div/div/reader-display-options/mat-dialog-content/mat-button-toggle-group/mat-button-toggle[3]/button"

more_button = r"/html/body/reader-app/reader-app-bar/div[last()]/button[7]"
info_button = r"/html/body/div[3]/div/div/mat-dialog-container/div/div/reader-overflow-menu/mat-dialog-content/button[1]"
book_title_tag = r"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/info-dialog/mat-dialog-content/div/div/h1"
author_tag = r"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/info-dialog/mat-dialog-content/div/div/h2/a"
publisher_tag = r"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/info-dialog/mat-dialog-content/div/div/h3[1]"
info_close_button = r"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/info-dialog/button"

content_table_button = r"/html/body/reader-app/reader-app-bar/div[last()]/button[4]"
first_page_button = r"/html/body/div[3]/div/div/mat-dialog-container/div/div/reader-contents/mat-tab-group/div/mat-tab-body[1]/div/reader-table-of-contents/mat-nav-list/a[1]"

next_page_button = r"/html/body/reader-app/div/reader-pages/reader-scrubber/div/button[2]"
book_page_containers = r"/html/body/reader-app/div/reader-pages/reader-horizontal-view/ol/li/reader-page"
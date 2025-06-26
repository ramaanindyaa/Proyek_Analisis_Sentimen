from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import random
import os
import pandas as pd

# Definisi kategori dan URL untuk scraping komprehensif
# Target: minimal 3.000 sampel review (lebih baik 10.000+)
categories = {
    "Pakaian_wanita.csv": [
        "https://www.tokopedia.com/istana-fashion11/april-top-atasan-wanita-korean-top-baju-knit-basic-long-sleeve-april-top-panjang-kemeja-bona-viral-1730393737063335819",
        "https://www.tokopedia.com/orloid-883/september-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-pendek-basic-short-sleeve-1729580958718460989",
        "https://www.tokopedia.com/firda-fashion-862/dress-kaftan-batik-elegan-wanita-pesta-aruna-1729615492746545673",
        "https://www.tokopedia.com/rizkizea-id/promo-kemeja-3pcs-100rb-paket-hemat-3-pcs-100-ribuan-atasan-wanita-ii-kemeja-wanita-kantoran-ii-blouse-wanita-terbaru-kemeja-wanita-murah-baju-casual-dewasa-shakila-1729861762620557669",
        "https://www.tokopedia.com/threeputraaaid/daster-wanita-katun-grade-a-baju-tidur-daster-daster-kekinian-fit-rayon-nyaman-motif-1730692648449640401",
        "https://www.tokopedia.com/outfitquu-325/blouse-kemeja-polos-oversize-atasan-basic-wanita-polo-linen-nami-1730399537829283452",
        "https://www.tokopedia.com/wssehat/dress-gaun-panjang-wanita-brokat-kekinian-terbaru-lengan-panjang-v-neck-slim-fitting-polos-bunga-jalan-manis-casual-pesta-kondangan-midi-karet-mewah-natal-maxi-baju-1729735582367254590",
        "https://www.tokopedia.com/chanmifashion/ch-jasmine-shirt-bordir-stripe-1731454929986880531"
    ],
    "Pakaian_pria.csv": [
        "https://www.tokopedia.com/novoidminds/no-void-minds-aezy-regular-fit-core-t-shirt-charcoal-charcoal-s-59ab9",
        "https://www.tokopedia.com/cozyclub/cozyclub-frank-polo-knit-shirt-kaos-kerah-pria-kaos-lengan-pendek-baju-brown-panjang-casual-1729625526336981441",
        "https://www.tokopedia.com/kenzidstore/sweater-halfzip-polos-unisex-pria-wanita-abu-misty-m-9f45d",
        "https://www.tokopedia.com/koel-toko/kemeja-polos-pria-lengan-panjang-katun-premium-baju-kerja-kampus-kondangan-kantor-formal-casual-santai-nyaman-simple-navy-putih-hitam-slimfit-kerah-kancing-variasi-hem-1729631591021577981",
        "https://www.tokopedia.com/rainstyle-store/t-shirt-kaos-polo-list-kerah-gior-since-1981-text-hitam-polo-kerah-unisex-pria-wanita-1730932775277069601",
        "https://www.tokopedia.com/kenzidstore-800/crewneck-polos-halfzif-bahan-fleece-pria-unisex-sweater-dewasa-panjang-1730210819252848107",
        "https://www.tokopedia.com/storeshop06/jaket-bomber-pria-waterproof-korea-blazer-casual-tebal-cream-m-65c4e",
        "https://www.tokopedia.com/tamp-xid/tamp-x-new-short-sleevemen-s-lapel-business-casual-shirtpoloshirt-polo-shirt-polo-tipis-1731542679684810533"
    ],
    "Alas_kaki.csv": [
        "https://www.tokopedia.com/juragansepatu-457/k9nine-sepatu-sneakers-pria-sepatu-import-fashion-olahraga-casual-shoes-1729643528337066827",
        "https://www.tokopedia.com/veranevada/vn-sepatu-blu-sneakers-wanita-sport-shoes-casual-black-a74-1729561661100033187",
        "https://www.tokopedia.com/dunia-fashion88/dunia-fashion-df-506-sepatu-wanita-sneakers-wanita-olahraga-premium-quality-1729385167729886935",
        "https://www.tokopedia.com/luckyfanstore/luckyfanstore-sepatus-fashion-casual-d27-pria-shoes-sport-kasual-running-sneaker-1729597526810986884",
        "https://www.tokopedia.com/techdoo/techdoo-sepatu-slip-on-sneakers-pria-hitam-sepatu-selop-cowok-sepatu-kerja-kuliah-sepatu-cowok-keren-anti-slip-sepatu-kekinian-mr713-1729653683394741325",
        "https://www.tokopedia.com/amanah-shop95/promo-sepatu-p-ma-classics-pria-formal-suede-xl-royal-blue-white-sepatu-sneakers-pria-wanita-unisexs-premium-high-quality-1730407108765386450",
        "https://www.tokopedia.com/gio-saverino/gio-saverino-sepatu-sneakers-pria-leo-black-casual-shoes-1729855660924307843",
        "https://www.tokopedia.com/leedoo/leedoo-sepatu-cowok-keren-sneakers-round-toe-running-shoes-sepatu-pria-casual-kekinian-kerja-karet-sneaker-murah-mc430-1729608198449564219"
    ],
    "Elektronik.csv": [
        "https://www.tokopedia.com/bestdealofficial/vivan-vps-p300-power-station-600w-220v-96000mah-300wh-powerbank-portable-charger-station-power-supply",
        "https://www.tokopedia.com/mgnstorepedia/s1s-drone-brushless-dual-camera-8k-sensor-anti-tabrak-optical-flow-s1s-2-battre",
        "https://www.tokopedia.com/blora-store-electrik/kipas-angin-lampu-plafon-infico-inf-520-b-langit-langit-rumah-remote-control-lamp-led-jumbo-20-5in-40watt-1731290155029136625",
        "https://www.tokopedia.com/huaiwen-pc-store/hw-komputer-full-pc-all-in-one-baru-terbaru-hd-super-tipis-intel-core-i3-i5-i7-untuk-rumah-belajar-kantor-gaming-dan-hiburan-19-22-24-27-inch-curve-gratis-keyboard-dan-mouse-kemasan-karton-dan-busa-rak-kayu-inklusif-garansi-1-tahun-kabel-layar-1731226945882785479",
        "https://www.tokopedia.com/jblstoreindonesia/100-original-jbl-flip-6-wireless-bluetooth-speaker-powerful-sound-deep-bass-ipx7-waterproof-outdoor-and-travel-speaker-portable-bluetoot-speaker-jbl-1731319285187183847",
        "https://www.tokopedia.com/agen-murah-99/panasonic-th-65mx650g-premium-4k-led-google-tv-65-inch-1731674337531037490",
        "https://www.tokopedia.com/angelwingssound/100-original-sony-wh-xb910n-over-ear-sony-headphones-wireless-headphones-bluetooth-headphones-with-microphone-sports-headphones-1730832754622170646",
        "https://www.tokopedia.com/originalappleaudio/100-ori-samsung-galaxy-watch-7-44mm-smartwatch-waterproof-bluetooth-fitness-blood-pressure-blood-oxygen-sleep-monitoring-sport-jam-smart-watch-wanita-galaxy-watch-6-watch-ultra-samsung-galaxy-bluetooth-watch-pria-wanita-for-ios-android-samsung-watch7-1731199197810820899"
    ],
    "Makanan_minuman.csv": [
        "https://www.tokopedia.com/gudeg-kaleng-bu-tjitro/gudeg-kaleng-bu-tjitro-all-varian-special-promo-basreng-orignal-7d26c",
        "https://www.tokopedia.com/chiputmandalawangi/makanan-instan-h-eat-makanan-gunung-nasi-putih-nasi-goreng-rendang-glai-dging-sapi-2144f",
        "https://www.tokopedia.com/bittersweet-by-najla/bts-satuan-snacktok-pilih-variant-1729601689662622465",
        "https://www.tokopedia.com/aneka-snack--food/seblak-campur-seblak-mix-500gr-aneka-kerupik-seblak-beton-seblak-asbes-seblak-sisir-seblak-kerupuk-rafael-renyah-pedas-1730419722794272733",
        "https://www.tokopedia.com/nyai-mercon-471/paket-pangsit-rangu-dan-pangsit-ayam-keju-makanan-instan-kemasan-rendah-gula-1729508894667082081",
        "https://www.tokopedia.com/indopowder/bubuk-minuman-aneka-rasa-99-variant-1-kg-1729544758982707880",
        "https://www.tokopedia.com/toko-bangsatria/5-lima-bungkus-seblak-instan-paket-hemat-bangsatria-food-jajanan-alami-makanan-pedas-1729991778552350859",
        "https://www.tokopedia.com/makijah/oseng-mercon-koyor-tetelan-sapi-pedas-siap-makan-1729741352567014921"
    ]
}

def setup_browser():
    """Setup dan mengembalikan instance browser Chrome"""
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    return webdriver.Chrome(options=chrome_options)

def close_popup_if_exists(driver, timeout=5):
    """Menutup popup jika muncul"""
    try:
        popup = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[role="dialog"]'))
        )
        print("Popup detected")
        close_button = popup.find_element(By.CSS_SELECTOR, 'button')
        close_button.click()
        print("Popup closed")
        sleep(1)
    except TimeoutException:
        print("No popup appeared")

def scrape_product_details(browser, url, category_file):
    """
    Scrape detail produk dari URL yang diberikan
    dan menyimpannya ke file CSV berdasarkan kategori
    """
    print(f"\n{'='*50}")
    print(f"🔍 Scraping: {url}")
    print(f"📁 Category: {category_file}")
    print(f"{'='*50}\n")
    
    browser.get(url)
    close_popup_if_exists(browser)
    
    try:
        print("Waiting for product detail to load...")
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-j63za0"))
        )
        print("✅ Page is ready!")
        sleep(3)  # Allow full JS to load

        html = browser.execute_script("return document.documentElement.innerHTML")
        soup = BeautifulSoup(html, "html.parser")

        # === Detect Product Name ===
        product_name_tag = soup.find("h1", class_="css-j63za0")
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else None
        if not product_name:
            product_name_tag = soup.find("h1", class_="css-14yroid")
            product_name = product_name_tag.get_text(strip=True) if product_name_tag else None
        
        if product_name:
            print(f"🔹 Product Name Detected: {product_name}")
        else:
            print("❌ Product name not found.")
            return False

        # === Get Product Prices ===
        current_price_tag = soup.find("div", {"data-testid": "lblPDPDetailProductPrice"})
        original_price_tag = soup.find("span", {"data-testid": "lblPDPDetailOriginalPrice"})

        current_price = current_price_tag.get_text(strip=True) if current_price_tag else "-"
        original_price = original_price_tag.get_text(strip=True) if original_price_tag else "-"

        print(f"💰 Current Price : {current_price}")
        print(f"💸 Original Price: {original_price}")

        # === Get Product Image URL ===
        image_tag = soup.find("img", {"data-testid": "PDPMainImage"})
        image_url = image_tag["src"] if image_tag and image_tag.has_attr("src") else "-"
        print(f"🖼️ Image URL     : {image_url}")

        # === Get Stock Quantity ===
        stock_tag = soup.find("p", {"data-testid": "stock-label"})
        stock_value = "-"
        if stock_tag:
            bold_tag = stock_tag.find("b")
            if bold_tag:
                stock_value = bold_tag.get_text(strip=True)

        print(f"📦 Stock        : {stock_value}")

        # Prepare product data
        product_data = {
            "Product Name": product_name or "-",
            "Current Price": current_price,
            "Original Price": original_price,
            "Image URL": image_url,
            "Stock": stock_value
        }

        # Save to CSV file
        save_product_to_csv(product_data, category_file)
        
        # Collect reviews (kirimkan category_file juga)
        review_count = scrape_and_save_reviews(browser, product_name, category_file)
        
        return True, review_count
        
    except TimeoutException:
        print("❌ Page load timeout!")
        return False, 0
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return False, 0

def save_product_to_csv(product_data, filename):
    """Menyimpan data produk ke file CSV dalam folder kategori"""
    # Buat nama folder dari nama file (hilangkan ekstensi .csv)
    folder_name = os.path.splitext(filename)[0]
    
    # Buat path folder
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Buat folder jika belum ada
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Created new directory: {folder_name}/")
    
    # Tentukan path file dalam folder
    file_path = os.path.join(folder_path, filename)
    
    # Proses seperti sebelumnya, tapi dengan path file yang baru
    if os.path.exists(file_path):
        # Read existing CSV to count rows
        existing_df = pd.read_csv(file_path)
        existing_rows = len(existing_df)

        # New item_id is next number
        item_id = existing_rows + 1
        product_data['item_id'] = item_id

        # Convert to DataFrame
        df = pd.DataFrame([product_data])

        # Append without header
        df.to_csv(file_path, mode='a', index=False, header=False)
        print(f"💾 Appended product info as item_id {item_id} to existing file: {folder_name}/{filename}")

    else:
        # First entry, item_id = 1
        product_data['item_id'] = 1

        # Convert to DataFrame
        df = pd.DataFrame([product_data])

        # Write new file with header
        df.to_csv(file_path, index=False)
        print(f"💾 Created new file and saved product info as item_id 1: {folder_name}/{filename}")

def scrape_and_save_reviews(browser, product_name, category_file):
    """Scrape dan menyimpan review produk dalam folder kategori"""
    try:
        print("🧭 Scrolling to review section...")
        sleep(2)

        # scrolling down slowly
        stopScrolling = 0
        while True:
            stopScrolling += 1
            browser.execute_script("window.scrollBy(0,40)")
            sleep(0.5)
            if stopScrolling > 120:
                break
        sleep(3)
    except Exception as e:
        print(f"⚠️ Couldn't scroll to review section: {e}")
        return 0

    all_reviews = []
    page_number = 1

    while True:
        print(f"\n📖 Scraping review page {page_number}...\n")

        # Scroll to Reviews Section
        try:
            review_container = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "review-feed"))
            )
            browser.execute_script("arguments[0].scrollIntoView();", review_container)
            sleep(2)
        except:
            print("⚠️ Review section not found or not visible yet.")
            break

        # Refresh soup after scroll
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find All Reviews
        review_articles = soup.find_all("article", class_="css-15m2bcr")
        page_review_count = 0
        
        for idx, article in enumerate(review_articles, 1):
            review_text_tag = article.find("span", {"data-testid": "lblItemUlasan"})
            review_text = review_text_tag.get_text(strip=True) if review_text_tag else None

            rating_tag = article.find("div", {"data-testid": "icnStarRating"})
            rating = rating_tag.get("aria-label") if rating_tag else None

            date_tag = article.find("p", string=lambda text: text and any(k in text for k in ["minggu", "hari", "bulan"]))
            review_date = date_tag.get_text(strip=True) if date_tag else None

            if review_text or rating or review_date:
                print(f"💬 Review #{len(all_reviews)+1}:")
                print(f"   📌 Text   : {review_text if review_text else '-'}")
                print(f"   ⭐ Rating : {rating if rating else '-'}")
                print(f"   🕒 Date   : {review_date if review_date else '-'}")
                all_reviews.append({
                    "review": review_text,
                    "rating": rating,
                    "date": review_date,
                    "product_name": product_name,
                    "category": category_file.replace('.csv', '')
                })
                page_review_count += 1
            else:
                print(f"💬 Review #{len(all_reviews)+1}: No content found.")

        print(f"📊 Reviews found on page {page_number}: {page_review_count}")
        
        # Try to Click Next Button - dengan batas maksimal halaman
        if page_number >= 15:  # Batasi maksimal 15 halaman per produk
            print("🔄 Reached maximum page limit (15 pages)")
            break
            
        try:
            next_button = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Laman berikutnya') and not(@disabled)]"))
            )
            print("➡️ Moving to next page...")
            next_button.click()
            page_number += 1
            sleep(3)  # Wait before scraping next page
        except (TimeoutException, NoSuchElementException):
            print("✅ Reached last page or next button is not clickable.")
            break

    # Save reviews to CSV
    review_count = len(all_reviews)
    if all_reviews:
        print(f"✅ Total reviews collected: {review_count}")
        df = pd.DataFrame(all_reviews)
        
        # Hilangkan karakter yang tidak valid untuk nama file di Windows
        safe_product_name = product_name[:50]
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            safe_product_name = safe_product_name.replace(char, '_')
        
        # Buat nama folder dari nama file kategori (hilangkan ekstensi .csv)
        folder_name = os.path.splitext(category_file)[0]
        folder_path = os.path.join(os.getcwd(), folder_name)
        
        # Pastikan folder sudah ada (seharusnya sudah dibuat saat menyimpan produk)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Set path file review di dalam folder kategori
        filename = f"{safe_product_name}_reviews.csv"
        file_path = os.path.join(folder_path, filename)
        
        df.to_csv(file_path, index=False)
        print(f"💾 Reviews saved to: {folder_name}/{filename}")
    else:
        print("⚠️ No reviews collected.")
    
    return review_count

def scrape_tokopedia_by_category(categories_dict, max_products_per_category=10):
    """
    Menjalankan scraper untuk setiap kategori dan URLnya
    Target: Minimal 3.000 review total (lebih baik 10.000+ untuk skor tinggi)
    
    Args:
        categories_dict: Dictionary dengan key=nama file kategori dan value=list URL
        max_products_per_category: Maksimal produk yang discrape per kategori
    """
    browser = setup_browser()
    total_reviews_scraped = 0
    
    try:
        for category_file, urls in categories_dict.items():
            print(f"\n\n{'*'*70}")
            print(f"📂 PROCESSING CATEGORY: {category_file}")
            print(f"{'*'*70}\n")
            
            # Batasi jumlah produk per kategori
            product_count = 0
            category_reviews = 0
            
            for url in urls:
                if product_count >= max_products_per_category:
                    break
                
                success, review_count = scrape_product_details(browser, url, category_file)
                if success:
                    product_count += 1
                    category_reviews += review_count
                    total_reviews_scraped += review_count
                
                # Tambahkan jeda untuk menghindari anti-scraping
                sleep_time = random.uniform(3, 7)
                print(f"⏲️ Waiting for {sleep_time:.1f} seconds before next product...")
                sleep(sleep_time)
                
            print(f"\n✅ Completed scraping {product_count} products for category: {category_file}")
            print(f"📊 Total reviews in this category: {category_reviews}")
            
        print(f"\n🎯 TOTAL REVIEWS SCRAPED: {total_reviews_scraped}")
        print(f"📋 Target: 3,000+ reviews {'✅ ACHIEVED!' if total_reviews_scraped >= 3000 else '❌ Need more data'}")
    
    finally:
        print("\n🏁 All scraping tasks completed!")
        browser.quit()
        return total_reviews_scraped

if __name__ == "__main__":
    # Informasi tentang kategori yang tersedia
    print("""
    🛍️ TOKOPEDIA SCRAPER 🛍️
    
    Kategori yang tersedia:
    1. Pakaian wanita
    2. Pakaian pria
    3. Alas kaki
    """)
    
    # Jalankan scraper dengan target minimal 3.000 review
    total_scraped = scrape_tokopedia_by_category(categories, max_products_per_category=8)
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"📊 Total reviews scraped: {total_scraped}")
    print(f"✅ Target achieved: {'YES' if total_scraped >= 3000 else 'NO - Need more URLs or increase max_products_per_category'}")
    print(f"📁 Data saved in category folders with individual CSV files")



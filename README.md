## ✨Yandex Market
~14 ~6 ~7 ~5 ~1 ~2 ~4 ~5 ~6 ~7 ~10 ~11 ~12 ~13 ~14 ~15
***
### **Main info**
Crawler YM mobile app (.apk version)    
Summary YM have ~ **50.000.000** products and about **10.000.000** available to buy         
Working {-only-} on webshare or other EU proxies, avg crawl speed about **3-4k** pages/min  
YM crawler gets Main/Secondary characteristics, Categories, Images and collecting price history from each product   
### **Spider list**

- **tositemap** - get new products from YM sitemap
- **toskuinfoOnStock** - get/update secondary characteristics, images, categories
- **toupdate** - get/update product prices and main characteristics 
- **tovladpersonal** - update offers product info 


### **Timer tasks**
| Spider | Args | Time start/end | Start method
| ---      | ---      | ---      | ---    
| tovladpersonal |  | 08:00 -> 20:00 | start after end
| toupdate | loaders_type = 3 | 08:00 -> 20:00 | start after end
| toupdate | loaders_type = 5 |  | every hour

### **Spiders info**
***
#### 🕷️️  tositemap🕷️️  
~11 ~7

Collect **main information** of each one product in YM sitemap
~ **50.000.000** requests
need ~ **1 week** for all products on **4000 req/min** speed
##### Connections
- **mysql: yandex-market-prices**
    -  skus
        - product_id
        - sku
        - reviews_count
        - updated
    -  products
        - id
        - reviews_count
        - is_avail
        - updated

##### Collected Information from pages
- **ID товара с YM**
    - {-yandex-market-prices-}.products.{+product_id+}
    - {-yandex-market-prices-}.skus.{+product_id+}
- **ID комплектации товара с YM**
    - {-yandex-market-prices-}.skus.{+sku+}
- **Доступен ли товар к покупке?**  
    - {-yandex-market-prices-}.products.{+is_avail+}
- **Колличество отзывов**
    - {-yandex-market-prices-}.products.{+reviews_count+}
    - {-yandex-market-prices-}.skus.{+reviews_count+}
- **Время обновления** 
    - {-yandex-market-prices-}.products.{+updated+}
    - {-yandex-market-prices-}.skus.{+updated+}

#### 🕷️️  tovladpersonal🕷️️  
~11 ~7

Collect offers information on each product in marketplace db
~ **7000** requests
~ **7 min** working  
##### Connections
- **mysql 89.223.69.85: marketplace**
    -  merchants_
        - min_price
        - min_price_second
        - min_price_shop_id
        - min_price_express
        - min_price_express_second
        - min_price_express_shop_id
        - min_our_price
        - min_our_price_express
        - min_price_last_update
        - our_minimal
        - only_ours
        - our_shop_count
    -  storages
        - marketplace_id
        - shop_id
##### Collected Information from pages
- **Самая низкая цена с `обычной` доставкой с предложений конкурентов**
    - {-marketplace-}.merchants_.{+min_price+}
- **Вторая цена с `обычной` доставкой с предложений конкурентов**
  - {-marketplace-}.merchants_.{+min_price_second+}
- **ID конкурента с самой низкой ценою и `обычной` доставкой**
    - {-marketplace-}.merchants_.{+min_price_shop_id+}
- **Самую низкую цену с `express` с предложений конкурентов**
    - {-marketplace-}.merchants_.{+min_price_express+}
- **Вторую цену с `express` с предложений конкурентов**
    - {-marketplace-}.merchants_.{+min_price_express_second+}
- **ID конкурента с самой низкой ценою и `express` доставкой**
    - {-marketplace-}.merchants_.{+min_price_express_shop_id+}
- **Самую низкую цену с `обычной` доставкой с наших предложений**
    - {-marketplace-}.merchants_.{+min_our_price+}
- **Самую низкую цену с `express` с наших предложений**
    - {-marketplace-}.merchants_.{+min_our_price_express+}
- **Время обновления**
    - {-marketplace-}.merchants_.{+min_price_last_update+}
- **Наша цена минимальная?**
    - {-marketplace-}.merchants_.{+our_minimal+}
- **Только наши предложения?**
    - {-marketplace-}.merchants_.{+only_ours+}
- **Колличество наших предложений**
    - {-marketplace-}.merchants_.{+our_shop_count+}

#### 🕷️️  toupdate🕷️️  
~11 ~7

Collect dynamic metrics and categories from each sku of products, from loaders
##### Arguments
- **loaders_type** - type of filtration data(sku/product) for toupdate spider
    - {+=1+} : SELECT `.all()`
    - {+=2+} : SELECT `.filter(Sku.shop_count != 0 and Sku.shop_count != 1 and Sku.yandex_price_min).all()`
    - {+=3+} : SELECT `.filter(Category.category_nid == Navnode.id).filter(Navnode.category == "91491").filter(Sku.product_id == Category.product_id).filter(Sku.shop_count > 1).filter(Sku.brand != "").all()`
    - {+=4+} : SELECT `.filter(or_(Sku.shop_count != 1, Sku.shop_count == None)).all()`
    - {+=5+} : SELECT `.filter(Sku.brand != "").filter(Sku.shop_count > 1).filter(Category.category_nid.in_(category_nid)).filter(Sku.product_id == Category.product_id).filter(Category.category_nid == "91491").all()`
##### Connections
- **mysql: yandex-market-prices**
    - skus
        - product_id
        - price_min
        - price_min_second
        - yandex_price_min
        - shop_count
        - updated
        - promo
        - reviews_count
        - shop_name
        - count
        - yandex_rest
    - products
        - id
        - updated
    - categories
        - product_id
        - category_hid
        - category_nid
    - navnode
        - id
        - name
        - fullName
        - entity
        - type
        - isLeaf
        - category
        - slug
- **postgres: yandex-market-prices**
    - yandex
        - sku_id
        - price
        - time
##### Collected Information from pages
- product id
    - {-yandex-market-prices-}.products.{+product_id+}
    - {-yandex-market-prices-}.skus.{+id+}
- sku
    - {-yandex-market-prices-}.skus.{+sku+}
- available  
    - {-yandex-market-prices-}.products.{+is_avail+}
- reviews count
    - {-yandex-market-prices-}.products.{+reviews_count+}
    - {-yandex-market-prices-}.skus.{+reviews_count+}
- time 
    - {-yandex-market-prices-}.products.{+updated+}
    - {-yandex-market-prices-}.skus.{+updated+}

define({ "api": [
  {
    "type": "GET",
    "url": "getproducts/",
    "title": "Get All products",
    "version": "1.0.0",
    "name": "ListProducts",
    "group": "Products",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "products_list",
            "description": "<p>All products</p>"
          }
        ]
      }
    },
    "filename": "mobileServer/productUtils.py",
    "groupTitle": "Products"
  },
  {
    "type": "GET",
    "url": "getshopinventory/:shop_id",
    "title": "Get Shop Inventory",
    "version": "1.0.0",
    "name": "GetShopInventory",
    "group": "Shop",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "shop_id",
            "description": "<p>Shop unique ID.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "product",
            "description": "<p>Product serialized data</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "price",
            "description": "<p>Product's price</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "Stock",
            "description": "<p>Product in Stock/out of stock</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "image_width",
            "description": "<p>Product's image width</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "image_height",
            "description": "<p>Product's image height</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error",
            "description": "<p>{String} The <code>id</code> of the Shop was not found</p>"
          }
        ]
      }
    },
    "filename": "mobileServer/inventoryUtils.py",
    "groupTitle": "Shop"
  }
] });

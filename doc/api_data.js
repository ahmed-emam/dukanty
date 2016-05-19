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
    "groupTitle": "Products",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/getproducts/"
      }
    ]
  },
  {
    "type": "post",
    "url": "debug/inventory/",
    "title": "create/update Shop Inventory",
    "version": "1.0.0",
    "name": "CreateShopInventory",
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
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "product_id",
            "description": "<p>Product to be created/updated unique ID.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "price",
            "description": "<p>Product's price</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "stock",
            "description": "<p>Product in stock/out of stock (1 == True)/(0 == False)</p>"
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
            "description": "<p>created/updated product serialized data</p>"
          }
        ]
      }
    },
    "filename": "mobileServer/inventoryUtils.py",
    "groupTitle": "Shop",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/debug/inventory/"
      }
    ],
    "error": {
      "fields": {
        "NotFound": [
          {
            "group": "NotFound",
            "type": "String",
            "optional": false,
            "field": "ShopNotFoundError",
            "description": "<p><code>shop_id</code> does not exist</p>"
          },
          {
            "group": "NotFound",
            "type": "String",
            "optional": false,
            "field": "ProductNotFoundError",
            "description": "<p><code>product_id</code> does not exist</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"12 does not exist\"\n }",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"12 does not exist\"\n }",
          "type": "json"
        }
      ]
    }
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
    "filename": "mobileServer/inventoryUtils.py",
    "groupTitle": "Shop",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/getshopinventory/:shop_id"
      }
    ],
    "error": {
      "fields": {
        "NotFound": [
          {
            "group": "NotFound",
            "type": "String",
            "optional": false,
            "field": "ShopNotFoundError",
            "description": "<p><code>shop_id</code> does not exist</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"12 does not exist\"\n }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "getshops/",
    "title": "Get list of all shops in the system",
    "version": "1.0.0",
    "name": "GetShops",
    "group": "Shop",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "Shops",
            "description": "<p>List of all Shops</p>"
          }
        ]
      }
    },
    "filename": "mobileServer/views.py",
    "groupTitle": "Shop",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/getshops/"
      }
    ]
  },
  {
    "type": "post",
    "url": "add_address/",
    "title": "Add address for user",
    "version": "1.0.0",
    "name": "AddAddress",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "user_email",
            "description": "<p>User's email</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "lat",
            "description": "<p>Latitude of added address</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "lon",
            "description": "<p>Longitude of added address</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Given title for added address</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "street",
            "description": "<p>street number/name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "building",
            "description": "<p>building number/name</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "type",
            "description": "<p>House==1/Building==2</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "phone_number",
            "description": "<p>Phone number to call on</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "zone",
            "description": "<p>Address's Zone id/name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "floor",
            "description": "<p>Floor Number for addresses of type=building</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "apartment",
            "description": "<p>Apartment number for addresses of type=building</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "extra_directions",
            "description": "<p>Additional info</p>"
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
            "field": "address",
            "description": "<p>serialized data of newly added address</p>"
          }
        ]
      }
    },
    "filename": "mobileServer/user_utils.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/add_address/"
      }
    ],
    "error": {
      "fields": {
        "NotFound": [
          {
            "group": "NotFound",
            "type": "String",
            "optional": false,
            "field": "UserNotFoundError",
            "description": "<p>user does not exist</p>"
          }
        ],
        "Incomplete": [
          {
            "group": "Incomplete",
            "type": "String",
            "optional": false,
            "field": "RequestParamsMissing",
            "description": "<p>Request Missing Parameters</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"user does not exist\"\n }",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"Request Missing Parameters\"\n }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "delAddress/",
    "title": "delete address for user",
    "version": "1.0.0",
    "name": "DelAddress",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "address_id",
            "description": "<p>Address unique id</p>"
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
            "field": "null",
            "description": ""
          }
        ]
      }
    },
    "filename": "mobileServer/user_utils.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/delAddress/"
      }
    ],
    "error": {
      "fields": {
        "NotFound": [
          {
            "group": "NotFound",
            "type": "String",
            "optional": false,
            "field": "AddressNotFoundError",
            "description": "<p><code>address_id</code> does not exist</p>"
          }
        ],
        "Incomplete": [
          {
            "group": "Incomplete",
            "type": "String",
            "optional": false,
            "field": "RequestParamsMissing",
            "description": "<p>Request Missing Parameters</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"10 Missing Parameters\"\n }",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"Request Missing Parameters\"\n }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "editAddress/",
    "title": "edit address for user",
    "version": "1.0.0",
    "name": "EditAddress",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "address_id",
            "description": "<p>Address unique id</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "lat",
            "description": "<p>Latitude of added address</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "lon",
            "description": "<p>Longitude of added address</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "name",
            "description": "<p>Given title for added address</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "street",
            "description": "<p>street number/name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "building",
            "description": "<p>building number/name</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "type",
            "description": "<p>House==1/Building==2</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "phone_number",
            "description": "<p>Phone number to call on</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "zone",
            "description": "<p>Address's Zone id/name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "floor",
            "description": "<p>Floor Number for addresses of type=building</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "apartment",
            "description": "<p>Apartment number for addresses of type=building</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "extra_directions",
            "description": "<p>Additional info</p>"
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
            "field": "null",
            "description": ""
          }
        ]
      }
    },
    "filename": "mobileServer/user_utils.py",
    "groupTitle": "User",
    "sampleRequest": [
      {
        "url": "https://dukanty.com/editAddress/"
      }
    ],
    "error": {
      "fields": {
        "NotFound": [
          {
            "group": "NotFound",
            "type": "String",
            "optional": false,
            "field": "AddressNotFoundError",
            "description": "<p><code>address_id</code> does not exist</p>"
          }
        ],
        "Incomplete": [
          {
            "group": "Incomplete",
            "type": "String",
            "optional": false,
            "field": "RequestParamsMissing",
            "description": "<p>Request Missing Parameters</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"10 Missing Parameters\"\n }",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 500 INTERNAL SERVER ERROR\n {\n   \"error\": \"Request Missing Parameters\"\n }",
          "type": "json"
        }
      ]
    }
  }
] });

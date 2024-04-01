use("grocery_store");

var order_id = 2;

// find order total value, write all order products with price, count and product total
db.order_product.aggregate([
  {
    $match: { order_id },
  },
  {
    $lookup: {
      from: "products",
      localField: "product_id",
      foreignField: "_id",
      as: "product_info",
    },
  },
  {
    $unwind: "$product_info",
  },
  {
    $group: {
      _id: "$_id",
      products: {
        $push: {
          product_name: "$product_info.product_name",
          price: "$product_info.price",
          count: "$count",
          product_total: { $multiply: ["$product_info.price", "$count"] },
        },
      },
      total_order_value: {
        $sum: { $multiply: ["$product_info.price", "$count"] },
      },
    },
  },
  {
    $group: {
      _id: null,
      products: { $push: "$products" },
      total_price: { $sum: "$total_order_value" },
    },
  },
]);

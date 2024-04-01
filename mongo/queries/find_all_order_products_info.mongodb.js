use("grocery_store");

const order_id = 2;

// for an order with the given id finds all products with category, price and quantity
db.order_product.aggregate([
  {
    $match: { order_id },
  },
  {
    $lookup: {
      from: "products",
      localField: "product_id",
      foreignField: "_id",
      as: "product",
    },
  },
  {
    $unwind: "$product",
  },
  {
    $lookup: {
      from: "categories",
      localField: "product.category_id",
      foreignField: "_id",
      as: "category",
    },
  },
  {
    $unwind: "$category",
  },
  {
    $project: {
      product_name: "$product.product_name",
      quantity: "$count",
      price: "$product.price",
      category_name: "$category.category_name",
    },
  },
]);

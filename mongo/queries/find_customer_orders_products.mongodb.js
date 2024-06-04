use("grocery_store");

const customer_id = 1;

// 1
// for all the customer orders finds the names of the products
db.orders.aggregate([
  {
    $match: { customer_id: customer_id },
  },
  {
    $lookup: {
      from: "order_product",
      localField: "_id",
      foreignField: "order_id",
      as: "order_products",
    },
  },
  {
    $unwind: "$order_products",
  },
  {
    $lookup: {
      from: "products",
      localField: "order_products.product_id",
      foreignField: "_id",
      as: "product",
    },
  },
  {
    $unwind: "$product",
  },
  {
    $group: {
      _id: "$_id",
      products: { $push: "$product.product_name" },
    },
  },
]);

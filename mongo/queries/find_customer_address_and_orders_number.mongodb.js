use("grocery_store");

// 4
// find customer address and number of orders
db.customers.aggregate([
  {
    $match: { _id: 1 },
  },
  {
    $lookup: {
      from: "orders",
      localField: "_id",
      foreignField: "customer_id",
      as: "orders",
    },
  },
  {
    $project: {
      _id: 1,
      street: 1,
      number: 1,
      city: 1,
      number_of_orders: { $size: "$orders" },
    },
  },
]);

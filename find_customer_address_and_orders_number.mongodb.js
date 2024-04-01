use("grocery_store");

const customer_id = 1;

db.customers.aggregate([
  {
    $match: { _id: customer_id },
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

db.products.aggregate([
    {
        $lookup: {
            from: "order_product",
            localField: "_id",
            foreignField: "product_id",
            as: "order_products"
        }
    },
    {
        $unwind: "$order_products"
    },
    {
        $lookup: {
            from: "orders",
            localField: "order_products.order_id",
            foreignField: "_id",
            as: "order"
        }
    },
    {
        $unwind: "$order"
    },
    {
        $lookup: {
            from: "customers",
            localField: "order.customer_id",
            foreignField: "_id",
            as: "customer"
        }
    },
    {
        $unwind: "$customer"
    },
    {
        $match: { "customer._id": 1 }
    },
    {
        $group: {
            _id: "$_id",
            product_name: { $first: "$product_name" },
            order_count: { $sum: 1 },
            total_count: { $sum: "$order_products.count" }
        }
    }
])
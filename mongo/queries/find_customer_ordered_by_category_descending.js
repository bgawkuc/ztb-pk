// 6
// finds ordered products from given category (id=1) grouped by customer and ordered by count descending
db.customers.aggregate([
    {
        $lookup: {
            from: "orders",
            localField: "_id",
            foreignField: "customer_id",
            as: "orders"
        }
    },
    {
        $unwind: "$orders"
    },
    {
        $lookup: {
            from: "order_product",
            localField: "orders._id",
            foreignField: "order_id",
            as: "order_products"
        }
    },
    {
        $unwind: "$order_products"
    },
    {
        $lookup: {
            from: "products",
            localField: "order_products.product_id",
            foreignField: "_id",
            as: "product"
        }
    },
    {
        $unwind: "$product"
    },
    {
        $lookup: {
            from: "categories",
            localField: "product.category_id",
            foreignField: "_id",
            as: "category"
        }
    },
    {
        $unwind: "$category"
    },
    {
        $match: { "category._id": 1 }
    },
    {
        $group: {
            _id: "$_id",
            name: { $first: "$name" },
            surname: { $first: "$surname" },
            address: { $first: { $concat: ["$street", ", ", {$toString: ["$number"]}, ", ", "$city"] } },
            count: { $sum: "$order_products.count" }
        }
    },
    {
        $sort: { count: -1 }
    }
]);
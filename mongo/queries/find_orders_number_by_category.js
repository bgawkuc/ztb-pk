db.order_product.aggregate([
    {
        $lookup: {
            from: "products",
            localField: "product_id",
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
        $group: {
            _id: "$category.category_name",
            number_of_orders: { $sum: { $cond: [{ $gt: ["$order_id", null] }, 1, 0] } }
        }
    }
])
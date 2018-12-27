var webpack = require('webpack');
module.exports = {
    entry: [
    "./src/index.js"
    ],
    output: {
        path: __dirname + "/../app/static/js",
        filename: "bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: [
                            "env",
                            "react"
                        ]
                    }
                }
            },
            {
                test: /\.css$/,
                loader: "style-loader!css-loader" }
        ]
    }
};
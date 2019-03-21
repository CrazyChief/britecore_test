const BundleTracker = require("webpack-bundle-tracker");

const isProdEnv = process.env.NODE_ENV === 'production';
const s3 = 'https://s3.us-east-2.amazonaws.com/britecore-test-static/frontend/';

module.exports = {
    publicPath: isProdEnv ? s3 : "http://0.0.0.0:8080",
    outputDir: '../britecore_test/dist/frontend/',

    chainWebpack: config => {

        config.optimization
            .splitChunks(false);

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../britecore_test/webpack-stats.json'}]);

        config.resolve.alias
            .set('__STATIC__', 'static');

        config.devServer
            .public('http://0.0.0.0:8080')
            .host('0.0.0.0')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
    }
};

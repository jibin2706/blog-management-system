// check production status
const isProd = process.env.NODE_ENV === 'production';

module.exports = {
  env: {
    BASE_URL: isProd ? 'https://blog-management-systems.herokuapp.com' : 'http://localhost:3000',
  },
};

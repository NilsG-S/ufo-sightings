const mysql = require('mysql');

const pool = mysql.createPool({
  host: 'localhost',
  user: process.env.DB_USER_NAME,
  password: process.env.DB_PASSWORD,
  database: 'ufo',
  multipleStatements: true,
  connectionLimit: 10,
});

async function open() {
  pool.getConnection((err, cnx) => {
    if (err) {
      throw err;
    }

    return cnx;
  });
}

module.exports = {
  open,
};

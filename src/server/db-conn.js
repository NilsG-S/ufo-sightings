const mysql = require('mysql');

const pool = mysql.createPool({
  host: 'localhost',
  user: process.env.DB_USER_NAME,
  password: process.env.DB_PASSWORD,
  database: 'ufo',
  multipleStatements: true,
  connectionLimit: 10,
});

function open() {
  return new Promise((resolve, reject) => {
    pool.getConnection((err, cnx) => {
      if (err) {
        reject(err);
      }

      resolve(cnx);
    });
  });
}

function exec(sql, values) {
  return new Promise((resolve, reject) => {
    pool.query(sql, values, (err, res) => {
      if (err) {
        reject(err);
      }

      resolve(res);
    });
  });
}

module.exports = {
  open,
  exec,
};

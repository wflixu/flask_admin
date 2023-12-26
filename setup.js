const { spawn } = require("node:child_process");
const path = require("node:path");

process.env.PGADMIN_SERVER_MODE = "OFF";

const pythonPath = `/Users/lixu/play/playground/flask_admin/venv/bin/python3`;
const pgadminFile = "./main.py";

pgadminServerProcess = spawn(path.resolve(pythonPath), [
  "-s",
  path.resolve(pgadminFile),
]);

pgadminServerProcess.stdout.setEncoding("utf8");
pgadminServerProcess.stdout.on("data", (chunk) => {
  console.log(chunk);
});

pgadminServerProcess.stderr.setEncoding("utf8");
pgadminServerProcess.stderr.on("data", (chunk) => {
  console.warn(chunk);
});

pgadminServerProcess.on("error", function (err) {
  console.error(error);
});

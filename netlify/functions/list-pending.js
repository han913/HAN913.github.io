const { getStore } = require("@netlify/blobs");

exports.handler = async (event) => {
  const pass = event.headers["x-admin-pass"];

  if (!process.env.ADMIN_PASS || pass !== process.env.ADMIN_PASS) {
    return { statusCode: 401, body: "Unauthorized" };
  }

  const store = getStore("graduation-album");
  const pending = await store.get("pending", { type: "json" }) || [];

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(pending)
  };
};
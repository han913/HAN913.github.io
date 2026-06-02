const { connectLambda, getStore } = require("@netlify/blobs");

function json(statusCode, data) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store"
    },
    body: JSON.stringify(data)
  };
}

function getHeader(event, name) {
  const target = name.toLowerCase();
  const headers = event.headers || {};

  for (const key of Object.keys(headers)) {
    if (key.toLowerCase() === target) {
      return headers[key];
    }
  }

  return "";
}

exports.handler = async (event) => {
  try {
    connectLambda(event);

    const pass = getHeader(event, "x-admin-pass");

    if (!process.env.ADMIN_PASS || pass !== process.env.ADMIN_PASS) {
      return json(401, {
        ok: false,
        error: "Unauthorized"
      });
    }

    const store = getStore("graduation-album");
    const pending = await store.get("pending", { type: "json" }) || [];

    return json(200, pending);
  } catch (err) {
    console.error("list-pending error:", err);

    return json(500, {
      ok: false,
      error: err.message
    });
  }
};
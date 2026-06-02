const { getStore } = require("@netlify/blobs");

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const pass = event.headers["x-admin-pass"];

  if (!process.env.ADMIN_PASS || pass !== process.env.ADMIN_PASS) {
    return { statusCode: 401, body: "Unauthorized" };
  }

  try {
    const { id, action } = JSON.parse(event.body || "{}");

    const store = getStore("graduation-album");

    let pending = await store.get("pending", { type: "json" }) || [];
    let approved = await store.get("approved", { type: "json" }) || [];

    const target = pending.find(p => p.id === id);

    if (!target) {
      return { statusCode: 404, body: "Photo not found" };
    }

    pending = pending.filter(p => p.id !== id);

    if (action === "approve") {
      approved.unshift({
        ...target,
        approved_at: new Date().toISOString()
      });
    }

    await store.set("pending", JSON.stringify(pending), {
      contentType: "application/json"
    });

    await store.set("approved", JSON.stringify(approved), {
      contentType: "application/json"
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ ok: true })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: err.message
    };
  }
};
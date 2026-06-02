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
  if (event.httpMethod !== "POST") {
    return json(405, {
      ok: false,
      error: "Method Not Allowed"
    });
  }

  try {
    connectLambda(event);

    const pass = getHeader(event, "x-admin-pass");

    if (!process.env.ADMIN_PASS || pass !== process.env.ADMIN_PASS) {
      return json(401, {
        ok: false,
        error: "Unauthorized"
      });
    }

    const { id, action } = JSON.parse(event.body || "{}");

    if (!id) {
      return json(400, {
        ok: false,
        error: "Missing photo id"
      });
    }

    const store = getStore("graduation-album");

    let pending = await store.get("pending", { type: "json" }) || [];
    let approved = await store.get("approved", { type: "json" }) || [];

    const target = pending.find((p) => p.id === id);

    if (!target) {
      return json(404, {
        ok: false,
        error: "Photo not found"
      });
    }

    pending = pending.filter((p) => p.id !== id);

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

    return json(200, {
      ok: true,
      success: true
    });
  } catch (err) {
    console.error("approve-photo error:", err);

    return json(500, {
      ok: false,
      error: err.message
    });
  }
};